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
from monitors.RMS_FilterSample1 import RMSFilterSample1

from scoreboards.adc_scoreboard import ADCScoreboard
from scoreboards.data_scoreboard import DataScoreboard

from model.ADC import ADC

@cocotb.test()
async def test_scse_main(scse_main):
    adc_model = ADC(
        HW_RNGSEL_2b=0b11)
    mode = "single"
    channel_cfg = {
                        1: {"amp": 5.0, "freq": 4000},
                        2: {"amp": 1.0, "freq": 4000},
                        3: {"amp": 2.0, "freq": 4000},
                        4: {"amp": 3.0, "freq": 4000},
                        5: {"amp": 7.0, "freq": 4000},
                        6: {"amp": 8.0, "freq": 4000},
                        7: {"amp": 9.0, "freq": 4000},
                        8: {"amp": 10.0, "freq": 4000}
                    }
    def sine_wave(t, amplitude, frequency):
        return amplitude * math.sin(2 * math.pi * frequency * t)

    async def drive_adc_inputs(adc_model):
        sample_count = 0
        sampling_rate = 64000.0
        sampling_period_ns = (1.0 / sampling_rate) * 1e9
        # Explicit per-channel configuration
        
        while True:
            t = sample_count / sampling_rate

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

    # Clock
    clk = ClockDriver(scse_main.clk_16, 62.5)
    clk.start()
    
    # Reset
    reset = ResetDriver(scse_main.POR, 2)
    cocotb.start_soon(reset.run())

    
    adc_driver = ADCDriver(scse_main, adc_model)
    cocotb.start_soon(drive_adc_inputs(adc_model))
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
    RMS_FilterSample1 = RMSFilterSample1(scse_main, adc_model)
    cocotb.start_soon(RMS_FilterSample1.run())
    
    await Timer(3, unit="ms")
    
    # Plotting Graphs
    data_plot.plot()
    
    expected_actual_op_monitor.plot()
