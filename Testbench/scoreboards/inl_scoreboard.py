# tb/monitors/inl_monitor.py

import cocotb
from cocotb.triggers import Timer
import matplotlib.pyplot as plt
import time
import csv
import time

class INLMonitor:
    def __init__(self, adc_model):
        self.adc = adc_model
        
    def plot_full_inl_profile(self):
        codes = self.adc.inl_error_lut.keys()
        inl_values = self.adc.inl_error_lut.values()
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(codes, inl_values, color='blue', linewidth=0.35)

        ax.axhline(0, color='gray', linewidth=0.5)
        ax.margins(x=0)
        ax.set_xlim(0,65536)

        ax.set_xlabel('CODE', fontsize=10, fontweight='bold')
        ax.set_ylabel('INL ERROR (LSBs)', fontsize=10, fontweight='bold')
        ax.set_title('Typical INL Error, ±10 V Range', fontsize=11, fontweight='bold')

        ax.grid(True, which='major', linestyle='-', linewidth=0.8,color='gray', alpha=0.5)
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        plt.savefig(f"INL_ADC_{time.strftime('%Y%m%d_%H%M%S')}.png", bbox_inches='tight', facecolor='white')
        plt.close()
        
    def write_inl_to_csv(self):
        filename = f"INL_ADC_{time.strftime('%Y%m%d_%H%M%S')}.csv"

        with open(filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['CODE', 'INL_ERROR_LSB'])  # header

            for code, inl in self.adc.inl_error_lut.items():
                writer.writerow([code, inl])
