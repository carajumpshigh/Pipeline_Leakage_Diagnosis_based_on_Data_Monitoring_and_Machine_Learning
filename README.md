# Pipeline Leakage Diagnosis based on Data Monitoring and Machine Learning

Interdiscipline project in civil engineering & mathematics for undergraduate thesis

*Shanghai Institute of Disaster Prevention and Relief & Tongji University*

## Introduction

With the lifeline pipeline network continuously extending and playing an increasingly crucial role as the basis for the normal operation of the city, this project builds a leakage detection model based on data analysis of the multi-source monitoring data of the existing lifeline pipeline network system, and then establishes the risk early warning system of the leakage of each pipeline segment, so as to response in time and reduce the impact of lifeline pipe network accidents and encourage the study of prevention mechanisms related to pipe network leakage.

- This project first studies the combo pipeline network leakage diagnosis method and time series anomaly detection method, and then proposes a time series anomaly detection algorithm for gas pipeline network leakage diagnosis scenarios. 
- Then, the clustering and anomaly detection models of SCADA measuring points are established. The DTW algorithm is used to measure the similarity of the internal trend of SCADA measuring points. Based on the spectral clustering algorithm, the typical template daily line is obtained. 
- Additionally, the model designed a double-layer clustering method to improve the efficiency. Training was carried out with more than 16,000 time series in 2015, and the validity of the anomaly detection model was proved by the test based on the data of 2016. 

- Then, the model above is further optimized considering the geographic distribution of accidents. A double-layer anomaly detection model based on Page Rank algorithm and risk cluster analysis is proposed. The model is tested by the 2015 example, which further improves the flexibility and work efficiency of the leak detection model.



## Leakage Diagnosis Model

- **Double-Layer CLustering Model**
![Double-Layer CLustering Model](https://github.com/carajumpshigh/Pipeline_Leakage_Diagnosis_based_on_Data_Monitoring_and_Machine_Learning/blob/master/Images/Leakage%20Diagnosis%20Model%20with%20Spatial%20Info.png)


Most of the compute load comes from calculating the DTW distances between each of the daily pressure trend. With double-layer clustering applied, **98%** of the total calculation is saved, which improves the efficency greatly.

<p align="center"><img src="https://github.com/carajumpshigh/Pipeline_Leakage_Diagnosis_based_on_Data_Monitoring_and_Machine_Learning/blob/master/Images/Calculation%20Comparison.png" width="300" height="100">


- **Optimized Model with Geographic Info**
![Optimized Model with Geographic Info](https://github.com/carajumpshigh/Pipeline_Leakage_Diagnosis_based_on_Data_Monitoring_and_Machine_Learning/blob/master/Images/Leakage%20Diagnosis%20Model.png)


