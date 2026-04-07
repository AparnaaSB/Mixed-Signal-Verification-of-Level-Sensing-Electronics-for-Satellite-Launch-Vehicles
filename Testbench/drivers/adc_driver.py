# tb/drivers/adc_driver.py

import cocotb
from cocotb.triggers import Timer

class ADCDriver:
    def __init__(self, scse_main, adc_model):
        self.scse_main = scse_main
        self.adc = adc_model

    async def run(self):
        while True:
            self.adc.RESET = self.scse_main.POR.value
            self.adc.WR = self.scse_main.WR_ADC1.value
            self.adc.RD = self.scse_main.RD_ADC1.value
            self.adc.CS = self.scse_main.CS_ADC1.value
            self.adc.CHSEL_3b = self.scse_main.CHSEL_ADC1.value
            self.adc.CONVST = self.scse_main.CONVST_ADC1.value
            self.scse_main.BUSY_ADC1.value = self.adc.BUSY
            self.scse_main.DATA_ADC1.value = self.adc.DB15_DB0
            await Timer(1, unit="ns")