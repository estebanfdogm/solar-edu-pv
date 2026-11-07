"""Modelo educativo y deliberadamente simple de curvas I-V y P-V."""

from __future__ import annotations

import math

import numpy as np


def calculate_pv_curve(
    effective_irradiance: float,
    panel_temperature: float,
    voc_ref: float,
    isc_ref: float,
    vmp_ref: float,
    imp_ref: float,
    beta_voc: float,
    reference_temperature: float = 25.0,
) -> dict[str, float | np.ndarray]:
    """Genera una curva I-V ajustada por irradiancia y temperatura.

    Se usa una expresión de una sola rodilla, calibrada con Voc, Isc, Vmp e Imp
    de referencia. Es adecuada para visualizar tendencias, no para diseñar un
    módulo comercial.
    """
    irradiance_ratio = max(0.0, effective_irradiance) / 1000.0
    voc = max(0.01, voc_ref + beta_voc * (panel_temperature - reference_temperature))
    isc = max(0.0, isc_ref * irradiance_ratio)
    vmp_target = min(voc * 0.98, max(0.01, vmp_ref * voc / max(voc_ref, 0.01)))
    imp_target = min(isc * 0.995, max(0.0, imp_ref * irradiance_ratio))

    if isc <= 0.0:
        voltage = np.linspace(0.0, voc, 220)
        current = np.zeros_like(voltage)
    else:
        voltage = np.linspace(0.0, voc, 220)
        mpp_voltage_ratio = np.clip(vmp_target / voc, 0.05, 0.98)
        mpp_current_ratio = np.clip(imp_target / isc, 0.02, 0.995)
        # Hace que la curva atraviese aproximadamente el par Vmp/Imp de catálogo.
        shape = math.log(1 - mpp_current_ratio) / math.log(mpp_voltage_ratio)
        current = isc * np.maximum(0.0, 1.0 - np.power(voltage / voc, shape))

    power = voltage * current
    mpp_index = int(np.argmax(power))
    pmax = float(power[mpp_index])
    vmp = float(voltage[mpp_index])
    imp = float(current[mpp_index])
    fill_factor = pmax / (voc * isc) if voc > 0 and isc > 0 else 0.0

    return {
        "voltage": voltage,
        "current": current,
        "power": power,
        "voc": voc,
        "isc": isc,
        "vmp": vmp,
        "imp": imp,
        "pmax": pmax,
        "fill_factor": fill_factor,
    }
