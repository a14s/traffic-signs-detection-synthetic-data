import os
import shutil
import albumentations as A
from synthetic import *
from sklearn.model_selection import train_test_split

backgrounds_path = "./backgrounds/"
results_path = "./results/"
objects_path = "./objects/"
source_images = ["no_entry.png"]

backgrounds = [backgrounds_path + bg for bg in os.listdir(backgrounds_path)]

bboxTransform = A.Compose([
    A.RandomBrightnessContrast((-0.3, 0.4), (-0.6, 0.4), always_apply=True),
    A.GaussNoise((10, 120), always_apply=True),
    A.Blur(5, p=0.7),
    A.HueSaturationValue(hue_shift_limit=15, val_shift_limit=40, p=0.6),
    A.MotionBlur(7, p=0.3),
    ])

def main():
    count = 0
    sign_per_image = 1
    for bg in backgrounds:
        bg_img = cv2.imread(bg, cv2.IMREAD_UNCHANGED)
        bg_h, bg_w, bg_ch = bg_img.shape
        bg_copy = np.copy(bg_img)
        labels = []
        for s, src in enumerate(source_images):
            for i in range(sign_per_image):
                src_img = cv2.imread(objects_path + src, cv2.IMREAD_UNCHANGED)
                src_h, src_w, src_ch = src_img.shape

                resized_img = cv2.resize(src_img, random_size(40, 220, src_h/src_w))
                tilted_img = tilt_image(resized_img, random_tilt(70, 2))

                alpha = tilted_img[:, :, 3]
                tilted_img = cv2.cvtColor(tilted_img, cv2.COLOR_BGRA2RGB)
                transformed = random_lighting(tilted_img[:, :, :3])
                transformed = bboxTransform(image=transformed)["image"]
                transformed = cv2.cvtColor(transformed, cv2.COLOR_RGB2BGRA)
                transformed[:, :, 3] = alpha
                
                h, w, ch = transformed.shape
                if random_probability(0.15):
                    random_poss = random_position(transformed, transformed)
                    erase_rectangle(transformed, (random_poss[0], random_poss[1]), (int(random_poss[0] + w*0.2), int(random_poss[1] + h * 0.2)))

                random_pos = random_position(transformed, np.copy(bg_img), 0)
                overlayed = overlay_transparent(transformed, bg_copy, random_pos)
                tl, br = (random_pos[0], random_pos[1]), (random_pos[0] + w, random_pos[1] + h)
                center_x, center_y, width, height = (tl[0]+w/2)/bg_w, (tl[1]+h/2)/bg_h, w/bg_w, h/bg_h
                labels.append("{} {} {} {} {}\n".format(s, center_x, center_y, width, height))
        
        if random_probability(0.05):
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


if __name__ == "__main__":
    """synthetic_photos = [photo for photo in os.listdir(results_path) if photo.split(".")[1] == "jpg"]
    train, test = train_test_split(synthetic_photos, train_size=0.75)
    test, val = train_test_split(test, train_size=0.3)
    print(len(train), len(val), len(test))

    train_path = "./synthetic_splits/train/"
    test_path = "./synthetic_splits/test/"
    val_path = "./synthetic_splits/val/"

    for pic in train:
        print(pic)
        shutil.move(results_path+pic, train_path)
        shutil.move(results_path+pic.split(".")[0]+".txt", train_path)

    for pic in test:
        print(pic)
        shutil.move(results_path+pic, test_path)
        shutil.move(results_path+pic.split(".")[0]+".txt", test_path)
    
    for pic in val:
        print(pic)
        shutil.move(results_path+pic, val_path)
        shutil.move(results_path+pic.split(".")[0]+".txt", val_path)

    real_photos_path = "./only-no-entry/"
    real_photos = [photo for photo in os.listdir(real_photos_path) if photo.split(".")[1] == "jpg"]
    real_train, real_test = train_test_split(real_photos, train_size=0.7)
    real_test, real_val = train_test_split(real_test, train_size=0.5)

    train_path = "./real_splits/train/"
    test_path = "./real_splits/test/"
    val_path = "./real_splits/val/"

    for pic in real_train:
        print(pic)
        shutil.copy(real_photos_path+pic, train_path)
        shutil.copy(real_photos_path+pic.split(".")[0]+".txt", train_path)

    for pic in real_test:
        print(pic)
        shutil.copy(real_photos_path+pic, test_path)
        shutil.copy(real_photos_path+pic.split(".")[0]+".txt", test_path)
    
    for pic in real_val:
        print(pic)
        shutil.copy(real_photos_path+pic, val_path)
        shutil.copy(real_photos_path+pic.split(".")[0]+".txt", val_path)
    """