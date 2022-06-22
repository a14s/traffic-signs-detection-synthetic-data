import os
import albumentations as A
from synthetic import *

backgrounds_path = "./backgrounds/"
results_path = "./results/"
objects_path = "./objects/"
source_images = ["no_entry.png"]

backgrounds = [backgrounds_path + bg for bg in os.listdir(backgrounds_path)]

bboxTransform = A.Compose([
    A.RandomBrightnessContrast((-0.25, 0.45), 0.6, always_apply=True),
    A.GaussNoise(p=0.7),
    A.Blur(3, p=0.6),
    ])

def cutouts(image):
    erase_pattern(image, 0.2)

def main():
    count = 0
    for bg in backgrounds:
        bg_img = cv2.imread(bg, cv2.IMREAD_UNCHANGED)
        bg_h, bg_w, bg_ch = bg_img.shape
        bg_copy = np.copy(bg_img)
        labels = []
        for s, src in enumerate(source_images):
            for i in range(0, random.randint(2, 3)):
                src_img = cv2.imread(objects_path + src, cv2.IMREAD_UNCHANGED)
                src_h, src_w, src_ch = src_img.shape

                resized_img = cv2.resize(src_img, random_size(20, 200, src_h/src_w))
                tilted_img = tilt_image(resized_img, random_tilt(45, 5))

                alpha = tilted_img[:, :, 3]
                tilted_img = cv2.cvtColor(tilted_img, cv2.COLOR_BGRA2RGB)
                transformed = bboxTransform(image=tilted_img[:,:,:3])["image"]
                transformed = cv2.cvtColor(transformed, cv2.COLOR_RGB2BGRA)
                transformed[:, :, 3] = alpha
                
                h, w, ch = transformed.shape
                if random_probability(0.25):
                    random_poss = random_position(transformed, transformed)
                    erase_rectangle(transformed, (random_poss[0], random_poss[1]), (int(random_poss[0] + w*0.2), int(random_poss[1] + h * 0.2)))
                random_pos = random_position(transformed, np.copy(bg_img), 0)
                overlayed = overlay_transparent(transformed, bg_copy, random_pos)
                tl, br = (random_pos[0], random_pos[1]), (random_pos[0] + w, random_pos[1] + h)
                center_x, center_y, width, height = (tl[0]+w/2)/bg_w, (tl[1]+h/2)/bg_h, w/bg_w, h/bg_h
                labels.append("{} {} {} {} {}\n".format(s, center_x, center_y, width, height))
        
        if random_probability(0.2):
            erase_pattern(overlayed, 0.01, 0.1, 0.01*5, pattern=random.randint(0, 2))
        # Checks labels
        # copy_overlayed = np.copy(overlayed)
        # for label in labels:
        #     s, center_x, center_y, width, height = label.replace("\n", "").split(" ")
        #     s, center_x, center_y, width, height = s, float(center_x), float(center_y), float(width), float(height)
        #     cv2.rectangle(copy_overlayed, (int((center_x-width/2)*bg_w), int((center_y-height/2)*bg_h)), (int((center_x+width/2)*bg_w), int((center_y+height/2)*bg_h)), (0, 255, 0))
        # cv2.imshow("w", copy_overlayed)
        # cv2.waitKey(0)

        cv2.imwrite(results_path + str(bg.split("/")[2]), overlayed)
        with open(results_path + str(bg.split("/")[2].split(".")[0]) + ".txt", "w") as f:
            f.writelines(labels)
        print(count + 1)
        count+=1
main()
