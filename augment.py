import cv2
import math
import numpy as np

#   TODO: make pitch
#   TODO: check shear
#   TODO: check motion blur
#   TODO: add values to noise
#   TODO: mosaic

def rotate_image(image, angle): #works for now but theres pixel go bye from sides maybe fix if needed np.int(math.sqrt(w**2 + h**2)) diagonal
    if angle == 0:
        return image
    h, w, c = image.shape
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def resize_image(image, w, h):
    return cv2.resize(image, (w, h))

def tilt_image(image, yaw):
    yaw = int(yaw)
    if yaw == 0:
        return image
    h, w, c = image.shape
    ratio = math.cos(math.radians(yaw))
    src_rect = np.array([
        [0, 0], [0, h],
        [w, h], [w, 0],
    ], dtype=np.float32)
    d = np.int((1 - ratio) * h)
    if d <= 0:
        d = 1

    if yaw < 0:
        tl = [0, 0 + d//2 + d//2]
        bl = [0, h - d//2 + d//2]
        br = [w * math.cos(math.radians(yaw)), h + d//2 + d//2]
        tr = [w * math.cos(math.radians(yaw)), 0 - d//2 + d//2]
    else:
        tl = [0, 0 - d//2 + d//2]
        bl = [0, h + d//2 + d//2]
        br = [w * math.cos(math.radians(yaw)), h - d//2 + d//2]
        tr = [w * math.cos(math.radians(yaw)), 0 + d//2 + d//2]

    dst_rect = np.array([tl, bl, br, tr], dtype=np.float32)
    max, min = np.max(dst_rect, axis=0), np.min(dst_rect, axis=0)
    M = cv2.getPerspectiveTransform(src_rect, dst_rect)
    tilted = cv2.warpPerspective(image, M, (np.int(max[0]), np.int(max[1])))[d//2:-d//2]
    #cv2.polylines(tilted, np.array([[tl, tr, br, bl]], np.int32), True, (255, 255, 255, 255))
    #print(yaw, ratio, d, max, min)

    return tilted

def crop_image(image, crop_ratio, start=(0, 0)):
    h, w, c = image.shape
    return image[start[1]:h*crop_ratio,start[0]:w*crop_ratio]

def add_gaussian_noise(image):
    row,col,ch= image.shape
    mean = 0
    var = 0.1
    sigma = var**0.5
    gauss = np.random.normal(mean,sigma,(row,col,ch))
    gauss = gauss.reshape(row,col,ch)
    noisy = image + gauss
    return noisy

def add_noise_saltAndPepper(image):
    row,col,ch = image.shape
    s_vs_p = 0.5
    amount = 0.004
    out = np.copy(image)
    num_salt = np.ceil(amount * image.size * s_vs_p)
    coords = [np.random.randint(0, i - 1, int(num_salt))
            for i in image.shape]
    out[coords] = 1
    num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i - 1, int(num_pepper))
            for i in image.shape]
    out[coords] = 0
    return out

def add_noise_poisson(image):
      vals = len(np.unique(image))
      vals = 2 ** np.ceil(np.log2(vals))
      noisy = np.random.poisson(image * vals) / float(vals)
      return noisy

def add_noise_speckle(image):
    row,col,ch = image.shape
    gauss = np.random.randn(row,col,ch)
    gauss = gauss.reshape(row,col,ch)        
    noisy = image + image * gauss
    return noisy

def add_brightness_contrast(image, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        buf = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
    else:
        buf = image.copy()

    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    return buf

def add_gaussian_blur(image, k_size):
    return cv2.GaussianBlur(image, (k_size, k_size), 0)

def add_motion_blur(image, k_size): # needs negative values and y motion blur
    kernel = np.zeros((k_size, k_size))
    kernel[int((k_size-1)/2), :] = np.ones(k_size)
    kernel = kernel / k_size
    return cv2.filter2D(image, -1, kernel)

def add_saturation(image, value):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = s*value
    s = np.clip(s,0,255)
    hsv = cv2.merge([h,s,v])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def shear_image(image, dx, dy, maxX, maxY): #values from 0 to 1
    if dx == 0 and dy == 0:
        return image
    h, w, c = image.shape
    dx, dy = dx * maxX * w, dy * maxY * h
    src_rect = np.array([
        [0, 0], [0, h],
        [w, h], [w, 0],
    ], dtype=np.float32)
    tl = [0, 0]
    bl = [0 + dx*2, h]
    br = [w + dx*2, h + dy*2]
    tr = [w, 0 + dy*2]
    dst_rect = np.array([tl, bl, br, tr], dtype=np.float32)
    max, min = np.max(dst_rect, axis=0), np.min(dst_rect, axis=0)
    M = cv2.getPerspectiveTransform(src_rect, dst_rect)
    sheared = cv2.warpPerspective(image, M, (np.int(max[0]), np.int(max[1])))
    #cv2.polylines(tilted, np.array([[tl, tr, br, bl]], np.int32), True, (255, 255, 255, 255))
    return sheared

def mirror_image(image, axis=0): # 0 for horizontal, 1 for vertical, -1 for both
    return cv2.flip(image, flipCode=axis)

def erase_rectangle(image, tl, br, noise=False): #make sure works for alpha
    h, w, c = image.shape
    if not noise:
        if c == 1:
            image[tl[1]:br[1], tl[0]:br[0]] = 0
        elif c == 3:
            image[tl[1]:br[1], tl[0]:br[0]] = (0, 0, 0)
        elif c == 4:
            image[tl[1]:br[1], tl[0]:br[0]] = (0, 0, 0, 0) # not sure
    else:
        if c == 1:
            image[tl[1]:br[1], tl[0]:br[0]] = np.random.randint(0, 255)
        elif c == 3:
            image[tl[1]:br[1], tl[0]:br[0]] = np.random.randint(0, 255, size=(3))
        elif c == 4:
            image[tl[1]:br[1], tl[0]:br[0]] = np.random.randint(0, 255, size=(4)) # not sure

    return image

def erase_pattern(image, ratio, border_ratio=0, step_ratio=0, pattern=0): #border ratio TODO
    h, w, c = image.shape
    count = int(w * ratio)
    if pattern == 0: #  square pattern
        if step_ratio == 0:
            step = int(count*2)
        else:
            step = int(step_ratio * w)
        for i in range(count//2, w, step):    #idk why w * 2 but doesnt work properly sometimes if only w ... well now i know
            for j in range(count//2, h, step):    #idk why h * 2 but doesnt work properly sometimes if only w ... well now i know
                image = erase_rectangle(image, (i, j), (i + count, j + count))
        return image
    elif pattern == 1:
        if step_ratio == 0:
            step = int(count*2)
        else:
            step = int(step_ratio * w)
        for i in range(count//2, w, step):
            image = erase_rectangle(image, (i, 0), (i + count, h))
        return image
    elif pattern == 2:
        if step_ratio == 0:
            step = int(count*2)
        else:
            step = int(step_ratio * h)
        for j in range(count//2, h, step):
            image = erase_rectangle(image, (0, j), (w, j + count))
        return image
    else:
        return image

def tweak_hue(image, percent=0):
    if percent == 0:
        return image
    percent = percent/100
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    #h = np.full_like(h, 180)
    h = (h + 180*percent) % 180
    h = np.clip(h,0,255)
    h = np.array(h, dtype=np.uint8)
    hsv = cv2.merge([h,s,v])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def illumination(image, mask):
    mask = cv2.GaussianBlur(mask, (153, 153), 0)
    return cv2.bitwise_or(image, mask)

def main():
    return

if __name__ == "__main__":
    main()




"""
hue:
    img = cv2.resize(cv2.imread("./objects/no_entry.png", cv2.IMREAD_UNCHANGED), (200, 200))
    for i in range(-10, 11):
        print(i)
        cv2.imshow("w", tweak_hue(img, i))
        cv2.waitKey(0)
"""