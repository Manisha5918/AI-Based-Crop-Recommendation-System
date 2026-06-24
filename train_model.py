import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB


data = pd.read_csv(
    "Crop_recommendation.csv"
)


X = data.drop(
    "label",
    axis=1
)

y = data["label"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


models = {

    "Random Forest":
    RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ),

    "Decision Tree":
    DecisionTreeClassifier(),

    "KNN":
    KNeighborsClassifier(),

    "SVM":
    SVC(
        probability=True
    ),

    "Naive Bayes":
    GaussianNB()

}


results = {}


best_accuracy = 0

best_model = None

best_name = ""


for name,model in models.items():


    model.fit(
        X_train,
        y_train
    )


    prediction=model.predict(
        X_test
    )


    accuracy=accuracy_score(
        y_test,
        prediction
    )


    results[name]=accuracy*100



    if accuracy>best_accuracy:


        best_accuracy=accuracy

        best_model=model

        best_name=name



pickle.dump(
    best_model,
    open(
        "crop_model.pkl",
        "wb"
    )
)


pickle.dump(
    results,
    open(
        "model_results.pkl",
        "wb"
    )
)


pickle.dump(
    list(X.columns),
    open(
        "features.pkl",
        "wb"
    )
)


print(
    "Best Model:",
    best_name
)


print(
    "Accuracy:",
    best_accuracy*100
)


print(
    "Training Completed"
)