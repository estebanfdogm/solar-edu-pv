"""Funciones de dimensionamiento off-grid, aisladas de la interfaz."""

from __future__ import annotations

import math

import pandas as pd


DEFAULT_LOADS = pd.DataFrame(
    [
        {"Nombre de la carga": "Iluminación LED", "Potencia (W)": 12.0, "Cantidad": 6, "Horas/día": 5.0},
        {"Nombre de la carga": "Portátil", "Potencia (W)": 65.0, "Cantidad": 2, "Horas/día": 4.0},
        {"Nombre de la carga": "Ventilador", "Potencia (W)": 45.0, "Cantidad": 1, "Horas/día": 6.0},
    ]
)


def _number(value: object) -> float:
    """Convierte entradas editables en un número no negativo."""
    converted = pd.to_numeric(value, errors="coerce")
    return max(0.0, 0.0 if pd.isna(converted) else float(converted))


def calculate_offgrid_sizing(
    loads: pd.DataFrame,
    autonomy_days: float,
    bank_voltage: int,
    depth_of_discharge: float,
    inverter_efficiency: float,
    controller_efficiency: float,
    peak_sun_hours: float,
    panel_power: float,
    battery_capacity_ah: float,
    desired_inverter_power: float,
) -> dict[str, float | int | pd.DataFrame]:
    """Dimensiona componentes con reglas sencillas y márgenes transparentes."""
    valid_loads = loads.copy()
    for column in ["Potencia (W)", "Cantidad", "Horas/día"]:
        valid_loads[column] = valid_loads[column].apply(_number)
    valid_loads["Wh/día"] = valid_loads["Potencia (W)"] * valid_loads["Cantidad"] * valid_loads["Horas/día"]

    daily_consumption_wh = float(valid_loads["Wh/día"].sum())
    peak_load_w = float((valid_loads["Potencia (W)"] * valid_loads["Cantidad"]).sum())
    total_efficiency = max(0.01, inverter_efficiency * controller_efficiency)
    corrected_consumption_wh = daily_consumption_wh / total_efficiency
    pv_power_required_w = corrected_consumption_wh / max(peak_sun_hours, 0.1)
    panel_count = math.ceil(pv_power_required_w / max(panel_power, 1.0)) if pv_power_required_w > 0 else 0
    battery_capacity_required_ah = (
        corrected_consumption_wh * max(autonomy_days, 0.1) / (max(bank_voltage, 1) * max(depth_of_discharge, 0.01))
    )
    battery_count = math.ceil(battery_capacity_required_ah / max(battery_capacity_ah, 1.0)) if battery_capacity_required_ah > 0 else 0
    array_power_w = panel_count * panel_power
    controller_current_a = array_power_w / max(bank_voltage, 1) * 1.25
    inverter_min_power_w = max(desired_inverter_power, peak_load_w * 1.25)

    components = pd.DataFrame(
        [
            ["Módulos fotovoltaicos", f"{panel_count} × {panel_power:.0f} W", f"Arreglo de {array_power_w:,.0f} Wp"],
            ["Banco de baterías", f"{battery_count} × {battery_capacity_ah:.0f} Ah", f"{bank_voltage} V, mínimo {battery_capacity_required_ah:,.0f} Ah"],
            ["Controlador de carga", f"≥ {controller_current_a:.0f} A", "Incluye 25% de margen"],
            ["Inversor", f"≥ {inverter_min_power_w:,.0f} W", "Considera carga simultánea y margen"],
        ],
        columns=["Componente", "Recomendación", "Criterio"],
    )

    return {
        "daily_consumption_wh": daily_consumption_wh,
        "corrected_consumption_wh": corrected_consumption_wh,
        "pv_power_required_w": pv_power_required_w,
        "panel_count": panel_count,
        "battery_capacity_required_ah": battery_capacity_required_ah,
        "battery_count": battery_count,
        "controller_current_a": controller_current_a,
        "inverter_min_power_w": inverter_min_power_w,
        "components": components,
    }
