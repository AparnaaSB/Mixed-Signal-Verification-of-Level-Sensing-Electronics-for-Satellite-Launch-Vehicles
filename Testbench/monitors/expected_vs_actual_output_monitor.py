#tb/monitors/expected_vs_actual_output.py

import cocotb
from cocotb.triggers import RisingEdge
import cocotb.utils
import math
import matplotlib.pyplot as plt
import time

class ExpectedVsActualMonitor:

    def __init__(self, scse_main, adc_model,channel_cfg,mode):
        self.scse_main = scse_main
        self.adc_model = adc_model
        self.channel_cfg = channel_cfg
        self.mode = mode
        self.time_list = []
        self.expected_output_list = []
        self.actual_output_list = []

    def _calc_int(self, signal) -> int:
        raw = signal.value
        if not raw.is_resolvable:
            return 0
        return int(raw)

    def _expected_op_ch1(self):
        if self.mode == "single":
            amp = self.channel_cfg[1]["amp"]
            expected_rms = amp / math.sqrt(2)
        elif self.mode == "dc":
            expected_rms = abs(self.adc_model.channels_A[0])
        return expected_rms

    async def run(self):
        while True:
            await RisingEdge(self.scse_main.clk_16)

            filter_ready = self._calc_int(self.scse_main.RMS_sample_ready1)

            if filter_ready == 1:
                sim_time = cocotb.utils.get_sim_time(unit="ns")

                expected_op = self._expected_op_ch1()

                median_code = self._calc_int(self.scse_main.median_level_ISR_T)
                if median_code >= 32768:
                    median_code -= 65536

                actual_op = median_code * (10 / 32768)

                self.time_list.append(sim_time)
                self.expected_output_list.append(expected_op)
                self.actual_output_list.append(actual_op)

    def plot(self):
        plt.figure(figsize=(10, 6))

        plt.plot(
            self.time_list,
            self.expected_output_list,
            label="Expected Output (Ch1)",
            linestyle="-."
        )
        plt.plot(
            self.time_list,
            self.actual_output_list,
            label="Actual Output (Ch1)",
            linestyle="-"
        )

        plt.xlabel("Simulation Time (ns)")
        plt.ylabel("Volts")
        plt.title("Expected vs Actual Outputs (Channel 1)")
        plt.legend()

        plt.grid(True, which='both', linestyle='-', linewidth=0.5, alpha=0.7)  # Major grid
        plt.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.5)  # Minor grid
        plt.minorticks_on() 
        
        filename = f"Output_Expected_vs_Actual_{time.strftime('%Y%m%d_%H%M%S')}.png"
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
