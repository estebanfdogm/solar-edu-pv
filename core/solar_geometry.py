"""Cálculos geométricos simplificados para la pestaña de simulación solar."""

from __future__ import annotations

import math

import numpy as np
import pvlib


def solar_vector(azimuth: float, elevation: float) -> np.ndarray:
    """Devuelve un vector unitario solar; azimut 0° es norte y 90° es este."""
    azimuth_rad = math.radians(azimuth)
    elevation_rad = math.radians(elevation)
    return np.array(
        [
            math.cos(elevation_rad) * math.sin(azimuth_rad),
            math.cos(elevation_rad) * math.cos(azimuth_rad),
            math.sin(elevation_rad),
        ]
    )


def panel_normal(panel_azimuth: float, panel_tilt: float) -> np.ndarray:
    """Devuelve el vector normal de la cara frontal del módulo."""
    azimuth_rad = math.radians(panel_azimuth)
    tilt_rad = math.radians(panel_tilt)
    return np.array(
        [
            math.sin(tilt_rad) * math.sin(azimuth_rad),
            math.sin(tilt_rad) * math.cos(azimuth_rad),
            math.cos(tilt_rad),
        ]
    )


def calculate_solar_metrics(
    irradiance_base: float,
    solar_azimuth: float,
    solar_elevation: float,
    panel_azimuth: float,
    panel_tilt: float,
) -> dict[str, float | np.ndarray]:
    """Calcula AOI y una irradiancia efectiva directa para fines educativos."""
    solar_zenith = float(np.clip(90 - solar_elevation, 0, 180))
    aoi = float(
        pvlib.irradiance.aoi(
            surface_tilt=panel_tilt,
            surface_azimuth=panel_azimuth,
            solar_zenith=solar_zenith,
            solar_azimuth=solar_azimuth,
        )
    )
    incidence_factor = max(0.0, math.cos(math.radians(aoi)))
    effective_irradiance = max(0.0, irradiance_base * incidence_factor)

    return {
        "aoi": aoi,
        "incidence_factor": incidence_factor,
        "effective_irradiance": effective_irradiance,
        "solar_vector": solar_vector(solar_azimuth, solar_elevation),
        "panel_normal": panel_normal(panel_azimuth, panel_tilt),
    }
