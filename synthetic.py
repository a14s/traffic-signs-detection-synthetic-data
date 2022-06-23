import random

from augment import *

#   TODO: generate random values for noise, blur, saturation, contrast and brightness

def random_probability(prob=0.5):
    """
    trueCount = 0
    falseCount = 0
    for i in range(10000):
        if random_probability(0.3):
            trueCount+=1
        else:
            falseCount+=1
    print(trueCount/10000, falseCount/10000)
    """
    return random.randint(0, 100) >= (1 - prob)*100

def random_number(range=(0, 100)):
    if type(range) == int:
        range = (0, range)
    return random.randint(range[0], range[1])

def random_number_gaussian(range=(0, 100)):
    if type(range) == int:
        range = (0, range)
    num1 = random.randint(range[0], range[1]//2)
    num2 = random.randint(range[1]//2, range[1])
    return num1 + num2

def random_position(overlay, background, overflow_ratio=0):
    h, w, c = overlay.shape
    hBG, wBG, cBG = background.shape
    if not np.array_equiv(overlay, background):
        y = np.round(random.randrange(int(-h * overflow_ratio), int(hBG - h*(1-overflow_ratio))))
        x = np.round(random.randrange(int(-w * overflow_ratio), int(wBG - w*(1-overflow_ratio))))
        return [x, y]
    else:
        y = np.round(random.randrange(int(-h * overflow_ratio), int(h*(1-overflow_ratio))))
        x = np.round(random.randrange(int(-w * overflow_ratio), int(w*(1-overflow_ratio))))
        return [x, y]

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

def random_lighting(img):
    mask = np.zeros_like(img, dtype=np.uint8)
    h, w, ch = mask.shape
    for i in range(w//2, 0, -10):
        for ii in range(i, w//2+1, 5):
            x, y = random_position(mask, mask)
            rx = random_number((0, i))
            ry = random_number((0, i))
            #idk = np.array(np.random.randint(0, 100, size=(ry, rx)), dtype=np.uint8)
            mask[y:y+ry, x:x+rx] = random_number((0, 255))
    return illumination(img, mask)

def main():
    return

if __name__ == "__main__":
    main()