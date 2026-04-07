# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0
export PYTHONPATH := $(PWD)/Testbench:$(PYTHONPATH)

# Makefile

# defaults
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl
GHDL_ARGS += --std=08 -fsynopsys
SIM_ARGS+=--vcd=output.vcd

VHDL_SOURCES += $(shell pwd)/RTL/ADC_interface_level.vhd
VHDL_SOURCES += $(shell pwd)/RTL/ahb_sram.vhd
VHDL_SOURCES += $(shell pwd)/RTL/avg_sq_sum.vhd
VHDL_SOURCES += $(shell pwd)/RTL/clkgen.vhd
VHDL_SOURCES += $(shell pwd)/RTL/filter_compute.vhd
VHDL_SOURCES += $(shell pwd)/RTL/median.vhd
VHDL_SOURCES += $(shell pwd)/RTL/mult16x16.vhd
VHDL_SOURCES += $(shell pwd)/RTL/RMS_compute.vhd
VHDL_SOURCES += $(shell pwd)/RTL/scse_main.vhd
VHDL_SOURCES += $(shell pwd)/RTL/sqroot.vhd

# use VHDL_SOURCES for VHDL files

# COCOTB_TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
COCOTB_TOPLEVEL = scse_main

# COCOTB_TEST_MODULES is the basename of the Python test file(s)
COCOTB_TEST_MODULES = test_scse_main

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
