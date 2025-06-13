import serial
import time

def controlDrone(bit, port='/dev/ttyACM0', baudrate=9600):
    """
    Controls the drone via Arduino pin 10 using a binary input.
    Bit 1 simulates a button press: sends '1' to Arduino via serial.
    Bit 0 does nothing (idle).
    """
    if bit not in (0, 1):
        print("Invalid input: only 0 or 1 allowed.")
        return

    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Allow Arduino to reset

        if bit == 1:
            print("Sending signal to drone...")
            ser.write(b'1')  # Send trigger signal
            time.sleep(0.2)
            print("Signal '1' sent.")
        elif bit ==0:
            ser.write(b'0')
            time.sleep(0.2)
            print("Signal '0' sent.")
        else:
            print("Bit 2 received: No action taken.")

        ser.close()

    except serial.SerialException as e:
        print(f"Serial error: {e}")

