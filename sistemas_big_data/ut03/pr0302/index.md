# PR0302: Lectura avanzada de datos de archivos

## Ingesta de datos en archivos CSV


```python
import pandas as pd
import datetime
df_norte = pd.read_csv("./ventas_norte_v2.csv", sep=";", dtype={"ID_Pedido": str, "Direccion_Envio": str, "Producto": str, "Unidades": int, "Precio_Unitario": int})
df_norte["Total_Factura"] = df_norte["Total_Factura"].apply(lambda x: x.split("$")[1]).astype(float)
df_norte = df_norte.rename(columns={"ID_Pedido": "id_transaccion", "Fecha_Transaccion": "fecha", "Producto": "producto", "Unidades": "cantidad", "Total_Factura": "total_venta"})
df_norte = df_norte.drop(columns=["Precio_Unitario", "Cliente_Nombre", "Direccion_Envio", "Precio_Unitario"])
df_norte["region"] = "Norte"
df_norte["ciudad"] = "Madrid"
df_norte = df_norte.set_index("id_transaccion")
df_norte
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fecha</th>
      <th>producto</th>
      <th>cantidad</th>
      <th>total_venta</th>
      <th>region</th>
      <th>ciudad</th>
    </tr>
    <tr>
      <th>id_transaccion</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>N-1000</th>
      <td>2023-05-10 03:00:00</td>
      <td>Laptop Gamer</td>
      <td>1</td>
      <td>970.0</td>
      <td>Norte</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>N-1001</th>
      <td>2023-06-18 09:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>4</td>
      <td>3708.0</td>
      <td>Norte</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>N-1002</th>
      <td>2023-03-10 05:00:00</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>2820.0</td>
      <td>Norte</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>N-1003</th>
      <td>2023-05-10 03:00:00</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>2538.0</td>
      <td>Norte</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>N-1004</th>
      <td>2023-02-25 17:00:00</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>908.0</td>
      <td>Norte</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>N-1145</th>
      <td>2023-04-17 10:00:00</td>
      <td>Teclado Mecánico</td>
      <td>4</td>
      <td>4204.0</td>
      <td>Norte</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>N-1146</th>
      <td>2023-04-08 00:00:00</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>2458.0</td>
      <td>Norte</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>N-1147</th>
      <td>2023-02-01 22:00:00</td>
      <td>Monitor 4K</td>
      <td>1</td>
      <td>1040.0</td>
      <td>Norte</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>N-1148</th>
      <td>2023-06-13 03:00:00</td>
      <td>Laptop Gamer</td>
      <td>1</td>
      <td>297.0</td>
      <td>Norte</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>N-1149</th>
      <td>2023-02-24 01:00:00</td>
      <td>Monitor 4K</td>
      <td>1</td>
      <td>909.0</td>
      <td>Norte</td>
      <td>Madrid</td>
    </tr>
  </tbody>
</table>
<p>150 rows × 6 columns</p>
</div>



## Ingesta de datos en archivos Excel


```python
df_sur_both_pages = pd.read_excel("ventas_sur_v2.xlsx", sheet_name=None)
df_sur = pd.concat([df_sur_both_pages["Q1_2023"], df_sur_both_pages["Q2_2023"]])
df_sur["Cantidad"] = df_sur["Cantidad"].astype(int) 
df_sur["Precio_Base"] = df_sur["Precio_Base"].astype(float) 
df_sur["Descuento_Aplicado"] = df_sur["Descuento_Aplicado"].astype(float) 
df_sur["Es_Cliente_Corporativo"] = df_sur["Es_Cliente_Corporativo"].astype(bool) 
df_sur["Total"] = df_sur["Precio_Base"] * df_sur["Cantidad"] * (1 - df_sur["Descuento_Aplicado"])
df_sur
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Ref_Venta</th>
      <th>Fecha_Alta</th>
      <th>Articulo</th>
      <th>Cantidad</th>
      <th>Precio_Base</th>
      <th>Descuento_Aplicado</th>
      <th>Es_Cliente_Corporativo</th>
      <th>Estado_Envio</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>S-5000</td>
      <td>2023-02-11 00:00:00</td>
      <td>Webcam HD</td>
      <td>9</td>
      <td>425.12</td>
      <td>0.20</td>
      <td>False</td>
      <td>Enviado</td>
      <td>3060.864</td>
    </tr>
    <tr>
      <th>1</th>
      <td>S-5001</td>
      <td>2023-02-03 12:00:00</td>
      <td>Teclado Mecánico</td>
      <td>8</td>
      <td>599.60</td>
      <td>0.00</td>
      <td>True</td>
      <td>Devuelto</td>
      <td>4796.800</td>
    </tr>
    <tr>
      <th>2</th>
      <td>S-5002</td>
      <td>2023-04-06 07:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>6</td>
      <td>971.36</td>
      <td>0.00</td>
      <td>False</td>
      <td>Completado</td>
      <td>5828.160</td>
    </tr>
    <tr>
      <th>3</th>
      <td>S-5003</td>
      <td>2023-04-02 05:00:00</td>
      <td>Monitor 4K</td>
      <td>1</td>
      <td>799.66</td>
      <td>0.10</td>
      <td>True</td>
      <td>Pendiente</td>
      <td>719.694</td>
    </tr>
    <tr>
      <th>4</th>
      <td>S-5004</td>
      <td>2023-06-17 12:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>2</td>
      <td>619.99</td>
      <td>0.05</td>
      <td>True</td>
      <td>Devuelto</td>
      <td>1177.981</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>75</th>
      <td>S-5075</td>
      <td>2023-05-17 22:00:00</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>1150.01</td>
      <td>0.10</td>
      <td>False</td>
      <td>Enviado</td>
      <td>2070.018</td>
    </tr>
    <tr>
      <th>76</th>
      <td>S-5076</td>
      <td>2023-01-29 13:00:00</td>
      <td>Webcam HD</td>
      <td>1</td>
      <td>874.12</td>
      <td>0.10</td>
      <td>True</td>
      <td>Devuelto</td>
      <td>786.708</td>
    </tr>
    <tr>
      <th>77</th>
      <td>S-5077</td>
      <td>2023-06-09 11:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>1</td>
      <td>145.92</td>
      <td>0.00</td>
      <td>True</td>
      <td>Devuelto</td>
      <td>145.920</td>
    </tr>
    <tr>
      <th>78</th>
      <td>S-5078</td>
      <td>2023-02-07 13:00:00</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>1152.24</td>
      <td>0.00</td>
      <td>False</td>
      <td>Enviado</td>
      <td>2304.480</td>
    </tr>
    <tr>
      <th>79</th>
      <td>S-5079</td>
      <td>2023-05-01 11:00:00</td>
      <td>Docking Station</td>
      <td>7</td>
      <td>261.88</td>
      <td>0.10</td>
      <td>True</td>
      <td>Enviado</td>
      <td>1649.844</td>
    </tr>
  </tbody>
