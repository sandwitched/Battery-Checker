import psutil
import time
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)
battery = psutil.sensors_battery()
# Safety check for desktop PCs
if battery is None:
    print("Error: No battery detected. Are you on a desktop PC?")
    exit()

percent = battery.percent
t_lst_prcnt = time.strftime("%H:%M:%S") 

def get_percent():
    global percent, t_lst_prcnt
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
    t_lst_prcnt = time.strftime("%H:%M:%S")
    return percent

print("=== BATTERY MONITOR ACTIVE ===")
print(f"Monitoring started at: {t_lst_prcnt}")
print(f"Starting Battery: {percent}%\n")

while True:
    time.sleep(1) 
    
    start_time = time.time()
    start_percent = percent
    
    # Wait for 5 minutes (300 seconds)
    print("Waiting 5 minutes for next check...")
    for remaining in range(5, 0, -1):
        print(f" -> {remaining} minutes remaining until check...")
        time.sleep(60) # Wait 1 minute chunks so you see progress
        
    old_percent = start_percent
    new_percent = get_percent()
    
    print(f"\nChecking levels at {t_lst_prcnt}:")
    print(f"  Previous: {old_percent}%")
    print(f"  Current: {new_percent}%")
    print(f"  Lost: {old_percent - new_percent}%\n")
    
    if (old_percent - new_percent) >= 3:
        print("Alert triggered!")
        messagebox.showinfo("Notification", "your have lost more than 3 percent of battery in 5 minutes if you have not been using heavy software you should get that checked out",parent=root)
