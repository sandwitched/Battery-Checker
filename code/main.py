import psutil
import time
import tkinter as tk
from tkinter import messagebox

# Initialize hidden Tkinter window for topmost alerts
root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)

# Initial battery safety check
battery = psutil.sensors_battery()
if battery is None:
    print("Error: No battery detected. Are you on a desktop PC?")
    exit()

# Global tracking variables
percent = battery.percent
t_lst_prcnt = time.strftime("%H:%M:%S")

def get_percent():
    global percent, t_lst_prcnt
    current_battery = psutil.sensors_battery()
    if current_battery:
        percent = current_battery.percent
        t_lst_prcnt = time.strftime("%H:%M:%S")
    return percent

print("=== BATTERY MONITOR ACTIVE ===")
print(f"Monitoring started at: {t_lst_prcnt}")
print(f"Starting Battery: {percent}%\n")

while True:
    start_percent = get_percent()  # Refresh baseline at the start of the interval
    
    print("Waiting 5 minutes for next check...")
    # Counts down 5 times, sleeping 60 seconds (1 minute) each time
    for remaining in range(5, 0, -1):
        print(f" -> {remaining} minutes remaining until check...")
        time.sleep(60) 

    old_percent = start_percent
    new_percent = get_percent()
    
    print(f"\nChecking levels at {t_lst_prcnt}:")
    print(f" Previous: {old_percent}%")
    print(f" Current: {new_percent}%")
    print(f" Lost: {old_percent - new_percent}%\n")
    
    # Alert 1: Fast drain check
    if (old_percent - new_percent) >= 3:
        print("Alert triggered: High drain rate!")
        messagebox.showinfo(
            "Notification", 
            "You have lost more than 3 percent of battery in 5 minutes. If you have not been using heavy software you should get that checked out.",
            parent=root
        )
        
    # Alert 2: Low battery check
    if new_percent <= 10:
        print("Alert triggered: Low battery!")
        messagebox.showinfo(
            "Notification", 
            "You have 10% or less left. You should charge it.",
            parent=root
        )
        
    # Alert 3: Audio alert if charging
    fresh_battery = psutil.sensors_battery()
    if fresh_battery and fresh_battery.power_plugged:
        if new_percent >= 85:
            print('\a')  # System bell sound

