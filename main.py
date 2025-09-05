# This script is made to do the sudoku:
# https://sudoku.com/

# To use open the website and ctrl + to enlarge it to 300% then line up
# the top to as near to the border as posible. Use the image in this folder
# as a guild to set it up

# 72x 124y
# 872x 924y

import pyautogui
import pyautogui as pag
import random
import time
import numpy as np
import win32api, win32con
import mss
import numpy as np
import cv2
import os

template_files = [
    "1_template.png",
    "2_template.png",
    "3_template.png",
    "4_template.png",
    "5_template.png",
    "6_template.png",
    "7_template.png",
    "8_template.png",
    "9_template.png",
    ]

def click():
    # time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def has_nearby(grid, x, y, num):
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if grid[i][j] == num:
                return 1
    return 0

def round_to_nearest(target):
    return min([1, 4, 7], key=lambda x: abs(x - target))

pag.moveTo(480, 606, 0)
click()
time.sleep(0.02)
click()

grid = [[0 for _ in range(9)] for _ in range(9)]

for jj in range(9):
    for j in range(9):
        maxmax = 0.8
        # Define the screen region (top, left, width, height)
        region = {'top': 124 + 89 * jj, 'left': 72 + 89 * j, 'width': 89, 'height': 89}

        with mss.mss() as sct:
            screenshot = sct.grab(region)
            img = np.array(screenshot)

            # Convert BGRA to BGR (OpenCV default)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

            img = cv2.adaptiveThreshold(
                img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY_INV, 11, 2
            )

            for i in range(9):
                template = cv2.imread(template_files[i])
                template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)

                result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
            
                if max_val >= maxmax:
                    maxmax = max_val
                    grid[jj][j] = i + 1

            # Show the captured region
            # cv2.imshow("Captured Region", img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

for w in range(9):
    print(grid[w])


for f in range(10):
    for num in range(9):
        for m in range(9):
            for n in range(9):
                if grid[m][n] == 0 or grid[m][n] > 10:
                    if all(row[n] != num+1 for row in grid) and num+1 not in grid[m] and has_nearby(grid, round_to_nearest(m), round_to_nearest(n), num+1) == 0:
                        if str(num + 11) not in str(grid[m][n]):
                            grid[m][n] = int(str(grid[m][n]) + str(num + 11))
                            # for w in range(9):
                            #     print(grid[w])
                            # print(str(has_nearby(grid, round_to_nearest(m), round_to_nearest(n), num+1)) + str(round_to_nearest(n))+str(round_to_nearest(m)))
                    elif grid[m][n] > 100: 
                        grid[m][n] = int(str(grid[m][n]).replace(str(num + 11), ""))

    for a in range(3):
        for b in range(3):
            for num in range(9):
                count = 0
                for l in range(2):
                    for m in range(3):
                        for n in range(3):
                            if str(num + 11) in str(grid[m+3*a][n+3*b]):
                                count += 1
                                # print(count)
                                # print(num)
                                # print(str(n)+str(m))
                                # print(l)
                            if str(num + 11) in str(grid[m+3*a][n+3*b]) and count == 2 and l == 1:
                                grid[m+3*a][n+3*b] = num + 1
                                pag.moveTo(72 + 40 + 89 * (n+3*b), 124 + 40 + 89 * (m+3*a), 0)
                                click()
                                pyautogui.write(str(grid[m+3*a][n+3*b]), interval=0)
                                count += 1

    for m in range(9):
        for n in range(9):
            if 10 < grid[m][n] < 20:
                grid[m][n] -= 10
                pag.moveTo(72 + 40 + 89 * n, 124 + 40 + 89 * m, 0)
                click()
                pyautogui.write(str(grid[m][n]), interval=0)



print()

for w in range(9):
    print(grid[w])