</table>
<p>160 rows × 9 columns</p>
</div>




```python
# Normalizacion para concatenacion posterior
df_sur = df_sur.drop(columns=["Precio_Base", "Descuento_Aplicado", "Es_Cliente_Corporativo", "Estado_Envio"])
df_sur = df_sur.rename(columns={"Ref_Venta": "id_transaccion", "Fecha_Alta": "fecha", "Articulo": "producto", "Cantidad": "cantidad", "Total": "total_venta"})
df_sur["region"] = "Sur"
df_sur["ciudad"] = "Madrid"
df_sur = df_sur.set_index("id_transaccion")
df_sur
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fecha</th>
      <th>producto</th>
      <th>cantidad</th>
      <th>total_venta</th>
      <th>region</th>
      <th>ciudad</th>
    </tr>
    <tr>
      <th>id_transaccion</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>S-5000</th>
      <td>2023-02-11 00:00:00</td>
      <td>Webcam HD</td>
      <td>9</td>
      <td>3060.864</td>
      <td>Sur</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>S-5001</th>
      <td>2023-02-03 12:00:00</td>
      <td>Teclado Mecánico</td>
      <td>8</td>
      <td>4796.800</td>
      <td>Sur</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>S-5002</th>
      <td>2023-04-06 07:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>6</td>
      <td>5828.160</td>
      <td>Sur</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>S-5003</th>
      <td>2023-04-02 05:00:00</td>
      <td>Monitor 4K</td>
      <td>1</td>
      <td>719.694</td>
      <td>Sur</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>S-5004</th>
      <td>2023-06-17 12:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>2</td>
      <td>1177.981</td>
      <td>Sur</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>S-5075</th>
      <td>2023-05-17 22:00:00</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>2070.018</td>
      <td>Sur</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>S-5076</th>
      <td>2023-01-29 13:00:00</td>
      <td>Webcam HD</td>
      <td>1</td>
      <td>786.708</td>
      <td>Sur</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>S-5077</th>
      <td>2023-06-09 11:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>1</td>
      <td>145.920</td>
      <td>Sur</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>S-5078</th>
      <td>2023-02-07 13:00:00</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>2304.480</td>
      <td>Sur</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>S-5079</th>
      <td>2023-05-01 11:00:00</td>
      <td>Docking Station</td>
      <td>7</td>
      <td>1649.844</td>
      <td>Sur</td>
      <td>Madrid</td>
    </tr>
  </tbody>
</table>
<p>160 rows × 6 columns</p>
</div>



## Ingesta de datos en archivos JSON


```python
import json
with open("ventas_este_v2.json") as f:
    data = json.load(f)
