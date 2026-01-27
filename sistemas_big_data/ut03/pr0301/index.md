# PR0301: Ingesta de datos de archivos

## Ingesta CSV


```python
import pandas as pd

df_norte = pd.read_csv("./ventas_norte.csv", sep=";", dtype={"Cantidad_Vendida": int, "Precio_Unit": int, "Nom_Producto": str}, parse_dates=["Fecha_Venta"], index_col="ID_Transaccion")
df_norte["region"] = "Norte"
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
      <th>Fecha_Venta</th>
      <th>Nom_Producto</th>
      <th>Cantidad_Vendida</th>
      <th>Precio_Unit</th>
      <th>region</th>
    </tr>
    <tr>
      <th>ID_Transaccion</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1000</th>
      <td>2023-02-21</td>
      <td>Laptop</td>
      <td>4</td>
      <td>423</td>
      <td>Norte</td>
    </tr>
    <tr>
      <th>1001</th>
      <td>2023-01-15</td>
      <td>Laptop</td>
      <td>2</td>
      <td>171</td>
      <td>Norte</td>
    </tr>
    <tr>
      <th>1002</th>
      <td>2023-03-13</td>
      <td>Laptop</td>
      <td>3</td>
      <td>73</td>
      <td>Norte</td>
    </tr>
    <tr>
      <th>1003</th>
      <td>2023-03-02</td>
      <td>Teclado</td>
      <td>1</td>
      <td>139</td>
      <td>Norte</td>
    </tr>
    <tr>
      <th>1004</th>
      <td>2023-01-21</td>
      <td>Monitor</td>
      <td>4</td>
      <td>692</td>
      <td>Norte</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1095</th>
      <td>2023-02-10</td>
      <td>Laptop</td>
      <td>3</td>
      <td>516</td>
      <td>Norte</td>
    </tr>
    <tr>
      <th>1096</th>
      <td>2023-01-29</td>
      <td>Monitor</td>
      <td>3</td>
      <td>321</td>
      <td>Norte</td>
    </tr>
    <tr>
      <th>1097</th>
      <td>2023-01-15</td>
      <td>Laptop</td>
      <td>4</td>
      <td>200</td>
      <td>Norte</td>
    </tr>
    <tr>
      <th>1098</th>
      <td>2023-02-14</td>
      <td>Mouse</td>
      <td>4</td>
      <td>626</td>
      <td>Norte</td>
    </tr>
    <tr>
      <th>1099</th>
      <td>2023-03-06</td>
      <td>Mouse</td>
      <td>3</td>
      <td>118</td>
      <td>Norte</td>
    </tr>
  </tbody>
</table>
<p>100 rows × 5 columns</p>
</div>




```python
df_norte.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Index: 100 entries, 1000 to 1099
    Data columns (total 5 columns):
     #   Column            Non-Null Count  Dtype         
    ---  ------            --------------  -----         
     0   Fecha_Venta       100 non-null    datetime64[ns]
     1   Nom_Producto      100 non-null    object        
     2   Cantidad_Vendida  100 non-null    int64         
     3   Precio_Unit       100 non-null    int64         
     4   region            100 non-null    object        
    dtypes: datetime64[ns](1), int64(2), object(2)
    memory usage: 4.7+ KB


## Ingesta Excel


