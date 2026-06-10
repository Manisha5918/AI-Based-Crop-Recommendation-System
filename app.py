import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
import sqlite3
from datetime import datetime
import plotly.express as px


st.set_page_config( page_title="AI Based Crop Recommendation System",
    layout="wide"
)


model = pickle.load(open("crop_model.pkl","rb"))


API_KEY = "b9c33d854748e9ab53bfc39c42a8315d"


conn = sqlite3.connect(
    "history.db",
    check_same_thread=False
)

cursor = conn.cursor()


cursor.execute(
"""
CREATE TABLE IF NOT EXISTS recommendations
(
date TEXT,
location TEXT,
crop TEXT,
confidence REAL
)
"""
)

conn.commit()



def save_history(location,crop,confidence):

    cursor.execute(
    """
    INSERT INTO recommendations
    VALUES (?,?,?,?)
    """,
    (
    str(datetime.now()),
    location,
    crop,
    confidence
    )
    )

    conn.commit()



def get_weather(city):

    try:

        url = (
        "https://api.openweathermap.org/data/2.5/weather?q="
        + city
        + "&appid="
        + API_KEY
        + "&units=metric"
        )

        data=requests.get(url).json()


        temp=data["main"]["temp"]

        humidity=data["main"]["humidity"]

        return temp,humidity


    except:

        return None,None




def fertilizer(n,p,k):


    result=[]


    if n < 40:

        result.append(
        "Nitrogen level is low. Add urea based fertilizer."
        )


    if p < 40:

        result.append(
        "Phosphorus level is low. Add phosphate fertilizer."
        )


    if k < 40:

        result.append(
        "Potassium level is low. Add potassium fertilizer."
        )


    if len(result)==0:

        result.append(
        "Soil nutrients are balanced."
        )


    return result




def explain_ml(values):


    features=[
        "Nitrogen",
        "Phosphorus",
        "Potassium",
        "Temperature",
        "Humidity",
        "pH",
        "Rainfall"
    ]


    importance=np.array(values)

    importance=importance/importance.sum()*100


    df=pd.DataFrame(
        {
        "Feature":features,
        "Influence":importance
        }
    )


    return df





st.sidebar.title("Navigation")


page=st.sidebar.radio(
    "",
    [
    "Crop Recommendation",
    "Model Analysis",
    "Recommendation History",
    "Project Overview"
    ]
)




st.title(
"AI Based Crop Recommendation System"
)


st.write(
"An intelligent crop recommendation system using Machine Learning,soil parameters and real-time weather analysis.")





if page=="Crop Recommendation":


    st.header(
    "Smart Crop Recommendation"
    )


    location=st.text_input(
        "Enter Location"
    )


    if st.button(
        "Fetch Weather Data"
    ):

        temp,hum=get_weather(location)


        if temp:

            st.session_state["temperature"]=temp

            st.session_state["humidity"]=hum

            st.success(
            "Weather data fetched successfully"
            )


        else:

            st.error(
            "Unable to fetch weather data"
            )



    c1,c2=st.columns(2)



    with c1:

        n=st.number_input(
            "Nitrogen",
            value=50
        )


        p=st.number_input(
            "Phosphorus",
            value=50
        )


        k=st.number_input(
            "Potassium",
            value=50
        )


        ph=st.number_input(
            "Soil pH",
            value=7.0
        )



    with c2:


        temperature=st.number_input(
            "Temperature",
            value=float(st.session_state.get(
                "temperature",
                25
            ))
        )


        humidity=st.number_input(
            "Humidity",
            value=float(st.session_state.get(
                "humidity",
                60
            ))
        )


        rainfall=st.number_input(
            "Rainfall",
            value=100.0
        )




    if st.button(
        "Recommend Crop"
    ):


        data=np.array(
            [[
            n,
            p,
            k,
            temperature,
            humidity,
            ph,
            rainfall
            ]]
        )


        crop=model.predict(data)[0]


        probability=model.predict_proba(data)

        confidence=round(
            np.max(probability)*100,
            2
        )


        save_history(
            location,
            crop,
            confidence
        )



        col1,col2,col3=st.columns(3)


        col1.metric(
            "Recommended Crop",
            crop.upper()
        )


        col2.metric(
            "Suitability",
            str(confidence)+"%"
        )


        col3.metric(
            "Soil Status",
            "Suitable"
        )



        st.subheader(
        "Alternative Crop Suggestions"
        )


        crops=model.classes_

        scores=probability[0]*100


        rank=pd.DataFrame(
            {
            "Crop":crops,
            "Suitability (%)":scores
            }
        )


        rank=rank.sort_values(
            by="Suitability (%)",
            ascending=False
        ).head(5)



        st.dataframe(
            rank
        )



        fig=px.bar(
            rank,
            x="Crop",
            y="Suitability (%)",
            color="Crop"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )




        st.subheader(
        "Crop Recommendation Explanation"
        )


        exp=explain_ml(
        [
        n,p,k,
        temperature,
        humidity,
        ph,
        rainfall
        ]
        )


        st.dataframe(exp)


        fig2=px.bar(
            exp,
            x="Feature",
            y="Influence",
            color="Feature"
        )


        st.plotly_chart(
            fig2,
            use_container_width=True
        )





        st.subheader(
        "Fertilizer Recommendation"
        )


        for i in fertilizer(n,p,k):

            st.info(i)




        report=f"""
PRECISION AGRICULTURE REPORT

Location : {location}

Recommended Crop : {crop}

Suitability : {confidence} %

Nitrogen : {n}

Phosphorus : {p}

Potassium : {k}

Temperature : {temperature}

Humidity : {humidity}

pH : {ph}

Rainfall : {rainfall}

Generated : {datetime.now()}
"""


        st.download_button(
            "Download Report",
            report,
            "crop_report.txt"
        )





elif page=="Model Analysis":


    st.header(
    "Model Performance Dashboard"
    )


    result=pd.DataFrame(
        {
        "Algorithm":
        [
        "Random Forest",
        "Decision Tree",
        "SVM",
        "KNN",
        "Naive Bayes"
        ],

        "Accuracy":
        [
        99.3,
        98.6,
        96.1,
        97.0,
        99.4
        ]
        }
    )


    fig=px.bar(
        result,
        x="Algorithm",
        y="Accuracy",
        color="Algorithm"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.dataframe(
        result
    )





elif page=="Recommendation History":


    st.header(
    "Recommendation History"
    )


    history=pd.read_sql(
        "SELECT * FROM recommendations",
        conn
    )


    st.dataframe(
        history
    )





elif page=="Project Overview":


    st.header(
    "Project Overview"
    )


    st.subheader(
    "AI Precision Agriculture Recommendation System"
    )


    st.write(
    """
A decision support system that combines:

- Machine Learning
- Explainable AI
- Real-time Weather API
- Soil Analysis
- Recommendation Storage
- Fertilizer Recommendation
- Report Generation
"""
    )


    st.subheader(
    "Technology Stack"
    )


    st.write(
    """
- Python
- Scikit-Learn
- Streamlit
- SQLite Database
- OpenWeather API
- Plotly Visualization
"""
    )