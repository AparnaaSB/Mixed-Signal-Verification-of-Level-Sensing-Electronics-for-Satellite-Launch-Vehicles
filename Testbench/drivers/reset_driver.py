# tb/drivers/reset_driver.py

from cocotb.triggers import Timer

class ResetDriver:
    def __init__(self, rst, duration):
        self.rst = rst
        self.duration = duration
    async def run(self):
        self.rst.value = 0
        await Timer(self.duration, "ms")
        self.rst.value = 1
