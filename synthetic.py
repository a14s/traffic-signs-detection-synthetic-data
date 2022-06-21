import random

from augment import *

#   TODO: generate random values for noise, blur, saturation, contrast and brightness

def random_position(overlay, background, overflow_ratio=0):
    h, w, c = overlay.shape
    hBG, wBG, cBG = background.shape
    if overlay != background:
        y = np.round(random.randrange(int(-h * overflow_ratio), int(hBG - h*(1-overflow_ratio))))
        x = np.round(random.randrange(int(-w * overflow_ratio), int(wBG - w*(1-overflow_ratio))))
        return x, y
    else:
        y = np.round(random.randrange(int(-h * overflow_ratio), int(h*(1-overflow_ratio))))
        x = np.round(random.randrange(int(-w * overflow_ratio), int(w*(1-overflow_ratio))))
        return x, y 

def random_tilt(range, step): #   from - range to range
    return random.randrange(-range - 1, range + 1, step)

def random_size(min, max, ratio): #ratio h/w
    w = random.randrange(min, max)
    h = w * ratio
    return int(w), int(h)

def overlay_transparent(overlay, background, position):
    x, y = position
    h, w, channels = overlay.shape
    wStart, wLimit, hStart, hLimit = x, x+w, y, y+h
    woStart, woLimit, hoStart, hoLimit = 0, w, 0, h
    hBackground, wBackground, cBackground = background.shape
    alpha = overlay[:, :, 3] / 255

    if wLimit < 0 or hLimit < 0:
        return background

    if wStart < 0:
        wStart = 0
        woStart = -x
    elif wStart >= wBackground:
        return background

    if wLimit > wBackground:
        wLimit = wBackground
        woLimit = np.abs(x - wBackground)

    if hStart < 0:
        hStart = 0
        hoStart = -y
    elif hStart >= hBackground:
        return background

    if hLimit > hBackground:
        hLimit = hBackground
        hoLimit = np.abs(y - hBackground)

    for c in range(3):
        background[hStart:hLimit, wStart:wLimit, c] = alpha[hoStart:hoLimit, woStart:woLimit] * overlay[hoStart:hoLimit, woStart:woLimit, c] + (1 - alpha)[hoStart:hoLimit, woStart:woLimit] * background[hStart:hLimit, wStart:wLimit, c]

    return background

def main():
    return

if __name__ == "__main__":
    main()