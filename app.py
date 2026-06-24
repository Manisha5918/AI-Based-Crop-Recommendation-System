import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
import sqlite3
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# --- Streamlit Page Configurations ---
st.set_page_config(
    page_title="Precision Agriculture AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Global CSS Styling Injection ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

/* Hide Streamlit default components to look like a real app */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stHeader"] {display: none !important;}
[data-testid="stFooter"] {display: none !important;}

/* Global styles */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #1e293b !important;
}

.stApp {
    background-color: #ffffff !important;
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: #f8fafc !important;
    border-right: 1px solid #e2e8f0 !important;
}

/* Sidebar Brand Header */
.sidebar-brand-container {
    text-align: center;
    padding: 24px 12px 16px 12px;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 20px;
}
.sidebar-brand-title {
    font-family: 'Outfit', sans-serif;
    color: #0f172a;
    font-weight: 800;
    font-size: 1.25rem;
    margin: 0;
    letter-spacing: -0.02em;
}
.sidebar-brand-subtitle {
    font-size: 0.75rem;
    color: #64748b;
    font-weight: 600;
    letter-spacing: 0.05em;
}

/* Sidebar Radio Navigation Override */
div[data-testid="stRadio"] > label {
    display: none !important; /* Hide standard heading */
}

div[data-testid="stRadio"] [role="radiogroup"] {
    padding: 0 4px !important;
}

div[data-testid="stRadio"] [role="radiogroup"] label {
    background-color: transparent !important;
    border: none !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    margin-bottom: 6px !important;
    cursor: pointer !important;
    transition: all 0.2s ease-in-out !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    color: #475569 !important;
}

div[data-testid="stRadio"] [role="radiogroup"] label:hover {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
}

/* Checked navigation item */
div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
    background-color: #f0fdf4 !important;
    color: #16a34a !important;
    font-weight: 600 !important;
    border-left: 4px solid #16a34a !important;
    border-radius: 0 8px 8px 0 !important;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02) !important;
}

div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) p {
    color: #16a34a !important;
    font-weight: 600 !important;
}

/* Hide standard radio dot wrapper */
div[data-testid="stRadio"] [role="radiogroup"] label > div:first-child {
    display: none !important;
}

/* Navigation items text styling */
div[data-testid="stRadio"] [role="radiogroup"] label p {
    margin: 0 !important;
    color: inherit !important;
    font-size: 0.9rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}

/* Navigation Icons base styling */
div[data-testid="stRadio"] [role="radiogroup"] label::before {
    content: "" !important;
    display: inline-block !important;
    width: 18px !important;
    height: 18px !important;
    min-width: 18px !important;
    min-height: 18px !important;
    background-size: contain !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    opacity: 0.7 !important;
    transition: opacity 0.2s ease !important;
}

div[data-testid="stRadio"] [role="radiogroup"] label:hover::before {
    opacity: 1 !important;
}

div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked)::before {
    opacity: 1 !important;
}

/* Vector icons for items */
div[data-testid="stRadio"] [role="radiogroup"] > div:nth-child(1) label::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23475569' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 9.8A7 7 0 0 1 11 20z'/%3E%3Cpath d='M19 2c-2.26 4.33-5.27 7.14-8 10'/%3E%3C/svg%3E") !important;
}
div[data-testid="stRadio"] [role="radiogroup"] > div:nth-child(1) label:has(input:checked)::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2316a34a' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 9.8A7 7 0 0 1 11 20z'/%3E%3Cpath d='M19 2c-2.26 4.33-5.27 7.14-8 10'/%3E%3C/svg%3E") !important;
}

div[data-testid="stRadio"] [role="radiogroup"] > div:nth-child(2) label::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23475569' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='4' y1='21' x2='4' y2='14'/%3E%3Cline x1='4' y1='10' x2='4' y2='3'/%3E%3Cline x1='12' y1='21' x2='12' y2='12'/%3E%3Cline x1='12' y1='8' x2='12' y2='3'/%3E%3Cline x1='20' y1='21' x2='20' y2='16'/%3E%3Cline x1='20' y1='12' x2='20' y2='3'/%3E%3Cline x1='1' y1='14' x2='7' y2='14'/%3E%3Cline x1='9' y1='8' x2='15' y2='8'/%3E%3Cline x1='17' y1='16' x2='23' y2='16'/%3E%3C/svg%3E") !important;
}
div[data-testid="stRadio"] [role="radiogroup"] > div:nth-child(2) label:has(input:checked)::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2316a34a' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='4' y1='21' x2='4' y2='14'/%3E%3Cline x1='4' y1='10' x2='4' y2='3'/%3E%3Cline x1='12' y1='21' x2='12' y2='12'/%3E%3Cline x1='12' y1='8' x2='12' y2='3'/%3E%3Cline x1='20' y1='21' x2='20' y2='16'/%3E%3Cline x1='20' y1='12' x2='20' y2='3'/%3E%3Cline x1='1' y1='14' x2='7' y2='14'/%3E%3Cline x1='9' y1='8' x2='15' y2='8'/%3E%3Cline x1='17' y1='16' x2='23' y2='16'/%3E%3C/svg%3E") !important;
}

div[data-testid="stRadio"] [role="radiogroup"] > div:nth-child(3) label::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23475569' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='18' y1='20' x2='18' y2='10'/%3E%3Cline x1='12' y1='20' x2='12' y2='4'/%3E%3Cline x1='6' y1='20' x2='6' y2='14'/%3E%3C/svg%3E") !important;
}
div[data-testid="stRadio"] [role="radiogroup"] > div:nth-child(3) label:has(input:checked)::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2316a34a' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='18' y1='20' x2='18' y2='10'/%3E%3Cline x1='12' y1='20' x2='12' y2='4'/%3E%3Cline x1='6' y1='20' x2='6' y2='14'/%3E%3C/svg%3E") !important;
}

div[data-testid="stRadio"] [role="radiogroup"] > div:nth-child(4) label::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23475569' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'/%3E%3C/svg%3E") !important;
}
div[data-testid="stRadio"] [role="radiogroup"] > div:nth-child(4) label:has(input:checked)::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2316a34a' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'/%3E%3C/svg%3E") !important;
}

div[data-testid="stRadio"] [role="radiogroup"] > div:nth-child(5) label::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23475569' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cellipse cx='12' cy='5' rx='9' ry='3'/%3E%3Cpath d='M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5'/%3E%3Cpath d='M3 12c0 1.66 4 3 9 3s9-1.34 9-3'/%3E%3C/svg%3E") !important;
}
div[data-testid="stRadio"] [role="radiogroup"] > div:nth-child(5) label:has(input:checked)::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2316a34a' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cellipse cx='12' cy='5' rx='9' ry='3'/%3E%3Cpath d='M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5'/%3E%3Cpath d='M3 12c0 1.66 4 3 9 3s9-1.34 9-3'/%3E%3C/svg%3E") !important;
}

div[data-testid="stRadio"] [role="radiogroup"] > div:nth-child(6) label::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23475569' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='3'/%3E%3Cpath d='M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z'/%3E%3C/svg%3E") !important;
}
div[data-testid="stRadio"] [role="radiogroup"] > div:nth-child(6) label:has(input:checked)::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2316a34a' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='3'/%3E%3Cpath d='M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z'/%3E%3C/svg%3E") !important;
}

/* Sidebar Widgets Section Styling */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    color: #64748b !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    margin-bottom: 8px !important;
}

/* Custom CSS classes */
.glass-card {
    background: #ffffff !important;
    border-radius: 12px !important;
    padding: 24px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03) !important;
    margin-bottom: 24px !important;
    transition: box-shadow 0.2s ease, border-color 0.2s ease !important;
}
.glass-card:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
    border-color: #cbd5e1 !important;
}

.card-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    margin-top: 0 !important;
    margin-bottom: 16px !important;
    border-bottom: 1px solid #f1f5f9 !important;
    padding-bottom: 8px !important;
    display: flex;
    align-items: center;
    gap: 8px;
}

