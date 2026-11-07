"""Gráficas Plotly reutilizables para SolarEdu PV."""

from __future__ import annotations

import math

import numpy as np
import plotly.graph_objects as go

from core.solar_geometry import panel_normal


CHART_LAYOUT = dict(
    template="plotly_white",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#ffffff",
    margin=dict(l=54, r=24, t=58, b=54),
    font=dict(family="Inter, Arial, sans-serif", color="#263238"),
    hoverlabel=dict(bgcolor="#16333c", font_color="#ffffff", bordercolor="#16333c"),
)


def _style_cartesian_figure(fig: go.Figure, title: str, yaxis_title: str, height: int) -> go.Figure:
    """Aplica un lenguaje visual común a las curvas de aprendizaje."""
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=title, x=0.02, xanchor="left", font=dict(size=18, color="#16333c")),
        height=height,
        hovermode="x unified",
        showlegend=True,
        legend=dict(orientation="h", x=0.02, y=1.12, font=dict(size=12)),
    )
    fig.update_xaxes(
        title="Voltaje [V]",
        showgrid=True,
        gridcolor="#e2edf1",
        zeroline=False,
        linecolor="#b9cbd1",
        ticks="outside",
    )
    fig.update_yaxes(
        title=yaxis_title,
        showgrid=True,
        gridcolor="#e2edf1",
        zeroline=False,
        linecolor="#b9cbd1",
        ticks="outside",
    )
    return fig


def create_solar_3d_figure(solar: dict, panel_azimuth: float, panel_tilt: float) -> go.Figure:
    """Crea una vista espacial sencilla del módulo y el vector solar."""
    normal = panel_normal(panel_azimuth, panel_tilt)
    azimuth_rad = math.radians(panel_azimuth)
    right = np.array([math.cos(azimuth_rad), -math.sin(azimuth_rad), 0.0])
    up = np.cross(normal, right)
    up = up / np.linalg.norm(up)
    corners = np.array([[-1.1, -0.7], [1.1, -0.7], [-1.1, 0.7], [1.1, 0.7]])
    points = np.array([x * right + y * up for x, y in corners])
    sun_end = solar["solar_vector"] * 1.9

    fig = go.Figure()
    fig.add_trace(
        go.Surface(
            x=points[:, 0].reshape(2, 2),
            y=points[:, 1].reshape(2, 2),
            z=points[:, 2].reshape(2, 2),
            colorscale=[[0, "#075985"], [1, "#38bdf8"]],
            showscale=False,
            opacity=0.95,
            hovertemplate="Panel FV<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=[0, sun_end[0]],
            y=[0, sun_end[1]],
            z=[0, sun_end[2]],
            mode="lines+markers",
            line=dict(color="#f59e0b", width=10),
            marker=dict(size=[2, 7], color=["#f59e0b", "#fbbf24"]),
            name="Vector solar",
            hovertemplate="Vector solar<extra></extra>",
        )
    )
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(
            text=f"Orientación del panel · AOI: {solar['aoi']:.1f}°",
            x=0.02,
            xanchor="left",
            font=dict(size=18, color="#16333c"),
        ),
        height=380,
        scene=dict(
            xaxis=dict(visible=False, range=[-2, 2]),
            yaxis=dict(visible=False, range=[-2, 2]),
            zaxis=dict(visible=False, range=[-0.4, 2]),
            bgcolor="#ffffff",
            camera=dict(eye=dict(x=1.45, y=-1.45, z=1.1)),
            aspectmode="cube",
        ),
        legend=dict(orientation="h", x=0.02, y=0.02, font=dict(size=12)),
    )
    return fig


def create_iv_figure(curve: dict) -> go.Figure:
    """Crea la curva corriente-voltaje con su punto MPP."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=curve["voltage"],
            y=curve["current"],
            mode="lines",
            name="Curva I-V",
            line=dict(color="#0284c7", width=3.5),
            hovertemplate="Voltaje: %{x:.1f} V<br>Corriente: %{y:.2f} A<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[curve["vmp"]],
            y=[curve["imp"]],
            mode="markers",
            name="Punto MPP",
            marker=dict(color="#f59e0b", size=11, line=dict(color="#ffffff", width=2)),
            hovertemplate="MPP<br>Vmp: %{x:.1f} V<br>Imp: %{y:.2f} A<extra></extra>",
        )
    )
    fig.add_vline(x=curve["vmp"], line_width=1.2, line_dash="dot", line_color="#f59e0b")
    fig.add_annotation(
        x=curve["vmp"],
        y=curve["imp"],
        text=f"<b>MPP</b><br>{curve['vmp']:.1f} V · {curve['imp']:.2f} A",
        showarrow=True,
        arrowhead=2,
        ax=-72,
        ay=-48,
        bgcolor="#fff7df",
        bordercolor="#fcd34d",
        borderpad=5,
    )
    return _style_cartesian_figure(fig, "Curva I-V · Corriente disponible", "Corriente [A]", 380)


def create_pv_figure(curve: dict) -> go.Figure:
    """Crea la curva potencia-voltaje con su punto MPP."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=curve["voltage"], y=curve["power"], mode="lines", name="Curva P-V", line=dict(color="#16a34a", width=3), fill="tozeroy",
            fillcolor="rgba(22, 163, 74, 0.13)",
            hovertemplate="Voltaje: %{x:.1f} V<br>Potencia: %{y:.0f} W<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[curve["vmp"]],
            y=[curve["pmax"]],
            mode="markers",
            name="Potencia máxima",
            marker=dict(color="#f59e0b", size=11, line=dict(color="#ffffff", width=2)),
            hovertemplate="Punto de máxima potencia<br>Vmp: %{x:.1f} V<br>Pmax: %{y:.0f} W<extra></extra>",
        )
    )
    fig.add_vline(x=curve["vmp"], line_width=1.2, line_dash="dot", line_color="#f59e0b")
    fig.add_annotation(
        x=curve["vmp"],
        y=curve["pmax"],
        text=f"<b>Pmax</b><br>{curve['pmax']:.0f} W",
        showarrow=True,
        arrowhead=2,
        ax=-58,
        ay=-45,
        bgcolor="#fff7df",
        bordercolor="#fcd34d",
        borderpad=5,
    )
    return _style_cartesian_figure(fig, "Curva P-V · Potencia del módulo", "Potencia [W]", 360)
