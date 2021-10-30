import requests

reqTimeout = 3
verbose = False

def checkSensor():

    try:
        status = requests.get("http://10.42.0.23/api0", timeout=reqTimeout).json()
    except Exception as e:
        print(f"[!] motion sensor error: {str(e)[:14]} [!]")
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
            print(f"[!] shelly {shellyNumber} error: {str(e)[:14]} [!]")
            resp = {"ison": "False"}
    else:
        try:
            resp = requests.get(f"http://10.42.0.2{shellyNumber}/relay/0?turn={switchStatus}",
                                timeout=reqTimeout).json()
        except Exception as e:
            print(f"[!] shelly {shellyNumber} error: {str(e)[:14]} [!]")
            resp = {"ison": "False"}
    if verbose:
        print(f"shelly resp: {resp}")
    switchStatus = resp["ison"]
    return switchStatus


'''
SHelly Examples:
http://10.42.0.40/relay/0?turn=on Will switch output ON.
http://10.42.0.40/relay/0?turn=on&timer=10 Will switch output ON for 10 sec.
http://10.42.0.40/relay/0?turn=toggle Will switch the output On if OFF or vice versa
'''