import serial
import time
import random

def OOKmodulation(bit_train, port='/dev/cu.usbmodem1101', baudrate=9600,
                  spray_duration=0.3, symbol_interval=4.0):
    
    assert all(bit in [0, 1] for bit in bit_train), "Only 0 and 1 are allowed in bit_train"

    print(f"Connecting to Arduino on {port}...")
    ser = serial.Serial(port, baudrate)
    time.sleep(2)  # Wait for Arduino to initialize
    print("Connection established.")

    print("Starting OOK transmission...")
    for i, bit in enumerate(bit_train):
        print(f"Transmitting bit {i+1}/{len(bit_train)}: {bit}")

        if bit == 1:
            ser.write(b'1')  # Spray ON
            time.sleep(spray_duration)
            ser.write(b'0')  # Spray OFF to ensure it's turned off
             # ser.write(b'0')  # Do nothing, stay OFF

        remaining_time = symbol_interval - spray_duration if bit == 1 else symbol_interval
        time.sleep(remaining_time)

    ser.close()
    print("Transmission complete.")



if __name__ == "__main__":
    bit_sequence = [random.randint(0, 1) for _ in range(7)]
    print(f"Random 7-bit sequence: {bit_sequence}")

    OOKmodulation(bit_sequence, spray_duration=0.2, symbol_interval=8)


