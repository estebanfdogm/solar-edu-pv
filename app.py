"""Punto de entrada de SolarEdu PV."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from components.charts import create_iv_figure, create_pv_figure, create_solar_3d_figure
from components.ui import apply_theme, education_card, hero_header, metric_cards, section_divider, section_title
from core.offgrid_sizing import DEFAULT_LOADS, calculate_offgrid_sizing
from core.ongrid_sizing import calculate_ongrid_sizing
from core.pv_curve_model import calculate_pv_curve
from core.solar_geometry import calculate_solar_metrics


st.set_page_config(
    page_title="SolarEdu PV",
    page_icon="☀️",
    layout="wide",
)
apply_theme()


def simulation_tab() -> None:
    """Renderiza el laboratorio de geometría solar y curvas I-V/P-V."""
    section_title(
        "Simulación solar interactiva",
        "Modifique los controles y observe en tiempo real cómo cambian la irradiancia, la orientación y la respuesta eléctrica del panel.",
        eyebrow="Laboratorio de comportamiento FV",
    )

    left_col, right_col = st.columns((0.37, 0.63), gap="large")

    with left_col:
        with st.container(border=True):
            st.markdown(
                """
                <p class="control-panel__eyebrow">Panel de controles</p>
                <h3 class="control-panel__title">Configura el escenario</h3>
                <p class="control-panel__hint">Los cambios se reflejan inmediatamente en las gráficas y resultados de la derecha.</p>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('<p class="control-section-title">Condiciones solares</p>', unsafe_allow_html=True)
            irradiance = st.slider("Irradiancia base (W/m²)", 0, 1200, 1000, 25)
            temperature = st.slider("Temperatura del panel (°C)", -10, 80, 25, 1)

            st.markdown('<p class="control-section-title">Orientación del panel</p>', unsafe_allow_html=True)
            solar_azimuth = st.slider("Azimut solar (°)", 0, 360, 180, 1)
            solar_elevation = st.slider("Elevación solar (°)", 0, 90, 55, 1)
            panel_azimuth = st.slider("Azimut del panel (°)", 0, 360, 180, 1)
            panel_tilt = st.slider("Inclinación del panel (°)", 0, 90, 20, 1)

            with st.expander("Parámetros eléctricos avanzados", expanded=False):
                st.caption("Use estos valores para representar un módulo FV específico.")
                voc_ref = st.number_input("Voc de referencia (V)", min_value=1.0, value=49.5, step=0.1)
                isc_ref = st.number_input("Isc de referencia (A)", min_value=0.1, value=13.9, step=0.1)
                vmp_ref = st.number_input("Vmp de referencia (V)", min_value=1.0, value=41.7, step=0.1)
                imp_ref = st.number_input("Imp de referencia (A)", min_value=0.1, value=13.2, step=0.1)
                beta_voc = st.number_input(
                    "Coeficiente térmico del voltaje (V/°C)", value=-0.12, step=0.01, format="%.3f"
                )

            st.caption("Consejo: compare una orientación alineada y otra opuesta al sol para observar el efecto sobre la potencia.")

    solar = calculate_solar_metrics(
        irradiance_base=irradiance,
        solar_azimuth=solar_azimuth,
        solar_elevation=solar_elevation,
        panel_azimuth=panel_azimuth,
        panel_tilt=panel_tilt,
    )
    curve = calculate_pv_curve(
        effective_irradiance=solar["effective_irradiance"],
        panel_temperature=temperature,
        voc_ref=voc_ref,
        isc_ref=isc_ref,
        vmp_ref=vmp_ref,
        imp_ref=imp_ref,
        beta_voc=beta_voc,
    )

    with right_col:
        metric_cards(
            [
                ("Irradiancia [W/m²]", f"{solar['effective_irradiance']:.0f}"),
                ("Incidencia [°]", f"{solar['aoi']:.1f}"),
                ("Pmax [W]", f"{curve['pmax']:.0f}"),
                ("Factor de forma", f"{curve['fill_factor']:.2f}"),
            ],
            title="Resultados principales",
            subtitle="Indicadores que cambian con el escenario configurado.",
            columns_per_row=4,
        )

        section_divider("Orientación y respuesta del módulo")
        with st.container(border=True):
            st.markdown("##### Panel y vector solar")
            st.caption("La vista 3D muestra la geometría que determina el ángulo de incidencia [°].")
            st.plotly_chart(
                create_solar_3d_figure(solar, panel_azimuth, panel_tilt),
                width="stretch",
                config={"displayModeBar": False},
            )

        section_divider("Curvas eléctricas")
        iv_col, pv_col = st.columns(2, gap="medium")
        with iv_col:
            with st.container(border=True):
                st.markdown("##### Corriente del panel")
                st.caption("La curva I-V indica la corriente disponible para cada voltaje [V].")
                st.plotly_chart(create_iv_figure(curve), width="stretch", config={"displayModeBar": False})
        with pv_col:
            with st.container(border=True):
                st.markdown("##### Potencia del panel")
                st.caption("El punto MPP identifica la potencia [W] máxima aprovechable.")
                st.plotly_chart(create_pv_figure(curve), width="stretch", config={"displayModeBar": False})

        education_card(
            "Qué observar",
            f"Con un ángulo de incidencia de {solar['aoi']:.1f}°, la irradiancia efectiva es de "
            f"{solar['effective_irradiance']:.0f} W/m². Una mejor alineación suele aumentar la corriente y Pmax.",
            icon="🎯",
        )


