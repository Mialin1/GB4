import time
import serial
import matplotlib.pyplot as plt
import numpy as np
from Drone_control import controlDrone

def detect_and_plot_OOK_real_time(duration=40, sampling_rate=10, symbol_interval=5, threshold=None, port='/dev/cu.usbmodem21401'):
    ser = serial.Serial(port, 9600)
    time.sleep(2)

    x_data = []
    y_data = []
    timestamps = []
    bits = []

    # === Plot Setup ===
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="Gas Sensor")
    threshold_line, = ax.plot([], [], 'r--', label="Dynamic Threshold")
    ax.set_ylim(0, 500)
    ax.set_xlim(0, 400)
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("Gas Value")
    ax.legend()

    start_time = time.time()
    delay = 2
    next_symbol_time = start_time + delay + symbol_interval
    interval_lines_drawn = []

    try:
        while time.time() - start_time < duration:
            if ser.in_waiting:
                line_str = ser.readline().decode('utf-8').strip()
                if line_str.isdigit():
                    val = int(line_str)
                    current_time = time.time()
                    timestamp = time.time() - start_time
                    x_data.append(len(x_data))
                    y_data.append(val)
                    timestamps.append(timestamp)

                    # Update Plot
                    line.set_xdata(x_data)
                    line.set_ydata(y_data)
                    
                    if len(x_data) > 1000:
                         break

                    # Dynamic threshold from initial values
                    if len(y_data) >= 10:
                        dynamic_threshold = 230
                        threshold_line.set_xdata(x_data)
                        threshold_line.set_ydata([dynamic_threshold] * len(x_data))
                    else:
                        dynamic_threshold = 230

                    ax.set_xlim(max(0, len(x_data) - 400), len(x_data))
                    plt.draw()
                    plt.pause(0.001)
                    
                    current_elapsed = current_time - (start_time + delay)
                    if current_elapsed >= 0:
                        elapsed_int = int(current_elapsed // symbol_interval)
                        for i in range(elapsed_int + 1):
                            t_line = delay + i * symbol_interval
                            if t_line not in interval_lines_drawn and t_line <= duration:
                                ax.axvline(x=len(x_data) * t_line / timestamp, color='gray', linestyle='--', linewidth=1)
                                interval_lines_drawn.append(t_line)

                    # Bit detection every symbol_interval seconds
                    if time.time() >= next_symbol_time:
                        symbol_start = next_symbol_time - symbol_interval - start_time
                        symbol_end = next_symbol_time - start_time
                        segment = [v for t, v in zip(timestamps, y_data) if symbol_start <= t < symbol_end]
                        
                        bit = 1 if max(segment, default=0) > dynamic_threshold else 0
                        bits.append(bit)
                        print(f"🔹 Detected Bit: {bit}")
                        next_symbol_time += symbol_interval
                        # transfer to drone control
                        controlDrone(bit, port, 9600)  # Uncomment to control drone
                    else:
                        bits.append(2)
                   
                       

            time.sleep(1 / sampling_rate)

    except KeyboardInterrupt:
        print("\n🛑 User interrupted.")

    finally:
        ser.close()
        plt.ioff()
        plt.show()

    return bits, timestamps, y_data




while __name__ == "__main__":
    bits, time, y = detect_and_plot_OOK_real_time(duration=100, sampling_rate=5, symbol_interval=12, threshold=170, port='/dev/cu.usbmodem21401')
    print("Starting OOK detection...")