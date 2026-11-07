# SolarEdu PV

Simulador en Python y Streamlit para explorar sistemas fotovoltaicos. Puedes mover el sol y cambiar la inclinación del panel, ver cómo cambian las curvas I–V y P–V, y estimar el tamaño de un arreglo con o sin conexión a la red.

## Ejecutar en local

Con Python 3.10 o superior, abre una terminal en la carpeta del proyecto.

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Abre la dirección que indica Streamlit, normalmente `http://localhost:8501`.

## Un ejemplo para comprobar

En **Dimensionamiento on-grid**, usa 300 kWh de consumo mensual, cobertura del 80 %, 4,5 horas solares pico, pérdidas del 20 % y módulos de 550 W. El cálculo pide unos 2,22 kWp antes de redondear. La aplicación debe proponer **5 paneles**. Si cada uno ocupa 2,6 m², el arreglo requiere **13 m²**.

El ejemplo usa valores didácticos. Para comparar escenarios, cambia solo un dato a la vez.

## Código y pruebas

- `app.py` conecta los controles de Streamlit con los modelos.
- `core/` contiene los cálculos de irradiancia, curvas y dimensionamiento.
- `components/` contiene las gráficas y elementos de interfaz.
- `sample_components.csv` es un catálogo de ejemplo para consultar.

Ejecuta las pruebas de cálculo desde la raíz del repositorio.

```powershell
python -m unittest discover -s tests -v
```

Los modelos son simplificados y están pensados para clase. El dimensionamiento real requiere revisar el sitio, las hojas de datos, la instalación y la normativa aplicable.
