"""Funciones de dimensionamiento on-grid para uso docente."""

from __future__ import annotations

import math


def calculate_ongrid_sizing(
    monthly_consumption_kwh: float,
    coverage: float,
    peak_sun_hours: float,
    system_losses: float,
    panel_power_w: float,
    available_area_m2: float,
    panel_area_m2: float,
    energy_rate_cop_kwh: float,
) -> dict[str, float | int | bool | str]:
    """Estima un sistema de autoconsumo sin modelar tarifas ni excedentes reales."""
    daily_energy_required_kwh = monthly_consumption_kwh * coverage / 30.0
    performance_ratio = max(0.01, 1.0 - system_losses)
    pv_power_required_kw = daily_energy_required_kwh / max(peak_sun_hours, 0.1) / performance_ratio
    panel_count = max(1, math.ceil((pv_power_required_kw * 1000) / max(panel_power_w, 1.0)))
    dc_installed_kw = panel_count * panel_power_w / 1000.0
    daily_production_kwh = dc_installed_kw * peak_sun_hours * performance_ratio
    monthly_production_kwh = daily_production_kwh * 30.0
    area_required_m2 = panel_count * panel_area_m2
    saved_energy_kwh = min(monthly_production_kwh, monthly_consumption_kwh)
    monthly_savings_cop = saved_energy_kwh * energy_rate_cop_kwh
    inverter_kw = dc_installed_kw / 1.15  # Relación DC/AC educativa de 1.15.

    return {
        "daily_energy_required_kwh": daily_energy_required_kwh,
        "pv_power_required_kw": pv_power_required_kw,
        "panel_count": panel_count,
        "dc_installed_kw": dc_installed_kw,
        "daily_production_kwh": daily_production_kwh,
        "monthly_production_kwh": monthly_production_kwh,
        "area_required_m2": area_required_m2,
        "fits_available_area": area_required_m2 <= available_area_m2,
        "monthly_savings_cop": monthly_savings_cop,
        "inverter_recommendation": f"Inversor on-grid cercano a {inverter_kw:.1f} kW AC",
    }
