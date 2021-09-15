import asyncio
from random import randint
from threading import Event
import time
import itertools
from pywizlight import wizlight, PilotBuilder, discovery

async def main():
    """Sample code to work with bulbs."""
    # Discover all bulbs in the network via broadcast datagram (UDP)
    # function takes the discovery object and returns a list with wizlight objects.
    #bulbs = await discovery.discover_lights(broadcast_space="192.168.1.255")
    # Print the IP address of the bulb on index 0
    #print(f"Bulb IP address: {bulbs[0].ip}")
    def rgbUpdate():
        r, g, b, a = (randint(100,255), randint(0,255), randint(0,255), randint(0,255))
        return r, g, b, a

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
    # Iterate over all returned bulbs
    #for bulb in bulbs:
    #    print(bulb.__dict__)
        # Turn off all available bulbs
        # await bulb.turn_off()

    # Set up a standard light
    light = wizlight("192.168.1.9")
    # Set up the light with a custom port
    #light = wizlight("your bulb's IP address", port=12345)

    # The following calls need to be done inside an asyncio coroutine
    # to run them fron normal synchronous code, you can wrap them with
    # asyncio.run(..).

    # Turn on the light into "rhythm mode"
    await light.turn_on(PilotBuilder())
    # Set bulb brightness
    await light.turn_on(PilotBuilder(brightness = 255))

    # Set bulb brightness (with async timeout)
    timeout = 10
    await asyncio.wait_for(light.turn_on(PilotBuilder(brightness = 255)), timeout)

    # Set bulb to warm white
    await light.turn_on(PilotBuilder(warm_white = 255))

    # Set RGB values
    for i in itertools.count():
        r, g, b, a = rgbUpdate()
        await light.turn_on(PilotBuilder(rgb = (r, g, b), brightness = a))
        state = await light.updateState()
        red, green, blue = state.get_rgb()
        print(f"red {red}, green {green}, blue {blue}, brightness {a}")
        time.sleep(0.1)

    # Get the current color temperature, RGB values
    state = await light.updateState()
    print(state.get_colortemp())
    red, green, blue = state.get_rgb()
    print(f"red {red}, green {green}, blue {blue}")
    
    #await light.turn_off()

    # Do operations on multiple lights parallely
    #bulb1 = wizlight("<your bulb1 ip>")
    #bulb2 = wizlight("<your bulb2 ip>")
    #await asyncio.gather(bulb1.turn_on(PilotBuilder(brightness = 255)),
    #    bulb2.turn_on(PilotBuilder(warm_white = 255)), loop = loop)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())