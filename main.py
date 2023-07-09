import math
import gsw
import numpy as np
#import matplotlib as plt

#TODO: find dataset of pressure, salinity and temperature variation with depth (5 deeps ??? where?)
#TODO: lookup the oriinal documentation of the gsw library (TEOS-10) and find the actual diff eq used (solve general case?)


p = [1,2,3,4,5]
t = [6,5,4,3,2]
s = [2,8,2,2,2]

def check_in(pr, temp, sal): 
    if(len(pr)!=len(temp)!=len(sal)):
        print("mismatched input size")
        exit(0)

def print_sound():
    check_in(p,t,s)
    speed = gsw.sound_speed(s,t,p)
    LD = max((v ,i) for i, v in enumerate(speed))[1]
    if (LD < 60):
        BD = 17 * math.sqrt(LD)
    else:
        BD = LD + 60
    print(speed)
    print(f"The layer is at{LD} and best depth occurs at {BD}")


def gen_paths():
    print("this is in TODO")


def main():
    print_sound()

if __name__ == "__main__" :
    main()