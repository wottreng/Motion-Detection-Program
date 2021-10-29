import os
import random


def playRandomSpookySound():
    soundFiles = os.listdir(f"{os.getcwd()}/soundClips")
    if "__pycache__" in soundFiles:
        soundFiles.pop(soundFiles.index("__pycache__"))
    randomSoundNumber = random.randint(0, len(soundFiles) - 1)
    soundClip = soundFiles[randomSoundNumber]
    if ".wav" in soundClip:
        os.popen(f"timeout 4s nvlc {os.getcwd()}/soundClips/{soundClip} &>/dev/null")
    else:
        print(f"sound file error: {soundClip}")

if __name__ == "__main__":
    playRandomSpookySound()
