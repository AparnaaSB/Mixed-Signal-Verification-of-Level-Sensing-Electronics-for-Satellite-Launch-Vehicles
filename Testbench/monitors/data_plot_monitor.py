#tb/monitors/data_plot_monitor.py

import cocotb
from cocotb.triggers import RisingEdge
import cocotb.utils
import matplotlib.pyplot as plt
import time

class DataPlotMonitor:
    
    def __init__(self, scse_main, adc_model):
        self.scse_main = scse_main
        self.adc_model = adc_model
        self.adc_vin_list = []
		
        self.time_list = []

        self.rms_list = []
		
        self.sample1_list = []
        self.sample2_list = []
        self.sample3_list = []
		
        self.median_list = []

    def _calc_int(self, signal) -> int:
        raw = signal.value
        if not raw.is_resolvable:
            return 0
        return int(raw)

    async def run(self):
        while True:
            await RisingEdge(self.scse_main.clk_16)

            t = cocotb.utils.get_sim_time(unit="ns")
            self.time_list.append(t)

            # RMS
            rms_code = self._calc_int(self.scse_main.rms_value1)
            if rms_code >= 32768:
                rms_code -= 65536
            rms_val = rms_code * (10 / 32768)
            self.rms_list.append(rms_val)

            # Filter
            self.sample1_list.append(self._calc_int(self.scse_main.level_ISR_T_sample1))
            self.sample2_list.append(self._calc_int(self.scse_main.level_ISR_T_sample2))
            self.sample3_list.append(self._calc_int(self.scse_main.level_ISR_T_sample3))
            
            # Median
            self.median_list.append(self._calc_int(self.scse_main.median_level_ISR_T))

            # ADC
            vin = self.adc_model.channels_A[0]
            self.adc_vin_list.append(vin)

    def plot(self):
        plt.figure(figsize=(12, 10))
        
        plt.subplot(4, 1, 1)
        frequency = 4000  # Hz
        N = len(self.adc_vin_list)
        samples_per_cycle = int(16000000 / frequency)
        cycles_to_show = 5
        Nshow = cycles_to_show * samples_per_cycle    
        plt.plot(self.adc_vin_list[:Nshow])
        plt.xlabel("Time in ns")
        plt.ylabel("ADC (V)")
        plt.title("ADC Computation")

        plt.subplot(4, 1, 2)
        plt.plot(self.time_list, self.rms_list)
        plt.ylabel("RMS (V)")
        plt.xlabel("Time in ns")
        plt.title("RMS Computation")

        plt.subplot(4, 1, 3)
        plt.plot(self.time_list, self.sample1_list, label="Sample1")
        plt.plot(self.time_list, self.sample2_list, label="Sample2")
        plt.plot(self.time_list, self.sample3_list, label="Sample3")
        plt.ylabel("Filter Samples in ADC Code")
        plt.xlabel("Time in ns")
        plt.title("Filter Computation")
        plt.legend()

        plt.subplot(4, 1, 4)
        plt.plot(self.time_list, self.median_list)
        plt.ylabel("Median Output in ADC Code")
        plt.xlabel("Time in ns")
        plt.title("Median Computation")

        plt.tight_layout()
        filename = f"Output_Plots{time.strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename)
        plt.close()
