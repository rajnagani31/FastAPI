import pyautogui
import time

print("Bot will start in 5 seconds...")
time.sleep(5)

while True:
    # Move mouse (small movement)
    pyautogui.moveRel(40, 0, duration=0.5)
    pyautogui.moveRel(-40, 0, duration=0.5)

    time.sleep(2)

    # ALT + TAB (switch window)
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')

    print("Mouse moved & ALT+TAB executed")

    # Repeat every 10 seconds
    time.sleep(1)
