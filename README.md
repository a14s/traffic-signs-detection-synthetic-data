# Traffic Signs Detection Using Synthetic Data
### This repo compares the results of a YOLOv5 object detection model trained on real data vs synthetic data. It also covers the techniques used for the generation of the synthetic data used.  
 
&nbsp;&nbsp;&nbsp;&nbsp; Nowadays, Deep Learning has been incorporated in so many different sectors. One of the popular applications for it is Object Detection, is applied on health, defence, security, and many other different fields. Unfortunately however, since Deep Learning depends on Supervised Learning, it requires a lot of labelled data to train which in return makes it hard to be applied on situations where little to no data is available. Another problem is with the labelling; when the data available increases the time and effort it takes to label them also increases.  

&nbsp;&nbsp;&nbsp;&nbsp; To solve these problems, synthetic datasets can be generated to mimic hard-to-get data; Labels can also be extracted in the generation process. The synthetic data must be similar to the data its supposed to detect, and it must be variant so the model doesn't overfit on a single feature. To understand if synthetic data is feasible or not against real data, a comparison must be made. From this study, I wanted to see if a mix between real and synthetic data could achieve better results than only real data with the same amount of real photos or less.

4 datasets will be tested:-
1. Real Data Only (300 Photos)
2. Synthetic Data Only (1200 Photos)
3. 30% Real Data and 70% Synthetic Data (300 Photos)
4. 30% Real Data and 70% Synthetic Data (1000 Photos)
 
 ### Real Dataset:  
 &nbsp;&nbsp;&nbsp;&nbsp; Some example photos from the real dataset to be used:  
 INSERT EXAMPLE REAL PHOTOS  
   
   
 ### Synthetic Dataset Generation Process:
&nbsp;&nbsp;&nbsp;&nbsp; The data required to train an object detection model with similar or better accuracy to real data must be variant and must depict real life situations. Some examples for such situations include perspective changes, variable lighting, blurring and others. Thus, our data generation algorithm must include such augmentations.  

![source sign image](https://github.com/a14s/traffic-signs-detection-synthetic-data/blob/3e2c6850716d6287049e1da97431fc6f829488d0/assets/no_entry.png "Source Sign Image")

#### *All photos in the synthetic dataset where generated using the same source sign. Due to this, many augmentation processes must be applied to imitiate real life signs.*
 
 
 #### Perspective: 
&nbsp;&nbsp;&nbsp;&nbsp; Since only one photo will be used as the source for all other photos, The source sign must be rotated along the y-axis to simulate different perspectives that can be found in real life. Traffic Signs lack 3D features and can be represented easily using 2D transformations. The scale of the sign must also be changed to achieve higher accuracy in relation to real life scenes.  
![different perspectives](https://github.com/a14s/traffic-signs-detection-synthetic-data/blob/3e2c6850716d6287049e1da97431fc6f829488d0/assets/tilted.png "Different Perspective Angles") 

 #### Color:
 &nbsp;&nbsp;&nbsp;&nbsp; Different textures, lighting, reflections, and natural occurances such as dust, rust, and others can change the color of the traffic signs or at least how the camera perceives it. To account for this, adjustments can be made to the Hue, Saturation, and color degree of the source sign.  
 ![color shades](https://github.com/a14s/traffic-signs-detection-synthetic-data/blob/3e2c6850716d6287049e1da97431fc6f829488d0/assets/colors.png "Different Color Shades") 
   
 #### Light:
 &nbsp;&nbsp;&nbsp;&nbsp; To imitiate real life scenes, different lightings must be accounted for. Brightness and Contrast of the source sign image can be randomized.  
 ![brightness contrast](https://github.com/a14s/traffic-signs-detection-synthetic-data/blob/3e2c6850716d6287049e1da97431fc6f829488d0/assets/lighting.png "Different Brighness and Contrast") 
 A simple algorithm that can generate irregular lighting on the source sign can also be used to accurately depict real life scenes. 
 ![irregular lighting](https://github.com/a14s/traffic-signs-detection-synthetic-data/blob/3e2c6850716d6287049e1da97431fc6f829488d0/assets/irregular_lighting.png "Irregular lighting") 
   
 #### Blur:
 &nbsp;&nbsp;&nbsp;&nbsp; Cameras aren't perfect, they won't always be focusing on the object they're supposed to focus on. Camera Defocus, Motion Blurring, and other similar effects must also be accounted for. Therefore, a gaussian blur and motion blur algorithms will be used for that.  
 ![blurring](https://github.com/a14s/traffic-signs-detection-synthetic-data/blob/3e2c6850716d6287049e1da97431fc6f829488d0/assets/blurring.png "Different Blur") 
   
 #### Deformation:
 &nbsp;&nbsp;&nbsp;&nbsp; In real life scenarios, many traffic signs can be deformed and covered with scratches, stickers, paint, and other stuff. This can be accounted for in synthetic data by applying Noise to the source signs. Another method is to randomly erase a part of the source sign so our model learns to not depend strictly on a full set of features.  
 ![deformation](https://github.com/a14s/traffic-signs-detection-synthetic-data/blob/3e2c6850716d6287049e1da97431fc6f829488d0/assets/deformed.png "Different Deformation") 
   
 #### Example Synthetic Photos Generated:
 
 ### Training
 
 ### Testing
 
 
 
|Model          |True Positives | False Positives | False Negatives |
|:-------------:|:-------------:|:---------------:|:---------------:|
|Real Data Only (300 Photos)| 67 | 62 | 14 |
|Synthetic Data Only (1200 Photos)| 42 | 13 | 39 |
|30% Real and 70% Synthetic Data (300 Photos)| 72 | 67 | 9 |
|30% Real and 70% Synthetic Data (1000 Photos)| 78 | 33 | 3 |