label, .stWidgetLabel, [data-testid="stWidgetLabel"] {
    color: #334155 !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
}

/* Spacer label for column button alignment */
.spacer-label {
    height: 25px;
}

/* Sleek Buttons styling */
div.stButton > button:first-child, div.stDownloadButton > button:first-child {
    background: #16a34a !important;
    color: white !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.5rem !important;
    border-radius: 8px !important;
    border: none !important;
    box-shadow: 0 1px 2px 0 rgba(22, 163, 74, 0.1) !important;
    transition: all 0.2s ease !important;
    width: 100%;
}
div.stButton > button:first-child:hover, div.stDownloadButton > button:first-child:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 6px -1px rgba(22, 163, 74, 0.15) !important;
    background: #15803d !important;
}

/* Metrics boxes styling */
.metric-row {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
    flex-wrap: wrap;
}

.metric-box {
    flex: 1;
    min-width: 200px;
    text-align: center;
    background: #f8fafc;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.metric-box:hover {
    transform: translateY(-2px);
    border-color: #cbd5e1;
}

.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #0f172a !important;
    font-family: 'Outfit', sans-serif;
    line-height: 1.1;
    letter-spacing: -0.02em;
}

.metric-label {
    font-size: 0.8rem;
    color: #64748b !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 8px;
    font-weight: 700;
}

.badge {
    background: #f0fdf4;
    color: #16a34a !important;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    border: 1px solid #dcfce7;
}