df_este = pd.json_normalize(data)
df_este = df_este[["data.id_registro", "data.payload.fecha_evento", "data.payload.comprador.ubicacion.ciudad", "data.payload.transaccion.detalles_producto.nombre_comercial", "data.payload.transaccion.cantidad_comprada", "data.payload.transaccion.detalles_producto.precio_lista", "data.payload.transaccion.detalles_producto.impuestos.monto_iva"]]
df_este = df_este.rename(columns={"data.id_registro": "id_transaccion", "data.payload.fecha_evento": "fecha", "data.payload.comprador.ubicacion.ciudad": "ciudad", "data.payload.transaccion.detalles_producto.nombre_comercial": "producto", "data.payload.transaccion.cantidad_comprada": "cantidad", "data.payload.transaccion.detalles_producto.precio_lista": "precio", "data.payload.transaccion.detalles_producto.impuestos.monto_iva": "iva"})
df_este["total_venta"] = (df_este["precio"] + df_este["iva"]) * df_este["cantidad"]
df_este = df_este.drop(columns=["precio", "iva"])
df_este["region"] = "Este"
df_este = df_este.set_index("id_transaccion")
df_este
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fecha</th>
      <th>ciudad</th>
      <th>producto</th>
      <th>cantidad</th>
      <th>total_venta</th>
      <th>region</th>
    </tr>
    <tr>
      <th>id_transaccion</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>E-8000</th>
      <td>2023-06-29 00:00:00</td>
      <td>Sevilla</td>
      <td>Monitor 4K</td>
      <td>1</td>
      <td>608.63</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>E-8001</th>
      <td>2023-04-12 00:00:00</td>
      <td>Sevilla</td>
      <td>Webcam HD</td>
      <td>1</td>
      <td>1357.62</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>E-8002</th>
      <td>2023-04-20 00:00:00</td>
      <td>Sevilla</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>2405.48</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>E-8003</th>
      <td>2023-04-14 00:00:00</td>
      <td>Madrid</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>3037.10</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>E-8004</th>
      <td>2023-01-03 00:00:00</td>
      <td>Sevilla</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>3528.36</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>E-8115</th>
      <td>2023-04-05 00:00:00</td>
      <td>Valencia</td>
      <td>Monitor 4K</td>
      <td>1</td>
      <td>1003.09</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>E-8116</th>
      <td>2023-04-23 00:00:00</td>
      <td>Valencia</td>
      <td>Laptop Gamer</td>
      <td>2</td>
      <td>2076.36</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>E-8117</th>
      <td>2023-06-03 00:00:00</td>
      <td>Sevilla</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>1541.54</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>E-8118</th>
      <td>2023-02-24 00:00:00</td>
      <td>Valencia</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>1214.84</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>E-8119</th>
      <td>2023-01-08 00:00:00</td>
      <td>Madrid</td>
      <td>Mouse Ergonómico</td>
      <td>1</td>
      <td>370.26</td>
      <td>Este</td>
    </tr>
  </tbody>
</table>
<p>120 rows × 6 columns</p>
</div>



## Juntar dataframes


```python
df = pd.concat([df_norte, df_sur, df_este])
df.to_csv(sep=",", encoding="utf-8", path_or_buf="ventas_consolidadas.csv")
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fecha</th>
      <th>producto</th>
      <th>cantidad</th>
      <th>total_venta</th>
      <th>region</th>
      <th>ciudad</th>
    </tr>
    <tr>
      <th>id_transaccion</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>N-1000</th>
      <td>2023-05-10 03:00:00</td>
      <td>Laptop Gamer</td>
      <td>1</td>
      <td>970.00</td>
      <td>Norte</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>N-1001</th>
      <td>2023-06-18 09:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>4</td>
      <td>3708.00</td>
      <td>Norte</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>N-1002</th>
      <td>2023-03-10 05:00:00</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>2820.00</td>
      <td>Norte</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>N-1003</th>
      <td>2023-05-10 03:00:00</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>2538.00</td>
      <td>Norte</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>N-1004</th>
      <td>2023-02-25 17:00:00</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>908.00</td>
      <td>Norte</td>
      <td>Madrid</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>E-8115</th>
      <td>2023-04-05 00:00:00</td>
      <td>Monitor 4K</td>
      <td>1</td>
      <td>1003.09</td>
      <td>Este</td>
      <td>Valencia</td>
    </tr>
    <tr>
      <th>E-8116</th>
      <td>2023-04-23 00:00:00</td>
      <td>Laptop Gamer</td>
      <td>2</td>
      <td>2076.36</td>
      <td>Este</td>
      <td>Valencia</td>
    </tr>
    <tr>
      <th>E-8117</th>
      <td>2023-06-03 00:00:00</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>1541.54</td>
      <td>Este</td>
      <td>Sevilla</td>
    </tr>
    <tr>
      <th>E-8118</th>
      <td>2023-02-24 00:00:00</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>1214.84</td>
      <td>Este</td>
      <td>Valencia</td>
    </tr>
    <tr>
      <th>E-8119</th>
      <td>2023-01-08 00:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>1</td>
      <td>370.26</td>
      <td>Este</td>
      <td>Madrid</td>
    </tr>
  </tbody>
</table>
<p>430 rows × 6 columns</p>
</div>



[ventas_consolidadas.csv](./ventas_consolidadas.csv)
