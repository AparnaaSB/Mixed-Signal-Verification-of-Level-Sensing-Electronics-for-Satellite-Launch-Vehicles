# tb/drivers/ahb_driver.py

import cocotb
import time
from cocotb.triggers import RisingEdge, Timer, ClockCycles

class AHBDriver:
    def __init__(self, scse_main):
        self.scse_main = scse_main
        self.HREADYOUT_lat = 0
        self.HREADYOUT_prev = 0
        
    async def latch_hreadyout(self):
        while True:
            await RisingEdge(self.scse_main.clk_16)
            self.HREADYOUT_prev = self.HREADYOUT_lat
            self.HREADYOUT_lat = self.scse_main.HREADYOUT.value

    async def WaitLatchedHreadyoutRise(self):
        while True:
            await RisingEdge(self.scse_main.clk_16)
            if self.HREADYOUT_prev == 0 and self.HREADYOUT_lat == 1:
                return

    async def sram_read(self):
        while True:
            if self.scse_main.POR.value == 0:
                self.scse_main.HSEL.value = 0
                self.scse_main.HREADYIN.value = 1
                self.scse_main.HADDR.value = 0x00000000
                self.scse_main.HBURST.value = 0b000
                self.scse_main.HSIZE.value = 0b010
                self.scse_main.HTRANS.value = 0b00
                self.scse_main.HWRITE.value = 0
                await Timer(1, unit="ms")

            else:
                self.scse_main.HSEL.value = 1
                self.scse_main.HREADYIN.value = 1
                self.scse_main.HADDR.value = 0x60000FFC
                self.scse_main.HBURST.value = 0b000        # SINGLE
                self.scse_main.HSIZE.value = 0b010         # WORD
                self.scse_main.HTRANS.value = 0b10         # NONSEQ
                self.scse_main.HWRITE.value = 0            # Read
                await ClockCycles(self.scse_main.clk_16, 4)

                self.scse_main.HADDR.value = 0x60000000
                await self.WaitLatchedHreadyoutRise()
                self.scse_main.HSEL.value = 0
                await ClockCycles(self.scse_main.clk_16, 4)

                base_addr = 0x60000000
                for i in range(9):
                    self.scse_main.HSEL.value = 1
                    self.scse_main.HREADYIN.value = 1

                    if i == 0:
                        self.scse_main.HADDR.value = base_addr
                    else:
                        self.scse_main.HADDR.value = int(base_addr) + i * 4

                    self.scse_main.HBURST.value = 0b000
                    self.scse_main.HSIZE.value = 0b010
                    self.scse_main.HTRANS.value = 0b10
                    self.scse_main.HWRITE.value = 0

                    await self.WaitLatchedHreadyoutRise()
                    await ClockCycles(self.scse_main.clk_16, 4)

            await Timer(0.2, unit="ms")
            return
