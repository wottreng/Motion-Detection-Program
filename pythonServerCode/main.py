import time
import requests
import datetime

verbose = True
devices = [6, 7, 8]  # last digit of ip address
reqTimeout = 3

def run():
    print(f"Motion Sensor Program started {datetime.datetime.now()}")
    laston = 0
    lastoff = 0
    lastCheckSensorTime = 0
    motionDetected = False
    switchStatus = False
    timeDelayCheckSensor = 3  # seconds
    timeDelayOperateSwitchOn = 20  # seconds
    timeDelayOperateSwitchOff = 10  # seconds

    while True:
        timeNow = int(time.time())  # seconds
        # check motion sensor
        if timeNow - lastCheckSensorTime > timeDelayCheckSensor:
            if verbose:
                print(f"check motion sensor: {timeNow}")
            lastCheckSensorTime = timeNow
            motionDetected = checkSensor()
            if verbose:
                print(f"-- motion: {motionDetected}")
                print(f"time since switch last on: {timeNow - laston} sec, switch last off: {timeNow - lastoff} sec")

        # if motion -> turn on -----
        if motionDetected and not switchStatus and (timeNow - lastoff) > timeDelayOperateSwitchOff:
            if verbose:
                print("[*] lights ON")
            for device in devices:
                switchStatus = operateShelly(shellyNumber=device, switchStatus="on")
                if verbose:
                    print(f"shelly {device} status:  {switchStatus}")
            laston = timeNow

        # if no motion -> turn off ----
        elif not motionDetected and switchStatus and (timeNow - laston) > timeDelayOperateSwitchOn:
            if verbose:
                print("[*] lights OFF")
            for device in devices:
                switchStatus = operateShelly(shellyNumber=device, switchStatus="off")
                if verbose:
                    print(f"shelly {device} status:  {switchStatus}")
            lastoff = timeNow


##  subFunctions ================================================================

def checkSensor():

    try:
        status = requests.get("http://10.42.0.23/api0", timeout=reqTimeout).json()
    except Exception as e:
        print(f"motion sensor error: {e}")
        status = {"motionDetected": "0"}
    if verbose:
        print(f"motion sensor resp: {status}")
    motionBinary = status["motionDetected"]
    if motionBinary == "1":
        motion = True
    else:
        motion = False
    return motion


def operateShelly(shellyNumber, switchStatus=None):

    if switchStatus == None:
        try:
            resp = requests.get(f"http://10.42.0.2{shellyNumber}/relay/0?turn=toggle", timeout=reqTimeout).json()
        except Exception as e:
            print(f"shelly {shellyNumber} error: {str(e)[:14]}")
            resp = {"ison": "False"}
    else:
        try:
            resp = requests.get(f"http://10.42.0.2{shellyNumber}/relay/0?turn={switchStatus}",
                                timeout=reqTimeout).json()
        except Exception as e:
            print(f"shelly {shellyNumber} error: {str(e)[:14]}")
            resp = {"ison": "False"}
    if verbose:
        print(f"shelly resp: {resp}")
    switchStatus = resp["ison"]
    return switchStatus


## ===================================================================================


if __name__ == '__main__':
    run()

'''
SHelly Examples:
http://10.42.0.40/relay/0?turn=on Will switch output ON.
http://10.42.0.40/relay/0?turn=on&timer=10 Will switch output ON for 10 sec.
http://10.42.0.40/relay/0?turn=toggle Will switch the output On if OFF or vice versa
'''
