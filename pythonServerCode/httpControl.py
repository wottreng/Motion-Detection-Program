import requests

reqTimeout = 3
verbose = False

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