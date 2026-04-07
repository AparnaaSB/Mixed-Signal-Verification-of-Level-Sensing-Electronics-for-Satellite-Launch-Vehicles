# tb/scoreboards/data_scoreboard.py

import csv
import time
import math
import cocotb
import cocotb.utils

class DataScoreboard:
    def __init__(self, adc_model, monitor, channel_cfg, mode):
        self.adc = adc_model
        self.monitor = monitor
        self.channel_cfg = channel_cfg
        self.mode = mode
        filename = f"Data_{time.strftime('%Y%m%d_%H%M%S')}.csv"
        self.log_file = open(filename, "w", newline="")
        self.writer = csv.writer(self.log_file)

        # CSV Header
        self.writer.writerow([
            "Channel",
            "RMS_Expected",
            "RMS_Actual",
            "Filter_Sample_1",
            "Filter_Sample_1",
            "Filter_Sample_1",
            "Median",
            "Difference(RMS_Expected_and_RMS_Actual)",
            "Difference(RMS_Expected_and_Median)"
        ])

    async def run(self):
        while True:
            channel, actual_rms, s1, s2, s3, median = await self.monitor.queue.get()
            sim_time = cocotb.utils.get_sim_time(unit="ns")

            if channel == 1:
                if self.mode == "single":
                    amp = self.channel_cfg[1]["amp"]
                    expected_rms = amp / math.sqrt(2)
                elif self.mode == "interference":
                    amp1 = self.channel_cfg[1]["amp1"]
                    amp2 = self.channel_cfg[1]["amp2"]
                    sqrd_rms = ((amp1*amp1)/2) + ((amp2*amp2)/2)
                    expected_rms = math.sqrt(sqrd_rms)
                elif self.mode == "modulation":
                    amp = self.channel_cfg[1]["amp"]
                    mi = self.channel_cfg[1]["mi"]
                    mi_int = ((mi*mi)/2) + 1
                    expected_rms = (amp)* math.sqrt(mi_int)
                elif self.mode == "dc":
                    expected_rms = abs(self.adc.channels_A[0])

            elif channel == 2:
                if self.mode == "single":
                    amp = self.channel_cfg[2]["amp"]
                    expected_rms = amp / math.sqrt(2)
                elif self.mode == "interference":
                    amp1 = self.channel_cfg[2]["amp1"]
                    amp2 = self.channel_cfg[2]["amp2"]
                    sqrd_rms = ((amp1*amp1)/2) + ((amp2*amp2)/2)
                    expected_rms = math.sqrt(sqrd_rms)
                elif self.mode == "modulation":
                    amp = self.channel_cfg[2]["amp"]
                    mi = self.channel_cfg[2]["mi"]
                    mi_int = ((mi*mi)/2) + 1
                    expected_rms = (amp/math.sqrt(2)) * math.sqrt(mi_int)                   
                elif self.mode == "dc":
                    expected_rms = abs(self.adc.channels_B[0])

            elif channel == 3:
                if self.mode == "single":
                    amp = self.channel_cfg[3]["amp"]
                    expected_rms = amp / math.sqrt(2)
                elif self.mode == "interference":
                    amp1 = self.channel_cfg[3]["amp1"]
                    amp2 = self.channel_cfg[3]["amp2"]
                    sqrd_rms = ((amp1*amp1)/2) + ((amp2*amp2)/2)
                    expected_rms = math.sqrt(sqrd_rms)
                elif self.mode == "modulation":
                    amp = self.channel_cfg[3]["amp"]
                    mi = self.channel_cfg[3]["mi"]
                    mi_int = ((mi*mi)/2) + 1
                    expected_rms = (amp/math.sqrt(2)) * math.sqrt(mi_int)                   
                elif self.mode == "dc":
                    expected_rms = abs(self.adc.channels_A[1])

            elif channel == 4:
                if self.mode == "single":
                    amp = self.channel_cfg[4]["amp"]
                    expected_rms = amp / math.sqrt(2)
                elif self.mode == "interference":
                    amp1 = self.channel_cfg[4]["amp1"]
                    amp2 = self.channel_cfg[4]["amp2"]
                    sqrd_rms = ((amp1*amp1)/2) + ((amp2*amp2)/2)
                    expected_rms = math.sqrt(sqrd_rms)
                elif self.mode == "modulation":
                    amp = self.channel_cfg[4]["amp"]
                    mi = self.channel_cfg[4]["mi"]
                    mi_int = ((mi*mi)/2) + 1
                    expected_rms = (amp/math.sqrt(2)) * math.sqrt(mi_int)                   
                elif self.mode == "dc":
                    expected_rms = abs(self.adc.channels_B[1])

            elif channel == 5:
                if self.mode == "single":
                    amp = self.channel_cfg[5]["amp"]
                    expected_rms = amp / math.sqrt(2)
                elif self.mode == "interference":
                    amp1 = self.channel_cfg[5]["amp1"]
                    amp2 = self.channel_cfg[5]["amp2"]
                    sqrd_rms = ((amp1*amp1)/2) + ((amp2*amp2)/2)
                    expected_rms = math.sqrt(sqrd_rms)
                elif self.mode == "modulation":
                    amp = self.channel_cfg[5]["amp"]
                    mi = self.channel_cfg[5]["mi"]
                    mi_int = ((mi*mi)/2) + 1
                    expected_rms = (amp/math.sqrt(2)) * math.sqrt(mi_int)                
                elif self.mode == "dc":
                    expected_rms = abs(self.adc.channels_A[2])

            elif channel == 6:
                if self.mode == "single":
                    amp = self.channel_cfg[6]["amp"]
                    expected_rms = amp / math.sqrt(2)
                elif self.mode == "interference":
                    amp1 = self.channel_cfg[6]["amp1"]
                    amp2 = self.channel_cfg[6]["amp2"]
                    sqrd_rms = ((amp1*amp1)/2) + ((amp2*amp2)/2)
                    expected_rms = math.sqrt(sqrd_rms)
                elif self.mode == "modulation":
                    amp = self.channel_cfg[6]["amp"]
                    mi = self.channel_cfg[6]["mi"]
                    mi_int = ((mi*mi)/2) + 1
                    expected_rms = (amp/math.sqrt(2)) * math.sqrt(mi_int)                   
                elif self.mode == "dc":
                    expected_rms = abs(self.adc.channels_B[2])

            elif channel == 7:
                if self.mode == "single":
                    amp = self.channel_cfg[7]["amp"]
                    expected_rms = amp / math.sqrt(2)
                elif self.mode == "interference":
                    amp1 = self.channel_cfg[7]["amp1"]
                    amp2 = self.channel_cfg[7]["amp2"]
                    sqrd_rms = ((amp1*amp1)/2) + ((amp2*amp2)/2)
                    expected_rms = math.sqrt(sqrd_rms)
                elif self.mode == "modulation":
                    amp = self.channel_cfg[7]["amp"]
                    mi = self.channel_cfg[7]["mi"]
                    mi_int = ((mi*mi)/2) + 1
                    expected_rms = (amp/math.sqrt(2)) * math.sqrt(mi_int)                 
                elif self.mode == "dc":
                    expected_rms = abs(self.adc.channels_A[3])

            elif channel == 8:
                if self.mode == "single":
                    amp = self.channel_cfg[1]["amp"]
                    expected_rms = amp / math.sqrt(2)
                elif self.mode == "interference":
                    amp1 = self.channel_cfg[8]["amp1"]
                    amp2 = self.channel_cfg[8]["amp2"]
                    sqrd_rms = ((amp1*amp1)/2) + ((amp2*amp2)/2)
                    expected_rms = math.sqrt(sqrd_rms)
                elif self.mode == "modulation":
                    amp = self.channel_cfg[8]["amp"]
                    mi = self.channel_cfg[8]["mi"]
                    mi_int = ((mi*mi)/2) + 1
                    expected_rms = (amp/math.sqrt(2)) * math.sqrt(mi_int)                 
                elif self.mode == "dc":
                    expected_rms = abs(self.adc.channels_B[3])
            else:
                continue

            diff_rms = abs(expected_rms - actual_rms)
            diff_op = abs(expected_rms - median)

            self.writer.writerow([channel,expected_rms, actual_rms, s1, s2, s3, median, diff_rms, diff_op])
