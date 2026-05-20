import joblib

modelo = joblib.load("modelo_intencion.pkl")

print("IA Veterinaria iniciada")
print("Escribe 'salir' para terminar\n")

while True:

    texto = input("Cliente: ")

    if texto.lower() == "salir":
        break

    prediccion = modelo.predict([texto])[0]

    print("IA detectó:", prediccion)
    print()