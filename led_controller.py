import asyncio
from threading import Thread
import RPi.GPIO as GPIO

switch_pin = 17


class LEDController:

    def __init__(self):
        self.state = "blink"  # 3 states: blink, occupied, vacant
        self.R_LED = 27
        self.G_LED = 22

        # initialize gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(switch_pin, GPIO.IN)
        GPIO.setup(self.R_LED, GPIO.OUT)
        GPIO.setup(self.G_LED, GPIO.OUT)

        self.blinkThread = Thread(target=self.LEDs_blink)
        self.blinkThread.start()  # Blink by default

    async def set_state(self, state):
        self.state = state
        if self.state == "blink":
            if not self.blinkThread.is_alive():  # Check if already blinking
                self.blinkThread.start()
        elif self.state == "occupied":
            if self.blinkThread.is_alive():  # Stop blinking and turn green
                self.blinkThread.join()
            await self.LEDs_state_occupied()
        elif self.state == "vacant":
            if self.blinkThread.is_alive():  # Stop blinking and turn red
                self.blinkThread.join()
            await self.LEDs_state_vacant()
        else:
            raise "Invalid state"

    # turns LEDs into position for switch ON, room OCCUPIED
    async def LEDs_state_occupied(self):
        GPIO.output(self.R_LED, GPIO.LOW)
        GPIO.output(self.G_LED, GPIO.HIGH)
        await asyncio.sleep(0.05)

    # turns LEDs into position for switch OFF, room VACANT
    async def LEDs_state_vacant(self):
        GPIO.output(self.R_LED, GPIO.HIGH)
        GPIO.output(self.G_LED, GPIO.LOW)
        await asyncio.sleep(0.05)

    # Sets the LEDs to blink, until stopped
    async def LEDs_blink(self):
        while self.state == "blink":
            GPIO.output(self.R_LED, GPIO.HIGH)
            GPIO.output(self.G_LED, GPIO.HIGH)
            await asyncio.sleep(0.25)

            GPIO.output(self.R_LED, GPIO.LOW)
            GPIO.output(self.G_LED, GPIO.LOW)
            await asyncio.sleep(0.25)
