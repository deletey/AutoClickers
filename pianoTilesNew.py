import pyautogui
import pygetwindow
import time
import threading

from pynput.keyboard import Key, Listener

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

run_game = False

def maxArr(arr):
    maxVal = 0
    maxIndex = 0

    for x in range(0, len(arr)):
        if arr[x] > maxVal:
            maxIndex = x
            maxVal = arr[x]

    return (maxVal, maxIndex)

def brightness(rgb):
    return (rgb[0] + rgb[1] + rgb[2]) / 3

def start_game():
    global run_game
    run_game = True

    gameX = 657
    gameY = 32
    gameW = 606
    gameH = 756

    blackCol = (0, 0, 0)
    blueCol = (54, 159, 198)

    colWidth = gameW / 4

    screenWidth, screenHeight = pyautogui.size()

    windows = pygetwindow.getAllWindows()
    pianoTiles = pygetwindow.getWindowsWithTitle("Piano Tiles 2018")[0]

    for x in windows:
        x.minimize()

    pianoTiles.maximize()
    pianoTiles.activate()

    time.sleep(1)

    start_time = time.time()

    lastColClick = -1

    while(run_game):
        pic = pyautogui.screenshot(region=(gameX, gameY, gameW, gameH))

        column = -1

        for x in range(0, 4):
            pix = pic.getpixel(((colWidth * x) + (colWidth / 2), gameY + gameH - 50))

            if brightness(pix) < 30 or pix == blueCol:
                column = x
                break
        
        if column != -1 and column != lastColClick:
            lastColClick = column

            current_time = time.time()
            pix_offset = int((current_time - start_time) * 0.9)

            pyautogui.moveTo(gameX + (column * colWidth) + (colWidth / 2), gameY + gameH - 10)
            pyautogui.click()

def on_press(key):
        global run_game
        if(key == Key.f3):
                t = threading.Thread(target=start_game)
                t.start()
        elif(key == Key.esc):
                run_game = False
                listener.stop()

with Listener(on_press=on_press) as listener:
    listener.join()

exit()