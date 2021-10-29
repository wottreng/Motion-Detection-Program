import time
import datetime
import spookySounds as spooky
import httpControl as control

verbose = True
sound = True
devices = [6, 7, 8]  # last digit of ip address



def run():

    print(f"Motion Sensor Program started {datetime.datetime.now()}")
    laston = 0  # timestamp
    lastoff = 0  # timestamp
    lastCheckSensorTime = 0  # timestamp
    motionDetected = False
    switchStatus = False
    timeDelayCheckSensor = 3  # seconds
    timeDelayOperateSwitchOn = 20  # seconds
    timeDelayOperateSwitchOff = 10  # seconds
    soundDelay = 6  # seconds
    soundLastOn = 0  # timestamp

    while True:
        time.sleep(1)  # keep program cpu usage low
        timeNow = int(time.time())  # seconds
        # check motion sensor
        if timeNow - lastCheckSensorTime > timeDelayCheckSensor:
            if verbose:
                print(f"check motion sensor: {timeNow}")
            lastCheckSensorTime = timeNow
            motionDetected = control.checkSensor()
            if verbose:
                print(f"-- motion: {motionDetected}")
                print(f"time since switch last on: {timeNow - laston} sec, switch last off: {timeNow - lastoff} sec")

        # motion -> turn on -----
        if motionDetected and not switchStatus and (timeNow - lastoff) > timeDelayOperateSwitchOff:
            if verbose:
                print("[*] lights ON [*]")
            for device in devices:
                switchStatus = control.operateShelly(shellyNumber=device, switchStatus="on")
                if verbose:
                    print(f"shelly {device} status:  {switchStatus}")
            laston = timeNow
            soundLastOn = timeNow  # stop sound from playing twice
            if sound:
                if verbose:
                    print("play spooky sound")
                spooky.playRandomSpookySound()

        # no motion -> turn off ----
        elif not motionDetected and switchStatus and (timeNow - laston) > timeDelayOperateSwitchOn:
            if verbose:
                print("[*] lights OFF [*]")
            for device in devices:
                switchStatus = control.operateShelly(shellyNumber=device, switchStatus="off")
                if verbose:
                    print(f"shelly {device} status:  {switchStatus}")
            lastoff = timeNow
            if sound:
                if verbose:
                    print("play spooky sound")
                spooky.playRandomSpookySound()

        # if motion -> make sounds
        if motionDetected and sound and ((timeNow - soundLastOn) > soundDelay):
            if verbose:
                print(f"play spooky sound while motion detected: {timeNow - soundLastOn}")
            soundLastOn = timeNow
            spooky.playRandomSpookySound()



if __name__ == '__main__':
    run()

'''
SHelly Examples:
http://10.42.0.40/relay/0?turn=on Will switch output ON.
http://10.42.0.40/relay/0?turn=on&timer=10 Will switch output ON for 10 sec.
http://10.42.0.40/relay/0?turn=toggle Will switch the output On if OFF or vice versa
'''
