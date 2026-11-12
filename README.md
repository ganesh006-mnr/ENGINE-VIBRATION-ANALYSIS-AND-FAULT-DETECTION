# ENGINE-VIBRATION-ANALYSIS-AND-FAULT-DETECTION
This notebook simulates vibration signals for five engine conditions and compares them using time-domain, frequency-domain and engine-order analysis.

# Engine Vibration Analysis Using Python

A Python project that simulates engine vibration signals and analyses them under five operating conditions.

**Note:** This project uses simulated data, not measurements from a real engine. It demonstrates basic signal-processing methods and is not a validated fault-diagnosis system.

## Project Objectives

- Simulate vibration signals for different engine conditions.
- Compare signals in the time domain.
- Calculate RMS vibration values.
- Analyse frequency components using FFT.
- Study frequency changes over time using STFT.
- Compare vibration amplitudes at different engine orders.

## Conditions Simulated

1. Normal operation
2. Rotor imbalance
3. Misalignment
4. Mechanical looseness
5. Bearing-fault-like repeated impacts

## Tools and Requirements

- Python 3
- NumPy
- Matplotlib
- SciPy

Install the required libraries:

```bash
python -m pip install numpy matplotlib scipy
```

## Files in This Repository

| File | Description |
|---|---|
| `Engine_Vibration_Analysis.py` | Main Python program. |
| `Engine_Vibration_Analysis.ipynb` | Notebook version of the project. |
| `README.md` | Project documentation. |

## How to Run

### Python File

1. Download or clone the repository.
2. Open a terminal in the project folder.
3. Install the required libraries.
4. Run:

```bash
python Engine_Vibration_Analysis.py
```

### Jupyter Notebook

1. Open `Engine_Vibration_Analysis.ipynb` in Jupyter Notebook or VS Code.
2. Ensure the required libraries are installed.
3. Run all cells from top to bottom.

## Analysis Performed

- **RMS:** Calculates the overall signal level.
- **FFT:** Shows frequency components in each signal.
- **STFT:** Shows how frequency content changes over time.
- **Engine-order analysis:** Compares vibration components with multiples of engine rotational frequency.

## Expected Output

The program prints RMS values and engine-order comparisons. It also displays three plots:

1. Time-domain comparison.
2. FFT frequency-spectrum comparison.
3. Engine-order tracking plot for mechanical looseness.

## Limitations

The signals are generated mathematically for demonstration. The results do not represent real machine measurements and should not be used for actual maintenance or safety decisions.

## Conclusion

This project demonstrates how Python can be used to generate and analyse vibration signals using RMS, FFT, STFT and engine-order analysis.
