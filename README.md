# AI Based Crop Recommendation System

A Machine Learning based smart agriculture system that recommends the most suitable crop using soil nutrients and real-time weather conditions.

---

## Features

- Crop Recommendation using Machine Learning
- Real-time Weather API Integration
- Soil Nutrient Analysis
- Explainable ML Analysis
- Alternative Crop Suggestions
- Fertilizer Recommendation
- Model Performance Dashboard
- Recommendation History Storage
- Interactive Data Visualization
- Report Generation

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

Multiple Machine Learning algorithms were trained and compared:

- Random Forest
- Decision Tree
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)
- Naive Bayes

The model with the highest accuracy is selected for generating crop recommendations.

---

## Dataset

The dataset used for this project is the Crop Recommendation Dataset from Kaggle.

Dataset Link:

https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset

The dataset contains soil nutrient information and environmental factors required for recommending suitable crops based on agricultural conditions.

### Input Features

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- Soil pH
- Rainfall

### Target Output

- Recommended Crop

---

## Project Modules

### Crop Recommendation Engine

Analyzes soil nutrients and weather parameters to recommend the most suitable crop.

### Weather Intelligence

Fetches real-time temperature and humidity values using OpenWeather API.

### Explainable ML Analysis

Shows the influence of different parameters on crop recommendation decisions.

### Nutrient Analysis

Visualizes soil nutrient values to understand soil conditions.

### Fertilizer Recommendation

Provides fertilizer suggestions based on nutrient deficiencies.

### Model Performance Dashboard

Compares different Machine Learning algorithms based on accuracy.

### Recommendation History

Stores previous crop recommendations using SQLite database.

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/Manisha5918/AI-Precision-Agriculture-Recommendation-System.git
```

Move into the project folder:

```bash
cd AI-Precision-Agriculture-Recommendation-System
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## Applications

- Precision Farming
- Smart Agriculture
- Crop Selection Assistance
- Soil Based Decision Support
- Agriculture Technology Solutions

---

## Future Enhancements

- Cloud Deployment
- Mobile Application Integration
- More Crop Dataset Expansion
- Advanced AI Agriculture Assistant