/* Dashboard Header SaaS Top Bar */
.dashboard-header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 16px;
    margin-bottom: 28px;
    width: 100%;
}
.dashboard-main-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.75rem !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    margin: 0 !important;
    padding: 0 !important;
    letter-spacing: -0.02em;
}
.dashboard-sub-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.875rem !important;
    font-weight: 400 !important;
    color: #64748b !important;
    margin: 4px 0 0 0 !important;
}
.dashboard-header-right {
    display: flex;
    align-items: center;
    gap: 12px;
}
.status-badge {
    background-color: #f0fdf4;
    border: 1px solid #dcfce7;
    border-radius: 9999px;
    padding: 6px 12px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.status-dot {
    width: 8px;
    height: 8px;
    background-color: #16a34a;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(22, 163, 74, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(22, 163, 74, 0); }
}
.status-text {
    font-size: 0.725rem;
    font-weight: 700;
    color: #16a34a;
    letter-spacing: 0.05em;
}
.tenant-badge {
    background-color: #f1f5f9;
    border: 1px solid #e2e8f0;
    color: #475569;
    font-size: 0.725rem;
    font-weight: 700;
    padding: 6px 12px;
    border-radius: 9999px;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)

# --- Load Models & Core Configs ---
@st.cache_resource
def load_all_models():
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.naive_bayes import GaussianNB
    
    try:
        df = pd.read_csv("Crop_recommendation.csv")
        X = df.drop("label", axis=1)
        y = df["label"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        models = {
            "Naive Bayes": GaussianNB(),
            "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
            "Decision Tree": DecisionTreeClassifier(random_state=42),
            "KNN": KNeighborsClassifier(),
            "SVM": SVC(probability=True, random_state=42)
        }
        
        for name, clf in models.items():
            clf.fit(X_train, y_train)
            
        return models
    except Exception as e:
        try:
            single_model = pickle.load(open("crop_model.pkl", "rb"))
            return {"Naive Bayes (Cached)": single_model}
        except Exception:
            return {}

models_dict = load_all_models()
API_KEY = "b9c33d854748e9ab53bfc39c42a8315d"

# --- Database Integration ---
def init_db():
    conn = sqlite3.connect("history.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='recommendations'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        cursor.execute("PRAGMA table_info(recommendations)")
        columns = [col[1] for col in cursor.fetchall()]
        if "nitrogen" not in columns:
            cursor.execute("DROP TABLE recommendations")
            table_exists = False
            
    if not table_exists:
        cursor.execute("""
        CREATE TABLE recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            location TEXT,
            nitrogen INTEGER,
            phosphorus INTEGER,
            potassium INTEGER,
            temperature REAL,
            humidity REAL,
            ph REAL,
            rainfall REAL,
            crop TEXT,
            confidence REAL,
            model_used TEXT
        )
        """)
        conn.commit()
    conn.close()

init_db()

def save_history(location, n, p, k, temp, hum, ph, rain, crop, confidence, model_name):
    conn = sqlite3.connect("history.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO recommendations (timestamp, location, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, crop, confidence, model_used)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        location or "Unknown Location",
        int(n),
        int(p),
        int(k),
        float(temp),
        float(hum),
        float(ph),
        float(rain),
        crop,
        float(confidence),
        model_name
    ))
    conn.commit()
    conn.close()

def delete_history_entry(entry_id):
    conn = sqlite3.connect("history.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recommendations WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

def clear_all_history():
    conn = sqlite3.connect("history.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recommendations")
    conn.commit()
    conn.close()

# --- OpenWeather API Integration ---
def get_weather(city, custom_key=None):
    if not city:
        return None
    key = custom_key if custom_key else API_KEY
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()
        if response.status_code == 200:
            return {
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"].capitalize(),
                "wind_speed": data["wind"]["speed"],
                "icon": data["weather"][0]["icon"],
                "city_name": f"{data['name']}, {data['sys']['country']}"
            }
        return None
    except Exception:
        return None

# --- Crop-Specific Optimal NPK Mapping ---
CROP_OPTIMAL_NPK = {
    'apple': {'N': 21, 'P': 134, 'K': 200},
    'banana': {'N': 100, 'P': 82, 'K': 50},
    'blackgram': {'N': 40, 'P': 67, 'K': 19},
    'chickpea': {'N': 40, 'P': 68, 'K': 80},
    'coconut': {'N': 22, 'P': 17, 'K': 31},
    'coffee': {'N': 101, 'P': 29, 'K': 30},
    'cotton': {'N': 118, 'P': 46, 'K': 20},
    'grapes': {'N': 23, 'P': 133, 'K': 200},
    'jute': {'N': 78, 'P': 47, 'K': 40},
    'kidneybeans': {'N': 21, 'P': 68, 'K': 20},
    'lentil': {'N': 19, 'P': 68, 'K': 19},
    'maize': {'N': 78, 'P': 48, 'K': 20},
    'mango': {'N': 20, 'P': 27, 'K': 30},
    'mothbeans': {'N': 21, 'P': 48, 'K': 20},
    'mungbean': {'N': 21, 'P': 47, 'K': 20},
    'muskmelon': {'N': 100, 'P': 18, 'K': 50},
    'orange': {'N': 20, 'P': 17, 'K': 10},
    'papaya': {'N': 50, 'P': 59, 'K': 50},
    'pigeonpeas': {'N': 21, 'P': 68, 'K': 20},
    'pomegranate': {'N': 19, 'P': 19, 'K': 40},
    'rice': {'N': 80, 'P': 48, 'K': 40},
    'watermelon': {'N': 99, 'P': 17, 'K': 50}
}

# --- Detailed Crop Profiles Metadata ---
CROP_PROFILES = {
    'apple': {
        'season': 'Winter / Early Spring',
        'duration': '120-150 days (harvest)',
        'water': 'Moderate to High',
        'demand': 'Premium',
        'tips': 'Requires well-drained loamy soil. Pruning is key. Monitor for aphids and scab disease.'
    },
    'banana': {
        'season': 'Year-round (Warm climate)',
        'duration': '300-365 days',
        'water': 'High',
        'demand': 'High & Stable',
        'tips': 'Needs high organic matter and constant moisture. Protect from strong winds.'
    },
    'blackgram': {
        'season': 'Kharif / Summer',
        'duration': '75-90 days',
        'water': 'Low',
        'demand': 'Stable',
        'tips': 'Drought-resistant leguminous crop. Fixes nitrogen in soil. Avoid waterlogging.'
    },
    'chickpea': {
        'season': 'Rabi (Winter)',
        'duration': '90-110 days',
        'water': 'Low to Moderate',
        'demand': 'High',
        'tips': 'Thrives in cool climate. Needs well-aerated soil. Excellent for crop rotation.'
    },
    'coconut': {
        'season': 'Year-round (Coastal/Tropical)',
        'duration': 'Perennial (5-7 years to fruit)',
        'water': 'High',
        'demand': 'Stable',
        'tips': 'Requires sandy-loamy soil and high humidity. Salt-tolerant.'
    },
    'coffee': {
        'season': 'Monsoon (Planting)',
        'duration': 'Perennial (3-4 years to harvest)',
        'water': 'High',
        'demand': 'Premium',
        'tips': 'Needs shade trees, organic mulch, and acidic soil (pH 5.0 - 6.0). Hand-picking is vital.'
    },
    'cotton': {
        'season': 'Kharif (Spring/Summer)',
        'duration': '150-180 days',
        'water': 'Moderate',
        'demand': 'High',
        'tips': 'Deep, fertile black clayey soil is ideal. Protect from bollworms.'
    },
    'grapes': {
        'season': 'Spring',
        'duration': 'Perennial (harvest once/year)',
        'water': 'Moderate',
        'demand': 'Premium',
        'tips': 'Drip irrigation is highly recommended. Needs trellising and regular pruning.'
    },
    'jute': {
        'season': 'Pre-monsoon',
        'duration': '120-150 days',
        'water': 'High',
        'demand': 'Stable',
        'tips': 'Requires hot, wet climate and alluvial soil. Standing water is beneficial during growth.'
    },
    'kidneybeans': {
        'season': 'Rabi (Winter)',
        'duration': '90-120 days',
        'water': 'Moderate',
        'demand': 'High',
        'tips': 'Sensitive to frost and waterlogging. Keep soil loose and well-aerated.'
    },
    'lentil': {
        'season': 'Rabi (Winter)',
        'duration': '110-130 days',
        'water': 'Low',
        'demand': 'Stable',
        'tips': 'Very cold-tolerant. Fits well in dryland agriculture. Fixes nitrogen.'
    },
    'maize': {
        'season': 'Kharif / Spring',
        'duration': '90-110 days',
        'water': 'Moderate',
        'demand': 'High',
        'tips': 'Heavy feeder of Nitrogen. Keep soil loose and weed-free during early stages.'
    },
    'mango': {
        'season': 'Summer (Harvest)',
        'duration': 'Perennial (4-6 years to fruit)',
        'water': 'Low to Moderate',
        'demand': 'Premium',
        'tips': 'Thrives in tropical climates. Avoid waterlogging during flowering stage.'
    },
    'mothbeans': {
        'season': 'Kharif (Monsoon)',
        'duration': '75-90 days',
        'water': 'Low',
        'demand': 'Stable',
        'tips': 'Extremely drought-resistant pulse crop. Performs well on sandy soil.'
    },
    'mungbean': {
        'season': 'Summer / Kharif',
        'duration': '60-75 days',
        'water': 'Low',
        'demand': 'Stable',
        'tips': 'Short-duration crop. Ideal for intercropping between major crop cycles.'
    },
    'muskmelon': {
        'season': 'Summer',
        'duration': '80-90 days',
        'water': 'Moderate',
        'demand': 'High',
        'tips': 'Requires hot, dry climate and sandy loam soil. Drip irrigation improves sugar content.'
    },
    'orange': {
        'season': 'Winter/Spring (Harvest)',
        'duration': 'Perennial',
        'water': 'Moderate',
        'demand': 'High',
        'tips': 'Requires well-drained, deep soil. Sensitive to waterlogging. Apply micronutrients.'
    },
    'papaya': {
        'season': 'Year-round',
        'duration': '270-300 days',
        'water': 'Moderate to High',
        'demand': 'High',
        'tips': 'Extremely sensitive to waterlogging (root rot). Grow on raised beds.'
    },
    'pigeonpeas': {
        'season': 'Kharif (Monsoon)',
        'duration': '150-180 days',
        'water': 'Low to Moderate',
        'demand': 'High',
        'tips': 'Deep root system makes it highly drought-tolerant. Protect from pod borers.'
    },
    'pomegranate': {
        'season': 'Winter (Harvest)',
        'duration': 'Perennial',
        'water': 'Low',
        'demand': 'Premium',
        'tips': 'Tolerates semi-arid conditions. Prune to maintain bush structure. Avoid excess water during fruit ripening.'
    },
    'rice': {
        'season': 'Kharif (Monsoon)',
        'duration': '120-150 days',
        'water': 'High (Flooded)',
        'demand': 'High & Stable',
        'tips': 'Requires heavy clayey or loamy soils. Flooded conditions during early growth are standard.'
    },
    'watermelon': {
        'season': 'Summer',
        'duration': '80-100 days',
        'water': 'Moderate',
        'demand': 'High',
        'tips': 'Needs long warm seasons. Sandy soil is perfect. Limit watering as harvest approaches to concentrate sugars.'
    }
}

# --- Soil Diagnostics & Health Profiler ---
def diagnose_soil(n, p, k, ph):
    if ph < 5.5:
        ph_class = "Strongly Acidic"
        ph_desc = "Highly acidic. Root growth and nutrient absorption are severely limited."
        ph_action = "Add Agricultural Lime (Calcium Carbonate) or Dolomite to raise soil pH."
        ph_color = "#ef4444"
        ph_grade = 40
    elif 5.5 <= ph < 6.0:
        ph_class = "Moderately Acidic"
        ph_desc = "Slightly acidic soil. Ideal for acid-loving crops, but others may experience minor limitations."
        ph_action = "Incorporate wood ash or small amounts of lime. Monitor pH regularly."
        ph_color = "#f59e0b"
        ph_grade = 70
    elif 6.0 <= ph <= 7.5:
        ph_class = "Optimal (Neutral)"
        ph_desc = "Perfect condition. Maximum nutrient availability and high microbial activity."
        ph_action = "Soil pH is ideal. Continue using balanced organic compost to maintain this range."
        ph_color = "#16a34a"
        ph_grade = 100
    elif 7.5 < ph <= 8.5:
        ph_class = "Moderately Alkaline"
        ph_desc = "Slightly basic soil. Essential micronutrients like Iron and Zinc might get locked."
        ph_action = "Apply organic mulch, peat moss, or acidifying fertilizers (like ammonium sulfate)."
        ph_color = "#f59e0b"
        ph_grade = 70
    else:
        ph_class = "Strongly Alkaline"
        ph_desc = "Highly basic. Severe nutrient locking causing leaf chlorosis and stunting."
        ph_action = "Incorporate agricultural sulfur or gypsum immediately to neutralize alkalinity."
        ph_color = "#ef4444"
        ph_grade = 40

    warnings = []
    score_components = []
    
    if n < 30:
        warnings.append("Nitrogen (N) is critically low.")
        score_components.append(30)
    elif n > 100:
        warnings.append("Nitrogen (N) is high (potential environmental leaching risk).")
        score_components.append(70)
    else:
        score_components.append(100)
        
    if p < 30:
        warnings.append("Phosphorus (P) is critically low.")
        score_components.append(30)
    elif p > 90:
        warnings.append("Phosphorus (P) is high.")
        score_components.append(70)
    else:
        score_components.append(100)
        
    if k < 30:
        warnings.append("Potassium (K) is critically low.")
        score_components.append(30)
    elif k > 110:
        warnings.append("Potassium (K) is high.")
        score_components.append(80)
    else:
        score_components.append(100)

    overall_score = round((sum(score_components) / 3.0) * 0.7 + ph_grade * 0.3)
    
    if overall_score >= 85:
        rating = "Excellent"
        rating_color = "#16a34a"
    elif overall_score >= 70:
        rating = "Good"
        rating_color = "#3b82f6"
    elif overall_score >= 50:
        rating = "Fair"
        rating_color = "#f59e0b"
    else:
        rating = "Poor"
        rating_color = "#ef4444"

    return {
        "ph_class": ph_class,
        "ph_desc": ph_desc,
        "ph_action": ph_action,
        "ph_color": ph_color,
        "warnings": warnings,
        "score": overall_score,
        "rating": rating,
        "rating_color": rating_color
    }

# --- Crop-Specific Fertilizer Recommender ---
def recommend_fertilizers_for_crop(crop_name, n_input, p_input, k_input):
    crop_key = crop_name.lower().strip()
    if crop_key not in CROP_OPTIMAL_NPK:
        return ["No specific target values found for this crop. Keep soil nutrients balanced."]
        
    optimal = CROP_OPTIMAL_NPK[crop_key]
    n_opt, p_opt, k_opt = optimal['N'], optimal['P'], optimal['K']
    
    advice = []
    
    n_diff = n_opt - n_input
    if n_diff > 10:
        urea_needed = round(n_diff * 2.17, 1)
        advice.append(f"Nitrogen Deficit: Crop needs {n_opt} units but soil has {n_input}. Add {urea_needed} kg/acre of Urea to boost vegetative growth.")
    elif n_diff < -15:
        advice.append(f"Nitrogen Surplus: Soil has excess nitrogen ({n_input} vs {n_opt} needed). Suspend nitrogen inputs to avoid leaf burn.")
    else:
        advice.append(f"Nitrogen Balanced: Current levels are perfect for {crop_name.capitalize()}.")

    p_diff = p_opt - p_input
    if p_diff > 10:
        dap_needed = round(p_diff * 2.17, 1)
        ssp_needed = round(p_diff * 6.25, 1)
        advice.append(f"Phosphorous Deficit: Crop needs {p_opt} units but soil has {p_input}. Add {dap_needed} kg/acre of DAP or {ssp_needed} kg/acre of Single Superphosphate (SSP).")
    elif p_diff < -15:
        advice.append(f"Phosphorous Surplus: Soil has excess phosphorous ({p_input} vs {p_opt} needed). Avoid phosphate fertilizers.")
    else:
        advice.append(f"Phosphorous Balanced: Current levels are perfect for {crop_name.capitalize()}.")

    k_diff = k_opt - k_input
    if k_diff > 10:
        mop_needed = round(k_diff * 1.67, 1)
        advice.append(f"Potassium Deficit: Crop needs {k_opt} units but soil has {k_input}. Add {mop_needed} kg/acre of Muriate of Potash (MOP).")
    elif k_diff < -15:
        advice.append(f"Potassium Surplus: Soil has excess potassium ({k_input} vs {k_opt} needed). Avoid potash fertilizers.")
    else:
        advice.append(f"Potassium Balanced: Current levels are perfect for {crop_name.capitalize()}.")
        
    return advice

# --- Visual Charts & Reporting Helper Functions ---

def get_radar_chart(crop_name, input_n, input_p, input_k):
    crop_key = crop_name.lower().strip()
    optimal = CROP_OPTIMAL_NPK.get(crop_key, {'N': 50, 'P': 50, 'K': 50})
    categories = ['Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)']
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[input_n, input_p, input_k],
        theta=categories,
        fill='toself',
        fillcolor='rgba(22, 163, 74, 0.2)',
        line=dict(color='#16a34a', width=2),
        name='Current Soil Nutrients'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[optimal['N'], optimal['P'], optimal['K']],
        theta=categories,
        fill='toself',
        fillcolor='rgba(2, 132, 199, 0.1)',
        line=dict(color='#0284c7', width=2, dash='dash'),
        name=f'Optimal for {crop_name.capitalize()}'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(200, input_n, input_p, input_k, optimal['N'], optimal['P'], optimal['K'])],
                gridcolor='rgba(0, 0, 0, 0.08)',
                linecolor='rgba(0, 0, 0, 0.08)',
                tickfont=dict(color='#475569', size=9)
            ),
            angularaxis=dict(
                gridcolor='rgba(0, 0, 0, 0.08)',
                linecolor='rgba(0, 0, 0, 0.08)',
                tickfont=dict(color='#334155', size=10)
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(color='#334155', size=10)
        ),
        margin=dict(t=20, b=20, l=20, r=20),
        height=280
    )
    return fig

