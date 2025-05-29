#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2025 Junhui Liu <junhui.liu@pigmoral.tech>
# SPDX-License-Identifier: BSD-2-Clause

#
# Board Info:
# https://www.milianke.com/product-item-108.html

from migen import *

from litex.build.generic_platform import *
from litex.build.anlogic.platform import AnlogicPlatform
from litex.build.openfpgaloader import OpenFPGALoader

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk25",  0, Pins("P63"), IOStandard("LVCMOS33")),

    # Leds
    ("user_led", 0, Pins("P91"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("P104"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("P109"), IOStandard("LVCMOS33")),
    ("user_led", 3, Pins("P112"), IOStandard("LVCMOS33")),
    ("user_led", 4, Pins("P133"), IOStandard("LVCMOS33")),
    ("user_led", 5, Pins("P148"), IOStandard("LVCMOS33")),
    ("user_led", 6, Pins("P151"), IOStandard("LVCMOS33")),

    # Buttons (KEY1 is hard reset button)
    ("user_btn", 0, Pins("P157"),  IOStandard("LVCMOS33")), # KEY2
    ("user_btn", 1, Pins("P161"),  IOStandard("LVCMOS33")), # KEY3
    ("user_btn", 2, Pins("P62"),  IOStandard("LVCMOS33")),  # KEY4

    # SDCard.
    ("spisdcard", 0,
        Subsignal("clk",  Pins("P25")),
        Subsignal("mosi", Pins("P32")),
        Subsignal("cs_n", Pins("P35")),
        Subsignal("miso", Pins("P19")),
        IOStandard("LVCMOS33"),
    ),
    ("sdcard", 0,
        Subsignal("data", Pins("P19 P11 P39 P35")),
        Subsignal("cmd",  Pins("P32")),
        Subsignal("clk",  Pins("P25")),
        Subsignal("cd",   Pins("P8")),
        IOStandard("LVCMOS33"),
    ),

    # Serial
    ("serial", 0,
        Subsignal("tx", Pins("P84")),
        Subsignal("rx", Pins("P86")),
        IOStandard("LVCMOS33")
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = []

# Platform -----------------------------------------------------------------------------------------

class Platform(AnlogicPlatform):
    default_clk_name   = "clk25"
    default_clk_period = 1e9/25e6

    def __init__(self, toolchain="td"):
        AnlogicPlatform.__init__(self, "EG4D20EG176", _io, _connectors, toolchain=toolchain)

    def create_programmer(self):
        return OpenFPGALoader("mlk-s200-eg4d20")

    def do_finalize(self, fragment):
        AnlogicPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk25", loose=True), 1e9/25e6)