```python
df_sur = pd.read_excel("./ventas_sur.xlsx", names=["ID_Transaccion", "Fecha_Venta", "Nom_Producto", "Cantidad_Vendida", "Precio_Unit"], dtype={"Cantidad_Vendida": int, "Precio_Unit": int, "Nom_Producto": str}, parse_dates=["Fecha_Venta"], index_col="ID_Transaccion")
df_sur["region"] = "Sur"
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
      <th>Fecha_Venta</th>
      <th>Nom_Producto</th>
      <th>Cantidad_Vendida</th>
      <th>Precio_Unit</th>
      <th>region</th>
    </tr>
    <tr>
      <th>ID_Transaccion</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2000</th>
      <td>2023-03-01</td>
      <td>Monitor</td>
      <td>6</td>
      <td>624</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2001</th>
      <td>2023-03-04</td>
      <td>Laptop</td>
      <td>7</td>
      <td>941</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2002</th>
      <td>2023-03-26</td>
      <td>Mouse</td>
      <td>3</td>
      <td>989</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2003</th>
      <td>2023-02-01</td>
      <td>Webcam</td>
      <td>3</td>
      <td>621</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2004</th>
      <td>2023-03-28</td>
      <td>Mouse</td>
      <td>5</td>
      <td>437</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2005</th>
      <td>2023-02-02</td>
      <td>Mouse</td>
      <td>6</td>
      <td>134</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2006</th>
      <td>2023-03-08</td>
      <td>Laptop</td>
      <td>9</td>
      <td>636</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2007</th>
      <td>2023-01-18</td>
      <td>Teclado</td>
      <td>5</td>
      <td>922</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2008</th>
      <td>2023-01-25</td>
      <td>Mouse</td>
      <td>1</td>
      <td>215</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2009</th>
      <td>2023-02-23</td>
      <td>Monitor</td>
      <td>4</td>
      <td>845</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2010</th>
      <td>2023-02-27</td>
      <td>Teclado</td>
      <td>5</td>
      <td>520</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2011</th>
      <td>2023-03-08</td>
      <td>Webcam</td>
      <td>5</td>
      <td>645</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2012</th>
      <td>2023-02-15</td>
      <td>Laptop</td>
      <td>7</td>
      <td>512</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2013</th>
      <td>2023-01-24</td>
      <td>Webcam</td>
      <td>4</td>
      <td>94</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2014</th>
      <td>2023-02-01</td>
      <td>Teclado</td>
      <td>1</td>
      <td>432</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2015</th>
      <td>2023-02-16</td>
      <td>Teclado</td>
      <td>5</td>
      <td>395</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2016</th>
      <td>2023-03-27</td>
      <td>Teclado</td>
      <td>7</td>
      <td>439</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2017</th>
      <td>2023-01-23</td>
      <td>Webcam</td>
      <td>6</td>
      <td>748</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2018</th>
      <td>2023-03-07</td>
      <td>Teclado</td>
      <td>5</td>
      <td>296</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2019</th>
      <td>2023-01-27</td>
      <td>Webcam</td>
      <td>4</td>
      <td>780</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2020</th>
      <td>2023-01-02</td>
      <td>Teclado</td>
      <td>2</td>
      <td>695</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2021</th>
      <td>2023-03-31</td>
      <td>Monitor</td>
      <td>4</td>
      <td>413</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2022</th>
      <td>2023-01-17</td>
      <td>Teclado</td>
      <td>3</td>
      <td>888</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2023</th>
      <td>2023-02-02</td>
      <td>Webcam</td>
      <td>1</td>
      <td>476</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2024</th>
      <td>2023-01-09</td>
      <td>Mouse</td>
      <td>8</td>
      <td>939</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2025</th>
      <td>2023-02-12</td>
      <td>Teclado</td>
      <td>5</td>
      <td>211</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2026</th>
      <td>2023-02-17</td>
      <td>Mouse</td>
      <td>4</td>
      <td>758</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2027</th>
      <td>2023-02-08</td>
      <td>Monitor</td>
      <td>8</td>
      <td>708</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2028</th>
      <td>2023-02-11</td>
      <td>Laptop</td>
      <td>7</td>
      <td>118</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2029</th>
      <td>2023-01-26</td>
      <td>Monitor</td>
      <td>2</td>
      <td>567</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2030</th>
      <td>2023-02-19</td>
      <td>Teclado</td>
      <td>1</td>
      <td>997</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2031</th>
      <td>2023-01-25</td>
      <td>Mouse</td>
      <td>4</td>
      <td>115</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2032</th>
      <td>2023-01-24</td>
      <td>Mouse</td>
      <td>8</td>
      <td>683</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2033</th>
      <td>2023-01-13</td>
      <td>Webcam</td>
      <td>2</td>
      <td>682</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2034</th>
      <td>2023-03-01</td>
      <td>Mouse</td>
      <td>3</td>
      <td>209</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2035</th>
      <td>2023-01-07</td>
      <td>Webcam</td>
      <td>1</td>
      <td>755</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2036</th>
      <td>2023-02-26</td>
      <td>Laptop</td>
      <td>1</td>
      <td>56</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2037</th>
      <td>2023-02-05</td>
      <td>Teclado</td>
      <td>3</td>
      <td>799</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2038</th>
      <td>2023-02-14</td>
      <td>Webcam</td>
      <td>5</td>
      <td>388</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2039</th>
      <td>2023-01-20</td>
      <td>Laptop</td>
      <td>3</td>
      <td>714</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2040</th>
      <td>2023-03-06</td>
      <td>Mouse</td>
      <td>1</td>
      <td>544</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2041</th>
      <td>2023-01-08</td>
      <td>Mouse</td>
      <td>1</td>
      <td>298</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2042</th>
      <td>2023-01-16</td>
      <td>Laptop</td>
      <td>8</td>
      <td>236</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2043</th>
      <td>2023-01-14</td>
      <td>Mouse</td>
      <td>2</td>
      <td>886</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2044</th>
      <td>2023-03-17</td>
      <td>Laptop</td>
      <td>3</td>
      <td>892</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2045</th>
      <td>2023-03-28</td>
      <td>Webcam</td>
      <td>2</td>
      <td>817</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2046</th>
      <td>2023-01-15</td>
      <td>Webcam</td>
      <td>3</td>
      <td>292</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2047</th>
      <td>2023-03-07</td>
      <td>Laptop</td>
      <td>7</td>
      <td>900</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2048</th>
      <td>2023-02-01</td>
      <td>Webcam</td>
      <td>1</td>
      <td>81</td>
      <td>Sur</td>
    </tr>
    <tr>
      <th>2049</th>
      <td>2023-03-28</td>
      <td>Webcam</td>
      <td>8</td>
      <td>615</td>
      <td>Sur</td>
    </tr>
  </tbody>
</table>
</div>



## Ingesta JSON


```python
import json
with open("./ventas_este.json") as f:
    info = json.load(f)