def get_gauge_chart(score, rating, color):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Soil Suitability ({rating})", 'font': {'size': 14, 'color': '#475569'}},
        number = {'font': {'color': '#0f172a', 'size': 32}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': color},
            'bgcolor': "rgba(0, 0, 0, 0.05)",
            'borderwidth': 1,
            'bordercolor': "rgba(0,0,0,0.05)",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.05)'},
                {'range': [50, 70], 'color': 'rgba(245, 158, 11, 0.05)'},
                {'range': [70, 85], 'color': 'rgba(59, 130, 246, 0.05)'},
                {'range': [85, 100], 'color': 'rgba(16, 185, 129, 0.05)'}
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=40, b=10, l=20, r=20),
        height=180
    )
    return fig

def generate_html_report(location, crop, confidence, diag, n, p, k, ph, temp, hum, rain, advice, profile):
    report_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Precision Agriculture Diagnostic Report</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: #2d3748;
                line-height: 1.6;
                background-color: #f7fafc;
                margin: 0;
                padding: 40px;
            }}
            .report-card {{
                background: white;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.05);
                padding: 40px;
                max-width: 800px;
                margin: auto;
                border-top: 8px solid #16a34a;
            }}
            .header {{
                text-align: center;
                border-bottom: 2px solid #edf2f7;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                margin: 0;
                color: #16a34a;
                font-size: 28px;
            }}
            .header p {{
                color: #718096;
                margin: 5px 0 0 0;
            }}
            .meta-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 30px;
            }}
            .meta-item {{
                background: #f8fafc;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
            }}
            .meta-label {{
                font-size: 11px;
                text-transform: uppercase;
                color: #718096;
                letter-spacing: 0.05em;
                font-weight: bold;
            }}
            .meta-value {{
                font-size: 18px;
                font-weight: bold;
                color: #1a202c;
            }}
            .section-title {{
                font-size: 18px;
                color: #0f172a;
                margin-top: 30px;
                margin-bottom: 15px;
                border-bottom: 1px solid #e2e8f0;
                padding-bottom: 5px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #edf2f7;
            }}
            th {{
                background-color: #f8fafc;
                color: #4a5568;
                font-weight: bold;
            }}
            .alert-box {{
                background: #f0fdf4;
                border-left: 4px solid #16a34a;
                padding: 15px;
                border-radius: 4px;
                margin-bottom: 20px;
            }}
            .warning-box {{
                background: #fffbeb;
                border-left: 4px solid #d97706;
                padding: 15px;
                border-radius: 4px;
                margin-bottom: 20px;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                color: #a0aec0;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="report-card">
            <div class="header">
                <h1>Precision Agriculture AI</h1>
                <p>Smart Agronomy Diagnostic Report</p>
            </div>
            
            <div class="meta-grid">
                <div class="meta-item">
                    <span class="meta-label">Recommended Crop</span><br>
                    <span class="meta-value" style="color: #16a34a;">{crop.upper()}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Suitability Match</span><br>
                    <span class="meta-value">{confidence}%</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Location / Region</span><br>
                    <span class="meta-value">{location}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Soil Rating</span><br>
                    <span class="meta-value" style="color: {diag['rating_color']};">{diag['score']}/100 ({diag['rating']})</span>
                </div>
            </div>
            
            <h2 class="section-title">Input Environment Metrics</h2>
            <table>
                <tr>
                    <th>Soil Metric</th>
                    <th>Value</th>
                    <th>Climate Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Nitrogen (N)</td>
                    <td>{n} mg/kg</td>
                    <td>Temperature</td>
                    <td>{temp} °C</td>
                </tr>
                <tr>
                    <td>Phosphorus (P)</td>
                    <td>{p} mg/kg</td>
                    <td>Humidity</td>
                    <td>{hum} %</td>
                </tr>
                <tr>
                    <td>Potassium (K)</td>
                    <td>{k} mg/kg</td>
                    <td>Rainfall</td>
                    <td>{rain} mm</td>
                </tr>
                <tr>
                    <td>Soil pH</td>
                    <td>{ph} ({diag['ph_class']})</td>
                    <td>-</td>
                    <td>-</td>
                </tr>
            </table>

            <h2 class="section-title">Soil Diagnostics</h2>
            <div class="meta-item" style="margin-bottom: 20px;">
                <p style="margin: 0; font-weight: bold;">{diag['ph_class']}</p>
                <p style="margin: 5px 0 0 0; color: #4a5568; font-size: 14px;">{diag['ph_desc']}</p>
                <p style="margin: 10px 0 0 0; font-size: 14px;"><b>Corrective Action:</b> {diag['ph_action']}</p>
            </div>
            
            {"".join([f'<div class="warning-box">Warning: {w}</div>' for w in diag['warnings']])}
            
            <h2 class="section-title">Crop Profile Details</h2>
            <table>
                <tr><td><b>Optimal Season</b></td><td>{profile.get('season', 'N/A')}</td></tr>
                <tr><td><b>Growth Cycle</b></td><td>{profile.get('duration', 'N/A')}</td></tr>
                <tr><td><b>Water Requirement</b></td><td>{profile.get('water', 'N/A')}</td></tr>
                <tr><td><b>Market Demand Tier</b></td><td>{profile.get('demand', 'N/A')}</td></tr>
                <tr><td><b>Agronomic Advice</b></td><td>{profile.get('tips', 'N/A')}</td></tr>
            </table>

            <h2 class="section-title">Fertilizer Recommendation Plan</h2>
            <div class="alert-box">
                <ul style="margin: 0; padding-left: 20px;">
                    {"".join([f'<li style="margin-bottom: 8px;">{item}</li>' for item in advice])}
                </ul>
            </div>
            
            <div class="footer">
                <p>Precision Decisions | Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p>This is an automated agronomic analysis. Please consult local extension services for secondary verification.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return report_html


# --- UI Layout ---

# Sidebar Navigation Panel
st.sidebar.markdown("""
<div class="sidebar-brand-container">
    <div class="sidebar-brand-title">Farmers Helper Portal</div>
    <div class="sidebar-brand-subtitle">CROP ADVISOR TOOL</div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation System",
    [
        "Find Best Crop",
        "Interactive Simulator",
        "Dataset Insights",
        "Ask Advisor Chat",
        "Saved Records Logs",
        "System Details"
    ]
)

# Sidebar Configuration Settings
st.sidebar.markdown("---")
st.sidebar.markdown("<span style='font-family: Outfit; font-weight:700; color:#0f172a; font-size:1rem;'>Prediction Settings</span>", unsafe_allow_html=True)
selected_model_name = st.sidebar.selectbox(
    "Prediction Method",
    options=list(models_dict.keys()) if models_dict else ["Naive Bayes"],
    index=0
)
custom_api_key = st.sidebar.text_input(
    "OpenWeather Map API Key",
    type="password",
    help="Optional. Enter your personal weather service key if the default limit is reached."
)

active_model = models_dict.get(selected_model_name)
if not active_model and models_dict:
    active_model = list(models_dict.values())[0]

# Main Header Section
st.markdown("""
<div class="dashboard-header-container">
    <div class="dashboard-header-left">
        <h1 class="dashboard-main-title">Crop Advisor Portal</h1>
        <p class="dashboard-sub-title">Find the best crop to grow by entering your soil conditions and local weather details.</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ----------------- PAGE 1: CROP RECOMMENDATION -----------------
if page == "Find Best Crop":
    # Soil Presets based on real Indian & global regional agronomic data
    SOIL_PRESETS = {
        "Manual Entry / Custom": None,
        "Black Clay Soil (e.g. Pune/Deccan - Moderate N, Low P, High K, Alkaline)": {"N": 50, "P": 40, "K": 135, "ph": 7.6, "rainfall": 85.0},
        "Red Loamy Soil (e.g. Bangalore/South India - Moderate N, Low P, Low K, Acidic)": {"N": 70, "P": 30, "K": 60, "ph": 6.2, "rainfall": 115.0},
        "Alluvial Soil (e.g. Ganges Plain/North India - Fertile, High N/P/K, Neutral)": {"N": 90, "P": 50, "K": 105, "ph": 7.0, "rainfall": 150.0},
        "Sandy Soil (e.g. Rajasthan/Arid regions - Low N/P/K, Alkaline, Low rain)": {"N": 25, "P": 20, "K": 45, "ph": 8.1, "rainfall": 35.0},
        "Laterite Soil (e.g. Western Ghats/Coastal - Low N/P/K, Highly Acidic, Heavy rain)": {"N": 40, "P": 25, "K": 35, "ph": 5.2, "rainfall": 230.0},
        "Peaty Soil (e.g. Kerala - High Organic N, Low P/K, Highly Acidic)": {"N": 60, "P": 15, "K": 30, "ph": 4.6, "rainfall": 290.0}
    }

    # Callback to apply typical preset soil values to widget session state keys
    def apply_soil_preset():
        choice = st.session_state["selected_preset_key"]
        preset_values = SOIL_PRESETS.get(choice)
        if preset_values:
            st.session_state["n_input"] = int(preset_values["N"])
            st.session_state["p_input"] = int(preset_values["P"])
            st.session_state["k_input"] = int(preset_values["K"])
            st.session_state["ph_input"] = float(preset_values["ph"])
            st.session_state["rain_input"] = float(preset_values["rainfall"])

    # Initialize session state keys for numeric inputs to allow seamless programmatic updates
    if "n_input" not in st.session_state: st.session_state["n_input"] = 50
    if "p_input" not in st.session_state: st.session_state["p_input"] = 50
    if "k_input" not in st.session_state: st.session_state["k_input"] = 50
    if "ph_input" not in st.session_state: st.session_state["ph_input"] = 7.0
    if "temp_input" not in st.session_state: st.session_state["temp_input"] = 25.0
    if "humidity_input" not in st.session_state: st.session_state["humidity_input"] = 60.0
    if "rain_input" not in st.session_state: st.session_state["rain_input"] = 100.0

    st.markdown("<div class='glass-card'><h3 class='card-title'>Find the Best Crop</h3>", unsafe_allow_html=True)
    
    col_w1, col_w2 = st.columns([2, 1])
    with col_w1:
        location = st.text_input("Enter Location / City Name", placeholder="e.g. Pune, London, Nairobi")
    with col_w2:
        st.markdown("<div class='spacer-label'></div>", unsafe_allow_html=True)
        fetch_weather_btn = st.button("Get Real-time Weather")
        
    if fetch_weather_btn and location:
        weather = get_weather(location, custom_api_key)
        if weather:
            st.session_state["temp_input"] = float(weather["temp"])
            st.session_state["humidity_input"] = float(weather["humidity"])
            st.session_state["weather_details"] = weather
            st.success(f"Weather loaded for {weather['city_name']}!")
            
            # Smart location-to-soil heuristics to auto-populate matching presets
            loc_lower = location.lower()
            if "pune" in loc_lower or "deccan" in loc_lower or "maharashtra" in loc_lower or "mumbai" in loc_lower:
                st.session_state["selected_preset_key"] = "Black Clay Soil (e.g. Pune/Deccan - Moderate N, Low P, High K, Alkaline)"
                apply_soil_preset()
            elif "bangalore" in loc_lower or "karnataka" in loc_lower or "mysore" in loc_lower or "chennai" in loc_lower:
                st.session_state["selected_preset_key"] = "Red Loamy Soil (e.g. Bangalore/South India - Moderate N, Low P, Low K, Acidic)"
                apply_soil_preset()
            elif "punjab" in loc_lower or "haryana" in loc_lower or "delhi" in loc_lower or "ganges" in loc_lower or "up" in loc_lower:
                st.session_state["selected_preset_key"] = "Alluvial Soil (e.g. Ganges Plain/North India - Fertile, High N/P/K, Neutral)"
                apply_soil_preset()
            elif "rajasthan" in loc_lower or "thar" in loc_lower or "arid" in loc_lower:
                st.session_state["selected_preset_key"] = "Sandy Soil (e.g. Rajasthan/Arid regions - Low N/P/K, Alkaline, Low rain)"
                apply_soil_preset()
            elif "kerala" in loc_lower or "cochin" in loc_lower or "marsh" in loc_lower:
                st.session_state["selected_preset_key"] = "Peaty Soil (e.g. Kerala - High Organic N, Low P/K, Highly Acidic)"
                apply_soil_preset()
        else:
            st.error("Failed to retrieve weather. Please check city spelling or custom API key.")
            
    # Display Weather Widget if loaded
    if "weather_details" in st.session_state and location:
        w = st.session_state["weather_details"]
        weather_html = f"""
        <div class="glass-card" style="margin-top: 10px; margin-bottom: 25px; border-left: 5px solid #16a34a;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; font-family: 'Outfit'; color: #0f172a;">Weather in {w['city_name']}</h4>
                    <p style="margin: 0; color: #475569; font-size: 0.9rem;">Condition: <b>{w['description']}</b></p>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 2.2rem; font-weight: 800; font-family: 'Outfit'; color: #16a34a;">{w['temp']}°C</span>
                </div>
            </div>
            <div style="display: flex; gap: 40px; margin-top: 15px; border-top: 1px solid #e2e8f0; padding-top: 12px;">
                <div>
                    <span style="color: #475569; font-size: 0.8rem; letter-spacing: 0.05em; font-weight: 600;">HUMIDITY</span><br>
                    <span style="font-weight: 600; color: #0f172a; font-size: 1.1rem;">{w['humidity']}%</span>
                </div>
                <div>
                    <span style="color: #475569; font-size: 0.8rem; letter-spacing: 0.05em; font-weight: 600;">WIND SPEED</span><br>
                    <span style="font-weight: 600; color: #0f172a; font-size: 1.1rem;">{w['wind_speed']} m/s</span>
                </div>
            </div>
        </div>
        """
        st.markdown(weather_html, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

    # Preset Selector Box
    st.markdown("<div class='glass-card'><h3 class='card-title'>Typical Soil Presets (Quick Fill)</h3>", unsafe_allow_html=True)
    st.selectbox(
        "Select a soil type to automatically fill typical measurements",
        options=list(SOIL_PRESETS.keys()),
        key="selected_preset_key",
        on_change=apply_soil_preset
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Form parameters
    st.markdown("<div class='glass-card'><h3 class='card-title'>Soil and Weather Measurements</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    with c1:
        n = st.number_input("Nitrogen (N) - mg/kg", min_value=0, max_value=200, key="n_input", help="Nitrogen ratio in soil")
        p = st.number_input("Phosphorus (P) - mg/kg", min_value=0, max_value=200, key="p_input", help="Phosphorus ratio in soil")
        k = st.number_input("Potassium (K) - mg/kg", min_value=0, max_value=200, key="k_input", help="Potassium ratio in soil")
        ph = st.number_input("Soil pH", min_value=1.0, max_value=14.0, step=0.1, key="ph_input", help="Acidity or basicity of soil")
        
    with c2:
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=0.0,
            max_value=50.0,
            step=0.1,
            key="temp_input"
        )
        humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="humidity_input"
        )
        rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=500.0, step=1.0, key="rain_input")
        
    st.write("")
    recommend_btn = st.button("Find Recommended Crop")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Recommendation Logic
    if recommend_btn:
        if not active_model:
            st.error("No prediction model loaded. Please verify features or training state.")
        else:
            data = np.array([[n, p, k, temperature, humidity, ph, rainfall]])
            crop = active_model.predict(data)[0]
            probability = active_model.predict_proba(data)
            confidence = round(np.max(probability) * 100, 2)
            
            # Save to Database with advanced parameters
            save_history(location if location else "Unknown Location", n, p, k, temperature, humidity, ph, rainfall, crop, confidence, selected_model_name)
            
            # Diagnostics
            diag = diagnose_soil(n, p, k, ph)
            crop_profile = CROP_PROFILES.get(crop.lower().strip(), {})
            
            # Custom Metric Cards
            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-box" style="border-top: 4px solid #16a34a;">
                    <div class="metric-value" style="color: #16a34a;">{crop.upper()}</div>
                    <div class="metric-label">Best Crop to Plant</div>
                </div>
                <div class="metric-box" style="border-top: 4px solid #0284c7;">
                    <div class="metric-value" style="color: #0284c7;">{confidence}%</div>
                    <div class="metric-label">Match Confidence</div>
                </div>
                <div class="metric-box" style="border-top: 4px solid {diag['rating_color']};">
                    <div class="metric-value" style="color: {diag['rating_color']};">{diag['score']}/100</div>
                    <div class="metric-label">Soil Condition ({diag['rating']})</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Split Results Layout
            col_res1, col_res2 = st.columns([1, 1])
            
            with col_res1:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 5px solid {diag['ph_color']};">
                    <div class="card-title">Soil Status Report</div>
                    <p style="color: {diag['ph_color']}; font-weight: 800; font-size: 1.1rem; margin-bottom: 2px;">{diag['ph_class']}</p>
                    <p style="color: #475569; font-size: 0.9rem; margin-bottom: 12px;">{diag['ph_desc']}</p>
                    <p style="font-weight: 600; color: #0f172a; margin-bottom: 2px; font-size: 0.95rem;">Recommended Treatment:</p>
                    <p style="color: #334155; font-size: 0.9rem;">{diag['ph_action']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if diag["warnings"]:
                    st.warning("Nutrient Warnings:\n" + "\n".join([f"- {w}" for w in diag["warnings"]]))
                    
                st.subheader("Fertilizer Recommendations")
                fert_advice = recommend_fertilizers_for_crop(crop, n, p, k)
                for advice_item in fert_advice:
                    st.info(advice_item)
                    
            with col_res2:
                # Crop Profile Metadata Display
                st.markdown(f"""
                <div class="glass-card" style="border-left: 5px solid #0284c7;">
                    <div class="card-title">{crop.capitalize()} Crop Guide</div>
                    <table style="width:100%; font-size:0.9rem; color:#334155;">
                        <tr style="border-bottom: 1px solid #edf2f7;"><td style="padding:6px 0; font-weight:600; color:#475569;">Best Season</td><td style="text-align:right; font-weight:bold; color:#0f172a;">{crop_profile.get('season', 'N/A')}</td></tr>
                        <tr style="border-bottom: 1px solid #edf2f7;"><td style="padding:6px 0; font-weight:600; color:#475569;">Time to Harvest</td><td style="text-align:right; font-weight:bold; color:#0f172a;">{crop_profile.get('duration', 'N/A')}</td></tr>
                        <tr style="border-bottom: 1px solid #edf2f7;"><td style="padding:6px 0; font-weight:600; color:#475569;">Water Needed</td><td style="text-align:right; font-weight:bold; color:#0f172a;">{crop_profile.get('water', 'N/A')}</td></tr>
                        <tr style="border-bottom: 1px solid #edf2f7;"><td style="padding:6px 0; font-weight:600; color:#475569;">Market Demand</td><td style="text-align:right; font-weight:bold; color:#0f172a;"><span class="badge" style="background:#f0fdf4; border-color:#dcfce7; color:#16a34a;">{crop_profile.get('demand', 'N/A')}</span></td></tr>
                    </table>
                    <p style="margin-top:12px; font-weight:600; color:#0f172a; font-size:0.95rem;">Success Tips for Farmers:</p>
                    <p style="color:#475569; font-size:0.85rem; line-height:1.4;">{crop_profile.get('tips', 'No specific tips.')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Gauge Chart for Suitability score
                fig_gauge = get_gauge_chart(diag['score'], diag['rating'], diag['rating_color'])
                st.plotly_chart(fig_gauge, use_container_width=True)

            # Interactive Radar and Alternative Crops
            st.markdown("---")
            col_v1, col_v2 = st.columns([1, 1])
            
            with col_v1:
                st.subheader("Soil Nutrient Analysis")
                fig_radar = get_radar_chart(crop, n, p, k)
                st.plotly_chart(fig_radar, use_container_width=True)
                
            with col_v2:
                st.subheader("Other Suitable Crops")
                crops_list = active_model.classes_
                scores = probability[0] * 100
                rank = pd.DataFrame({"Crop": crops_list, "Suitability (%)": scores})
                rank = rank.sort_values(by="Suitability (%)", ascending=False).head(5)
                
                fig_bar = px.bar(
                    rank,
                    x="Suitability (%)",
                    y="Crop",
                    orientation="h",
                    color="Crop",
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    height=280
                )
                fig_bar.update_layout(
                    yaxis={'categoryorder':'total ascending'},
                    showlegend=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#334155'),
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                
            # Download Professional HTML Report Section
            report_html = generate_html_report(
                location or "Unknown Location",
                crop,
                confidence,
                diag,
                n, p, k, ph,
                temperature, humidity, rainfall,
                fert_advice,
                crop_profile
            )
            st.download_button(
                "Download Advice Report (HTML)",
                report_html,
                "crop_advisor_report.html",
                "text/html"
            )

# ----------------- PAGE 2: WHAT-IF SIMULATOR -----------------
elif page == "Interactive Simulator":
    st.header("Crop Growth Simulator")
    st.write("Adjust soil and weather values to see how recommendations change in real-time.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Adjust Soil & Weather")
        sim_n = st.slider("Nitrogen (N) - mg/kg", 0, 200, 50, key="sim_n")
        sim_p = st.slider("Phosphorus (P) - mg/kg", 5, 200, 50, key="sim_p")
        sim_k = st.slider("Potassium (K) - mg/kg", 5, 200, 50, key="sim_k")
        sim_temp = st.slider("Temperature (°C)", 8.0, 45.0, 25.0, step=0.5, key="sim_temp")
        sim_hum = st.slider("Humidity (%)", 14.0, 100.0, 60.0, step=0.5, key="sim_hum")
        sim_ph = st.slider("Soil pH", 3.5, 9.9, 6.5, step=0.1, key="sim_ph")
        sim_rain = st.slider("Rainfall (mm)", 20.0, 400.0, 100.0, step=1.0, key="sim_rain")
        
    with col2:
        if not active_model:
            st.error("No prediction model loaded. Check configuration.")
        else:
            st.subheader("Prediction Results")
            sim_data = np.array([[sim_n, sim_p, sim_k, sim_temp, sim_hum, sim_ph, sim_rain]])
            
            sim_crop = active_model.predict(sim_data)[0]
            sim_probs = active_model.predict_proba(sim_data)[0] * 100
            sim_classes = active_model.classes_
            
            sim_df = pd.DataFrame({"Crop": sim_classes, "Probability (%)": sim_probs})
            sim_df = sim_df.sort_values("Probability (%)", ascending=False).head(5)
            
            st.success(f"Recommended Crop: **{sim_crop.upper()}**")
            st.write(f"Confidence score: **{round(sim_df.iloc[0]['Probability (%)'], 2)}%** (Model: {selected_model_name})")
            
            fig_sim = px.bar(
                sim_df,
                x="Probability (%)",
                y="Crop",
                orientation="h",
                color="Crop",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                title="Top 5 Suitable Crops",
                height=260
            )
            fig_sim.update_layout(
                yaxis={'categoryorder':'total ascending'}, 
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#334155')
            )
            st.plotly_chart(fig_sim, use_container_width=True)
            
            # Radar chart and quick soil stats
            fig_radar_sim = get_radar_chart(sim_crop, sim_n, sim_p, sim_k)
            st.plotly_chart(fig_radar_sim, use_container_width=True)
            
            diag = diagnose_soil(sim_n, sim_p, sim_k, sim_ph)
            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid {diag['ph_color']}; margin-top:10px;">
                <h4 style="margin: 0; font-family: 'Outfit';">Soil Condition: <span style="color:{diag['rating_color']}">{diag['score']}/100 ({diag['rating']})</span></h4>
                <p style="margin-top: 5px; color:#475569; font-size: 0.9rem;">pH Condition: <b>{diag['ph_class']}</b> ({diag['ph_desc']})</p>
            </div>
            """, unsafe_allow_html=True)

# ----------------- PAGE 3: DATA INSIGHTS -----------------
elif page == "Dataset Insights":
    st.header("Interactive Crop & Soil Data Explorer")
    st.write("Explore patterns, relationships, and distributions within the Crop Recommendation dataset.")
    
    try:
        df_csv = pd.read_csv("Crop_recommendation.csv")
        
        tab1, tab2, tab3 = st.tabs(["Dataset Viewer", "Feature Correlations", "Class Distributions"])
        
        with tab1:
            st.subheader("Filter & Inspect Records")
            selected_crop_filter = st.multiselect("Select Crops to Filter:", options=list(df_csv['label'].unique()), default=["rice", "maize", "cotton"])
            
            filtered_df = df_csv[df_csv['label'].isin(selected_crop_filter)] if selected_crop_filter else df_csv
            st.dataframe(filtered_df, use_container_width=True)
            
            # Download filtered data
            csv_data = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Filtered Data (CSV)",
                data=csv_data,
                file_name="filtered_crop_data.csv",
                mime="text/csv"
            )
            
        with tab2:
            st.subheader("Feature Correlation Matrix")
            st.write("Inspect how numeric dimensions interact linearly with one another.")
            corr = df_csv.drop('label', axis=1).corr()
            fig_corr = px.imshow(
                corr,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale="Viridis",
                title="Correlation Heatmap of Agricultural Metrics"
            )
            fig_corr.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#334155')
            )
            st.plotly_chart(fig_corr, use_container_width=True)
            
        with tab3:
            st.subheader("Nutrient & Climate Range distribution")
            selected_feature = st.selectbox("Select Attribute for Distribution Analysis:", options=["N", "P", "K", "temperature", "humidity", "ph", "rainfall"])
            
            fig_dist = px.box(
                df_csv,
                x="label",
                y=selected_feature,
                color="label",
                title=f"Spread of {selected_feature} across various Crop Types"
            )
            fig_dist.update_layout(
                xaxis={'categoryorder':'total ascending'},
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#334155')
            )
            st.plotly_chart(fig_dist, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error loading Crop_recommendation.csv: {e}")

# ----------------- PAGE 4: AGRI-ADVISOR CHATBOT -----------------
elif page == "Ask Advisor Chat":
    st.header("Ask Advisor Chat")
    st.write("Ask questions about soil chemistry, fertilizing, crop growth, or pH adjustments.")
    
    # Initialize Chat History
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am your AI Agri-Advisor. Ask me agronomic questions like 'What fertilizer raises nitrogen?' or 'Tell me about coffee crop'."}
        ]
        
    # Render messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # Process User Input
    user_msg = st.chat_input("Enter your agriculture question...")
    
    if user_msg:
        # Save user message
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.write(user_msg)
            
        # Advisor responses logic
        msg_lower = user_msg.lower().strip()
        response = ""
        
        # Check Crop Names
        matched_crop = None
        for crop_key in CROP_PROFILES.keys():
            if crop_key in msg_lower:
                matched_crop = crop_key
                break
                
        if "nitrogen" in msg_lower or " n " in msg_lower or "deficit n" in msg_lower:
            response = ("**Nitrogen (N) Advice**:\n"
                        "- Nitrogen is vital for vegetative leaf growth. Deficiency shows as yellowing of leaves starting from the bottom.\n"
                        "- Chemical solution: Urea (46% N) is the fastest corrector. Standard dose is around 40-50 kg/acre depending on crop.\n"
                        "- Organic solution: High-quality compost, poultry manure, or leguminous crop rotation (cowpea, blackgram).")
        elif "phosphorus" in msg_lower or " p " in msg_lower or "deficit p" in msg_lower:
            response = ("**Phosphorus (P) Advice**:\n"
                        "- Phosphorus fuels root development and blooming. Deficiencies lead to stunted roots and purplish/dark-green leaf tips.\n"
                        "- Chemical solution: DAP (Diammonium Phosphate) or SSP (Single Superphosphate).\n"
                        "- Organic solution: Rock phosphate, bone meal, or mycorrhizal soil inoculants.")
        elif "potassium" in msg_lower or " k " in msg_lower or "deficit k" in msg_lower:
            response = ("**Potassium (K) Advice**:\n"
                        "- Potassium controls water regulation, stomatal opening, and builds disease resistance. Deficiencies present as scorched/brown leaf edges.\n"
                        "- Chemical solution: MOP (Muriate of Potash) or Potassium Sulfate.\n"
                        "- Organic solution: Wood ash (contains potash), seaweed extract, or greensand.")
        elif "ph" in msg_lower or "acidic" in msg_lower or "alkaline" in msg_lower:
            response = ("**Soil pH & Acidity/Alkalinity Guidance**:\n"
                        "- Acidic Soil (pH < 5.5): Nutrient uptake gets blocked. Correct by applying agricultural lime (Calcium Carbonate) or Dolomite.\n"
                        "- Alkaline Soil (pH > 7.5): Micronutrients like iron and zinc lock up. Correct by applying Elemental Sulfur or Gypsum, or adding acidic organic mulch.")
        elif matched_crop:
            profile = CROP_PROFILES[matched_crop]
            response = (f"**Crop Profile: {matched_crop.upper()}**\n"
                        f"- Best Planting Season: {profile['season']}\n"
                        f"- Growth Cycle Duration: {profile['duration']}\n"
                        f"- Irrigation Level: {profile['water']}\n"
                        f"- Market Demand Tier: {profile['demand']}\n"
                        f"- Agronomy Success Tips: {profile['tips']}")
        elif "hi" in msg_lower or "hello" in msg_lower or "hey" in msg_lower:
            response = "Greetings! I am here to assist with your agricultural calculations. Ask me about NPK, soil pH, fertilizer correction dosages, or crop characteristics."
        else:
            response = ("I'm here to support. You can ask me questions about:\n"
                        "1. Nutrient elements (Nitrogen, Phosphorus, Potassium)\n"
                        "2. Soil pH balance (Acidic, Alkaline correction)\n"
                        "3. Specific crop specifications (e.g., 'Tell me about cotton')\n"
                        "4. Fertilizer calculations and deficiencies.")
                        
        # Save and render assistant response
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

# ----------------- PAGE 5: DIAGNOSTIC LOGS -----------------
elif page == "Saved Records Logs":
    st.header("Saved Records Logs")
    st.write("Browse, query, and manage historical recommendation records.")
    
    try:
        # Load detailed logs from db
        conn = sqlite3.connect("history.db")
        history = pd.read_sql("SELECT * FROM recommendations ORDER BY timestamp DESC", conn)
        conn.close()
        
        if history.empty:
            st.info("No recommendation diagnostics found. Generate recommendations to populate history.")
        else:
            # Record metrics
            st.subheader("Log Records Summary")
            col_l1, col_l2, col_l3 = st.columns(3)
            with col_l1:
                st.metric("Total Records Saved", len(history))
            with col_l2:
                top_crop = history['crop'].mode()[0].upper() if not history['crop'].empty else "N/A"
                st.metric("Most Recommended Crop", top_crop)
            with col_l3:
                avg_confidence = round(history['confidence'].mean(), 2) if not history['confidence'].empty else 0.0
                st.metric("Average Suitability", f"{avg_confidence}%")
                
            # Filters
            st.subheader("Search and Filter logs")
            cf1, cf2 = st.columns(2)
            with cf1:
                search_city = st.text_input("Filter by Location Name:", value="", placeholder="e.g. Pune")
            with cf2:
                unique_crops = list(history['crop'].unique())
                filter_crop = st.multiselect("Filter by Crop:", options=unique_crops, default=[])
                
            filtered = history
            if search_city:
                filtered = filtered[filtered['location'].str.contains(search_city, case=False, na=False)]
            if filter_crop:
                filtered = filtered[filtered['crop'].isin(filter_crop)]
                
            st.dataframe(filtered, use_container_width=True)
            
            # Export
            log_csv = filtered.to_csv(index=False).encode('utf-8')
            st.download_button("Export Selected Logs (CSV)", log_csv, "agriculture_logs.csv", "text/csv")
            
            # Management options
            st.markdown("---")
            st.subheader("Record Retention Management")
            
            col_d1, col_d2 = st.columns([2, 1])
            with col_d1:
                selected_id = st.selectbox(
                    "Select specific Record ID to delete:",
                    options=list(filtered['id'].values) if not filtered.empty else []
                )
            with col_d2:
                st.markdown("<div class='spacer-label'></div>", unsafe_allow_html=True)
                delete_btn = st.button("Delete Selected Record")
                
            if delete_btn and selected_id:
                delete_history_entry(int(selected_id))
                st.success(f"Record #{selected_id} deleted successfully.")
                st.rerun()
                
            if st.button("Clear All Diagnostic Logs"):
                clear_all_history()
                st.success("Diagnostic history database successfully cleared.")
                st.rerun()
                
    except Exception as e:
        st.error(f"Error fetching SQLite database logs: {e}")

# ----------------- PAGE 6: ENGINE & MODEL ANALYTICS -----------------
elif page == "System Details":
    st.header("System Details & Model Accuracy")
    st.write("Compare model parameters and check accuracy metrics of different classifiers.")
    
    try:
        with open("model_results.pkl", "rb") as f:
            model_results = pickle.load(f)
            
        res_df = pd.DataFrame({
            "Algorithm": list(model_results.keys()),
            "Accuracy (%)": list(model_results.values())
        }).sort_values("Accuracy (%)", ascending=False)
        
        fig = px.bar(
            res_df,
            x="Accuracy (%)",
            y="Algorithm",
            orientation="h",
            color="Algorithm",
            text="Accuracy (%)",
            color_discrete_sequence=px.colors.qualitative.Vivid,
            height=280
        )
        fig.update_layout(
            xaxis_range=[85, 100],
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#334155')
        )
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Model Validation Specifics")
        st.dataframe(res_df, use_container_width=True)
        
        st.markdown(f"""
        <div class="glass-card">
            <h4 style="margin-top:0; font-family:'Outfit'; color:#0f172a;">Active Prediction Engine: {selected_model_name}</h4>
            <p style="font-size:0.9rem; color:#334155;">The system is configured with 5 classification classifiers. If Naive Bayes or Random Forest is active, it represents optimal classification splits. Toggling models in the sidebar updates recommendations dynamically.</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading model training diagnostics: {e}")
        
    st.markdown("""
    <div class="glass-card">
        <div class="card-title">Agri-AI Platform Specifications</div>
        <ul style="font-size:0.9rem; color:#334155;">
            <li><b>User Interface:</b> Streamlit Core with Custom Glassmorphism</li>
            <li><b>Data Utilities:</b> Pandas, NumPy, Scikit-Learn</li>
            <li><b>Visualizations:</b> Plotly Radar, Gauge, Bar, Heatmaps</li>
            <li><b>Databases:</b> SQLite3 Local Logs Storage</li>
            <li><b>Weather Integration:</b> OpenWeather Map APIs</li>
            <li><b>Model Types:</b> Naive Bayes, Random Forest, Decision Tree, KNN, SVM</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)