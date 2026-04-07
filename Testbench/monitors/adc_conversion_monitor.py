#tb/monitors/adc_conversion_monitor.py

import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.queue import Queue

class ADCConversionMonitor:

    def __init__(self, adc_model):
        self.adc = adc_model
        self.queue = Queue()

    async def run(self):
        prev_rd = 0
        while True:
            await Timer(1, unit="ns")
            current_rd = self.adc.RD
            if current_rd == 0 and prev_rd == 1:
                for result in self.adc.conversion_results:
                    await self.queue.put(result)
            prev_rd = current_rd    
                
