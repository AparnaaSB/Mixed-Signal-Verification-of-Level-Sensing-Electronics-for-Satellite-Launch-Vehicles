# tb/monitors/debug_inl_monitor.py

import cocotb
from cocotb.triggers import Timer
import matplotlib.pyplot as plt
import numpy as np

class DebugINL:
    def __init__(self, adc_model):
        self.adc = adc_model
        
    async def run(self):
        await Timer(100, unit="ns")
        self.generate_debug_plots()
        
    def generate_debug_plots(self):
        if not self.adc.dnl_enabled:
            print("[DEBUG] DNL/INL not enabled")
            return
            
        N_CODES = 65536
        dnl_errors = self.adc.dnl_array
        inl_values = self.adc.inl_array

        fig, axes = plt.subplots(3, 3, figsize=(18, 10))
        fig.suptitle('INL Generation Debug Analysis', fontsize=16, fontweight='bold')
        
        axes[0, 0].hist(dnl_errors, bins=100, edgecolor='black', alpha=0.7)
        axes[0, 0].set_title('DNL Distribution')
        axes[0, 0].set_xlabel('DNL (LSB)')
        axes[0, 0].set_ylabel('Count')
        axes[0, 0].axvline(-self.adc.dnl_max_lsb, color='r', linestyle='--', linewidth=2, label=f'Limit: ±{self.adc.dnl_max_lsb}')
        axes[0, 0].axvline(self.adc.dnl_max_lsb, color='r', linestyle='--', linewidth=2)
        axes[0, 0].axvline(0, color='gray', linestyle='-', linewidth=0.5)
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        axes[1, 0].plot(dnl_errors, 'b-', linewidth=0.3, alpha=0.8)
        axes[1, 0].set_title('DNL vs Code')
        axes[1, 0].set_xlabel('Code')
        axes[1, 0].set_ylabel('DNL (LSB)')
        axes[1, 0].axhline(-self.adc.dnl_max_lsb, color='r', linestyle='--', linewidth=1)
        axes[1, 0].axhline(self.adc.dnl_max_lsb, color='r', linestyle='--', linewidth=1)
        axes[1, 0].axhline(0, color='gray', linestyle='-', linewidth=0.5)
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].set_ylim(-1.5, 1.5)

        axes[2, 0].plot(inl_values, 'k-', linewidth=0.35)
        axes[2, 0].axhline(self.adc.inl_max_lsb, color='r', linestyle='--', linewidth=1, label=f'Spec: ±{self.adc.inl_max_lsb} LSB')
        axes[2, 0].axhline(-self.adc.inl_max_lsb, color='r', linestyle='--', linewidth=1)
        axes[2, 0].axhline(0, color='gray', linestyle='-', linewidth=0.5)
        axes[2, 0].set_title('INL Distribution')
        axes[2, 0].set_xlabel('Code')
        axes[2, 0].set_ylabel('INL (LSB)')
        axes[2, 0].set_ylim(-3, 3)
        axes[2, 0].grid(True, alpha=0.3)
        axes[2, 0].legend()
        
        plt.tight_layout()
        plt.savefig('inl_dnl_debug_analysis.png', dpi=600, bbox_inches='tight')
        plt.close()
