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

        furthestDown = -1
        furthestIndex = -1

        for y in range(250, gameH):
            colY = gameY + y

            for x in range(0, 4):
                colX = (colWidth * x) + (colWidth / 2)
                pixel = pic.getpixel((colX, y))
                if brightness(pixel) < 20 or pixel == blueCol and y > furthestDown:
                    furthestDown = y
                    furthestIndex = x
        
        if furthestIndex != -1 and furthestDown > gameY + 250 and furthestIndex != lastColClick:
            lastColClick = furthestIndex

            current_time = time.time()
            pix_offset = int((current_time - start_time) / 1.5)

            pyautogui.moveTo(gameX + (furthestIndex * colWidth) + (colWidth / 2), furthestDown + gameY + pix_offset)
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