def offgrid_tab() -> None:
    """Renderiza el dimensionamiento pedagógico de un sistema aislado."""
    section_title(
        "Dimensionamiento off-grid",
        "Construya una estimación orientativa para un sistema aislado a partir de las cargas y de la autonomía deseada.",
        eyebrow="Sistema aislado · Energía almacenada",
    )
    education_card(
        "Secuencia de diseño",
        "Primero registre el consumo diario. Después ajuste autonomía y eficiencias; el sistema traduce esos datos en componentes orientativos.",
        icon="🔋",
    )
    section_divider("1 · Perfil de consumo")
    st.markdown("#### Cargas eléctricas")
    loads = st.data_editor(
        DEFAULT_LOADS.copy(),
        num_rows="dynamic",
        width="stretch",
        hide_index=True,
        column_config={
            "Nombre de la carga": st.column_config.TextColumn(required=True),
            "Potencia (W)": st.column_config.NumberColumn(min_value=0.0, format="%.1f"),
            "Cantidad": st.column_config.NumberColumn(min_value=0, step=1),
            "Horas/día": st.column_config.NumberColumn(min_value=0.0, max_value=24.0, format="%.1f"),
        },
        key="offgrid_loads",
    )

    section_divider("2 · Parámetros del sistema")
    controls = st.columns(4, gap="medium")
    with controls[0]:
        autonomy_days = st.number_input("Días de autonomía", min_value=0.5, max_value=10.0, value=2.0, step=0.5)
        bank_voltage = st.selectbox("Voltaje del banco", [12, 24, 48], index=1, format_func=lambda value: f"{value} V")
    with controls[1]:
        dod = st.slider("Profundidad de descarga", 20, 90, 50, 5, format="%d%%") / 100
        inverter_efficiency = st.slider("Eficiencia del inversor", 70, 100, 90, 1, format="%d%%") / 100
    with controls[2]:
        controller_efficiency = st.slider("Eficiencia del controlador", 70, 100, 95, 1, format="%d%%") / 100
        peak_sun_hours = st.number_input("Horas solares pico", min_value=1.0, max_value=10.0, value=4.5, step=0.1)
    with controls[3]:
        panel_power = st.number_input("Potencia del panel (W)", min_value=50.0, value=550.0, step=10.0)
        battery_capacity = st.number_input("Capacidad de batería (Ah)", min_value=10.0, value=200.0, step=10.0)
        desired_inverter_power = st.number_input("Potencia del inversor deseado (W)", min_value=0.0, value=1500.0, step=100.0)

    result = calculate_offgrid_sizing(
        loads=loads,
        autonomy_days=autonomy_days,
        bank_voltage=bank_voltage,
        depth_of_discharge=dod,
        inverter_efficiency=inverter_efficiency,
        controller_efficiency=controller_efficiency,
        peak_sun_hours=peak_sun_hours,
        panel_power=panel_power,
        battery_capacity_ah=battery_capacity,
        desired_inverter_power=desired_inverter_power,
    )

    metric_cards(
        [
            ("Consumo diario", f"{result['daily_consumption_wh']:,.0f} Wh/día"),
            ("Consumo con pérdidas", f"{result['corrected_consumption_wh']:,.0f} Wh/día"),
            ("Potencia FV requerida", f"{result['pv_power_required_w']:,.0f} W"),
            ("Paneles", f"{result['panel_count']} unidades"),
            ("Banco de baterías", f"{result['battery_capacity_required_ah']:,.0f} Ah"),
            ("Controlador mínimo", f"{result['controller_current_a']:.0f} A"),
        ],
        title="Resultado de dimensionamiento",
        subtitle="Capacidades calculadas con las pérdidas y el margen configurados.",
        columns_per_row=3,
    )

    section_divider("3 · Componentes recomendados")
    col_table, col_note = st.columns((1.4, 0.6), gap="large")
    with col_table:
        with st.container(border=True):
            st.markdown("##### Selección orientativa")
            st.caption("Use esta tabla como punto de partida para discutir configuraciones y márgenes de diseño.")
            st.dataframe(result["components"], width="stretch", hide_index=True)
    with col_note:
        education_card(
            "Criterio aplicado",
            "El cálculo incorpora pérdidas de inversor y controlador, además de un margen del 25% para controlador e inversor.",
            icon="📐",
        )
        st.caption(
            f"Se asumen baterías unitarias equivalentes a {bank_voltage} V y {battery_capacity:.0f} Ah. "
            "La configuración serie/paralelo real depende del voltaje nominal de cada batería."
        )


