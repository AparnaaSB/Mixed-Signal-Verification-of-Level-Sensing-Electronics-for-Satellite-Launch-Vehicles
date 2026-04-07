#tb/monitors/enob_histogram_monitor.py

import cocotb
from cocotb.triggers import Timer
from cocotb.queue import Queue
import csv
import matplotlib.pyplot as plt
import numpy as np
import time

class ENOBHistogramMonitor:
    def __init__(self, adc_model):
        self.adc = adc_model
        self.queue = Queue()
        self.data = [] 
        self.codes_sn = set()
        
    async def run(self):
        prev_rd = 0
        while True:
            await Timer(1, unit="ns")
            current_rd = self.adc.RD
            
            if current_rd == 0 and prev_rd == 1:
                if hasattr(self.adc, 'conversion_results') and self.adc.conversion_results:
                    for result in self.adc.conversion_results:
                        code = result['code']
                        channel = result['channel']
                        if channel == 'V0A':
                            if code in self.adc.dnl_voltage_lut_positive:
                                Vin = self.adc.dnl_voltage_lut_positive[code]
                            elif code in self.adc.dnl_voltage_lut_negative:
                                Vin = self.adc.dnl_voltage_lut_negative[code]

                            dnl_record = {'code': code, 'input_voltage': Vin, 'channel': result['channel']}
                            self.data.append(dnl_record)
                            self.codes_sn.add(code)
                            await self.queue.put(dnl_record)
            prev_rd = current_rd
       
    def plot_dc_histogram(self, center_code=None, code_window=10):

        code_counts = {}
        for record in self.data:
            code = record['code']
            code_counts[code] = code_counts.get(code, 0) + 1
        

        if center_code is None:
            center_code = max(code_counts, key=code_counts.get)
        

        min_code = center_code - code_window
        max_code = center_code + code_window
        

        codes_to_plot = range(min_code, max_code + 1)
        counts = [code_counts.get(code, 0) for code in codes_to_plot]

        fig, ax = plt.subplots(figsize=(10, 7))

        bars = ax.bar(codes_to_plot, counts, width=0.8, color='black', edgecolor='black')

        for i, (code, count) in enumerate(zip(codes_to_plot, counts)):
            if count > 0:
                ax.text(code, count + max(counts)*0.02, str(count),ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        ax.set_xlabel('CODE', fontsize=11, fontweight='bold')
        ax.set_ylabel('NUMBER OF HITS', fontsize=11, fontweight='bold')

        if hasattr(self.adc, 'HW_RNGSEL_2b'):
            if self.adc.HW_RNGSEL_2b == 0b01:
                range_str = "±2.5V RANGE"
            elif self.adc.HW_RNGSEL_2b == 0b10:
                range_str = "±5V RANGE"
            else:  # 0b11 or 0b00
                range_str = "±10V RANGE"
        else:
            range_str = "±10V RANGE"
        
        total_samples = sum(counts)
        title = f"DC Histogram of Codes at Code Center, {range_str}\n"
        title += f"VxA AND VxB/GND SHORTED TOGETHER\n{total_samples} SAMPLES"
        ax.set_title(title, fontsize=10, fontweight='bold')
        

        ax.grid(True, axis='y', linestyle='-', linewidth=0.8, color='gray', alpha=0.3)
        ax.set_axisbelow(True)
        

        ax.set_xlim(min_code - 0.5, max_code + 0.5)
        ax.set_ylim(0, max(counts) * 1.15)
        

        ax.set_xticks(codes_to_plot)
        ax.set_xticklabels(codes_to_plot, fontsize=9)
        
        plt.tight_layout()
        filename = f"dc_histogram_{time.strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')       
        plt.close()