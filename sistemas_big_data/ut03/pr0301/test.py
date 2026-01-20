
import pandas as pd

df = pd.read_csv("./ventas_norte.csv", sep=";", dtype={"Cantidad_Vendida": int, "Precio_Unit": int, "Nom_Producto": str}, parse_dates=["Fecha_Venta"], index_col="ID_Transaccion")