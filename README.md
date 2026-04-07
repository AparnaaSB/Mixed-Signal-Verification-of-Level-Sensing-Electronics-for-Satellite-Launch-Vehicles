# Mixed-Signal Verification of Level Sensing Electronics for Satellite Launch Vehicles

## Overview

This project presents a robust mixed-signal design and verification framework for a real-time propellant level sensing system used in satellite launch vehicles.  Developed as part of my MSc thesis in collaboration with ISRO, the work addresses a critical gap in aerospace electronics verification: the inability of conventional analog-digital partitioned flows to detect cross-domain faults at the ADC interface under radiation stress.

The framework integrates SPICE-simulated analog waveforms directly with FPGA RTL  logic using cocotb, enabling end-to-end mixed-signal verification of a flight-critical avionics subsystem.

**Note:** The RTL design is proprietary to ISRO–VSSC and hence, not included. This repository includes the testbench along with documentation of the methodology, architecture and results.

## System Architecture

The Level Sensing Electronics (LSE) subsystem measures real-time propellant levels in semi-cryogenic and cryogenic engines using capacitive sensors. The complete signal chain:
ANALOG FRONT END (Capacitive Sensor → Signal Conditioning → Filter) → ANALOG-DIGITAL CONVERSION (ADC) → DIGITAL SIGNAL PROCESSING IN FPGA (ADC Interface → RMS Computation → Digital Filter → Median Filter → AHB Interface) → DATA COMMUNICATION (Processor → Ethernet)
## Framework Architecture

Four-component Python testbench interfacing with QuestaSim via FLI:

- **Drivers**:                ADC interface stimulus, AHB bus, clock and reset
- **Behavioral ADC Model**:   Non-ideal 16-bit SAR ADC with radiation effects
- **Monitors**:               RTL signal capture, expected vs actual validation
- **Scoreboard**:             Coverage aggregation, DNL/INL/ENOB metrics

## ADC Behavioral Model — Non-Idealities Modeled (AD7616)

- **ENOB degradation**:                          Uniformly distributed noise achieving ~80 dB SINAD 
- **DNL/INL nonlinearity**:                      Parabolic envelope ±0.8 LSB mid-code, constrained to ±2 LSB INL per datasheet
- **Radiation-induced SEU fault injection**:     Self-defined worst-case MSB inversion methodology

## Test Scenarios

- **DC - Baseline Fidelity**
- **DC Full-Scale Linearity Sweep**            
- **AC Nominal**
- **Overrange / Clipping**
- **AC Modulation - Propellant Depletion**
- **Multi-frequency Interference**
