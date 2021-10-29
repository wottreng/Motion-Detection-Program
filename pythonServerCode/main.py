import time
import requests
import datetime

verbose = False

def run():
    print(f"Motion Sensor Program started {datetime.datetime.now()}")
    laston = 0
    lastoff = 0
    lastCheckSensorTime = 0
    motionDetected = False
    switchStatus6 = False
    timeDelayCheckSensor = 3  # seconds
    timeDelayOperateSwitch = 10  # seconds
    # lightStatus = False
    while True:
        timeNow = int(time.time())  # seconds
        # check motion sensor
        if timeNow - lastCheckSensorTime > timeDelayCheckSensor:
            # print(f"check sensor: {timeNow}")
            lastCheckSensorTime = timeNow
            motionDetected = checkSensor()
            if verbose:
                print(f"-- motion: {motionDetected}")
        # if motion turn on -----
        if motionDetected and not switchStatus6 and (timeNow - lastoff) > timeDelayOperateSwitch:
            switchStatus6 = operateShelly(shellyNumber=6, switchStatus="on")
            switchStatus8 = operateShelly(shellyNumber=8, switchStatus="on")
            laston = timeNow
            if verbose:
                print("[*] lights ON")
                print(f"shelly 6:  {switchStatus6}")
                print(f"shelly 8:  {switchStatus8}")
        # if no motion turn off ----
        elif not motionDetected and switchStatus6 and (timeNow - laston) > timeDelayOperateSwitch:
            switchStatus6 = operateShelly(shellyNumber=6, switchStatus="off")
            switchStatus8 = operateShelly(shellyNumber=8, switchStatus="off")
            lastoff = timeNow
            if verbose:
                print("[*] lights OFF")
                print(f"shelly 6:  {switchStatus6}")
                print(f"shelly 8:  {switchStatus8}")
        # if Error then end
        if switchStatus6 == "error":
            print("[*]  error  [*]")
            # quit()


##  subFunctions ================================================================

def checkSensor():
    status = requests.get("http://10.42.0.23/api0").json()
    motionBinary = status["motionDetected"]
    if motionBinary == "1":
        motion = True
    else:
        motion = False
    return motion


def operateShelly(shellyNumber, switchStatus=None):
    if switchStatus == None:
        resp = requests.get(f"http://10.42.0.2{shellyNumber}/relay/0?turn=toggle").json()
        # print(resp)
    elif switchStatus == "on":
        resp = requests.get(f"http://10.42.0.2{shellyNumber}/relay/0?turn=on").json()
        # print(resp)
    elif switchStatus == "off":
        resp = requests.get(f"http://10.42.0.2{shellyNumber}/relay/0?turn=off").json()
        # print(resp)
    else:
        resp = {"ison": "error"}
        # print('error request')

    switchStatus = resp["ison"]
    return switchStatus


## ===================================================================================


if __name__ == '__main__':
    run()

'''
SHelly Examples:
http://192.168.0.40/relay/0?turn=on Will switch output ON.
http://192.168.0.40/relay/0?turn=on&timer=10 Will switch output ON for 10 sec.
http://192.168.0.40/relay/0?turn=toggle Will switch the output On if OFF or vice versa
'''
