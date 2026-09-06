"""
theme.py — Tema visual hijau modern untuk Sistem Verifikasi Obat Otomatis.
Dipakai bersama oleh semua halaman (streamlit_app.py + pages/*.py) supaya
tampilan konsisten. Semua ikon berupa SVG inline buatan sendiri (bukan
gambar dari internet), jadi tetap tampil kaya visual walau dijalankan
offline / tanpa koneksi internet.
"""
import streamlit as st

PRIMARY_DARK = "#0B3D2E"
PRIMARY = "#146C43"
PRIMARY_BRIGHT = "#22C55E"
ACCENT = "#4ADE80"
BG_SOFT = "#EFFBF3"


def inject_base_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}
    h1, h2, h3, h4 {{
        font-family: 'Poppins', sans-serif !important;
        color: {PRIMARY_DARK};
    }}

    .stApp {{
        background: linear-gradient(180deg, #F4FBF6 0%, #E7F7EC 45%, #F4FBF6 100%);
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(200deg, {PRIMARY_DARK} 0%, #145A3C 60%, #1B7A43 100%);
    }}
    section[data-testid="stSidebar"] * {{
        color: #EAFBF0 !important;
    }}
    section[data-testid="stSidebar"] .stRadio label, 
    section[data-testid="stSidebar"] a {{
        color: #EAFBF0 !important;
    }}

    /* Kotak input di sidebar (text_input, textarea, dsb) tetap berlatar putih,
       jadi teksnya harus gelap supaya kebaca -- jangan ikut aturan putih di atas */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] [data-baseweb="input"],
    section[data-testid="stSidebar"] [data-baseweb="textarea"],
    section[data-testid="stSidebar"] [data-baseweb="select"] * {{
        color: {PRIMARY_DARK} !important;
        background-color: #FFFFFF !important;
    }}
    section[data-testid="stSidebar"] input::placeholder,
    section[data-testid="stSidebar"] textarea::placeholder {{
        color: #7A9C8C !important;
    }}

    /* Hero banner */
    .hero-box {{
        background: linear-gradient(120deg, {PRIMARY_DARK} 0%, {PRIMARY} 55%, {PRIMARY_BRIGHT} 100%);
        border-radius: 24px;
        padding: 2.6rem 2.4rem;
        color: white;
        box-shadow: 0 18px 40px -12px rgba(11,61,46,0.45);
        margin-bottom: 1.6rem;
        position: relative;
        overflow: hidden;
    }}
    .hero-box h1 {{ color: white !important; font-size: 2.1rem; margin-bottom: 0.4rem; }}
    .hero-box p {{ color: #DFF7E8; font-size: 1.05rem; max-width: 640px; }}
    .hero-badge {{
        display: inline-block; background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.35);
        padding: 4px 14px; border-radius: 999px; font-size: 0.8rem;
        margin-bottom: 14px; letter-spacing: 0.3px;
    }}

    /* Feature / info cards */
    .green-card {{
        background: white;
        border-radius: 18px;
        padding: 1.4rem 1.3rem;
        box-shadow: 0 8px 24px -10px rgba(20,108,67,0.25);
        border: 1px solid #DCF3E4;
        height: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .green-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 14px 30px -10px rgba(20,108,67,0.38);
    }}
    .green-card h4 {{ margin-top: 0.6rem; margin-bottom: 0.3rem; }}
    .green-card p {{ color: #446358; font-size: 0.92rem; }}

    .metric-pill {{
        display: inline-flex; align-items: baseline; gap: 6px;
        background: {BG_SOFT}; border: 1px solid #C9EFD7;
        border-radius: 14px; padding: 10px 16px; margin: 4px 6px 4px 0;
    }}
    .metric-pill .val {{ font-family: 'Poppins'; font-weight: 700; font-size: 1.3rem; color: {PRIMARY_DARK}; }}
    .metric-pill .lbl {{ font-size: 0.78rem; color: #4B6E5F; }}

    .status-chip {{
        display: inline-block; padding: 6px 16px; border-radius: 999px;
        font-weight: 600; font-size: 0.95rem;
    }}
    .status-sesuai {{ background: #DCFCE7; color: #15803D; }}
    .status-tidak-sesuai {{ background: #FEE2E2; color: #B91C1C; }}
    .status-tidak-yakin {{ background: #FEF3C7; color: #92400E; }}
    .status-gangguan {{ background: #E5E7EB; color: #374151; }}

    .section-title {{
        display: flex; align-items: center; gap: 10px;
        margin: 1.6rem 0 0.6rem 0;
    }}
    .section-title h2 {{ margin: 0; }}
    .divider-glow {{
        height: 3px; border: none; border-radius: 3px; margin: 0.2rem 0 1.4rem 0;
        background: linear-gradient(90deg, {ACCENT}, transparent);
    }}

    .stButton>button {{
        background: linear-gradient(120deg, {PRIMARY} 0%, {PRIMARY_BRIGHT} 100%);
        color: white; border: none; border-radius: 12px; font-weight: 600;
        padding: 0.55rem 1.4rem; box-shadow: 0 8px 18px -8px rgba(20,108,67,0.55);
    }}
    .stButton>button:hover {{ filter: brightness(1.06); }}

    footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)


def page_setup(title: str, icon: str = "💊"):
    st.set_page_config(page_title=title, page_icon=icon, layout="wide")
    inject_base_css()


# ---------------------------------------------------------------------------
# Ikon SVG inline (buatan sendiri, tanpa dependensi internet)
# ---------------------------------------------------------------------------
def icon(name: str, size: int = 40, color: str = "#146C43") -> str:
    icons = {
        "scan": f'''<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none">
            <rect x="6" y="6" width="12" height="4" rx="2" fill="{color}"/>
            <rect x="6" y="6" width="4" height="12" rx="2" fill="{color}"/>
            <rect x="30" y="38" width="12" height="4" rx="2" fill="{color}"/>
            <rect x="38" y="30" width="4" height="12" rx="2" fill="{color}"/>
            <rect x="30" y="6" width="12" height="4" rx="2" fill="{color}"/>
            <rect x="38" y="6" width="4" height="12" rx="2" fill="{color}"/>
            <rect x="6" y="38" width="12" height="4" rx="2" fill="{color}"/>
            <rect x="6" y="30" width="4" height="12" rx="2" fill="{color}"/>
            <circle cx="24" cy="24" r="9" stroke="{color}" stroke-width="3"/>
            <circle cx="24" cy="24" r="3" fill="{color}"/>
        </svg>''',
        "pill": f'''<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none">
            <rect x="6" y="18" width="36" height="14" rx="7" fill="{color}" opacity="0.18"/>
            <path d="M14 32 L34 32 A9 9 0 0 0 34 14 L14 14 A9 9 0 0 0 14 32 Z" stroke="{color}" stroke-width="3"/>
            <line x1="24" y1="14" x2="24" y2="32" stroke="{color}" stroke-width="3"/>
        </svg>''',
        "chart": f'''<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none">
            <rect x="8" y="26" width="7" height="14" rx="2" fill="{color}" opacity="0.55"/>
            <rect x="20" y="16" width="7" height="24" rx="2" fill="{color}" opacity="0.8"/>
            <rect x="32" y="8" width="7" height="32" rx="2" fill="{color}"/>
        </svg>''',
        "shield": f'''<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none">
            <path d="M24 6 L40 12 V22 C40 33 33 40 24 43 C15 40 8 33 8 22 V12 Z" stroke="{color}" stroke-width="3" fill="{color}" fill-opacity="0.12"/>
            <path d="M17 24 L22 29 L32 18" stroke="{color}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>''',
        "brain": f'''<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none">
            <circle cx="18" cy="18" r="9" stroke="{color}" stroke-width="3" fill="{color}" fill-opacity="0.1"/>
            <circle cx="30" cy="18" r="9" stroke="{color}" stroke-width="3" fill="{color}" fill-opacity="0.1"/>
            <path d="M18 27 V34 M30 27 V34 M13 24 h22" stroke="{color}" stroke-width="3" stroke-linecap="round"/>
        </svg>''',
        "flask": f'''<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none">
            <path d="M19 6 H29 V18 L38 38 A4 4 0 0 1 34 44 H14 A4 4 0 0 1 10 38 L19 18 Z" stroke="{color}" stroke-width="3" fill="{color}" fill-opacity="0.12"/>
            <path d="M15 32 H33" stroke="{color}" stroke-width="3"/>
            <line x1="17" y1="6" x2="31" y2="6" stroke="{color}" stroke-width="3" stroke-linecap="round"/>
        </svg>''',
        "hospital": f'''<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none">
            <rect x="8" y="14" width="32" height="28" rx="3" stroke="{color}" stroke-width="3" fill="{color}" fill-opacity="0.1"/>
            <path d="M24 20 V32 M18 26 H30" stroke="{color}" stroke-width="3.4" stroke-linecap="round"/>
            <path d="M16 14 V8 H32 V14" stroke="{color}" stroke-width="3"/>
        </svg>''',
        "check-circle": f'''<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none">
            <circle cx="24" cy="24" r="18" fill="{color}" fill-opacity="0.14" stroke="{color}" stroke-width="3"/>
            <path d="M16 24 L21 30 L33 18" stroke="{color}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>''',
        "clock": f'''<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none">
            <circle cx="24" cy="24" r="17" stroke="{color}" stroke-width="3" fill="{color}" fill-opacity="0.1"/>
            <path d="M24 14 V24 L31 29" stroke="{color}" stroke-width="3.2" stroke-linecap="round"/>
        </svg>''',
    }
    return icons.get(name, "")


def hero(badge: str, title: str, subtitle: str):
    st.markdown(f"""
    <div class="hero-box">
        <span class="hero-badge">{badge}</span>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def feature_card(icon_name: str, title: str, desc: str):
    st.markdown(f"""
    <div class="green-card">
        {icon(icon_name, 38)}
        <h4>{title}</h4>
        <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)


def metric_pill(value: str, label: str):
    st.markdown(f"""
    <span class="metric-pill"><span class="val">{value}</span><span class="lbl">{label}</span></span>
    """, unsafe_allow_html=True)


def status_chip(status: str) -> str:
    mapping = {
        "SESUAI": ("status-sesuai", "✅ SESUAI"),
        "TIDAK_SESUAI": ("status-tidak-sesuai", "❌ TIDAK SESUAI"),
        "TIDAK_YAKIN": ("status-tidak-yakin", "⚠️ TIDAK YAKIN — perlu cek manual"),
        "GANGGUAN_DATA": ("status-gangguan", "⛔ GANGGUAN DATA"),
    }
    cls, text = mapping.get(status, ("status-gangguan", status))
    return f'<span class="status-chip {cls}">{text}</span>'


def section_title(icon_name: str, title: str):
    st.markdown(f"""
    <div class="section-title">{icon(icon_name, 30)}<h2>{title}</h2></div>
    <hr class="divider-glow">
    """, unsafe_allow_html=True)
