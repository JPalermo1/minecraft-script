from pywinauto import Application
from pynput.keyboard import Controller, Key, Listener
from pynput.mouse import Controller as MouseController, Button
import time
import threading
import pygetwindow as gw
import sys

keyboard = Controller()
mouse = MouseController()
minecraft_title = "Minecraft 1.8.9"  # Minecraft window title.
vscode_title = "Minecraft.py - Visual Studio Code"

# Flag to control whether the cycle should run.
running = True

# Bring Minecraft to the front using its exact title.
def focus_minecraft():
    try:
        app = Application().connect(title=minecraft_title)
        window = app.window(title=minecraft_title)
        window.set_focus()  # Activate the window to send input.
        return window
    except Exception as e:
        print("Minecraft wsindow not found or failed to focus:", e)
        return None

# Send key press using pynput.
def send_key(key): 
    keyboard.press(key)
    time.sleep(0.1)  # Short delay to simulate natural key press.
    keyboard.release(key)

# Hold a key for a specific duration (in seconds), showing countdown.
def hold_key(key, duration):
    for remaining_time in range(duration, 0, -1):
        print(f"Holding '{key}' for {remaining_time} seconds...")  # Countdown display.
        keyboard.press(key)
        time.sleep(1)  # Wait for 1 second.
        keyboard.release(key)
    print(f"Finished holding '{key}'.")

# Hold left-click down for the entire duration the script is running.
def hold_left_click():
    mouse.press(Button.left)
    print("Holding left-click...")
    while running:
        time.sleep(0.1)  # Sleep to keep the left click pressed.
    mouse.release(Button.left)  # Release left click when stopping the script.

# Cycle through holding W, A, and S with countdown.
def movement_cycle():
    global running
    while running:
        print("Starting to hold 'S' for 71 seconds...")
        hold_key('s', 71)  # Hold 'S' for 71 seconds.
        if not running: break  # Check running flag to exit early if needed
        print("Starting to hold 'A' for 1 second...")
        hold_key('a', 1)  # Hold 'A' for 1 second.
        if not running: break  # Check running flag to exit early if needed
        print("Starting to hold 'W' for 56 seconds...")
        hold_key('w', 56)  # Hold 'W' for 56 seconds.
        if not running: break  # Check running flag to exit early if needed
        print("Starting to hold 'A' for 1 second...")
        hold_key('a', 1)  # Hold 'A' for 1 second.

# Stop the script when the 'F8' key is pressed.
def on_press(key):
    global running
    if key == Key.f8:  # Use F8 as the key to stop the script
        print("F8 key pressed. Stopping the script...")
        running = False
        return False  # Stop the listener

# Focus Minecraft and send ESC to resume the game.
window = focus_minecraft()

if window:
    print("Minecraft window focused!")
    time.sleep(1)  # Wait to ensure the window is active.
    send_key(Key.esc)  # Send 'ESC' to resume the game if it's in the menu.
    time.sleep(1)  # Wait for the game to resume.

    # Start the left click hold in a separate thread.
    left_click_thread = threading.Thread(target=hold_left_click)
    left_click_thread.daemon = True  # Set as daemon so it stops when the program exits.
    left_click_thread.start()

    # Start the movement cycle in a new thread to avoid blocking.
    cycle_thread = threading.Thread(target=movement_cycle)
    cycle_thread.daemon = True  # Set as daemon so it stops when the program exits.
    cycle_thread.start()

    # Start the listener for the F8 key.
    with Listener(on_press=on_press) as listener:
        listener.join()  # Block and wait for the F8 key to stop the script.

    # After stopping the listener, join the cycle thread and left click thread.
    cycle_thread.join()
    left_click_thread.join()  # Ensure both threads stop properly when exiting.
else:
    print("Minecraft window not found!")
