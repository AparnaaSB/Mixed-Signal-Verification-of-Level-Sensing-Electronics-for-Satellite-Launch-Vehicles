# tb/monitors/code_voltage_lut_monitor.py

import cocotb
from cocotb.triggers import Timer
import csv
import matplotlib.pyplot as plt
import numpy as np
import time

class CodeVoltageLUTMonitor:
    def __init__(self, adc_model):
        self.adc = adc_model

    def write_code_voltage_to_csv(self):
        filename = f"Code_Voltage_LUT_{time.strftime('%Y%m%d_%H%M%S')}.csv"

        with open(filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['CODE', 'VOLTAGE'])

            for code, voltage in self.adc.dnl_voltage_lut_positive.items():
                writer.writerow([code, voltage])
            for code, voltage in self.adc.dnl_voltage_lut_negative.items():
                writer.writerow([code, voltage])