def ongrid_tab() -> None:
    """Renderiza el dimensionamiento educativo de un sistema conectado a red."""
    section_title(
        "Dimensionamiento on-grid",
        "Estime un sistema de autoconsumo a partir del consumo mensual, el recurso solar y el área disponible.",
        eyebrow="Sistema conectado · Autoconsumo",
    )

    education_card(
        "Qué representa la cobertura",
        "La cobertura indica la fracción del consumo mensual que se busca atender con energía solar. Las pérdidas reducen la producción útil del arreglo.",
        icon="🏠",
    )
    section_divider("1 · Datos de partida")
    controls = st.columns(4, gap="medium")
    with controls[0]:
        monthly_consumption = st.number_input("Consumo mensual (kWh)", min_value=1.0, value=300.0, step=10.0)
        coverage = st.slider("Cobertura deseada", 10, 100, 80, 5, format="%d%%") / 100
    with controls[1]:
        peak_sun_hours = st.number_input(
            "Horas solares pico", min_value=1.0, max_value=10.0, value=4.5, step=0.1, key="ongrid_peak_sun_hours"
        )
        system_losses = st.slider("Pérdidas del sistema", 5, 35, 20, 1, format="%d%%") / 100
    with controls[2]:
        panel_power = st.number_input("Potencia del panel (W)", min_value=100.0, value=550.0, step=10.0, key="ongrid_panel")
        available_area = st.number_input("Área disponible (m²)", min_value=1.0, value=30.0, step=1.0)
    with controls[3]:
        panel_area = st.number_input("Área estimada por panel (m²)", min_value=0.5, value=2.6, step=0.1)
        energy_rate = st.number_input("Tarifa de energía (COP/kWh)", min_value=0.0, value=900.0, step=50.0)

    result = calculate_ongrid_sizing(
        monthly_consumption_kwh=monthly_consumption,
        coverage=coverage,
        peak_sun_hours=peak_sun_hours,
        system_losses=system_losses,
        panel_power_w=panel_power,
        available_area_m2=available_area,
        panel_area_m2=panel_area,
        energy_rate_cop_kwh=energy_rate,
    )

    metric_cards(
        [
            ("Energía diaria requerida", f"{result['daily_energy_required_kwh']:.1f} kWh"),
            ("Potencia FV requerida", f"{result['pv_power_required_kw']:.2f} kW"),
            ("Número de paneles", f"{result['panel_count']} unidades"),
            ("Potencia DC instalada", f"{result['dc_installed_kw']:.2f} kW"),
            ("Producción mensual", f"{result['monthly_production_kwh']:.0f} kWh"),
            ("Ahorro mensual", f"${result['monthly_savings_cop']:,.0f} COP"),
        ],
        title="Resumen del sistema propuesto",
        subtitle="Producción y ahorro aproximados para las condiciones ingresadas.",
        columns_per_row=3,
    )

    section_divider("2 · Comprobación de instalación")
    col_summary, col_education = st.columns((1.2, 0.8), gap="large")
    with col_summary:
        with st.container(border=True):
            st.markdown("##### Resumen de instalación")
            summary = pd.DataFrame(
                [
                    ["Producción diaria estimada", f"{result['daily_production_kwh']:.1f} kWh/día"],
                    ["Área requerida", f"{result['area_required_m2']:.1f} m²"],
                    ["Área disponible", f"{available_area:.1f} m²"],
                    ["Estado del área", "Disponible" if result["fits_available_area"] else "Insuficiente"],
                    ["Inversor recomendado", result["inverter_recommendation"]],
                ],
                columns=["Indicador", "Resultado"],
            )
            st.dataframe(summary, width="stretch", hide_index=True)
    with col_education:
        education_card(
            "Lectura del resultado",
            "El área y la producción estimada permiten evaluar si el arreglo es viable antes de pasar a un diseño técnico detallado.",
            icon="📊",
        )
        if result["fits_available_area"]:
            st.success("El arreglo propuesto cabe dentro del área disponible.")
        else:
            st.warning(
                f"Faltan aproximadamente {result['area_required_m2'] - available_area:.1f} m² para instalar todos los paneles."
            )
        st.caption(
            "El ahorro es una aproximación de energía autoconsumida valorizada con la tarifa indicada. "
            "No incluye cargos, impuestos, degradación ni reglas de compensación de excedentes."
        )


hero_header(
    "SolarEdu PV",
    "Explora de forma visual cómo la radiación, la orientación y el consumo definen el comportamiento de un sistema fotovoltaico.",
)

tab_simulation, tab_offgrid, tab_ongrid = st.tabs(
    ["☀️ Simulación solar", "🔋 Dimensionamiento off-grid", "🏠 Dimensionamiento on-grid"]
)
with tab_simulation:
    simulation_tab()
with tab_offgrid:
    offgrid_tab()
with tab_ongrid:
    ongrid_tab()
