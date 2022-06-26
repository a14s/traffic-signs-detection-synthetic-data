# Traffic Signs Detection Using Synthetic Data
### This repo compares the results of a YOLOv5 object detection model trained on real data vs synthetic data. It also covers the techniques used for the generation of the synthetic data used.  

### Introduction  

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
&nbsp;&nbsp;&nbsp;&nbsp; The data required to train an object detection model with similar or better accuracy to real data must be variant and must depict real life situations. Some examples for such situations include perspective changes, variable lighting, blurring and others. Thus, the data generation algorithm to be used must include such augmentations.  

![source sign image](https://github.com/a14s/traffic-signs-detection-synthetic-data/blob/3e2c6850716d6287049e1da97431fc6f829488d0/assets/no_entry.png "Source Sign Image")

 &nbsp;&nbsp;&nbsp;&nbsp; ***All photos in the synthetic dataset where generated using the same source sign. Due to this, many augmentation processes must be applied to imitiate real life signs.***
 
 
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
 &nbsp;&nbsp;&nbsp;&nbsp; In real life scenarios, many traffic signs can be deformed and covered with scratches, stickers, paint, and other stuff. This can be accounted for in synthetic data by applying Noise to the source signs. Another method is to randomly erase a part of the source sign so the model learns to not depend strictly on a full set of features.  
 ![deformation](https://github.com/a14s/traffic-signs-detection-synthetic-data/blob/3e2c6850716d6287049e1da97431fc6f829488d0/assets/deformed.png "Different Deformation") 
   
 #### Example Synthetic Photos Generated:
 INSERT EXAAMPLE PHOTOS HERE  
   
   
 ### Training
 &nbsp;&nbsp;&nbsp;&nbsp; Training was done using the YOLOv5m model architecture on Pytorch. All models were trained with the same settings: 50 epochs, batch size of 32, input image of size 416x416, and the same hyper-parameters. For the splitting of the datasets, both the real and synthetic datasets were split into a train set, a validation set, and a test set. From the train sets of the real and synthetic datasets, the train sets of the mixed datasets were then made.  
###### ***The Synthetic Dataset was validated on the synthetic validation split to check the health of the dataset. The rest of the models were all validated on the same real validation split to check their performance.***  
  
 <img src="https://github.com/a14s/traffic-signs-detection-synthetic-data/blob/3e2c6850716d6287049e1da97431fc6f829488d0/assets/mAP_0.5.svg" width="400"> 

 ### Testing
 &nbsp;&nbsp;&nbsp;&nbsp; Testing was done on the same test set for all models. The test set used contains only real photos. The input image size used for inference was 416x416. The table below shows the test results of 61 real photos containing 81 traffic signs in total:
 
 
|Model          |True Positives | False Positives | False Negatives |
|:-------------:|:-------------:|:---------------:|:---------------:|
|Real Data Only (300 Photos)| 67 | 62 | 14 |
|Synthetic Data Only (1200 Photos)| 42 | 13 | 39 |
|30% Real and 70% Synthetic Data (300 Photos)| 72 | 67 | 9 |
|30% Real and 70% Synthetic Data (1000 Photos)| 78 | 33 | 3 |  


example true photos
example false photos

### Possible Improvements
 &nbsp;&nbsp;&nbsp;&nbsp; Although the results show an improvment in the detection of the signs with the mixed datasets, synthetic data alone didn't show good results. The number of false positives is still high for the mixed datasets. Here are some methods to improve the results more:
 + Inference results could be improved by increasing the size of the input images when training or after training when detecting.
 + The parameters of the synthetic data generation could be tweaked to impose more variation. (for example: more blur and noise)
 + Other augmentation processes could be used to even properly mimic real life situations. (example: x-axis and z-axis rotation)
 + The usage of a real sign image as the source sign image instead of a digital image would drastically improve the results. A synthetic dataset generated using a set of real sign images could even standalone and show similar results to a real dataset.
 + Using a 3D rendering engine to generate the synthetic data will be a better approach than an image processing approach as most 3D engines can simulate real lighting, shadows, camera focus, reflections, textures, *ETC*., and all of the could be generated using only a 3D model of the object. 
 
### Conclusion
 &nbsp;&nbsp;&nbsp;&nbsp; In summary, object detection has many applications but the lack of data makes it harder to applied effectively. According to the testing results, synthetic datasets could be used as a way of improving results of real datasets with a limited number of images. Synthetic datasets could also help the detection of cases real datasets fail to detect. It is also very apparent that synthetic data generation still has a lot of room for improvment; a few examples for methods to improve it has also been provided.
