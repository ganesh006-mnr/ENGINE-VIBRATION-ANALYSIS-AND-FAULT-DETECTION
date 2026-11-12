"""
Engine Vibration Analysis and Fault Detection
---------------------------------------------
A student-level Python project using simulated vibration signals.

The program compares five engine conditions:
1. Normal operation
2. Rotor imbalance
3. Misalignment
4. Mechanical looseness
5. Bearing fault

It displays time-domain, frequency-domain, and engine-order plots.
The signals are simulated; they are not measurements from a real engine.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft


# ---------------------------------------------------------
# 1. CREATE TIME AND ENGINE SPEED
# ---------------------------------------------------------

sampling_rate = 2000       # Samples recorded per second (Hz)
duration = 6                # Simulation length in seconds

time = np.arange(0, duration, 1 / sampling_rate)

start_rpm = 1000
end_rpm = 4000

# Engine speed increases gradually during the simulation.
rpm = np.linspace(start_rpm, end_rpm, len(time))
rotational_frequency = rpm / 60  # Convert RPM to rotations per second

# Phase is used to create vibration signals whose frequency
# follows the changing engine speed.
phase = 2 * np.pi * np.cumsum(rotational_frequency) / sampling_rate

# Use a fixed seed so the same random noise is produced each run.
random_generator = np.random.default_rng(7)
sensor_noise = 0.1 * random_generator.standard_normal(len(time))


# ---------------------------------------------------------
# 2. SIMULATE VIBRATION FOR EACH ENGINE CONDITION
# ---------------------------------------------------------

# Normal engine: mostly 1X vibration, with smaller 2X and 3X parts.
normal_signal = (
    1.0 * np.sin(phase)
    + 0.5 * np.sin(2 * phase)
    + 0.25 * np.sin(3 * phase)
    + sensor_noise
)

# Imbalance: represented by a stronger 1X component.
imbalance_signal = (
    2.0 * np.sin(phase)
    + 0.5 * np.sin(2 * phase)
    + 0.25 * np.sin(3 * phase)
    + sensor_noise
)

# Misalignment: represented by stronger 2X and 3X components.
misalignment_signal = (
    1.0 * np.sin(phase)
    + 1.0 * np.sin(2 * phase)
    + 0.7 * np.sin(3 * phase)
    + sensor_noise
)

# Looseness: represented by several harmonic components.
looseness_signal = (
    1.0 * np.sin(phase)
    + 0.8 * np.sin(2 * phase)
    + 0.6 * np.sin(3 * phase)
    + 0.45 * np.sin(4 * phase)
    + 0.30 * np.sin(5 * phase)
    + sensor_noise
)

# Bearing fault: repeated impacts create short, decaying vibrations.
impact_frequency = 120  # Impacts per second (Hz)
impact_interval = int(sampling_rate / impact_frequency)
bearing_response = np.zeros(len(time))

decay_length = int(0.03 * sampling_rate)

for impact_start in range(0, len(time), impact_interval):
    impact_end = min(impact_start + decay_length, len(time))
    local_time = np.arange(impact_end - impact_start) / sampling_rate

    decay = np.exp(-120 * local_time)
    high_frequency_vibration = np.sin(2 * np.pi * 600 * local_time)

    bearing_response[impact_start:impact_end] += (
        decay * high_frequency_vibration
    )

bearing_signal = normal_signal + 0.8 * bearing_response


# Keep signals together so the same plotting and analysis steps
# can be applied to each condition.
signals = {
    "Normal": normal_signal,
    "Imbalance": imbalance_signal,
    "Misalignment": misalignment_signal,
    "Looseness": looseness_signal,
    "Bearing fault": bearing_signal,
}


# ---------------------------------------------------------
# 3. TIME-DOMAIN PLOT
# ---------------------------------------------------------

plt.figure(figsize=(12, 5))

for condition, signal in signals.items():
    plt.plot(time, signal, label=condition, linewidth=1)

plt.xlim(0, 1)  # Show the first second for easier comparison.
plt.xlabel("Time (seconds)")
plt.ylabel("Vibration amplitude")
plt.title("Engine Vibration Under Different Conditions")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# ---------------------------------------------------------
# 4. RMS VIBRATION LEVEL
# ---------------------------------------------------------

print("\nVIBRATION FEATURE ANALYSIS")
print("--------------------------")

rms_values = {}

for condition, signal in signals.items():
    # RMS gives an overall measure of vibration level.
    rms = np.sqrt(np.mean(signal ** 2))
    rms_values[condition] = rms
    print(f"{condition:15s} RMS: {rms:.3f}")


# ---------------------------------------------------------
# 5. FFT FREQUENCY SPECTRUM
# ---------------------------------------------------------

number_of_samples = len(time)
frequencies = np.fft.rfftfreq(number_of_samples, d=1 / sampling_rate)

# Calculate the FFT amplitude for each condition.
fft_amplitudes = {}

for condition, signal in signals.items():
    fft_values = np.fft.rfft(signal)
    fft_amplitudes[condition] = 2 * np.abs(fft_values) / number_of_samples

plt.figure(figsize=(12, 5))

for condition, amplitude in fft_amplitudes.items():
    plt.plot(frequencies, amplitude, label=condition, linewidth=1)

plt.xlim(0, 1000)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.title("Frequency Spectrum - Engine Fault Comparison")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# ---------------------------------------------------------
# 6. SHORT-TIME FOURIER TRANSFORM (STFT)
# ---------------------------------------------------------

# STFT shows how the frequency content changes over time.
stft_results = {}

for condition, signal in signals.items():
    stft_frequencies, stft_times, stft_values = stft(
        signal,
        fs=sampling_rate,
        nperseg=1024,
        noverlap=768,
    )
    stft_results[condition] = np.abs(stft_values)

# Estimate the engine RPM at each STFT time point.
rpm_at_stft_time = np.interp(stft_times, time, rpm)

# Convert frequency in Hz into engine order:
# order = vibration frequency / engine rotational frequency.
order_grid = (
    stft_frequencies[:, np.newaxis] * 60
    / rpm_at_stft_time[np.newaxis, :]
)


# ---------------------------------------------------------
# 7. ENGINE-ORDER FEATURE COMPARISON
# ---------------------------------------------------------

def get_order_amplitude(magnitude, target_order, tolerance=0.08):
    """Return the average STFT amplitude close to a chosen engine order."""
    close_to_order = np.abs(order_grid - target_order) < tolerance
    matching_values = magnitude[close_to_order]

    if matching_values.size == 0:
        return 0.0

    return float(np.mean(matching_values))


print("\nENGINE ORDER COMPARISON")
print("-----------------------")

for condition in ["Normal", "Imbalance", "Misalignment", "Looseness"]:
    magnitude = stft_results[condition]
    print(f"\n{condition}:")

    # Compare the first three orders for each condition.
    for order in [1, 2, 3]:
        value = get_order_amplitude(magnitude, order)
        print(f"  {order}X order amplitude: {value:.4f}")

# Looseness is also checked at the 4X and 5X orders.
looseness_magnitude = stft_results["Looseness"]

print("\nLooseness higher orders:")
for order in [4, 5]:
    value = get_order_amplitude(looseness_magnitude, order)
    print(f"  {order}X order amplitude: {value:.4f}")


# ---------------------------------------------------------
# 8. ENGINE-ORDER TRACKING MAP FOR LOOSENESS
# ---------------------------------------------------------

plt.figure(figsize=(12, 6))

plt.pcolormesh(
    stft_times,
    order_grid,
    looseness_magnitude,
    shading="auto",
)

plt.xlabel("Time (seconds)")
plt.ylabel("Engine order")
plt.title("Engine Order Tracking - Mechanical Looseness")
plt.colorbar(label="Vibration amplitude")
plt.ylim(0, 5)

# Dashed lines mark the 1X to 5X engine orders.
for order in range(1, 6):
    plt.axhline(order, linestyle="--", linewidth=1)

plt.tight_layout()
plt.show()
