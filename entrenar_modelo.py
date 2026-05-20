import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

# Cargar dataset
df = pd.read_csv("dataset_veterinaria.csv")

X = df["texto"]
y = df["intencion"]

# Separar entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# Modelos a comparar
modelos = {
    "Naive Bayes": MultinomialNB(),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "SVM": LinearSVC()
}

resultados = {}

mejor_modelo = None
mejor_nombre = ""
mejor_accuracy = 0

# Entrenar y evaluar modelos
for nombre, clasificador in modelos.items():
    modelo = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
        ("clasificador", clasificador)
    ])

    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    resultados[nombre] = accuracy

    print("\n==============================")
    print(f"Modelo: {nombre}")
    print("==============================")
    print(f"Accuracy: {accuracy:.2f}")
    print(classification_report(y_test, y_pred))

    if accuracy > mejor_accuracy:
        mejor_accuracy = accuracy
        mejor_modelo = modelo
        mejor_nombre = nombre
        mejor_pred = y_pred

# Gráfica de comparación
plt.figure(figsize=(8, 5))
plt.bar(resultados.keys(), resultados.values())
plt.title("Comparación de modelos de IA")
plt.xlabel("Modelo")
plt.ylabel("Accuracy")
plt.ylim(0, 1)

for i, valor in enumerate(resultados.values()):
    plt.text(i, valor + 0.02, f"{valor:.2f}", ha="center")

plt.tight_layout()
plt.show()

# Matriz de confusión del mejor modelo
cm = confusion_matrix(y_test, mejor_pred, labels=mejor_modelo.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=mejor_modelo.classes_)
disp.plot()
plt.title(f"Matriz de confusión - Mejor modelo: {mejor_nombre}")
plt.show()

# Guardar el mejor modelo
joblib.dump(mejor_modelo, "modelo_intencion.pkl")

print("\n==============================")
print("MEJOR MODELO")
print("==============================")
print(f"Modelo seleccionado: {mejor_nombre}")
print(f"Accuracy: {mejor_accuracy:.2f}")
print("Modelo guardado como modelo_intencion.pkl")