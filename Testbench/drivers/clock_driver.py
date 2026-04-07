# tb/drivers/clock_driver.py

import cocotb
from cocotb.clock import Clock

class ClockDriver:
    def __init__(self, clk, duration):
        self.clk = clk
        self.duration = duration
    def start(self):
        clock = Clock(self.clk, self.duration,"ns")
        cocotb.start_soon(clock.start())
