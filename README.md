# SolarEdu PV

Aplicación educativa en Streamlit para visualizar conceptos básicos de energía solar fotovoltaica. Incluye una simulación de irradiancia y curvas I-V/P-V, además de dimensionamientos orientativos off-grid y on-grid.

> No reemplaza el diseño eléctrico, estructural o normativo de un proyecto real. Los cálculos son deliberadamente simplificados para uso en clase.

## Requisitos

- Python 3.10 o superior
- `pip`

## Instalación y ejecución

Desde la carpeta del proyecto:

```powershell
pip install -r requirements.txt
streamlit run app.py
```

Streamlit mostrará la dirección local de la aplicación, normalmente `http://localhost:8501`.

## Estructura

```text
solar_edu_pv/
├── app.py
├── requirements.txt
├── README.md
├── core/                  # Modelos de cálculo independientes de la interfaz
├── components/            # Tema y gráficas Plotly reutilizables
├── data/                  # Reservado para datos locales de ejercicios
└── sample_components.csv  # Ejemplo de catálogo didáctico
```

## Alcance de los modelos

- La irradiancia efectiva se estima con el ángulo de incidencia calculado mediante `pvlib`.
- La curva I-V usa un modelo de una sola rodilla ajustado con parámetros de referencia del módulo.
- El dimensionamiento off-grid aplica eficiencias, autonomía, profundidad de descarga y márgenes educativos.
- El dimensionamiento on-grid estima producción con horas solares pico y pérdidas globales; no contempla compensación de excedentes, sombreado ni normativa local.
