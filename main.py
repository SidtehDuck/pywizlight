import asyncio
import time
from random import randint
from threading import Event
from itertools import count
from pywizlight import wizlight, PilotBuilder, discovery

def redundant():
    #bulbs = await discovery.discover_lights(broadcast_space="192.168.1.255")
    #print(f"Bulb IP address: {bulbs}")
    '''Sample code to work with bulbs.
    # Discover all bulbs in the network via broadcast datagram (UDP)
    # function takes the discovery object and returns a list with wizlight objects.
    
    # Print the IP address of the bulb on index 0
    #print(f"Bulb IP address: {bulbs[0].ip}")

    def rgbAlter():
        r, g, b = rgbUpdate()
        l = [r, g, b]
        print(l)

    def setInterval(func,itergap, elapsed):
        e = Event()
        timeout = time.time() + elapsed
        while not e.wait(itergap):
            func()
            if time.time() > timeout:
                break

    setInterval(rgbUpdate,0.01, 1)
    
    
    for bulb in bulbs:
        print(bulb.__dict__)
        await bulb.turn_off()
    '''

async def main():

    # Function to generate randomg colours
    def rgbUpdate():
        r, g, b, a = (randint(0,255), randint(0,255), randint(0,255), randint(0,255))
        return r, g, b, a

    # Set up a standard light
    light = wizlight("192.168.1.9")

    # Set bulb to warm white
    # await light.turn_on(PilotBuilder(warm_white = 255))

    def colored(r, g, b, text):
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)
  

    # Set RGB values and print em on console
    for i in count():
        r, g, b, a = rgbUpdate()
        await light.turn_on(PilotBuilder(rgb = (255, 0, 255), brightness = 255))
        state = await light.updateState()
        red, green, blue = state.get_rgb()
        text = (f"Red {red}, Green {green}, Blue {blue}, Brightness {a}")
        colored_text = colored(red, green, blue, text)
        print(colored_text)
        time.sleep(2)

    # Turn off the light
    #await light.turn_off()

    # Do operations on multiple lights parallely
    #bulb1 = wizlight("<your bulb1 ip>")
    #bulb2 = wizlight("<your bulb2 ip>")

    # await asyncio.gather(bulb1.turn_on(PilotBuilder(brightness = 255)),
    # bulb2.turn_on(PilotBuilder(warm_white = 255)), loop = loop)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())