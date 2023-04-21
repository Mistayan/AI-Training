import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

print("Loading dataset")
data = pd.read_csv("../../csv/ex1-2.csv")
print(data)
x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values
print(y)
print()

print(f"Data visualisation head :\n{data.head()}")
print(f"Visualisation of data's shape :\n{data.shape}")

print("\nDividing dataset for learning and tests")
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
classifier = SVC(kernel='linear')  # Instantiate SVC Model
print(x_train)
print(y_train)
classifier.fit(x_train, y_train)  # TRAIN

print(x_test)
y_pred = classifier.predict(x_test)
print(f"Predictions on dataset :\n{y_pred}")

print(f"Confusion Matrice :\n{confusion_matrix(y_test, y_pred)}")
print(classification_report(y_test, y_pred))


def test():
    ...
