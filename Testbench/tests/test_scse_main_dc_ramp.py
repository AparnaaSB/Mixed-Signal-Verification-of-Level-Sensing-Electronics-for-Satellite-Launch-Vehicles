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
from scoreboards.dnl_scoreboard import DNLMonitor
from scoreboards.inl_scoreboard import INLMonitor

from model.ADC import ADC

@cocotb.test()

async def test_scse_main(scse_main):
    adc_model = ADC(
        HW_RNGSEL_2b=0b11)
    mode = "dc"
    channel_cfg = {}
    async def drive_dc_inputs(adc_model):
        sampling_rate = 64000.0
        sampling_period_ns = (1.0 / sampling_rate) * 1e9


        step_time = 0.008  


        dc_levels = [-10.0,-9.0,-8.0,-7.0,-6.0,-5.0,-4.0,-3.0,-2.0,-1.0,0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0]

        sample_count = 0

        while True:
            t = sample_count / sampling_rate
            step_index = int(t / step_time)

            if step_index >= len(dc_levels):
                step_index = len(dc_levels) - 1

            dc_val = dc_levels[step_index]
            adc_model.channels_A[0] = dc_val
            adc_model.channels_B[0] = dc_val
            adc_model.channels_A[1] = dc_val
            adc_model.channels_B[1] = dc_val
            adc_model.channels_A[2] = dc_val
            adc_model.channels_B[2] = dc_val
            adc_model.channels_A[3] = dc_val
            adc_model.channels_B[3] = dc_val

            sample_count += 1
            await Timer(sampling_period_ns, "ns")


    clk = ClockDriver(scse_main.clk_16, 62.5)
    clk.start()

    reset = ResetDriver(scse_main.POR, 2)
    cocotb.start_soon(reset.run())
    
    adc_driver = ADCDriver(scse_main, adc_model)
    cocotb.start_soon(adc_driver.run())
    cocotb.start_soon(drive_dc_inputs(adc_model))

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
    await Timer(220, unit="ms")
    
    data_plot.plot()
    expected_actual_op_monitor.plot()