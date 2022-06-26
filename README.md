# Traffic Signs Detection Using Synthetic Data
### This repo compares the results of a YOLOv5 object detection model trained on real data vs synthetic data. It also covers the techniques used for the generation of the synthetic data used.  
 
&nbsp;&nbsp;&nbsp;&nbsp; Nowadays, Deep Learning has been incorporated in so many different sectors. One of the popular applications for it is Object Detection, is applied on health, defence, security, and many other different fields. Unfortunately however, since Deep Learning depends on Supervised Learning, it requires a lot of labelled data to train which in return makes it hard to be applied on situations where little to no data is available. Another problem is with the labelling; when the data available increases the time and effort it takes to label them also increases.  

&nbsp;&nbsp;&nbsp;&nbsp; To solve these problems, synthetic datasets can be generated to mimic hard-to-get data; Labels can also be extracted in the generation process. The synthetic data must be similar to the data its supposed to detect, and it must be variant so the model doesn't overfit on a single feature. To understand if synthetic data is feasible or not against real data, a comparison must be made. From this study, I wanted to see if a mix between real and synthetic data could achieve better results than only real data with the same amount of real photos or less.

4 datasets will be tested:-
1. Real Data Only (300 Photos)
2. Synthetic Data Only (1200 Photos)
3. 30% Real Data and 70% Synthetic Data (300 Photos)
4. 30% Real Data and 70% Synthetic Data (1000 Photos)
 
 ### Synthetic Dataset Generation Process:
&nbsp;&nbsp;&nbsp;&nbsp; The data required to train an object detection model with similar or better accuracy to real data must be variant and must depict real life situations. Some examples for such situations include perspective changes, variable lighting, blurring and others. Thus, our data generation algorithm must include such augmentations.  

### *All photos in the synthetic dataset where generated using the same source sign. Due to this, many augmentation processes must be applied to imitiate real life signs.*
 
 
 #### Perspective:
 
 #### Color:
 
 #### Light:
 
 #### Blur:
 
 #### Deformation:
 
 
 
 
 
|Model          |True Positives | False Positives | False Negatives |
|:-------------:|:-------------:|:---------------:|:---------------:|
|Real Data Only (300 Photos)| 67 | 62 | 14 |
|Synthetic Data Only (1200 Photos)| 42 | 13 | 39 |
|30% Real and 70% Synthetic Data (300 Photos)| 72 | 67 | 9 |
|30% Real and 70% Synthetic Data (1000 Photos)| 78 | 33 | 3 |
