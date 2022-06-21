import os
import albumentations as A
from synthetic import *

backgrounds_path = "./screenPhotos/newPhotos/"
results_path = "./result/"
objects_path = "./objects/"
source_images = ["no_entry.png", "Stop_sign.png"]

backgrounds = [backgrounds_path + bg for bg in os.listdir(backgrounds_path)]

bboxTransform = A.Compose([
    A.RandomBrightnessContrast(0.4, 0.6, always_apply=True),
    A.GaussNoise(p=0.9),
    A.Blur(3, p=0.6),
    ])

def main():
    for bg in backgrounds:
        bg_img = cv2.imread(bg, cv2.IMREAD_UNCHANGED)
        bg_copy = np.copy(bg_img)
        labels = []
        for s, src in enumerate(source_images):
            src_img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
            src_h, src_w, src_ch = src_img.shape

            resized_img = cv2.resize(src_img, random_size(20, 80, src_h/src_w))
            tilted_img = tilt_image(resized_img, random_tilt(45, 5))

            alpha = tilted_img[:, :, 3]
            tilted_img = cv2.cvtColor(tilted_img, cv2.COLOR_BGRA2RGB)
            transformed = bboxTransform(image=tilted_img[:,:,:3])["image"]
            transformed = cv2.cvtColor(transformed, cv2.COLOR_RGB2BGRA)
            transformed[:, :, 3] = alpha

            h, w, ch = transformed.shape
            random_pos = random_position(transformed, np.copy(bg_img), 0.2)
            overlayed = overlay_transparent(transformed, bg_copy, random_pos)
            tl, br = (random_pos[0], random_pos[1]), (random_pos[0] + w, random_pos[1] + h)
            labels.append("{} {} {} {} {}\n".format(s, w, h, tl[0], tl[1]))
            #cv2.rectangle(overlayed, tl, br, (0, 255, 0))

        cv2.imwrite(results_path + str(bg.split("/")[3]), overlayed)
        with open(results_path + str(bg.split("/")[3].split(".")[0]) + ".txt", "w") as f:
            f.writelines(labels)
        #print(bg)
        
main()

"""

    A.MotionBlur()
"""