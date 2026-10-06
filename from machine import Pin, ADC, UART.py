from machine import Pin, ADC, UART
import time

# Initialize UART0 cross-connected to Pico 1
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Initialize ADC0 on GP26 to capture the filtered analog average voltage
adc = ADC(Pin(26))

print("Pico 2: Listening for data and reading ADC loop...")

while True:
    if uart.any():
        incoming_bytes = uart.readline()
        try:
            desired_pct = float(incoming_bytes.decode().strip())
            
            # Read the filtered DC average voltage from the RC filter circuit
            adc_raw = adc.read_u16()
            measured_pct = (adc_raw / 65535.0) * 100.0
            
            difference = desired_pct - measured_pct
            print(f"Pico 2 Report -> Expected: {desired_pct}% | Measured: {measured_pct:.2f}% | Local Delta: {difference:.2f}%")
            
            # Loop the measured value back to Pico 1
            uart.write(f"{measured_pct}\n".encode())
        except (ValueError, UnicodeError):
            pass
            
    time.sleep(0.05)
