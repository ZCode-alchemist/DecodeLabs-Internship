# Project 2: Data Classification Using AI
# Dataset used: Iris flower dataset (built into scikit-learn)
# - 150 samples, 4 features (sepal/petal length & width), 3 classes (species)
# - Great for a first classification project: clean, small, no missing data


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ------Load and understand the dataset-----------------------------------

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df["species"] = iris.target
df["species_name"] = df["species"].map(dict(enumerate(iris.target_names)))

print("=" * 60)
print("STEP 1: DATASET OVERVIEW")
print("=" * 60)
print(f"\nShape: {df.shape[0]} rows, {df.shape[1]} columns")
print("\nFirst 5 rows:")
print(df.head())
print("\nClass distribution:")
print(df["species_name"].value_counts())
print("\nSummary statistics:")
print(df.describe())

# -----Split data into training and testing sets---------------------------------

X = df[iris.feature_names]
y = df["species"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # 80% train, 20% test
    random_state=42,    # reproducibility
    stratify=y          # keep class balance in both sets
)

print("\n" + "=" * 60)
print("STEP 2: TRAIN/TEST SPLIT")
print("=" * 60)
print(f"Training samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ------Applying a simple classification algorithm-----------------------------------

model = LogisticRegression(max_iter=200)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)

print("\n" + "=" * 60)
print("STEP 3: MODEL TRAINING & EVALUATION")
print("=" * 60)
acc = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {acc:.2%}")
print("\nClassification report:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# -----Visualize results-----------------------------------

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Greens",
            xticklabels=iris.target_names, yticklabels=iris.target_names)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=150)
print("\nConfusion matrix saved as confusion_matrix.png")

# -------Trying a prediction on a new sample-----------------------------------

sample = [[5.1, 3.5, 1.4, 0.2]]
sample_scaled = scaler.transform(sample)
prediction = model.predict(sample_scaled)
print(f"\nExample prediction for {sample[0]}: {iris.target_names[prediction[0]]}")
