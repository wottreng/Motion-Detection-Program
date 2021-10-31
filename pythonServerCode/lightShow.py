import random
import time
import datetime
import spookySounds as spooky
import httpControls as control

class halloweenLights:

    def __init__(self):
        self.verbose = False
        self.sound = False
        self.devices = ["6", "7", "8", "9"]  # last digit of ip address
        self.numberOfDevices = len(self.devices)
        self.timeDelayCheckSensor = 3  # seconds
        self.timeDelayOperateSwitchOn = 20  # seconds
        self.timeDelayOperateSwitchOff = 6  # seconds
        self.soundDelay = 6  # seconds
        self.randomLightTimes = False
        self.randomNumberOfLightsOff = self.numberOfDevices

    def run(self):
        rate = 1
        laston = 0  # timestamp
        lastoff = 0  # timestamp
        lastCheckSensorTime = 0  # timestamp
        motionDetected = False
        switchStatus = False
        soundLastOn = 0  # timestamp

        print(f"Motion Sensor Program started {datetime.datetime.now()}")
        while True:
            timeNow = int(time.time())  # seconds
            # check motion sensor
            if timeNow - lastCheckSensorTime > self.timeDelayCheckSensor:
                if self.verbose:
                    print(f"check motion sensor: {timeNow}")
                lastCheckSensorTime = timeNow
                motionDetected = control.checkSensor()
                if self.verbose:
                    print(f"-- motion: {motionDetected}")
                    print(f"time since switch last on: {timeNow - laston} sec, switch last off: {timeNow - lastoff} sec")
            # motion -> turn on -----
            if motionDetected and not switchStatus and (timeNow - lastoff) > self.timeDelayOperateSwitchOff:
                # lights ---
                if self.verbose:
                    print("[*] lights ON [*]")
                for device in self.devices:
                    switchStatus = control.operateShelly(shellyNumber=device, switchStatus="on")
                    if self.verbose:
                        print(f"shelly {device} status:  {switchStatus}")
                laston = timeNow
                if self.randomLightTimes:
                    self.timeDelayOperateSwitchOn = random.randint(3, 9)
                # sound ----
                soundLastOn = timeNow  # stop sound from playing twice
                if self.sound:
                    if self.verbose:
                        print("play spooky sound")
                    spooky.playRandomSpookySound()
            # no motion -> turn off ----
            elif not motionDetected and switchStatus and (timeNow - laston) > self.timeDelayOperateSwitchOn:
                # lights ----
                if self.verbose:
                    print("[*] lights OFF [*]")
                    if self.randomLightTimes:
                        self.randomNumberOfLightsOff = random.randint(0, self.numberOfDevices-1)
                        random.shuffle(self.devices)
                for device in self.devices:
                    if self.devices.index(device) >= self.randomNumberOfLightsOff:
                        break
                    switchStatus = control.operateShelly(shellyNumber=device, switchStatus="off")
                    if self.verbose:
                        print(f"shelly {device} status:  {switchStatus}")
                lastoff = timeNow
                if self.randomLightTimes:
                    self.timeDelayOperateSwitchOff = random.randint(10, 20)
                # sound ----
                if self.sound:
                    if self.verbose:
                        print("play spooky sound")
                    spooky.playRandomSpookySound()
            # if motion -> make sounds
            if motionDetected and self.sound and ((timeNow - soundLastOn) > self.soundDelay):
                if self.verbose:
                    print(f"play spooky sound while motion detected: {timeNow - soundLastOn}")
                soundLastOn = timeNow
                spooky.playRandomSpookySound()
            if time.time() - timeNow < rate:
                if self.verbose:
                    print(f"[-] sleep for {time.time() - timeNow}")
                time.sleep(time.time() - timeNow)  # keep cpu load down kinda like fps

