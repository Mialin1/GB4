import time
import serial
import matplotlib.pyplot as plt
import numpy as np
from Drone_control import controlDrone

def detect_and_plot_PDM_real_time(duration=60, sampling_rate=5, duration_threshold=10.0, port='/dev/cu.usbmodem101'):
    ser = serial.Serial(port, 9600)
    time.sleep(2)
    print(" Started real-time PDM detection...")

    x_data = []
    y_data = []
    timestamps = []
    bits = []
    active = False
    t_rise = None
    last_bit_time = time.time()
    symbol_check_interval = 2  # Interval to insert '2' if no bit detected

    # === Plot Setup ===
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="Gas Sensor")
    threshold_line, = ax.plot([], [], 'r--', label="Dynamic Threshold")
    ax.set_ylim(0, 500)
    ax.set_xlim(0, 10000)
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("Gas Value")
    ax.legend()

    start_time = time.time()

    try:
        while time.time() - start_time < duration:
            now = time.time()

            if now - last_bit_time > symbol_check_interval:
                #bits.append(2)
                print(" No bit detected recently → Inserted 2")
                last_bit_time = now

            if ser.in_waiting:
                line_str = ser.readline().decode('utf-8').strip()
                if line_str.isdigit():
                    val = int(line_str)
                    timestamp = time.time() - start_time
                    x_data.append(len(x_data))
                    y_data.append(val)
                    timestamps.append(timestamp)

                    # Dynamic threshold
                    dynamic_threshold = 230
                    if len(y_data) >= 10:
                        baseline = np.mean(y_data[:10])
                        #peak = max(y_data[-10:])
                        # dynamic_threshold = baseline + 0.35 * (peak - baseline)
                        baseline = 0.95 * baseline + 0.1 * val
                        dynamic_threshold = baseline + 90  # offset
                        threshold_line.set_xdata(x_data)
                        threshold_line.set_ydata([dynamic_threshold] * len(x_data))

                    # PDM detection
                    if val > dynamic_threshold and not active:
                        t_rise = timestamp
                        active = True

                    elif val <= dynamic_threshold and active:
                        t_fall = timestamp
                        duration_high = t_fall - t_rise 
                        active = False
                        if duration_high >= duration_threshold:
                            bit = 1
                        else:
                            bit = 0
                        bits.append(bit)
                        if len(bits)>1 and bits[-2] == bit:
                            bit=2
                       
                        last_bit_time = time.time()
                        print(f"Detected Bit: {bit}, Duration Above Threshold: {duration_high:.2f}s")
                        controlDrone(bit, port, 9600)

                    # Plotting
                    line.set_xdata(x_data)
                    line.set_ydata(y_data)
                    ax.set_xlim(max(0, len(x_data) - 10000), len(x_data))
                    plt.draw()
                    plt.pause(0.01)

            time.sleep(1 / sampling_rate)

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        ser.close()
        plt.ioff()
        plt.show()
        print(" Serial port closed.")
        return bits, timestamps, y_data

if __name__ == "__main__":
    bits, ts, y = detect_and_plot_PDM_real_time(duration=10000, sampling_rate=5, duration_threshold=6, port='/dev/cu.usbmodem101')
