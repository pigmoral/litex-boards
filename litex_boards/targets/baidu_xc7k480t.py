#!/usr/bin/env python3

#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2025 Junhui Liu <junhui.liu@pigmoral.tech>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *

from litex.gen import *

from litex_boards.platforms import baidu_xc7k480t

from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *

from litex.soc.cores.clock import *
from litex.soc.cores.led import LedChaser

from litedram.modules import MT41K256M8
from litedram.phy import s7ddrphy

from litepcie.phy.s7pciephy import S7PCIEPHY
from litepcie.software import generate_litepcie_software

# CRG ----------------------------------------------------------------------------------------------

class _CRG(LiteXModule):
    def __init__(self, platform, sys_clk_freq):
        self.rst          = Signal()
        self.cd_sys       = ClockDomain()
        self.cd_sys4x     = ClockDomain()
        self.cd_sys4x_dqs = ClockDomain()
        self.cd_idelay    = ClockDomain()

        # Clk / Rst.
        clk200 = platform.request("clk200")
        rst_n  = platform.request("user_btn", 0)

        # PLL.
        self.pll = pll = S7PLL()
        self.comb += pll.reset.eq(~rst_n | self.rst)
        pll.register_clkin(clk200, 200e6)
        pll.create_clkout(self.cd_sys,       sys_clk_freq)
        pll.create_clkout(self.cd_sys4x,     4*sys_clk_freq)
        pll.create_clkout(self.cd_sys4x_dqs, 4*sys_clk_freq, phase=90)
        pll.create_clkout(self.cd_idelay,    200e6)
        platform.add_false_path_constraints(self.cd_sys.clk, pll.clkin) # Ignore sys_clk to pll.clkin path created by SoC's rst.

        # IDelayCtrl.
        self.idelayctrl = S7IDELAYCTRL(self.cd_idelay)

# BaseSoC ------------------------------------------------------------------------------------------

class BaseSoC(SoCCore):
    def __init__(self, sys_clk_freq=50e6,
        with_pcie       = False,
        with_led_chaser = True,
        **kwargs):
        platform = baidu_xc7k480t.Platform()

        # CRG --------------------------------------------------------------------------------------
        self.crg = _CRG(platform, sys_clk_freq)

        # SoCCore ----------------------------------------------------------------------------------
        SoCCore.__init__(self, platform, sys_clk_freq, ident="LiteX SoC on Baidu xc7k480t", **kwargs)

        # DDR3 SDRAM -------------------------------------------------------------------------------
        if not self.integrated_main_ram_size:
            # we need to use A7DDRPHY instead of K7DDRPHY, because the 480T has no ODELAYE2
            self.ddrphy = s7ddrphy.A7DDRPHY(platform.request("ddram"),
                memtype      = "DDR3",
                nphases      = 4,
                sys_clk_freq = sys_clk_freq)
            self.add_sdram("sdram",
                phy           = self.ddrphy,
                module        = MT41K256M8(sys_clk_freq, "1:4"),
                size          = 0x40000000,
                l2_cache_size = kwargs.get("l2_size", 8192)
            )

        # PCIe -------------------------------------------------------------------------------------
        if with_pcie:
            self.pcie_phy = S7PCIEPHY(platform, platform.request("pcie_x4"),
                data_width = 128,
                bar0_size  = 0x20000)
            self.add_pcie(phy=self.pcie_phy, ndmas=1)

        # Leds -------------------------------------------------------------------------------------
        if with_led_chaser:
            self.leds = LedChaser(
                pads         = platform.request_all("user_led"),
                sys_clk_freq = sys_clk_freq)

# Build --------------------------------------------------------------------------------------------
def main():
    from litex.build.parser import LiteXArgumentParser
    parser = LiteXArgumentParser(platform=baidu_xc7k480t.Platform, description="LiteX SoC on Baidu xc7k480t.")
    parser.add_target_argument("--sys-clk-freq", default=50e6, type=float,  help="System clock frequency.")
    parser.add_target_argument("--with-pcie",    action="store_true",       help="Enable PCIe support.")
    parser.add_target_argument("--driver",       action="store_true",       help="Generate PCIe driver.")
    args = parser.parse_args()

    soc = BaseSoC(
        sys_clk_freq = args.sys_clk_freq,
        with_pcie    = args.with_pcie,
        **parser.soc_argdict
    )
    builder = Builder(soc, **parser.builder_argdict)
    if args.build:
        builder.build(**parser.toolchain_argdict)

    if args.driver:
        generate_litepcie_software(soc, os.path.join(builder.output_dir, "driver"))

    if args.load:
        prog = soc.platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"))

if __name__ == "__main__":
    main()
