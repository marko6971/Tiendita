import pandas as pd

df_ventas = pd.read_csv("ventas.csv")

print("-"*30)
print("Encabezado")
print(df_ventas.head())
print("-"*30)
print("Informacion tipos de dato")
print(df_ventas.info())
print("-"*30)

ventas_altas = df_ventas[df_ventas["monto_total"]>10000]

print(ventas_altas)


ventas_totales = df_ventas["monto_total"].sum()
ventas_promedio = df_ventas["monto_total"].mean()
total_transacciones = df_ventas["id_venta"].count()

print(f"Ventas Totales: ${ventas_totales:2f}")
print(f"Ventas Promedio: ${ventas_promedio:2f}")
print(f"Total Transacciones: {total_transacciones}")
