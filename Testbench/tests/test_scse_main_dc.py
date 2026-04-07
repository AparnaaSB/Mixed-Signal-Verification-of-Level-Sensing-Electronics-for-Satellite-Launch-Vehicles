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
        HW_RNGSEL_2b=0b11,
        V0A =   0.5, V0B =  -2,
        V1A =   -3, V1B =  4,
        V2A =   6, V2B =  -5,
        V3A =   7, V3B =  -8,
        V4A =   0.0,    V4B =  0.0,
        V5A =   0.0,    V5B =  0.0,
        V6A =   0.0,    V6B =  0.0,
        V7A =   0.0,    V7B =  0.0)
    mode = "dc"
    channel_cfg = {}

    clk = ClockDriver(scse_main.clk_16, 62.5)
    clk.start()
    

    reset = ResetDriver(scse_main.POR, 2)
    cocotb.start_soon(reset.run())

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
    RMS_FilterSample1 = RMSFilterSample1(scse_main, adc_model)
    cocotb.start_soon(RMS_FilterSample1.run())
    
    dnl_monitor = DNLMonitor(adc_model)
    cocotb.start_soon(dnl_monitor.run())
    
    inl_monitor = DNLMonitor(adc_model)
    cocotb.start_soon(inl_monitor.run())
    await Timer(12, unit="ms")

    data_plot.plot()
    
    expected_actual_op_monitor.plot()
    
    RMS_FilterSample1.plot()
    
    dnl_monitor.plot()
    dnl_monitor.plot_full_dnl_profile()    
    dnl_monitor.plot_dc_histogram(None,10)

    inl_monitor.plot()
    inl_monitor.plot_full_inl_profile()    
    inl_monitor.plot_dc_histogram(None,10)