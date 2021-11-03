
import sys
from lightShow import halloweenLights


if __name__ == '__main__':
    # --
    lightShow = halloweenLights()
    # --
    args = sys.argv
    if len(args) > 1:
        if "-v" in args:
            lightShow.verbose = True
            print("verbose mode on")
        if "-s" in args:
            lightShow.sound = True
            print("spooky sounds turned on")
        if "-h" in args:
            print("possible args: -v:verbose, -s:output sound, -d:devices x,x,x,\n -toff: light off delay, -ton: light on delay, -r: random light on/off")
            quit()
        if "-d" in args:
            Index = args.index("-d")
            lightShow.devices = args[Index + 1].split(",")
            print(f"devices: {lightShow.devices}")
        if "-toff" in args:
            Index = args.index("-toff")
            lightShow.timeDelayOperateSwitchOff = int(args[Index + 1])
            print(f"switch off time delay: {lightShow.timeDelayOperateSwitchOff}")
        if "-ton" in args:
            Index = args.index("-ton")
            lightShow.timeDelayOperateSwitchOn = int(args[Index + 1])
            print(f"switch on time delay: {lightShow.timeDelayOperateSwitchOn}")
        if "-r" in args:
            print("random light times on")
            lightShow.randomLightTimes = True

    lightShow.run()
