---
date: 2023-10-12
authors: [nima-ch]
categories:
  - Data analysis
  - Outlier
tags:
  - Z-Score
  - Interquartile Range
slug: data-outlier-detection-techniques
readtime: 20
---

# Outlier Detection Techniques: Use Cases, and Distinctions

## Introduction:
Outlier detection is a critical task in data preprocessing, especially in fields like fraud detection, network security, and quality control in manufacturing. The identification and handling of outliers, which are data points that significantly deviate from the other observations, is crucial as they can skew the analysis and lead to incorrect conclusions. This essay delineates various outlier detection methods, elucidates their practical applications, and underscores the differences among them.

## Outlier Detection Methods:

**Statistical Methods:**

### Standard Deviation (SD) Method
When `method` is set to "SD", the function uses standard deviation as the basis for outlier detection:

- First, data is normalized using a specified normalization method (`zscore` or `minmax`).
- For each QC metric (module), the data values that fall below or above a certain threshold, set by `sd_step_dict` or `default_sd_step`, are flagged as outliers. These thresholds are usually set in terms of standard deviations. For instance, a typical choice could be values that are more than 2 standard deviations away from the mean.

Mathematically:

$$\text{Outliers} = \{ x \mid x < \mu - k\sigma \} \cup \{ x \mid x > \mu + k\sigma \}$$

Where:

- $x$ is a data point
- $\mu$ is the mean of the data
- $\sigma$ is the standard deviation of the data
- $k$ is the step value, which can vary for each module or use the default step

### Interquartile Range or Tukey’s Fences Method 
When `method` is set to "IQR", the function uses the interquartile range for outlier detection:

- The Interquartile Range (IQR) is the range between the 1st quartile (25th percentile) and the 3rd quartile (75th percentile) of the data.

$$\text{IQR} = Q3 - Q1$$

Where:

- $ Q1 $ is the 1st quartile (25th percentile)
- $ Q3 $ is the 3rd quartile (75th percentile)
- To flag outliers, the function considers values that fall below the lower bound or above the upper bound:

$$\text{Lower bound} = Q1 - \text{multiplier} \times \text{IQR}$$

$$\text{Upper bound} = Q3 + \text{multiplier} \times \text{IQR}$$

Where `multiplier` is a specified input parameter, often set to 1.5 for moderate outliers or 3 for extreme outliers. 

Any data value below the lower bound or above the upper bound is considered an outlier.

**quantile_limit**:
   
- The `quantile_limit` determines the boundaries for the lower and upper quantiles.
- If set to a value like 0.25, then the lower and upper quantiles will be the 25th percentile (Q1) and the 75th percentile (Q3) respectively.
- This essentially defines the Interquantile Range which will be used in the next step to calculate the bounds for outliers. 

**multiplier**:

- Once the Interquantile Range (IQR) is calculated as $ IQR = Q3 - Q1 $, the `multiplier` is used to determine how far above Q3 and below Q1 a data point needs to be in order to be considered an outlier.
- Specifically, the bounds for outliers are computed as:
  - Lower bound = $Q1 - (\text{multiplier} \times IQR)$
  - Upper bound = $Q3 + (\text{multiplier} \times IQR)$
- A common value for the `multiplier` in traditional statistics, when using the Interquartile Range method for outlier detection, is 1.5. However, this function allows the user to specify their own multiplier, offering flexibility in how aggressive or conservative they want the outlier detection to be. 
- A higher multiplier will result in a broader range and fewer outliers, while a lower multiplier will create a narrower range and flag more points as outliers.



**Machine Learning-Based Methods:**

- Isolation Forest: Isolates outliers by randomly selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature.

- One-Class SVM: Identifies outliers by classifying data points in a high-dimensional feature space using support vector machines.

**Neighborhood-Based Methods:**

- K-Nearest Neighbors (K-NN): Detects outliers by measuring the distance of a point to its nearest neighbors.

- Local Outlier Factor (LOF): Identifies outliers by comparing the density of a point to the density of its neighbors.

**Deep Learning Methods:**

- Autoencoders: Identifies outliers by learning a low-dimensional representation of the data, then reconstructing the data and measuring reconstruction errors.

The choice between normalization and raw data largely depends on the nature and distribution of the data.

The choice between normalization and raw data largely depends on the nature and distribution of the data

## Use Cases, and Distinctions
### Interquartile Range (IQR)

1. **Nature**: IQR measures the middle 50% of the data. It inherently accounts for the spread and central tendency of the data without making any assumptions about the data's distribution.

2. **Outliers**: By design, IQR can detect outliers in data without requiring normalization, as it focuses on the range between quartiles that are less sensitive to extreme values.

3. **Usage**: For data that has a skewed distribution, IQR can be particularly useful. Additionally, if data has multiple modes (multimodal), or in the presence of heavy tails, the IQR remains a robust method.

### Standard Deviation (SD)

1. **Nature**: Standard deviation is a measure of how spread out the numbers in a dataset are on average. It is sensitive to outliers.

2. **Assumptions**: SD assumes that data has a nearly normal distribution. When applied to highly skewed data or data with significant outliers, the SD may not accurately capture the true spread of the data.

3. **Normalization**: Given the sensitivity of SD to outliers and its assumptions about data distribution, normalization becomes crucial. Normalizing the data can make it more symmetrical and lessen the impact of extreme values, making the SD more representative of the true data variability.

   - For example, using z-score normalization scales the data such that it has a mean of 0 and a standard deviation of 1. This helps ensure that the data conforms more closely to a standard normal distribution, making the use of SD for outlier detection more appropriate.

### When to Use IQR Without Normalization?

1. **Skewed Data**: If your dataset is skewed to the right or left, the IQR remains consistent as it focuses on the middle 50% of the data, making it less sensitive to extreme values.

2. **Heavy-tailed or Light-tailed Data**: For distributions that have heavy tails (more frequent extreme values than the normal distribution) or light tails (less frequent extreme values), the IQR can be a robust measure.

3. **Multimodal Data**: If your data has several peaks or modes, the IQR can still effectively measure the spread of the central data points.

In summary, while both IQR and SD are measures of data spread and can be used for outlier detection, their applicability and need for normalization vary based on the nature of the data. IQR is generally more robust to non-normal data distributions and outliers, while SD, particularly when used for outlier detection, often benefits from normalization to mitigate its sensitivity to extreme values.
## Conclusion

In summary, while both IQR and SD are measures of data spread and can be used for outlier detection, their applicability and need for normalization vary based on the nature of the data. IQR is generally more robust to non-normal data distributions and outliers, while SD, particularly when used for outlier detection, often benefits from normalization to mitigate its sensitivity to extreme values.

