import psycopg2
import pandas as pd
from datetime import datetime, timedelta

conn_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'clima_agro',
    'user': 'postgres',
    'password': 'YLA_1522'
}

conn = psycopg2.connect(**conn_params)
cursor = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS lecturas (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    temperatura_2m DECIMAL(5, 2),
    humedad_relativa_2m DECIMAL(5, 2),
    UNIQUE(fecha)
);
"""

cursor.execute(create_table_query)
conn.commit()
print("✓ Tabla 'lecturas' creada exitosamente")

df = pd.read_csv('datos_guayas.csv', skiprows=10)

df.columns = df.columns.str.strip()

df = df[['YEAR', 'DOY', 'T2M', 'RH2M']].copy()

df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce')
df['DOY'] = pd.to_numeric(df['DOY'], errors='coerce')
df['T2M'] = pd.to_numeric(df['T2M'], errors='coerce')
df['RH2M'] = pd.to_numeric(df['RH2M'], errors='coerce')

df = df.dropna()

def doy_to_date(year, doy):
    return datetime(int(year), 1, 1) + timedelta(days=int(doy) - 1)

df['fecha'] = df.apply(lambda row: doy_to_date(row['YEAR'], row['DOY']), axis=1)

insert_query = """
INSERT INTO lecturas (fecha, temperatura_2m, humedad_relativa_2m)
VALUES (%s, %s, %s)
ON CONFLICT (fecha) DO NOTHING;
"""

for _, row in df.iterrows():
    cursor.execute(insert_query, (row['fecha'], row['T2M'], row['RH2M']))

conn.commit()
print(f"✓ {len(df)} registros insertados en la tabla 'lecturas'")

cursor.close()
conn.close()
print("✓ Conexión cerrada")