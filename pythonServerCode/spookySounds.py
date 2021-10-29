import os
import random

verbose = False


def playRandomSpookySound():
    soundFiles = os.listdir(f"{os.getcwd()}/soundClips")
    if "__pycache__" in soundFiles:
        soundFiles.pop(soundFiles.index("__pycache__"))
    randomSoundNumber = random.randint(0, len(soundFiles) - 1)
    soundClip = soundFiles[randomSoundNumber]
    os.popen(f"timeout 4s nvlc {os.getcwd()}/soundClips/{soundClip} &>/dev/null")


if __name__ == "__main__":
    playRandomSpookySound()
