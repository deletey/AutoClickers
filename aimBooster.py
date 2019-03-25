import pyautogui
import pygetwindow
import time
import threading

from pynput.keyboard import Key, Listener

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

run_game = False

def findTargetLocation(image, lastClick, colour):
    for x in range(0, image.width):
        for y in range(0, image.height):
            if image.getpixel((x, y)) == colour:
                return (x, y)

    return False

def findTargets(image, colour):
    targets = []

    for x in range(0, image.width):
        for y in range(0, image.height):
            if image.getpixel((x, y)) == colour and not withinRangeOf((x, y), targets, 50):
                targets.append((x, y))

    return targets

def withinRangeOf(position, targets, r):
    if len(targets) == 0:
        return False
    
    for target in targets:
        if withinRange(position, target, r):
            return True
    
    return False
    
def withinRange(position, target, r):
    if position[0] > target[0] - r and position[0] < target[0] + r and position[1] > target[1] - r and position[1] < target[1] + r:
        return True
    
    return False


def start_game():
    global run_game
    run_game = True

    gameX = 662
    gameY = 340
    gameW = 597
    gameH = 417

    targetColour = (255, 219, 195)

    screenWidth, screenHeight = pyautogui.size()

    #windows = pygetwindow.getAllWindows()
    #pianoTiles = pygetwindow.getWindowsWithTitle("Aim Booster - Google Chrome")[0]

    #for x in windows:
    #    x.minimize()

    #pianoTiles.maximize()
    #pianoTiles.activate()

    #time.sleep(1)

    lastClick = (-1, -1)

    while(run_game):
        pic = pyautogui.screenshot(region=(gameX, gameY, gameW, gameH))
        
        #target = findTargetLocation(pic, lastClick, targetColour)

        #if target and not withinRange(target, lastClick, 5):
        #    lastClick = target
        #    pyautogui.moveTo(gameX + target[0], gameY + target[1])
        #    pyautogui.click()

        targets = findTargets(pic, targetColour)

        if len(targets) > 0:
            for target in targets:
                pyautogui.moveTo(gameX + target[0], gameY + target[1])
                pyautogui.click()

        time.sleep(0.05)


def on_press(key):
        global run_game
        if(key == Key.f3):
                t = threading.Thread(target=start_game)
                t.start()
        elif(key == Key.f4):
                run_game = False
        elif(key == Key.f5):
                run_game = False
                listener.stop()

with Listener(on_press=on_press) as listener:
    listener.join()

exit()