df_este = pd.json_normalize(info)
df_este = df_este[["id_orden", "timestamp", "detalles_producto.nombre", "detalles_producto.specs.cantidad", "detalles_producto.specs.precio"]]
df_este["timestamp"] = df_este["timestamp"].apply(lambda x: x.split(" ")[0])
df_este = df_este.rename(columns={"id_orden": "ID_Transaccion", "timestamp": "Fecha_Venta", "detalles_producto.nombre": "Nom_Producto", "detalles_producto.specs.cantidad": "Cantidad_Vendida", "detalles_producto.specs.precio": "Precio_Unit"})
df_este = df_este.set_index("ID_Transaccion")
df_este["region"] = "Este"
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
      <th>Fecha_Venta</th>
      <th>Nom_Producto</th>
      <th>Cantidad_Vendida</th>
      <th>Precio_Unit</th>
      <th>region</th>
    </tr>
    <tr>
      <th>ID_Transaccion</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>ORD-3000</th>
      <td>2023-03-09</td>
      <td>Monitor</td>
      <td>2</td>
      <td>244</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>ORD-3001</th>
      <td>2023-01-20</td>
      <td>Laptop</td>
      <td>2</td>
      <td>578</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>ORD-3002</th>
      <td>2023-01-01</td>
      <td>Mouse</td>
      <td>2</td>
      <td>339</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>ORD-3003</th>
      <td>2023-02-07</td>
      <td>Webcam</td>
      <td>2</td>
      <td>158</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>ORD-3004</th>
      <td>2023-03-18</td>
      <td>Monitor</td>
      <td>1</td>
      <td>692</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>ORD-3095</th>
      <td>2023-03-28</td>
      <td>Webcam</td>
      <td>1</td>
      <td>857</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>ORD-3096</th>
      <td>2023-01-18</td>
      <td>Webcam</td>
      <td>2</td>
      <td>375</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>ORD-3097</th>
      <td>2023-02-10</td>
      <td>Mouse</td>
      <td>1</td>
      <td>696</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>ORD-3098</th>
      <td>2023-01-25</td>
      <td>Mouse</td>
      <td>2</td>
      <td>618</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>ORD-3099</th>
      <td>2023-03-27</td>
      <td>Webcam</td>
      <td>1</td>
      <td>844</td>
      <td>Este</td>
    </tr>
  </tbody>
</table>
<p>100 rows × 5 columns</p>
</div>




```python
df_junto = pd.concat([df_norte, df_sur, df_este])
df_junto
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
      <th>Fecha_Venta</th>
      <th>Nom_Producto</th>
      <th>Cantidad_Vendida</th>
      <th>Precio_Unit</th>
      <th>region</th>
    </tr>
    <tr>
      <th>ID_Transaccion</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1000</th>
      <td>2023-02-21 00:00:00</td>
      <td>Laptop</td>
      <td>4</td>
      <td>423</td>
      <td>Norte</td>
    </tr>
    <tr>
      <th>1001</th>
      <td>2023-01-15 00:00:00</td>
      <td>Laptop</td>
      <td>2</td>
      <td>171</td>
      <td>Norte</td>
    </tr>
    <tr>
      <th>1002</th>
      <td>2023-03-13 00:00:00</td>
      <td>Laptop</td>
      <td>3</td>
      <td>73</td>
      <td>Norte</td>
    </tr>
    <tr>
      <th>1003</th>
      <td>2023-03-02 00:00:00</td>
      <td>Teclado</td>
      <td>1</td>
      <td>139</td>
      <td>Norte</td>
    </tr>
    <tr>
      <th>1004</th>
      <td>2023-01-21 00:00:00</td>
      <td>Monitor</td>
      <td>4</td>
      <td>692</td>
      <td>Norte</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>ORD-3095</th>
      <td>2023-03-28</td>
      <td>Webcam</td>
      <td>1</td>
      <td>857</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>ORD-3096</th>
      <td>2023-01-18</td>
      <td>Webcam</td>
      <td>2</td>
      <td>375</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>ORD-3097</th>
      <td>2023-02-10</td>
      <td>Mouse</td>
      <td>1</td>
      <td>696</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>ORD-3098</th>
      <td>2023-01-25</td>
      <td>Mouse</td>
      <td>2</td>
      <td>618</td>
      <td>Este</td>
    </tr>
    <tr>
      <th>ORD-3099</th>
      <td>2023-03-27</td>
      <td>Webcam</td>
      <td>1</td>
      <td>844</td>
      <td>Este</td>
    </tr>
  </tbody>
</table>
<p>250 rows × 5 columns</p>
</div>




```python
df_junto.to_csv(index=False, sep=",", encoding="utf-8", path_or_buf="./ventas_consolidadas.csv")
```

[ventas_consolidadas.csv](./ventas_consolidadas.csv)