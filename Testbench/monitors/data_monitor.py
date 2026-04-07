# tb/monitors/data_monitor.py

import cocotb
from cocotb.triggers import RisingEdge
from cocotb.queue import Queue

class DataMonitor:
    def __init__(self, scse_main, num_channels=8):
        self.scse_main = scse_main
        self.queue = Queue()
        self.prev_rdy1 = 0
        self.prev_rdy2 = 0
        self.prev_rdy3 = 0
        self.prev_rdy4 = 0
        self.prev_rdy5 = 0
        self.prev_rdy6 = 0
        self.prev_rdy7 = 0
        self.prev_rdy8 = 0

    def _calc_int(self, signal) -> int:
        raw = signal.value
        if not raw.is_resolvable:
            return 0
        return int(raw)

    async def run(self):
        while True:
            await RisingEdge(self.scse_main.clk_16)
            rdy1 = self._calc_int(self.scse_main.RMS_sample_ready1)
            rdy2 = self._calc_int(self.scse_main.RMS_sample_ready2)
            rdy3 = self._calc_int(self.scse_main.RMS_sample_ready3)
            rdy4 = self._calc_int(self.scse_main.RMS_sample_ready4)
            rdy5 = self._calc_int(self.scse_main.RMS_sample_ready5)
            rdy6 = self._calc_int(self.scse_main.RMS_sample_ready6)
            rdy7 = self._calc_int(self.scse_main.RMS_sample_ready7)
            rdy8 = self._calc_int(self.scse_main.RMS_sample_ready8)
            
            # Ch:1
            if rdy1 == 1 and self.prev_rdy1 == 0:
                
                rms_code = self._calc_int(self.scse_main.rms_value1)
                if rms_code >= 32768:
                    rms_code -= 65536
                rms = rms_code * (10.0 / 32768.0)
                
                s1_code = self._calc_int(self.scse_main.level_ISR_T_sample1)
                if s1_code >= 32768:
                    s1_code -= 65536
                s1 = s1_code * (10.0 / 32768.0)
                
                s2_code = self._calc_int(self.scse_main.level_ISR_T_sample2)
                if s2_code >= 32768:
                    s2_code -= 65536
                s2 = s2_code * (10.0 / 32768.0)

                s3_code = self._calc_int(self.scse_main.level_ISR_T_sample3)
                if s3_code >= 32768:
                    s3_code -= 65536
                s3 = s3_code * (10.0 / 32768.0)

                median_code = self._calc_int(self.scse_main.median_level_ISR_T)
                if median_code >= 32768:
                    median_code -= 65536
                median = median_code * (10.0 / 32768.0)                
                await self.queue.put((1, rms, s1, s2, s3, median))

            # Ch:2
            if rdy2 == 1 and self.prev_rdy2 == 0:
                
                rms_code = self._calc_int(self.scse_main.rms_value2)
                if rms_code >= 32768:
                    rms_code -= 65536
                rms = rms_code * (10.0 / 32768.0)
                
                s1_code = self._calc_int(self.scse_main.level_LOX_T_sample1)
                if s1_code >= 32768:
                    s1_code -= 65536
                s1 = s1_code * (10.0 / 32768.0)
                
                s2_code = self._calc_int(self.scse_main.level_LOX_T_sample2)
                if s2_code >= 32768:
                    s2_code -= 65536
                s2 = s2_code * (10.0 / 32768.0)

                s3_code = self._calc_int(self.scse_main.level_LOX_T_sample3)
                if s3_code >= 32768:
                    s3_code -= 65536
                s3 = s3_code * (10.0 / 32768.0)

                median_code = self._calc_int(self.scse_main.median_level_LOX_T)
                if median_code >= 32768:
                    median_code -= 65536
                median = median_code * (10.0 / 32768.0)                
                await self.queue.put((2, rms, s1, s2, s3, median))

            # Ch:3
            if rdy3 == 1 and self.prev_rdy3 == 0:
                
                rms_code = self._calc_int(self.scse_main.rms_value3)
                if rms_code >= 32768:
                    rms_code -= 65536
                rms = rms_code * (10.0 / 32768.0)
                
                s1_code = self._calc_int(self.scse_main.level_ISR_M_sample1)
                if s1_code >= 32768:
                    s1_code -= 65536
                s1 = s1_code * (10.0 / 32768.0)
                
                s2_code = self._calc_int(self.scse_main.level_ISR_M_sample2)
                if s2_code >= 32768:
                    s2_code -= 65536
                s2 = s2_code * (10.0 / 32768.0)

                s3_code = self._calc_int(self.scse_main.level_ISR_M_sample3)
                if s3_code >= 32768:
                    s3_code -= 65536
                s3 = s3_code * (10.0 / 32768.0)

                median_code = self._calc_int(self.scse_main.median_level_ISR_M)
                if median_code >= 32768:
                    median_code -= 65536
                median = median_code * (10.0 / 32768.0)                
                await self.queue.put((3, rms, s1, s2, s3, median))

            # Ch:4
            if rdy4 == 1 and self.prev_rdy4 == 0:
                
                rms_code = self._calc_int(self.scse_main.rms_value4)
                if rms_code >= 32768:
                    rms_code -= 65536
                rms = rms_code * (10.0 / 32768.0)
                
                s1_code = self._calc_int(self.scse_main.level_LOX_M_sample1)
                if s1_code >= 32768:
                    s1_code -= 65536
                s1 = s1_code * (10.0 / 32768.0)
                
                s2_code = self._calc_int(self.scse_main.level_LOX_M_sample2)
                if s2_code >= 32768:
                    s2_code -= 65536
                s2 = s2_code * (10.0 / 32768.0)

                s3_code = self._calc_int(self.scse_main.level_LOX_M_sample3)
                if s3_code >= 32768:
                    s3_code -= 65536
                s3 = s3_code * (10.0 / 32768.0)

                median_code = self._calc_int(self.scse_main.median_level_LOX_M)
                if median_code >= 32768:
                    median_code -= 65536
                median = median_code * (10.0 / 32768.0)                
                await self.queue.put((4, rms, s1, s2, s3, median))

            # Ch:5
            if rdy5 == 1 and self.prev_rdy5 == 0:
                
                rms_code = self._calc_int(self.scse_main.rms_value5)
                if rms_code >= 32768:
                    rms_code -= 65536
                rms = rms_code * (10.0 / 32768.0)
                
                s1_code = self._calc_int(self.scse_main.level_ISR_B_sample1)
                if s1_code >= 32768:
                    s1_code -= 65536
                s1 = s1_code * (10.0 / 32768.0)
                
                s2_code = self._calc_int(self.scse_main.level_ISR_B_sample2)
                if s2_code >= 32768:
                    s2_code -= 65536
                s2 = s2_code * (10.0 / 32768.0)

                s3_code = self._calc_int(self.scse_main.level_ISR_B_sample3)
                if s3_code >= 32768:
                    s3_code -= 65536
                s3 = s3_code * (10.0 / 32768.0)

                median_code = self._calc_int(self.scse_main.median_level_ISR_B)
                if median_code >= 32768:
                    median_code -= 65536
                median = median_code * (10.0 / 32768.0)                
                await self.queue.put((5, rms, s1, s2, s3, median))

            # Ch:6
            if rdy6 == 1 and self.prev_rdy6 == 0:
                
                rms_code = self._calc_int(self.scse_main.rms_value6)
                if rms_code >= 32768:
                    rms_code -= 65536
                rms = rms_code * (10.0 / 32768.0)
                
                s1_code = self._calc_int(self.scse_main.level_LOX_B_sample1)
                if s1_code >= 32768:
                    s1_code -= 65536
                s1 = s1_code * (10.0 / 32768.0)
                
                s2_code = self._calc_int(self.scse_main.level_LOX_B_sample2)
                if s2_code >= 32768:
                    s2_code -= 65536
                s2 = s2_code * (10.0 / 32768.0)

                s3_code = self._calc_int(self.scse_main.level_LOX_B_sample3)
                if s3_code >= 32768:
                    s3_code -= 65536
                s3 = s3_code * (10.0 / 32768.0)

                median_code = self._calc_int(self.scse_main.median_level_LOX_B)
                if median_code >= 32768:
                    median_code -= 65536
                median = median_code * (10.0 / 32768.0)                
                await self.queue.put((6, rms, s1, s2, s3, median))

            # Ch:7
            if rdy7 == 1 and self.prev_rdy7 == 0:
                
                rms_code = self._calc_int(self.scse_main.rms_value7)
                if rms_code >= 32768:
                    rms_code -= 65536
                rms = rms_code * (10.0 / 32768.0)
                
                s1_code = self._calc_int(self.scse_main.level_ISR_EXC_sample1)
                if s1_code >= 32768:
                    s1_code -= 65536
                s1 = s1_code * (10.0 / 32768.0)
                
                s2_code = self._calc_int(self.scse_main.level_ISR_EXC_sample2)
                if s2_code >= 32768:
                    s2_code -= 65536
                s2 = s2_code * (10.0 / 32768.0)

                s3_code = self._calc_int(self.scse_main.level_ISR_EXC_sample3)
                if s3_code >= 32768:
                    s3_code -= 65536
                s3 = s3_code * (10.0 / 32768.0)

                median_code = self._calc_int(self.scse_main.median_level_ISR_EXC)
                if median_code >= 32768:
                    median_code -= 65536
                median = median_code * (10.0 / 32768.0)                
                await self.queue.put((7, rms, s1, s2, s3, median))

            # Ch:8
            if rdy8 == 1 and self.prev_rdy8 == 0:
                
                rms_code = self._calc_int(self.scse_main.rms_value8)
                if rms_code >= 32768:
                    rms_code -= 65536
                rms = rms_code * (10.0 / 32768.0)
                
                s1_code = self._calc_int(self.scse_main.level_LOX_EXC_sample1)
                if s1_code >= 32768:
                    s1_code -= 65536
                s1 = s1_code * (10.0 / 32768.0)
                
                s2_code = self._calc_int(self.scse_main.level_LOX_EXC_sample2)
                if s2_code >= 32768:
                    s2_code -= 65536
                s2 = s2_code * (10.0 / 32768.0)

                s3_code = self._calc_int(self.scse_main.level_LOX_EXC_sample3)
                if s3_code >= 32768:
                    s3_code -= 65536
                s3 = s3_code * (10.0 / 32768.0)

                median_code = self._calc_int(self.scse_main.median_level_LOX_EXC)
                if median_code >= 32768:
                    median_code -= 65536
                median = median_code * (10.0 / 32768.0)                
                await self.queue.put((8, rms, s1, s2, s3, median))

            self.prev_rdy1 = rdy1
            self.prev_rdy2 = rdy2
            self.prev_rdy3 = rdy3
            self.prev_rdy4 = rdy4
            self.prev_rdy5 = rdy5
            self.prev_rdy6 = rdy6
            self.prev_rdy7 = rdy7
            self.prev_rdy8 = rdy8
         

