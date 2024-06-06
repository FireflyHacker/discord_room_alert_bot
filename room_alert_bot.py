#!/usr/bin/env python3
########################################
# is_ieee_open.py
# jbokor@uci.edu, April 2022
#
#  "Small", "quick" python program written for
#  UCI IEEE to show whether the room is open or not
#  in the club's Discord server.
########################################
import asyncio
import RPi.GPIO as GPIO
import hackerlabbot
import led_controller
import sys

switch_pin = 17


async def switchLoop():
    # script initialization block
    leds = led_controller.LEDController()
    await leds.set_state("blink")

    # state tracking
    prev_input = 0
    message_success = False
    fail_count = 0  # number of failed attempts

    try:
        while True:
            # switch is now "ON". it's backwards, I know. 
            if GPIO.input(switch_pin) == GPIO.LOW:
                if prev_input != 1:
                    message_success = False
                    prev_input = 1

                if not message_success:  # if message was already successfully sent, don't sent another
                    # if function returns false, sending was unsuccessful
                    a = await hackerlabbot.openLab()
                    if a:
                        await leds.set_state("occupied")
                        message_success = True
                        fail_count = 0
                    else:
                        fail_count += 1
                        await asyncio.sleep(2)

                await asyncio.sleep(0.05)

            else:
                # switch now low
                if prev_input != 0:
                    message_success = False
                    prev_input = 0

                if not message_success:  # if message was already successfully sent, don't sent another
                    # if function returns false, sending was unsuccessful
                    a = await hackerlabbot.closeLab()
                    if a:
                        await leds.set_state("vacant")
                        message_success = True
                        fail_count = 0
                    else:
                        fail_count += 1
                        await asyncio.sleep(2)

                await asyncio.sleep(0.05)

            # if 5 failures occur and email hasn't been sent for 4 hours, send another

            # things aren't going well. lets slow our roll
            if fail_count > 30:
                await leds.set_state("blink")
                await asyncio.sleep(20)

            elif fail_count > 4:
                await leds.set_state("blink")


    except Exception as err:
        print("ERROR:", err, file=sys.stderr)

    except KeyboardInterrupt as err:
        quit()

    finally:
        GPIO.cleanup()


async def main():
    await asyncio.gather(hackerlabbot.startBot(), switchLoop())


asyncio.run(main())
