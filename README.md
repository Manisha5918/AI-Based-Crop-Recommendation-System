# AI Based Crop Recommendation System

## Precision Agriculture AI using Machine Learning and Real-Time Weather Intelligence

A smart agriculture decision-support system that recommends the most suitable crop using soil nutrients, environmental conditions, and Machine Learning models.

The system combines crop prediction, real-time weather analysis, fertilizer recommendations, explainable ML insights, and agricultural analytics through an interactive Streamlit dashboard.

---

## Features

- Crop Recommendation using Machine Learning
- Real-Time Weather API Integration
- Soil Nutrient Analysis (NPK and pH)
- Explainable Machine Learning Analysis
- Alternative Crop Suggestions
- Fertilizer Recommendation System
- Agricultural Advisor Chat Assistant
- Model Performance Dashboard
- Recommendation History Storage using SQLite
- Interactive Data Visualization
- Crop Analysis Report Generation

---

## Technologies Used

- Python
- Streamlit
- Scikit-Learn
- Pandas
- NumPy
- SQLite
- OpenWeather API
- Plotly

---

## Machine Learning Models

Multiple Machine Learning algorithms are trained and compared:

- Random Forest Classifier
- Decision Tree Classifier
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)
- Gaussian Naive Bayes

The model with the highest accuracy is selected automatically for crop prediction.

Generated files:

```
crop_model.pkl
features.pkl
model_results.pkl
```

---

## Dataset

Dataset Used:

Crop Recommendation Dataset - Kaggle

Dataset Link:

https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset

The dataset contains agricultural records with soil nutrient values and environmental factors.

### Input Features

| Feature | Description |
|---|---|
| N | Nitrogen content |
| P | Phosphorus content |
| K | Potassium content |
| Temperature | Temperature value |
| Humidity | Relative humidity |
| pH | Soil acidity/basicity |
| Rainfall | Rainfall value |

### Output

Recommended Crop

---

## Project Modules

### Crop Recommendation Engine

Uses trained Machine Learning models to analyze soil nutrients and weather parameters to recommend suitable crops.

### Weather Intelligence

Integrates OpenWeather API to fetch:

- Current temperature
- Humidity

### Soil Health Analysis

Analyzes:

- Soil pH level
- NPK nutrient balance
- Nutrient deficiencies
- Soil health score

### Fertilizer Recommendation System

Provides fertilizer suggestions based on soil nutrient requirements.

Supports:

- Urea
- DAP
- SSP
- MOP

### Agricultural Advisor Chat

Interactive farming assistant that provides guidance about:

- Crop information
- Soil nutrients
- Fertilizer management
- Soil improvement

### Analytics Dashboard

Includes:

- Dataset exploration
- Feature analysis
- Correlation visualization
- Crop distribution analysis
- ML model comparison

### Recommendation History

Stores prediction records using SQLite database:

- Date and time
- Location
- Soil values
- Weather information
- Predicted crop
- Confidence score
- ML model used

---

## Project Structure

```
AI-Based-Crop-Recommendation-System

├── app.py
├── train_model.py
├── Crop_recommendation.csv

├── crop_model.pkl
├── features.pkl
├── model_results.pkl

├── history.db
├── requirements.txt
├── Procfile
├── README.md

└── .streamlit
      └── config.toml
```

---

## Installation and Setup

Clone the repository:

```bash
git clone https://github.com/Manisha5918/AI-Based-Crop-Recommendation-System.git
```

Move into the folder:

```bash
cd AI-Based-Crop-Recommendation-System
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
streamlit run app.py
```

---

## Applications

- Precision Farming
- Smart Agriculture
- Crop Selection Assistance
- Soil-Based Decision Support
- Agricultural Technology Solutions

---

## Future Enhancements

- IoT Sensor Integration
- Mobile Application Development
- Multilingual Farmer Assistant
- Satellite-Based Soil Analysis
- Deep Learning Based Recommendation System

