import re
import serial
import subprocess

# Set up the serial connection to /dev/ttyACM0
ser = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)

# Variables to store the latest battery percentage and charging status
battery_percentage = None
charging_status = None

def update_battery_state():
    """Update battery state if both percentage and charging status are available."""
    if battery_percentage is not None and charging_status is not None:
        # Set charging state
        charging_state = '1' if charging_status else '0'
        subprocess.run(f"echo 'charging = {charging_state}' | sudo tee /dev/anyon_e_battery", shell=True)
        
        # Set battery capacity
        subprocess.run(f"echo 'capacity0 = {battery_percentage}' | sudo tee /dev/anyon_e_battery", shell=True)
        print(f"Updated: charging={charging_status}, capacity={battery_percentage}%")

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        
        # Check for battery percentage
        if "BATTERY PERCENT:" in line:
            match = re.search(r"BATTERY PERCENT: (\d+)", line)
            if match:
                battery_percentage = int(match.group(1))
                print(f"Battery percentage detected: {battery_percentage}%")
                update_battery_state()

        # Check for charging status
        elif "CHARGING:" in line:
            match = re.search(r"CHARGING: (YES|NO)", line)
            if match:
                charging_status = True if match.group(1) == "YES" else False
                print(f"Charging status detected: {'charging' if charging_status else 'not charging'}")
                update_battery_state()
                
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
