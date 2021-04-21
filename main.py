#!/usr/bin/env python3
 
import pyautogui as pg
import pytesseract as pt
from googletrans import Translator, constants
from pprint import pprint
import win32api, win32con
import keyboard
import time
 
# pip install pyautogui
# pip install keyboard
# pip install googletrans
# pip install opencv-python
# pip install pytesseract
 
pt.pytesseract.tesseract_cmd = (r'C:\\OCR\\Tesseract-OCR\\tesseract.exe')
translator = Translator()
 
#Clicks on the screen
def click(x, y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01) #This pauses the script for 0.01 seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
 
# Checks to see if the screen has been updated
def check_image(old_image):
    while True:
        new_image = pg.screenshot(region=(270, 680, 1100, 130))
        if old_image != new_image:
            break
        else:
            time.sleep(.05)
            continue
 
#Check for a change in words
def check_word_change(old_recv_st1, new_recv_st1):
    while True:
        new_image = pg.screenshot(region=(270, 680, 1100, 130))
        new_recv_st1 = pt.image_to_string(new_image)
        if old_recv_st1 != new_recv_st1:
            break
        else:
            print("No change in words")
            time.sleep(.5)
            continue
 
 
# Translates Specific Language to English
def recv_translator(new_recv_st1):
    while True:
        try:
            recv_st1_translation = translator.translate(new_recv_st1)
            recv_language = recv_st1_translation.src
            if recv_language == "en":
                print("Words are already in english")
                break
            else:
                print(recv_st1_translation.text)
                send_translator(recv_language)
                break
        except AttributeError:
            print("No text found")
            break
        except:
            print("Something else went wrong")
 
# Translates English to Specific Language
def send_translator(recv_language):
    send_st1 = input("Type Response: ")
    time.sleep(2)
    send_st1_translation = translator.translate(send_st1, dest=recv_language)
    click(665, 900)
    pg.typewrite(send_st1_translation.text,.02)
 
# Main loop
while keyboard.is_pressed('q') == False:
    new_image = pg.screenshot(region=(270, 680, 1100, 130))
    new_recv_st1 = pt.image_to_string(new_image)
    recv_translator(new_recv_st1)
    old_image = new_image
    old_recv_st1 = new_recv_st1
    check_word_change(old_recv_st1, new_recv_st1)
    check_image(old_image)
