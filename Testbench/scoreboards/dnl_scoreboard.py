# tb/monitors/dnl_monitor.py

import cocotb
from cocotb.triggers import Timer
import csv
import matplotlib.pyplot as plt
import numpy as np
import time

class DNLMonitor:
    def __init__(self, adc_model):
        self.adc = adc_model
        
    def plot_full_dnl_profile(self):
        codes = self.adc.dnl_error_lut.keys()
        dnl_values = self.adc.dnl_error_lut.values()
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(codes, dnl_values, color='blue', linewidth=0.3, alpha=0.8)
      
        ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
        ax.margins(x=0)
        ax.set_xlim(0,65536)
        ax.set_xlabel('CODE', fontsize=10, fontweight='bold')
        ax.set_ylabel('DNL ERROR (LSBs)', fontsize=10, fontweight='bold')
        ax.set_title('Typical DNL Error, ±10 V Range', fontsize=11, fontweight='bold')

        ax.grid(True, which='major', linestyle='-', linewidth=0.8, color='gray', alpha=0.5)
        ax.set_axisbelow(True)
        
        plt.tight_layout()

        filename = f"DNL_ADC_{time.strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename, bbox_inches='tight', facecolor='white')
        plt.close()

    def write_dnl_to_csv(self):
        filename = f"DNL_ADC_{time.strftime('%Y%m%d_%H%M%S')}.csv"

        with open(filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['CODE', 'DNL_ERROR_LSB'])  # header

            for code, dnl in self.adc.dnl_error_lut.items():
                writer.writerow([code, dnl])