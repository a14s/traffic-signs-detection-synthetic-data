import os
import cv2
import time

import numpy as np
import matplotlib.pyplot as plt

def delabel_result(label):
    label = label.strip().split(" ")
    c, x, y, w, h, conf = label
    c, x, y, w, h, conf = float(c), float(x), float(y), float(w), float(h), float(conf)
    return [c, x, y, w, h, conf]

def delabel_truth(label):
    label = label.strip().split(" ")
    c, center_x, center_y, w, h = label
    c, x, y, w, h = float(c), float(center_x) - float(w)/2, float(center_y) - float(h)/2, float(w), float(h)
    return [c, x, y, w, h]

def compare_labels(label_truth, label_result, thresh=0.1):
    return np.abs(label_truth[1] - label_result[1]) <= thresh and np.abs(label_truth[2] - label_result[2]) <= thresh

def compare_labels_2(label_truth, label_result):
    return np.abs(label_truth[1] - label_result[1]) <= label_truth[3] and np.abs(label_truth[2] - label_result[2]) <= label_truth[4]


#figure, axis = plt.subplots(2, 2)

MODELS = ["no_entry_real_14", "no_entry_real_16", "no_entry_3070_", "no_entry_30701000_"]

RESULT_LABELS_PATH = "./result_labels_0.1/"
TRUTH_TXTS_PATH = "./results/labels/"
for MODEL in MODELS:

    TP = 0
    FP = 0
    FN = 0
    TL = 0
    TR = 0

    TP_CONF = []
    FP_CONF = []

    txts_path = RESULT_LABELS_PATH+MODEL+"/"
    result_txts = os.listdir(txts_path)

    for txt in result_txts:
        result_labels = []
        truth_labels = []

        with open(txts_path+txt, 'r') as f:
            result_labels = f.readlines()
        with open(TRUTH_TXTS_PATH+txt, 'r') as f:
            truth_labels = f.readlines()

        result_labels = [delabel_result(lbl) for lbl in result_labels if lbl != "\n" and lbl != " " and lbl != ""]
        truth_labels = [delabel_truth(lbl) for lbl in truth_labels if lbl != "\n" and lbl != " " and lbl != ""]

        tp = 0
        fp = 0
        fn = 0

        fp_cpy = result_labels[:]
        
        TL += len(truth_labels)
        TR += len(result_labels)

        for tl in truth_labels:
            if result_labels:
                for rli, rl in enumerate(result_labels):
                    if compare_labels_2(tl, rl) == True:
                        tp += 1
                        fp_cpy.remove(rl)
                        # if int(rl[5] * 10) == 1:
                        #     print("CHECK", MODEL, txt)
                        TP_CONF.append(int(rl[5] * 10))
                        break
                    else:
                        if rli == len(result_labels) - 1:
                            fn += 1
            else:
                fn += 1
        
        fp = len(result_labels) - tp
        for lbl in fp_cpy:
            if int(lbl[5] * 10) == 9:
                print("CHECK", MODEL, lbl[1] + lbl[3]/2, lbl[2] + lbl[4]/2, txt)
            FP_CONF.append(int(lbl[5] * 10))

        TP += tp
        if fp > 0:
            FP += fp
        FN += fn

    #print(TP_CONF)
    #print(FP_CONF)
    print(MODEL)
    print(TP, FP, FN)
    print(TL, TR)
    #print(TP_CONF)
    #print(FP_CONF)

    bar_tp = [0 for i in range(9)]
    bar_fp = [0 for i in range(9)]
    bar_x = np.array([(i+1)/10 for i in range(9)])
    
    for num in TP_CONF:
        bar_tp[num-1] += 1
    
    for num in FP_CONF:
        bar_fp[num-1] += 1
    
    # plt.bar(bar_x - 0.0125, bar_tp, 0.025)
    # plt.bar(bar_x + 0.0125, bar_fp, 0.025)
    # plt.xticks(bar_x, bar_x)
    # plt.xlabel("Confidence")
    # plt.title("Real Data Only (300 Photos)")
    # plt.ylabel("Frequency")
    # plt.legend(["True Positives", "False Positives"])
    # plt.plot()
    # plt.waitforbuttonpress()
        

        
        