import os
import cv2
import torch

MODEL_PATH = "/.pt"
IMAGES_PATH = "//"
LABELS_SAVE_PATH = "//"

CONF_THRESH = 0.7

images_paths = os.listdir(IMAGES_PATH)
images = [cv2.imread(img)[:, :, ::-1] for img in images_paths]

#images_paths = ["bus.jpg", "zidane.jpg"]
#images = [cv2.imread(img)[:, :, ::-1] for img in images_paths]

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH)

# Inference
model.conf = CONF_THRESH
results = model(images, size=416)

# Results
results.print()  # print results to screen
#results.show()  # display results
results.save()  # save as results1.jpg, results2.jpg... etc.

for p, pic in enumerate(results.xywhn):
    pic_labels = []
    for result in pic:
        x, y, w, h, conf, c = result
        x, y, w, h, conf, c = float(x), float(y), float(w), float(h), float(conf), float(c)
        pic_labels.append(str(c) + " " + str(x) + " " + str(y) + " " + str(w) + " " + str(h) + " " + str(conf) + "\n")
        #center_x, center_y = x + w/2, y + h/2
        #print(center_x, center_y, w, h, conf, c)
    with open(LABELS_SAVE_PATH+images_paths[p].split(".")+".txt", "w") as f:
        f.writelines(pic_labels)

        