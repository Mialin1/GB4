import speech_recognition as sr
import time
import wave
#from OOK_transmitter import OOKmodulation
from PDM_transmitter import pulsemodulation
import serial
import serial
import time

def pulsemodulation(bit_train, 
                    short_duration=0.2, long_duration=1.0, 
                    symbol_interval=5.0, 
                    port='/dev/cu.usbmodem1401', baudrate=9600):

    assert all(bit in [0, 1] for bit in bit_train), "bit_train must only contain 0 and 1"

    print(f" Connecting to Arduino on {port}...")
    ser = serial.Serial(port, baudrate)
    time.sleep(2)  # Wait for Arduino to initialize
    print(" Connected.")

    print("Starting Pulse Duration Modulation...")
    for i, bit in enumerate(bit_train):
        print(f" Bit {i+1}/{len(bit_train)}: {bit}")
        if bit == 1:
            ser.write(b'1')
            time.sleep(long_duration)
        else:
            ser.write(b'1')
            time.sleep(short_duration)

        ser.write(b'0')  # Ensure spray is turned off

        remaining = symbol_interval - (long_duration if bit == 1 else short_duration)
        time.sleep(max(0, remaining))

    ser.close()
    print("Transmission complete.")

def listen_commands(mic_index=1, interval=14, port='/dev/cu.usbmodem101'):

    recognizer = sr.Recognizer()

    try:
        while True:
            start_time = time.time()

            with sr.Microphone(device_index=mic_index) as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)

                print("Speak：")
                audio = recognizer.listen(source)

            # 保存录音以供调试
            with open("command.wav", "wb") as f:
                f.write(audio.get_wav_data())

            duration = len(audio.frame_data) / (audio.sample_rate * audio.sample_width)
            print(f" Completed,Time duration：{duration:.2f} 秒")

            try:
                text = recognizer.recognize_google(audio).lower()
                print(f" Result：{text}")

                if "go up" in text:
                    print(" Command：UP")
                    pulsemodulation([1], short_duration=0.2, long_duration=1.0, symbol_interval=5.0, port=port)
                    # 例如调用：controlDrone(1)
                elif "go down" in text:
                    print("Command：DOWN")
                    pulsemodulation([0], short_duration=0.2, long_duration=1.0, symbol_interval=5.0, port=port)
                    # 例如调用：controlDrone(1)
                else:
                    print(" Undefined Command")

            except sr.UnknownValueError:
                print("Undefined Command")
            except sr.RequestError as e:
                print(f"Request Error")
                break

            elapsed = time.time() - start_time
            sleep_time = max(0, interval - elapsed)
            print(f"Wait for {sleep_time:.1f} seconds until the next time...\n")
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("Exit")


listen_commands(mic_index=1, interval=7, port='/dev/cu.usbmodem21301')
#     # 例如：listen_commands(mic_index=1, interval=14, port='/dev/cu.usbmodem101')