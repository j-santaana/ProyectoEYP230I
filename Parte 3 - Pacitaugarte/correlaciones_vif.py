import pandas as pd
from pathlib import Path

proyecto = Path(__file__).resolve().parent.parent
carpeta_salida = Path(__file__).resolve().parent

ruta = proyecto / "Parte 1 - j-santaana" / "Base de datos procesada" / "energydata_limpio.csv"

df = pd.read_csv(ruta)

print("Dimensiones:", df.shape)
print("\nColumnas disponibles:")
print(df.columns.tolist())


import matplotlib.pyplot as plt
import seaborn as sns

predictores = df.drop(
    columns=["date", "Appliances", "lights"]
)

correlaciones = predictores.corr()

plt.figure(figsize=(14, 11))

sns.heatmap(
    correlaciones,
    cmap="coolwarm",
    center=0,
    vmin=-1,
    vmax=1,
    annot=False
)

plt.title("Matriz de correlaciones entre predictores")
plt.tight_layout()

plt.savefig(
    carpeta_salida / "mapa_correlaciones.png",
    dpi=300
)

plt.close()

import numpy as np

mascara = np.triu(
    np.ones(correlaciones.shape, dtype=bool),
    k=1
)

pares = correlaciones.where(mascara).stack()

pares = pares.reindex(
    pares.abs().sort_values(ascending=False).index
)

print("\nLas 15 correlaciones más fuertes:")
print(pares.head(15))


from statsmodels.stats.outliers_influence import (
    variance_inflation_factor
)
import statsmodels.api as sm

# Agregar intercepto a la matriz de predictores
X = sm.add_constant(predictores)

# Calcular VIF
tabla_vif = pd.DataFrame({
    "Variable": X.columns,
    "VIF": [
        variance_inflation_factor(X.values, i)
        for i in range(X.shape[1])
    ]
})

# Excluir el intercepto
tabla_vif = tabla_vif[
    tabla_vif["Variable"] != "const"
]

# Ordenar de mayor a menor
tabla_vif = tabla_vif.sort_values(
    "VIF", ascending=False
)

print("\nTabla de VIF:")
print(tabla_vif.to_string(index=False))

# VIF de un conjunto reducido

# No representa una selección definitiva !!!!!
variables_prueba = [
    "T1",
    "RH_1",
    "T_out",
    "RH_out",
    "Press_mm_hg",
    "Windspeed",
    "Visibility"
]

X_reducido = sm.add_constant(
    df[variables_prueba]
)

# Calcular VIF
vif_reducido = pd.DataFrame({
    "Variable": X_reducido.columns,
    "VIF": [
        variance_inflation_factor(
            X_reducido.values, i
        )
        for i in range(X_reducido.shape[1])
    ]
})


# Excluir el intercepto del VIF reducido
vif_reducido = vif_reducido[
    vif_reducido["Variable"] != "const"
]

# Ordenar de mayor a menor
vif_reducido = vif_reducido.sort_values(
    "VIF", ascending=False
)

# Mostrar resultados
print("\nVIF del conjunto reducido:")
print(vif_reducido.to_string(index=False))

# Guardar VIF completo
tabla_vif.to_csv(
    carpeta_salida / "tabla_vif.csv",
    index=False
)

# Guardar VIF reducido
vif_reducido.to_csv(
    carpeta_salida / "vif_reducido.csv",
    index=False
)

# Guardar correlaciones más fuertes
pares.head(15).to_csv(
    carpeta_salida / "correlaciones_fuertes.csv",
    header=["Correlacion"]
)

print("\nArchivos guardados correctamente.")
