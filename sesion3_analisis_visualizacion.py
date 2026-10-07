import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

# Credenciales PostgreSQL
conn_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'clima_agro',
    'user': 'postgres',
    'password': 'YLA_1522'
}

# Conectar a PostgreSQL
conn = psycopg2.connect(**conn_params)

# Leer datos desde PostgreSQL
query = "SELECT fecha, temperatura_2m, humedad_relativa_2m FROM lecturas ORDER BY fecha;"
df = pd.read_sql(query, conn)
conn.close()

# Filtrar valores inválidos (-999 representa datos faltantes)
df = df[(df['temperatura_2m'] > -999) & (df['humedad_relativa_2m'] > -999)].copy()

print("=" * 60)
print("SESIÓN 3: ANÁLISIS BÁSICO Y VISUALIZACIÓN DE DATOS")
print("=" * 60)

# 1. Mostrar primeros registros
print("\n1. PRIMEROS REGISTROS (df.head()):")
print(df.head(10))

# 2. Estadísticas descriptivas
print("\n2. ESTADÍSTICAS DESCRIPTIVAS (df.describe()):")
print(df.describe())

# 3. Encontrar días con mayor humedad
print("\n3. ANÁLISIS DE HUMEDAD:")
max_humedad_idx = df['humedad_relativa_2m'].idxmax()
max_humedad_row = df.loc[max_humedad_idx]
print(f"   Día con mayor humedad: {max_humedad_row['fecha']}")
print(f"   Humedad: {max_humedad_row['humedad_relativa_2m']}%")

# Top 5 días con mayor humedad
print("\n   Top 5 días con mayor humedad:")
top5_humedad = df.nlargest(5, 'humedad_relativa_2m')[['fecha', 'humedad_relativa_2m']]
for idx, (_, row) in enumerate(top5_humedad.iterrows(), 1):
    print(f"   {idx}. {row['fecha']}: {row['humedad_relativa_2m']}%")

# 4. Correlación entre temperatura y humedad
print("\n4. CORRELACIÓN TEMPERATURA vs HUMEDAD:")
correlation, p_value = pearsonr(df['temperatura_2m'], df['humedad_relativa_2m'])
print(f"   Coeficiente de correlación de Pearson: {correlation:.4f}")
print(f"   P-value: {p_value:.2e}")

if correlation < 0:
    print(f"   Interpretación: Existe una CORRELACIÓN NEGATIVA de {abs(correlation):.4f}")
    print("   → A mayor temperatura, menor humedad (relación inversa)")
elif correlation > 0:
    print(f"   Interpretación: Existe una CORRELACIÓN POSITIVA de {correlation:.4f}")
    print("   → A mayor temperatura, mayor humedad")
else:
    print("   No hay correlación entre temperatura y humedad")

# 5. Gráfico de líneas: Temperatura y Humedad por tiempo
print("\n5. GENERANDO GRÁFICOS...")

fig, axes = plt.subplots(3, 1, figsize=(14, 12))

# Gráfico 1: Temperatura
axes[0].plot(df['fecha'], df['temperatura_2m'], color='red', linewidth=1.5, label='Temperatura')
axes[0].set_ylabel('Temperatura (°C)', fontsize=11, fontweight='bold')
axes[0].set_title('Temperatura a 2 metros - Serie Temporal', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3)
axes[0].legend()

# Gráfico 2: Humedad Relativa
axes[1].plot(df['fecha'], df['humedad_relativa_2m'], color='blue', linewidth=1.5, label='Humedad Relativa')
axes[1].set_ylabel('Humedad Relativa (%)', fontsize=11, fontweight='bold')
axes[1].set_title('Humedad Relativa a 2 metros - Serie Temporal', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3)
axes[1].legend()

# Gráfico 3: Scatter plot de correlación
axes[2].scatter(df['temperatura_2m'], df['humedad_relativa_2m'], alpha=0.5, color='green')
# Agregar línea de tendencia
z = np.polyfit(df['temperatura_2m'], df['humedad_relativa_2m'], 1)
p = np.poly1d(z)
axes[2].plot(df['temperatura_2m'], p(df['temperatura_2m']), "r--", linewidth=2, label='Línea de tendencia')
axes[2].set_xlabel('Temperatura (°C)', fontsize=11, fontweight='bold')
axes[2].set_ylabel('Humedad Relativa (%)', fontsize=11, fontweight='bold')
axes[2].set_title(f'Correlación Temperatura vs Humedad (r={correlation:.4f})', fontsize=12, fontweight='bold')
axes[2].grid(True, alpha=0.3)
axes[2].legend()

plt.tight_layout()
plt.savefig('analisis_clima_agro.png', dpi=300, bbox_inches='tight')
print("   ✓ Gráficos guardados en 'analisis_clima_agro.png'")
plt.show()

print("\n" + "=" * 60)
print("ANÁLISIS COMPLETADO")
print("=" * 60)
