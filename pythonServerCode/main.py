
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
        if "-s" in args:
            lightShow.sound = True
        if "-h" in args:
            print("possible args: -v:verbose, -s:output sound, -d:devices x,x,x")
            quit()
        if "-d" in args:
            Index = args.index("-d")
            lightShow.devices = args[Index + 1].split(",")
        if "-toff" in args:
            Index = args.index("-toff")
            lightShow.timeDelayOperateSwitchOff = int(args[Index + 1])
        if "-ton" in args:
            Index = args.index("-ton")
            lightShow.timeDelayOperateSwitchOff = int(args[Index + 1])
        if "-r" in args:
            print("random light times on")
            lightShow.randomLightTimes = True

    lightShow.run()
