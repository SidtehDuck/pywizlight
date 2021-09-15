from random import randint
from threading import Event
from time import time

def rgbUpdate():
    r, g, b = (randint(0,255), randint(0,255), randint(0,255))
    return r, g, b

def rgbAlter():
    r, g, b = rgbUpdate()
    l = [r, g, b]
    print(l)

def setInterval(func,itergap, elapsed):
    e = Event()
    timeout = time() + elapsed
    while not e.wait(itergap):
        func()
        if time() > timeout:
            break


setInterval(rgbAlter, 1, 10)