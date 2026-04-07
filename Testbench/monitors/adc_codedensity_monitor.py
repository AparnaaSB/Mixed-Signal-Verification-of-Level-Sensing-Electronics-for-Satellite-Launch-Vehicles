# tb/monitors/adc_codedensity_monitor.py

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
import numpy as np
import matplotlib.pyplot as plt
import time

class ADCCODEDensityMonitor:
    def __init__(self, adc_model,scse_main):
        self.adc = adc_model
        self.scse_main = scse_main
        self.n_bits = 16
        self.n_codes = 65536

        self.histogram = np.zeros(self.n_codes, dtype=np.int64)
        self.sample_count = 0

    async def run(self):
        prev_rd = 0
        while True:
            current_rd = self.adc.RD
            if self.adc.CS == 0 and current_rd == 0 and prev_rd == 1:
                code = int(self.adc.DB15_DB0.value)
                if 0 <= code < self.n_codes:
                    self.histogram[code] += 1
                    self.sample_count += 1
            prev_rd = current_rd
    def plot_histogram(self):
        codes = np.arange(self.n_codes)

        plt.figure(figsize=(12, 6))
        plt.bar(codes, self.histogram, width=1.0)
        plt.xlabel("ADC Output Code")
        plt.ylabel("Number of Hits")
        plt.title("CODE_DENSITY_HISTOGRAM")
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()
        plt.savefig(f"CODE_DENSITY_HISTOGRAM_{time.strftime('%Y%m%d_%H%M%S')}.png",dpi=600, bbox_inches='tight', facecolor='white')
        plt.close()
