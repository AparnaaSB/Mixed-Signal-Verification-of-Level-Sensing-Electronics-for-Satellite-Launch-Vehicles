#tb/monitors/RMS_FilterSample1.py

import cocotb
from cocotb.triggers import RisingEdge
import cocotb.utils
import matplotlib.pyplot as plt
import time
import math

class RMSFilterSample1:
    def __init__(self, scse_main, adc_model):
        self.scse_main = scse_main
        self.adc_model = adc_model
        self.time_list = []
        self.rms_list = []
        self.sample1_list = []
        
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

            # RMS-ch:1
            rms_code = self._calc_int(self.scse_main.rms_value1)
            if rms_code >= 32768:
                rms_code -= 65536
            rms_val = rms_code * (10 / 32768)
            self.rms_list.append(rms_val)

            # Filter
            filter_sample = self._calc_int(self.scse_main.level_ISR_T_sample1)
            if filter_sample >= 32768:
                filter_sample -= 65536
            filter_sample_val = filter_sample * (10 / 32768)
            self.sample1_list.append(filter_sample_val)

    def plot(self):
        plt.figure(figsize=(16, 8), dpi=600) 

        ax1 = plt.gca() 
        ax1.plot(self.time_list, self.rms_list, label="RMS (V)", color="tab:blue") 
        ax1.set_xlabel("Time (ns)") 
        ax1.set_ylabel("RMS (V)", color="tab:blue") 
        ax1.set_ylim(min(self.rms_list) - 0.01,max(self.rms_list) + 0.1) 
        ax1.tick_params(axis="y", labelcolor="tab:blue") 

        ax2 = ax1.twinx() 
        ax2.plot(self.time_list, self.sample1_list, label="Sample1 (ADC Code)", color="tab:orange") 
        ax2.set_ylabel("Filter Output (ADC Code)", color="tab:orange") 
        ax2.tick_params(axis="y", labelcolor="tab:orange") 
        ax2.set_ylim(min(self.sample1_list) - 0.01, max(self.sample1_list) + 0.1) 
        
        ax1.minorticks_on() 
        ax2.minorticks_on() 

        ax1.grid(True, which="both", linestyle="--", linewidth=0.1) 
        lines_1, labels_1 = ax1.get_legend_handles_labels() 
        lines_2, labels_2 = ax2.get_legend_handles_labels() 
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="lower right") 
        plt.title("RMS and Filter Output vs Time") 
        plt.tight_layout() 
        filename = f"RMS_FilterSample1{time.strftime('%Y%m%d_%H%M%S')}.png" 
        plt.savefig(filename) 
        plt.close()