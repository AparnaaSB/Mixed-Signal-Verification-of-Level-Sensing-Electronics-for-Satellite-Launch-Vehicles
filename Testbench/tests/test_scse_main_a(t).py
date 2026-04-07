import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge
import math

from drivers.adc_driver import ADCDriver
from drivers.clock_driver import ClockDriver
from drivers.reset_driver import ResetDriver
from drivers.ahb_driver import AHBDriver

from monitors.data_plot_monitor import DataPlotMonitor
from monitors.data_monitor import DataMonitor
from monitors.expected_vs_actual_output_monitor import ExpectedVsActualMonitor
from monitors.adc_conversion_monitor import ADCConversionMonitor

from scoreboards.adc_scoreboard import ADCScoreboard
from scoreboards.data_scoreboard import DataScoreboard

from model.ADC import ADC

@cocotb.test()
async def test_scse_main(scse_main):
    adc_model = ADC(
        HW_RNGSEL_2b=0b11)
    mode = "single"
    channel_cfg = {ch: {"amp": 0.0,"freq": 0.0} for ch in range(1, 9)}

    def sine_wave(t, amplitude, frequency):
        return amplitude * math.sin(2 * math.pi * frequency * t)

    async def drive_adc_inputs(adc_model):
        sample_count = 0
        sampling_rate = 64000.0
        sampling_period_ns = (1.0 / sampling_rate) * 1e9

        amp_sequence_ch0 = [1.0, 2.0, 3.0, 4.0, 5.0] 
        amp_sequence_ch1 = [2.0, 3.0, 4.0, 5.0, 6.0]
        amp_sequence_ch2 = [3.0, 4.0, 5.0, 6.0, 7.0] 
        amp_sequence_ch3 = [4.0, 5.0, 6.0, 7.0, 8.0] 
        amp_sequence_ch4 = [5.0, 6.0, 7.0, 8.0, 9.0]  
        amp_sequence_ch5 = [6.0, 7.0, 8.0, 9.0, 10.0] 
        amp_sequence_ch6 = [7.0, 8.0, 9.0, 10.0, 11.0] 
        amp_sequence_ch7 = [8.0, 9.0, 10.0, 11.0, 12.0] 
        
        while True:
            t = sample_count / sampling_rate
            segment_index = int(t / 0.010)  
            amp_ch0 = amp_sequence_ch0[segment_index] if segment_index < len(amp_sequence_ch0) else amp_sequence_ch0[-1]
            amp_ch1 = amp_sequence_ch1[segment_index] if segment_index < len(amp_sequence_ch1) else amp_sequence_ch1[-1]
            amp_ch2 = amp_sequence_ch2[segment_index] if segment_index < len(amp_sequence_ch2) else amp_sequence_ch2[-1]
            amp_ch3 = amp_sequence_ch3[segment_index] if segment_index < len(amp_sequence_ch3) else amp_sequence_ch3[-1]
            amp_ch4 = amp_sequence_ch4[segment_index] if segment_index < len(amp_sequence_ch4) else amp_sequence_ch4[-1]
            amp_ch5 = amp_sequence_ch5[segment_index] if segment_index < len(amp_sequence_ch5) else amp_sequence_ch5[-1]
            amp_ch6 = amp_sequence_ch6[segment_index] if segment_index < len(amp_sequence_ch6) else amp_sequence_ch6[-1]
            amp_ch7 = amp_sequence_ch7[segment_index] if segment_index < len(amp_sequence_ch7) else amp_sequence_ch7[-1]
            
            channel_cfg[1]["amp"] = amp_ch0
            channel_cfg[2]["amp"] = amp_ch1
            channel_cfg[3]["amp"] = amp_ch2
            channel_cfg[4]["amp"] = amp_ch3
            channel_cfg[5]["amp"] = amp_ch4
            channel_cfg[6]["amp"] = amp_ch5
            channel_cfg[7]["amp"] = amp_ch6
            channel_cfg[8]["amp"] = amp_ch7
            
            channel_cfg[1]["freq"] = 4000
            channel_cfg[2]["freq"] = 4000
            channel_cfg[3]["freq"] = 4000
            channel_cfg[4]["freq"] = 4000
            channel_cfg[5]["freq"] = 4000
            channel_cfg[6]["freq"] = 4000
            channel_cfg[7]["freq"] = 4000
            channel_cfg[8]["freq"] = 4000 
            
            adc_model.channels_A[0] = sine_wave(t, channel_cfg[1]["amp"],channel_cfg[1]["freq"])
            adc_model.channels_B[0] = sine_wave(t, channel_cfg[2]["amp"],channel_cfg[2]["freq"])
            adc_model.channels_A[1] = sine_wave(t, channel_cfg[3]["amp"],channel_cfg[3]["freq"])
            adc_model.channels_B[1] = sine_wave(t, channel_cfg[4]["amp"],channel_cfg[4]["freq"])
            adc_model.channels_A[2] = sine_wave(t, channel_cfg[5]["amp"],channel_cfg[5]["freq"])
            adc_model.channels_B[2] = sine_wave(t, channel_cfg[6]["amp"],channel_cfg[6]["freq"])
            adc_model.channels_A[3] = sine_wave(t, channel_cfg[7]["amp"],channel_cfg[7]["freq"])
            adc_model.channels_B[3] = sine_wave(t, channel_cfg[8]["amp"],channel_cfg[8]["freq"])

            sample_count += 1
            await Timer(sampling_period_ns, "ns")       
        

    clk = ClockDriver(scse_main.clk_16, 62.5)
    clk.start()

    reset = ResetDriver(scse_main.POR, 2)
    cocotb.start_soon(reset.run())
    
    cocotb.start_soon(drive_adc_inputs(adc_model))

    adc_driver = ADCDriver(scse_main, adc_model)
    cocotb.start_soon(adc_driver.run())

    conv_monitor = ADCConversionMonitor(adc_model)
    adc_scoreboard = ADCScoreboard(conv_monitor)
    cocotb.start_soon(conv_monitor.run())
    cocotb.start_soon(adc_scoreboard.run())

    ahb = AHBDriver(scse_main)
    cocotb.start_soon(ahb.latch_hreadyout())
    cocotb.start_soon(ahb.sram_read())

    data_monitor = DataMonitor(scse_main)
    cocotb.start_soon(data_monitor.run())

    data_scoreboard = DataScoreboard(adc_model, data_monitor, channel_cfg, mode)
    cocotb.start_soon(data_scoreboard.run())

    data_plot = DataPlotMonitor(scse_main, adc_model)
    cocotb.start_soon(data_plot.run())
    expected_actual_op_monitor = ExpectedVsActualMonitor(scse_main, adc_model,channel_cfg,mode)
    cocotb.start_soon(expected_actual_op_monitor.run())
    
    await Timer(20, unit="ms")
    data_plot.plot()
    expected_actual_op_monitor.plot()