# tb/model/adc.py

import cocotb
from cocotb.triggers import Timer,FallingEdge, RisingEdge
import math
import random
import numpy as np
class ADC:
    def __init__(          
        self,
        RESET : int = 0b0,
        SCLK: int = 0b0,
        WR : int = 0b1,
        RD : int = 0b0,
        CS: int = 0b0,
        CHSEL_3b : int = 0b000,
        CONVST : int = 0b0,
        V0A : float = 0.0,
        V1A : float = 0.0,
        V2A : float = 0.0,
        V3A : float = 0.0,
        V4A : float = 0.0,
        V5A : float = 0.0,
        V6A : float = 0.0,
        V7A : float = 0.0,
        V0B : float = 0.0,
        V1B : float = 0.0,
        V2B : float = 0.0,
        V3B : float = 0.0,
        V4B : float = 0.0,
        V5B : float = 0.0,
        V6B : float = 0.0,
        V7B : float = 0.0,
        HW_RNGSEL_2b: int = 0b11,
        REFINOUT : float = 2.5,                
        SEQEN: int = 0b1,
        SER_PAR : int = 0b0,                    # Parallel Mode
        SER1W : int = 0b0,                      # READ SDOA only; High means READ SDOA and SDOB
        # SDI : int = 0b0,                      # Used Incase of Serial Mode
        OS : int = 0b000,                       # No Oversampling
        CRC_EN : int = 0b0,                     # Redundancy Check not enabled
        REFSEL : int = 0b0                      # External Reference, use REFINOUT = 2.5V

    ) -> None:
        self.RESET = RESET
        self.SCLK = SCLK
        self.WR = WR
        self.RD = RD
        self.CS = CS
        self.CHSEL_3b = CHSEL_3b
        self.CONVST= CONVST
        self.channels_A = [V0A, V1A, V2A, V3A, V4A, V5A, V6A, V7A]
        self.channels_B = [V0B, V1B, V2B, V3B, V4B, V5B, V6B, V7B]
        self.HW_RNGSEL_2b = HW_RNGSEL_2b
        self.REFINOUT = REFINOUT
        self.SEQEN = SEQEN
        self.SER_PAR = SER_PAR
        self.SER1W = SER1W
        # self.SDI = SDI, In parallel mode, its bit 10
        self.OS = OS
        self.CRC_EN = CRC_EN
        self.REFSEL = REFSEL
              
        self.tconv = 475.0                        # Minimum Conversion Time as per Datasheet; Max 520ns
        self.tacq = 480.0                         # Acquisition Time for Selected Channel pair as per Datasheet
        

        self.DB15_DB0 = 0x0000                    
        self.BUSY = 0
        self.read_index = 0                       
        self.current_channel_index = 0            
        self.convst_count = 0
        
        self.seu_inject_at_value = 100000
        self.SNR_dB = 82
        self.apply_seu = False
        self.conversion_results = []

        if self.HW_RNGSEL_2b == 0b01:
            self.vfs = 2.5
        elif self.HW_RNGSEL_2b == 0b10:
            self.vfs = 5
        elif self.HW_RNGSEL_2b == 0b11:
            self.vfs = 10
        else:
            self.vfs = 10
            
        self.generate_dnl_profile(self.vfs)
            
        cocotb.start_soon(self.run())
        print("ADC model initialized")
    
    def generate_dnl_profile(self,vfs):
        #V[k] = (DNL_error[k] + 1) * lsb + V[k-1] ; k from 1.
        N_CODES = 65536
        self.vfs = vfs
        lsb = (2 * self.vfs)/N_CODES
        
        self.dnl_voltage_lut_positive = {}
        self.dnl_voltage_lut_negative = {}
        self.dnl_error_lut = {}
        self.inl_error_lut = {}
        
        mid_code = (N_CODES - 1) / 2
        max_error_lsb = 0.3
        min_error_lsb = 0.5
        
        V_current_upward = 0 
        V_current_downward = 0
        step = 0.001
        

        for code in range(N_CODES):
            x = (code - mid_code) / mid_code
            y = random.randint(-5, 5) * step
            dnl_error_lsb = max_error_lsb * (1.0 - x * x) + y + min_error_lsb
            sign = (-1) ** code
            dnl_error = sign * dnl_error_lsb
            self.dnl_error_lut[code] = dnl_error
            

        self.inl_error_lut[0] = 0  
        for code in range(1,N_CODES):
            self.inl_error_lut[code] = self.dnl_error_lut[code-1] + self.inl_error_lut[code-1]
            

        self.dnl_voltage_lut_positive[0] = self.dnl_error_lut[0] * lsb
        for code in range(1,32768):
            V_current_upward += (1 + self.dnl_error_lut[code]) * lsb 
            self.dnl_voltage_lut_positive[code] = V_current_upward
            
        for code in range(65535,32767,-1):
            V_current_downward -= (1 + self.dnl_error_lut[code]) * lsb
            self.dnl_voltage_lut_negative[code] = V_current_downward
            
    def apply_dnl(self, Vin: float) -> int:
        if Vin >= 0:
            if Vin <=self.dnl_voltage_lut_positive[0]:
                code = 0
            elif Vin > self.dnl_voltage_lut_positive[32767]:
                code = 32767
            else:
                for c in range (32767):
                    if self.dnl_voltage_lut_positive[c] < Vin <= self.dnl_voltage_lut_positive[c+1]:
                        code = c
        else:
            if Vin >= self.dnl_voltage_lut_negative[65535]:
                code = 0
            elif Vin < self.dnl_voltage_lut_negative[32768]:
                code = 32768
            else:
                for c in range (65535,32768,-1):
                    if self.dnl_voltage_lut_negative[c] > Vin >= self.dnl_voltage_lut_negative[c-1]:
                        code = c
        return code
        
    def apply_enob_noise(self, Vin: float, Vrms_signal: float) -> float:

        noise_rms = Vrms_signal / (10 ** (self.SNR_dB / 20))

        a = math.sqrt(3) * noise_rms

        noise = random.uniform(-a, a)

        return Vin + noise
        
    def apply_seu_output(self, code: int) -> int:

        #N_BITS = 16
        if self.apply_seu:
            corrupted = code ^ (1 << 15)
            print("SEU! Bit 15 flipped")
            self.apply_seu = False
            return corrupted & 0xFFFF
        return code
        
    def get_num_channels_from_chsel(self) -> int:
        
        if self.CHSEL_3b == 0b000:
            return 1
        elif self.CHSEL_3b == 0b001:
            return 2
        elif self.CHSEL_3b == 0b010:
            return 3
        elif self.CHSEL_3b == 0b011:
            return 4
        elif self.CHSEL_3b == 0b100:
            return 5
        elif self.CHSEL_3b == 0b101:
            return 6
        elif self.CHSEL_3b == 0b110:
            return 7
        elif self.CHSEL_3b == 0b111:
            return 8
               
    def calculate_burst_time(self, n: int) -> float:
        
        #tburst = (tconv + 25ns) + (n - 1)*(tacq + tconv) ; n = number of channel pairs
        tburst = (self.tconv + 25) + (n - 1) * (self.tacq + self.tconv)
        return tburst
    
    def calculate_single_pair_time(self) -> float:
        
        # tsingle = tconv + tacq 
        tsingle = self.tconv + self.tacq
        return tsingle          
        
    def get_channel_voltage(self, channel_index: int, is_A_side: bool = True) -> float:

        if is_A_side:
            return self.channels_A[channel_index]
        else:
            return self.channels_B[channel_index]
              
    def calculate_adc_code(self, Vin: float) -> int:
      
        Vrms_signal = self.vfs / math.sqrt(2)
        Vin = self.apply_enob_noise(Vin, Vrms_signal)
        code = self.apply_dnl(Vin)
        return code & 0xFFFF

    async def perform_conversion(self):
        num_pairs = self.get_num_channels_from_chsel()
        # t_BUSY_DELAY
        await Timer(32, unit='ns')
        self.BUSY = 1
        print("BUSY HIGH")
        
        # self.conversion_results = []
        self.read_index = 0
        
        if self.WR == 1:
            conversions = []
            for ch_num in range(num_pairs):
                voltage_A = self.get_channel_voltage(ch_num, is_A_side=True)
                voltage_B = self.get_channel_voltage(ch_num, is_A_side=False)
                
                code_A = self.calculate_adc_code(voltage_A)
                code_B = self.calculate_adc_code(voltage_B)
                
                code_A = self.apply_seu_output(code_A)
                code_B = self.apply_seu_output(code_B)
                conversions.append({
                    'ch_num': ch_num,
                    'voltage_A': voltage_A,
                    'voltage_B': voltage_B,
                    'code_A': code_A,
                    'code_B': code_B

                })
                print(f"Ch{ch_num}A: {voltage_A:+.4f}V -> 0x{code_A:04X}")
                print(f"Ch{ch_num}B: {voltage_B:+.4f}V -> 0x{code_B:04X}")

            if self.SEQEN == 1:

                for conv in conversions:
                    self.conversion_results.append({
                        'channel': f'V{conv["ch_num"]}A',
                        'voltage': conv['voltage_A'],
                        'code': conv['code_A']
                    })
                    self.conversion_results.append({
                        'channel': f'V{conv["ch_num"]}B',
                        'voltage': conv['voltage_B'],
                        'code': conv['code_B']
                    })
            else:

                for conv in conversions:
                    self.conversion_results.append({
                        'channel': f'V{conv["ch_num"]}A',
                        'voltage': conv['voltage_A'],
                        'code': conv['code_A']
                    })
                for conv in conversions:
                    self.conversion_results.append({
                        'channel': f'V{conv["ch_num"]}B',
                        'voltage': conv['voltage_B'],
                        'code': conv['code_B']
                    })
            
            burst_time = self.calculate_burst_time(num_pairs)
            await Timer(burst_time, unit='ns')
        else:
            ch_num = self.current_channel_index % num_pairs

            voltage_A = self.get_channel_voltage(ch_num, is_A_side=True)
            voltage_B = self.get_channel_voltage(ch_num, is_A_side=False)
            
            code_A = self.calculate_adc_code(voltage_A)
            code_B = self.calculate_adc_code(voltage_B)
            
            code_A = self.apply_seu_output(code_A)
            code_B = self.apply_seu_output(code_B)

            if self.SEQEN == 1:

                self.conversion_results.append({
                    'channel': f'V{ch_num}A',
                    'voltage': voltage_A,
                    'code': code_A
                })
                self.conversion_results.append({
                    'channel': f'V{ch_num}B',
                    'voltage': voltage_B,
                    'code': code_B
                })
            else:

                self.conversion_results.append({
                    'channel': f'V{ch_num}A',
                    'voltage': voltage_A,
                    'code': code_A
                })
                self.conversion_results.append({
                    'channel': f'V{ch_num}B',
                    'voltage': voltage_B,
                    'code': code_B
                })
            
            self.current_channel_index = (self.current_channel_index + 1) % num_pairs
            
            single_pair_time = self.calculate_single_pair_time()
            await Timer(single_pair_time, unit='ns')
           
        self.BUSY = 0
        print(f"Conversion complete, {len(self.conversion_results)} results ready")
        
    async def output_data(self):
        await Timer(30, unit='ns')
        if self.read_index < len(self.conversion_results):
            result = self.conversion_results[self.read_index]
            self.DB15_DB0 = (result['code'])
            print(f"RD pulse #{self.read_index}: {result['channel']} = 0x{result['code']:04X} ({result['voltage']:+.4f}V)")
            self.read_index += 1
    
    async def run(self):
        prev_convst = 0 
        prev_rd = 0 
        while True:
            await Timer(0.5, unit='ns')
            current_convst = self.CONVST
            current_rd = self.RD
            current_reset = self.RESET
            await Timer(0.5, unit='ns')
            if current_reset  == 1:
                if self.HW_RNGSEL_2b != 0b00:
                    if current_convst == 1 and prev_convst == 0:
                        self.convst_count += 1
                        print("CONVST Count : {self.convst_count}")
                        if (self.convst_count == self.seu_inject_at_value) :
                            self.apply_seu = True
                        await(self.perform_conversion())
                if self.CS == 0 and current_rd == 0 and prev_rd == 1:
                    cocotb.start_soon(self.output_data()) 
                elif self.CS == 1:
                    await Timer(11, unit='ns')
                    self.DB15_DB0 = 0x0000
                
                prev_rd = current_rd
                prev_convst = current_convst
            else:
                prev_convst = 0
                prev_rd = 0
                self.BUSY = 0
                self.DB15_DB0 = 0x0000
 
                            