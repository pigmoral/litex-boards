#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2025 Junhui Liu <junhui.liu@pigmoral.tech>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.xilinx import Xilinx7SeriesPlatform, VivadoProgrammer

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk
    ("clk50", 0, Pins("AA28"), IOStandard("LVCMOS18")),
    ("clk200", 0,
        Subsignal("p", Pins("AH27"), IOStandard("DIFF_SSTL15")),
        Subsignal("n", Pins("AH28"), IOStandard("DIFF_SSTL15")),
    ),
    ("clk200", 1,
        Subsignal("p", Pins("G25"), IOStandard("DIFF_SSTL15")),
        Subsignal("n", Pins("G26"), IOStandard("DIFF_SSTL15")),
    ),

    # LEDs
    ("user_led", 0, Pins("P30"), IOStandard("LVCMOS18")),
    ("user_led", 1, Pins("M30"), IOStandard("LVCMOS18")),
    ("user_led", 2, Pins("N30"), IOStandard("LVCMOS18")),

    # Buttons
    ("user_btn", 0, Pins("R28"), IOStandard("LVCMOS18")),

    # PCIe
    ("pcie_x8", 0,
        Subsignal("rst_n", Pins("Y26"), IOStandard("LVCMOS33")),
        Subsignal("clk_n", Pins("J7")),
        Subsignal("clk_p", Pins("J8")),
        Subsignal("rx_n",  Pins("H5 J3 K5 L3 M5 P5 R3 T5")),
        Subsignal("rx_p",  Pins("H6 J4 K6 L4 M6 P6 R4 T6")),
        Subsignal("tx_n",  Pins("F1 H1 K1 M1 N3 P1 T1 U3")),
        Subsignal("tx_p",  Pins("F2 H2 K2 M2 N4 P2 T2 U4")),
    ),

    # PCIe
    ("pcie_x4", 0,
        Subsignal("rst_n", Pins("Y26"), IOStandard("LVCMOS33")),
        Subsignal("clk_n", Pins("J7")),
        Subsignal("clk_p", Pins("J8")),
        Subsignal("rx_n",  Pins("H5 J3 K5 L3")),
        Subsignal("rx_p",  Pins("H6 J4 K6 L4")),
        Subsignal("tx_n",  Pins("F1 H1 K1 M1")),
        Subsignal("tx_p",  Pins("F2 H2 K2 M2")),
    ),

    # PCIe
    ("pcie_x2", 0,
        Subsignal("rst_n", Pins("Y26"), IOStandard("LVCMOS33")),
        Subsignal("clk_n", Pins("J7")),
        Subsignal("clk_p", Pins("J8")),
        Subsignal("rx_n",  Pins("H5 J3")),
        Subsignal("rx_p",  Pins("H6 J4")),
        Subsignal("tx_n",  Pins("F1 H1")),
        Subsignal("tx_p",  Pins("F2 H2")),
    ),

    # PCIe
    ("pcie_x1", 0,
        Subsignal("rst_n", Pins("Y26"), IOStandard("LVCMOS33")),
        Subsignal("clk_n", Pins("J7")),
        Subsignal("clk_p", Pins("J8")),
        Subsignal("rx_n",  Pins("H5")),
        Subsignal("rx_p",  Pins("H6")),
        Subsignal("tx_n",  Pins("F1")),
        Subsignal("tx_p",  Pins("F2")),
    ),

    # DDR3 SDRAM
    ("ddram", 0,
        Subsignal("a", Pins(
            "AK27 AN23 AL24 AK26 AH24 AH25 AL26 AJ24",  # A0-A7
            "AJ25 AM23 AL28 AL25 AM25 AK24 AM27"),      # A8-A14
            IOStandard("SSTL15")),
        Subsignal("ba",    Pins("AM26 AP24 AN28"), IOStandard("SSTL15")),
        Subsignal("ras_n", Pins("AJ29"), IOStandard("SSTL15")),
        Subsignal("cas_n", Pins("AP26"), IOStandard("SSTL15")),
        Subsignal("we_n",  Pins("AN27"), IOStandard("SSTL15")),
        Subsignal("cs_n",  Pins("AK28"), IOStandard("SSTL15")),
        #Subsignal("dm",   Pins("")), # gnd
        Subsignal("dq", Pins(
            "AG17 AG16 AH17 AJ19 AH18 AH19 AJ16 AJ17",  # 0-7
            "AL20 AN17 AL19 AM16 AL18 AL16 AM20 AN18",  # 8-15
            "AL23 AN20 AK23 AP19 AN22 AN19 AM22 AP20",  # 16-23
            "AJ21 AH22 AK21 AG21 AG22 AG20 AH23 AG23",  # 24-31
            "AJ32 AK32 AK31 AL30 AL34 AL31 AK34 AL29",  # 32-39
            "AJ34 AH32 AJ30 AH34 AF31 AG30 AG31 AF30",  # 40-47
            "AE32 AC33 AF33 AC32 AD34 AC34 AE33 AE31",  # 48-55
            "AE26 AF29 AE24 AF28 AF24 AG25 AF26 AF25",  # 56-63
            "AN34 AP30 AM33 AN29 AP32 AP29 AM31 AP31"), # 64-71
            IOStandard("SSTL15"),
            Misc("IN_TERM=UNTUNED_SPLIT_50")),
        Subsignal("dqs_p", Pins(
            "AK16 AM17 AP21 AH20 AK33 AG33 AE34 AE27", # 0-7
            "AN32"), # 8
            IOStandard("DIFF_SSTL15"),
            Misc("IN_TERM=UNTUNED_SPLIT_50")),
        Subsignal("dqs_n", Pins(
            "AK17 AM18 AP22 AJ20 AL33 AH33 AF34 AE28", # 0-7
            "AP33"), # 8
            IOStandard("DIFF_SSTL15"),
            Misc("IN_TERM=UNTUNED_SPLIT_50")),
        Subsignal("clk_p", Pins("AN25"),    IOStandard("DIFF_SSTL15")),
        Subsignal("clk_n", Pins("AP25"),    IOStandard("DIFF_SSTL15")),
        Subsignal("cke",   Pins("AP27"),    IOStandard("SSTL15")),
        Subsignal("odt",   Pins("AK29"),    IOStandard("SSTL15")),
        Subsignal("reset_n", Pins("AD31"), IOStandard("LVCMOS15")),
        Misc("SLEW=FAST"),
    ),

    # DDR3 SDRAM
    ("ddram", 1,
        Subsignal("a", Pins(
            "E27 C27 B28 D27 C24 D24 C25 A24 ", # A0-A7
            "A25 J24 F26 D26 H25 D25 B26"),     # A8-A14
            IOStandard("SSTL15")),
        Subsignal("ba",    Pins("F24 J25 E24"), IOStandard("SSTL15")),
        Subsignal("ras_n", Pins("E28"), IOStandard("SSTL15")),
        Subsignal("cas_n", Pins("E26"), IOStandard("SSTL15")),
        Subsignal("we_n",  Pins("F25"), IOStandard("SSTL15")),
        Subsignal("cs_n",  Pins("F28"), IOStandard("SSTL15")),
        #Subsignal("dm",   Pins("")), # gnd
        Subsignal("dq", Pins(
            "A29 B33 A31 C33 C32 A30 B30 A33",  # 0-7
            "D31 F33 D30 D29 E33 E34 E31 F34",  # 8-15
            "B23 A21 C23 B20 B22 A23 C20 B21",  # 16-23
            "G31 G32 F29 F31 E29 G33 H33 H32",  # 24-31
            "B18 C17 C19 B16 A18 A16 C18 B17",  # 32-39
            "K27 L24 K24 L28 K26 M27 L25 M26",  # 40-47
            "F16 E18 E16 H19 H17 H20 E17 H18",  # 48-55
            "D20 F21 E23 G21 G20 D21 F20 F23",  # 56-63
            "L34 K34 K31 K33 L31 J30 L33 J34"), # 64-71
            IOStandard("SSTL15"),
            Misc("IN_TERM=UNTUNED_SPLIT_50")),
        Subsignal("dqs_p", Pins(
            "B31 D34 A19 H29 D16 K28 G17 G22",  # 0-7
            "K32"),                             # 8
            IOStandard("DIFF_SSTL15"),
            Misc("IN_TERM=UNTUNED_SPLIT_50")),
        Subsignal("dqs_n", Pins(
            "B32 C34 A20 H30 D17 K29 G18 G23",  # 0-7
            "J32"),                             # 8
            IOStandard("DIFF_SSTL15"),
            Misc("IN_TERM=UNTUNED_SPLIT_50")),
        Subsignal("clk_p", Pins("B25"),    IOStandard("DIFF_SSTL15")),
        Subsignal("clk_n", Pins("A26"),    IOStandard("DIFF_SSTL15")),
        Subsignal("cke",   Pins("A28"),    IOStandard("SSTL15")),
        Subsignal("odt",   Pins("B27"),    IOStandard("SSTL15")),
        Subsignal("reset_n", Pins("F18"), IOStandard("LVCMOS15")),
        Misc("SLEW=FAST"),
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = []

# Platform -----------------------------------------------------------------------------------------

class Platform(Xilinx7SeriesPlatform):
    default_clk_name   = "clk50"
    default_clk_period = 1e9/50e6

    def __init__(self, toolchain="vivado"):
        Xilinx7SeriesPlatform.__init__(self, "xc7k480tffg1156-2", _io, toolchain=toolchain)

    def create_programmer(self):
        return VivadoProgrammer()

    def do_finalize(self, fragment):
        Xilinx7SeriesPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk50", loose=True), 1e9/50e6)

        self.add_platform_command("set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]")
        self.add_platform_command("set_property BITSTREAM.CONFIG.CONFIGRATE 12 [current_design]")
        self.add_platform_command("set_property BITSTREAM.CONFIG.UNUSEDPIN Pullup [current_design]")
