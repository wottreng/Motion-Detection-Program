import os
import random

verbose = False

def evilLaugh():
    os.system(f"timeout 5s nvlc {os.getcwd()}/soundClips/EvilLaughCackle.wav 1>/dev/null")

def femaleScream():
    os.system(f"timeout 2s nvlc {os.getcwd()}/soundClips/FemaleScream.wav 1>/dev/null")

def scaryTheme():
    os.system(f"timeout 4s nvlc {os.getcwd()}/soundClips/ScaryTheme.wav 1>/dev/null")

def playSpookySound():
    var = random.randint(0,8)
    try:
        if var < 3:
            evilLaugh()
        elif var < 6:
            femaleScream()
        else:
            scaryTheme()
    except Exception as e:
        if verbose:
            print(f"error: {str(e)[:60]}")


if __name__ == "__main__":
    evilLaugh()
    #femaleScream()
    #scaryTheme()

