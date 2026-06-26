"""Elementos de presentación compartidos para el dashboard educativo."""

from __future__ import annotations

import streamlit as st


def apply_theme() -> None:
    """Aplica una apariencia clara, legible y consistente al dashboard."""
    st.markdown(
        """
        <style>
            .stApp { background: linear-gradient(180deg, #f7fbff 0%, #f6faf8 100%); }
            [data-testid="stHeader"] { background: rgba(0,0,0,0); }
            [data-testid="stMainBlockContainer"] {
                max-width: 1280px;
                padding-top: 2.2rem;
                padding-bottom: 3rem;
            }
            h1, h2, h3, h4 { color: #16333c; }
            .hero {
                position: relative;
                overflow: hidden;
                padding: 1.65rem 1.8rem;
                border: 1px solid #dbeafe;
                border-radius: 1.15rem;
                background: linear-gradient(115deg, #ffffff 0%, #eff8ff 100%);
                box-shadow: 0 12px 30px rgba(15, 61, 76, 0.08);
                margin-bottom: 1.4rem;
            }
            .hero::after {
                content: "";
                position: absolute;
                width: 15rem;
                height: 15rem;
                top: -10rem;
                right: -4rem;
                border-radius: 50%;
                background: rgba(251, 191, 36, 0.18);
            }
            .hero__eyebrow, .section-intro__eyebrow, .metric-heading__eyebrow,
            .education-card__eyebrow {
                margin: 0 0 0.35rem;
                color: #0f766e;
                font-size: 0.72rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }
            .hero h1 {
                position: relative;
                margin: 0;
                color: #123c4b;
                font-size: clamp(2rem, 4vw, 3rem);
                font-weight: 800;
                letter-spacing: -0.045em;
            }
            .hero__subtitle {
                position: relative;
                max-width: 45rem;
                margin: 0.55rem 0 0;
                color: #526a73;
                font-size: 1.02rem;
                line-height: 1.55;
            }
            .section-intro { margin: 0.4rem 0 1rem; }
            .section-intro h2 {
                margin: 0;
                font-size: 1.7rem;
                letter-spacing: -0.025em;
            }
            .section-intro__subtitle {
                max-width: 56rem;
                margin: 0.35rem 0 0;
                color: #60757d;
                line-height: 1.55;
            }
            [data-testid="stMetric"] {
                min-height: 7.1rem;
                padding: 1rem 1.05rem;
                border: 1px solid #d8e7ec;
                border-top: 3px solid #38bdf8;
                border-radius: 0.9rem;
                background: rgba(255,255,255,0.9);
                box-shadow: 0 5px 18px rgba(15, 61, 76, 0.06);
            }
            [data-testid="stMetricLabel"] { color: #42626c; font-size: 0.84rem; }
            [data-testid="stMetricValue"] { color: #075985; font-size: 1.58rem; }
            .metric-heading { margin: 1.45rem 0 0.7rem; }
            .metric-heading h3 { margin: 0; font-size: 1.16rem; }
            .metric-heading__subtitle { margin: 0.2rem 0 0; color: #60757d; font-size: 0.9rem; }
            .control-panel__eyebrow {
                margin: 0 0 0.35rem;
                color: #0f766e;
                font-size: 0.72rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }
            .control-panel__title { margin: 0; color: #16333c; font-size: 1.15rem; }
            .control-panel__hint {
                margin: 0.35rem 0 0.9rem;
                color: #60757d;
                font-size: 0.88rem;
                line-height: 1.45;
            }
            .control-section-title {
                margin: 1rem 0 0.35rem;
                color: #28515d;
                font-size: 0.92rem;
                font-weight: 750;
            }
            .section-rule {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin: 1.5rem 0 1rem;
                color: #34616c;
                font-size: 0.78rem;
                font-weight: 750;
                letter-spacing: 0.06em;
                text-transform: uppercase;
            }
            .section-rule::after {
                content: "";
                height: 1px;
                flex: 1;
                background: linear-gradient(90deg, #cde7ee, transparent);
            }
            .education-card {
                display: flex;
                gap: 0.9rem;
                padding: 1.05rem 1.1rem;
                border: 1px solid #cbe8e4;
                border-radius: 0.9rem;
                background: linear-gradient(135deg, #f0fdfa 0%, #f8fffe 100%);
            }
            .education-card__icon {
                display: grid;
                flex: 0 0 2.25rem;
                width: 2.25rem;
                height: 2.25rem;
                place-items: center;
                border-radius: 0.7rem;
                background: #ccfbf1;
                font-size: 1.15rem;
            }
            .education-card h4 { margin: 0; font-size: 1rem; }
            .education-card__body { margin: 0.28rem 0 0; color: #4b6870; line-height: 1.5; font-size: 0.9rem; }
            .stTabs [data-baseweb="tab-list"] { gap: 0.45rem; border-bottom: 1px solid #dbe6ea; }
            .stTabs [data-baseweb="tab"] { height: 3rem; border-radius: 0.65rem 0.65rem 0 0; }
            .stTabs [aria-selected="true"] { background-color: #e6f7fb; color: #075985; }
            [data-testid="stExpander"] {
                border: 1px solid #dbe6ea;
                border-radius: 0.9rem;
                background: rgba(255,255,255,0.75);
            }
            [data-testid="stVerticalBlockBorderWrapper"] {
                border-color: #dbe6ea;
                border-radius: 0.9rem;
                background: rgba(255,255,255,0.72);
            }
            [data-testid="stDataFrame"] { border: 1px solid #dbe6ea; border-radius: 0.75rem; overflow: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero_header(title: str, subtitle: str) -> None:
    """Muestra la identidad y el propósito didáctico de la plataforma."""
    st.markdown(
        f"""
        <section class="hero">
            <p class="hero__eyebrow">Plataforma docente · Energía fotovoltaica</p>
            <h1>☀️ {title}</h1>
            <p class="hero__subtitle">{subtitle}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, subtitle: str, eyebrow: str = "Laboratorio guiado") -> None:
    """Muestra un título de sección con contexto claro y breve."""
    st.markdown(
        f"""
        <section class="section-intro">
            <p class="section-intro__eyebrow">{eyebrow}</p>
            <h2>{title}</h2>
            <p class="section-intro__subtitle">{subtitle}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def section_divider(label: str) -> None:
    """Añade un separador visual para organizar una secuencia didáctica."""
    st.markdown(f'<div class="section-rule"><span>{label}</span></div>', unsafe_allow_html=True)


def education_card(title: str, body: str, icon: str = "💡") -> None:
    """Presenta una idea educativa corta sin interrumpir el flujo de trabajo."""
    st.markdown(
        f"""
        <aside class="education-card">
            <div class="education-card__icon">{icon}</div>
            <div>
                <p class="education-card__eyebrow">Concepto clave</p>
                <h4>{title}</h4>
                <p class="education-card__body">{body}</p>
            </div>
        </aside>
        """,
        unsafe_allow_html=True,
    )


def metric_cards(cards, columns_per_row=4, **kwargs) -> None:
    """Renderiza métricas en tarjetas, con soporte para tuplas y diccionarios."""
    if not cards:
        return

    if isinstance(cards, dict):
        cards = [cards]
    elif isinstance(cards, tuple) and len(cards) >= 2 and not isinstance(cards[0], (dict, list, tuple)):
        cards = [cards]
    else:
        cards = list(cards)

    try:
        columns_per_row = int(columns_per_row)
    except (TypeError, ValueError):
        columns_per_row = 4
    columns_per_row = max(1, columns_per_row)

    title = kwargs.get("title")
    subtitle = kwargs.get("subtitle")
    if title:
        subtitle_html = f'<p class="metric-heading__subtitle">{subtitle}</p>' if subtitle else ""
        st.markdown(
            f"""
            <div class="metric-heading">
                <p class="metric-heading__eyebrow">Resultados</p>
                <h3>{title}</h3>
                {subtitle_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    custom_metric_card = globals().get("metric_card")
    for start in range(0, len(cards), columns_per_row):
        row_cards = cards[start : start + columns_per_row]
        columns = st.columns(columns_per_row, gap="medium")
        for column, card in zip(columns, row_cards):
            with column:
                if isinstance(card, dict):
                    label = card.get("title", card.get("label", "Métrica"))
                    value = card.get("value", "")
                    unit = card.get("unit", "")
                    delta = card.get("delta")
                    help_text = card.get("help_text", card.get("help"))
                    display_value = f"{value} {unit}".strip()

                    if callable(custom_metric_card):
                        try:
                            custom_metric_card(title=label, value=value, unit=unit, help_text=help_text)
                            continue
                        except Exception:
                            pass

                    st.metric(label=str(label), value=str(display_value), delta=delta, help=help_text)
                elif isinstance(card, (list, tuple)) and len(card) >= 2:
                    st.metric(label=str(card[0]), value=str(card[1]))
                else:
                    st.metric(label="Métrica", value=str(card))
