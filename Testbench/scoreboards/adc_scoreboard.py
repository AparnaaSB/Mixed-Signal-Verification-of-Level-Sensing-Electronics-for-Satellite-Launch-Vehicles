#tb/scoreboards/adc_scoreboard.py

import csv
import time
import cocotb
from collections import defaultdict

class ADCScoreboard:
    def __init__(self, monitor):
        self.monitor = monitor

        filename = f"ADC_Conversions_{time.strftime('%Y%m%d_%H%M%S')}.csv"
        self.log_file = open(filename, "w", newline="")
        self.writer = csv.writer(self.log_file)
        self.writer.writerow(["Channel",
            "Voltage (V)",
            "ADC_Code_Hex (Decimal)"
        ])

    async def run(self):
        while True:
            result = await self.monitor.queue.get()
            ch = result["channel"]
            voltage = result["voltage"]
            code = int(result["code"]) & 0xFFFF

            voltage_str = f"{voltage:+.4f}"
            hex_str = f"0x{code:04X}"
            dec_str = f"{code:d}"
            self.writer.writerow([ch,
                voltage_str,
                f"{hex_str} ({dec_str})"
            ])
            self.log_file.flush()