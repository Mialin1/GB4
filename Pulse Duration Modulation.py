import serial
import time

def pulsemodulation(bit_train, 
                    short_duration=0.2, long_duration=0.7, 
                    symbol_interval=5.0, 
                    port='/dev/cu.usbmodem1101', baudrate=9600):

    assert all(bit in [0, 1] for bit in bit_train), "bit_train must only contain 0 and 1"

    print(f"🔌 Connecting to Arduino on {port}...")
    ser = serial.Serial(port, baudrate)
    time.sleep(2)  # Wait for Arduino to initialize
    print("Connected.")

    print("Starting Pulse Duration Modulation...")
    for i, bit in enumerate(bit_train):
        print(f"🔢 Bit {i+1}/{len(bit_train)}: {bit}")
        if bit == 1:
            ser.write(b'1')
            time.sleep(long_duration)
        else:
            ser.write(b'1')
            time.sleep(short_duration)

        ser.write(b'0')  # Ensure spray is turned off

        remaining = symbol_interval - (long_duration if bit == 1 else short_duration)
        #time.sleep(max(0, remaining))
        time.sleep(max(0, symbol_interval))

    ser.close()
    print("✅ Transmission complete.")


if __name__ == "__main__":
    bit_sequence = [random.randint(0, 1) for _ in range(7)]
    print(f"Random 7-bit sequence: {bit_sequence}")
    pulsemodulation(bits,
                    short_duration=0.2, 
                    long_duration=1, 
                    symbol_interval=30.0) 
