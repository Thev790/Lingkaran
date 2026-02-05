import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Wedge, Polygon, Circle
import matplotlib.patches as patches

# Konfigurasi halaman
st.set_page_config(
    page_title="Komponen Komponen pada Lingkaran",
    page_icon="⭕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Custom untuk styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 30px;
    }
    .component-title {
        font-size: 2rem;
        font-weight: bold;
        color: #1565C0;
        margin-bottom: 20px;
        padding: 10px;
        background: linear-gradient(90deg, #E3F2FD, #BBDEFB);
        border-radius: 10px;
        text-align: center;
    }
    .formula-box {
        background: linear-gradient(135deg, #FFF8E1, #FFECB3);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #FFA000;
        margin: 20px 0;
    }
    .result-box {
        background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #4CAF50;
        margin: 20px 0;
    }
    .info-box {
        background: linear-gradient(135deg, #F3E5F5, #E1BEE7);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 10px;
        margin: 5px 0;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .nav-button {
        background: linear-gradient(135deg, #42A5F5, #1976D2) !important;
        color: white !important;
    }
    .component-btn {
        background: linear-gradient(135deg, #66BB6A, #43A047) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Inisialisasi session state untuk navigasi
if 'current_slide' not in st.session_state:
    st.session_state.current_slide = 'menu'
if 'history' not in st.session_state:
    st.session_state.history = []

def go_to_slide(slide_name):
    st.session_state.history.append(st.session_state.current_slide)
    st.session_state.current_slide = slide_name

def go_back():
    if st.session_state.history:
        st.session_state.current_slide = st.session_state.history.pop()
    else:
        st.session_state.current_slide = 'menu'

def reset_app():
    st.session_state.current_slide = 'menu'
    st.session_state.history = []

# Fungsi untuk membuat visualisasi lingkaran
def draw_circle_with_radius(r):
    fig, ax = plt.subplots(figsize=(6, 6))
    circle = Circle((0, 0), r, fill=False, color='#1976D2', linewidth=3)
    ax.add_patch(circle)
    ax.plot([0, r], [0, 0], 'r-', linewidth=3, label=f'Jari-jari (r) = {r}')
    ax.plot(0, 0, 'ro', markersize=8)
    ax.text(r/2, 0.3, f'r = {r}', fontsize=12, color='red', fontweight='bold')
    ax.set_xlim(-r-1, r+1)
    ax.set_ylim(-r-1, r+1)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title('Jari-Jari Lingkaran', fontsize=14, fontweight='bold')
    return fig

def draw_circle_with_diameter(d):
    r = d / 2
    fig, ax = plt.subplots(figsize=(6, 6))
    circle = Circle((0, 0), r, fill=False, color='#1976D2', linewidth=3)
    ax.add_patch(circle)
    ax.plot([-r, r], [0, 0], 'g-', linewidth=3, label=f'Diameter (d) = {d}')
    ax.plot(0, 0, 'ro', markersize=8)
    ax.text(0, 0.5, f'd = {d}', fontsize=12, color='green', fontweight='bold', ha='center')
    ax.set_xlim(-r-1, r+1)
    ax.set_ylim(-r-1, r+1)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title('Diameter Lingkaran', fontsize=14, fontweight='bold')
    return fig

def draw_circle_area(r):
    fig, ax = plt.subplots(figsize=(6, 6))
    circle = Circle((0, 0), r, fill=True, color='#4CAF50', alpha=0.3, linewidth=3)
    ax.add_patch(circle)
    circle_border = Circle((0, 0), r, fill=False, color='#1976D2', linewidth=3)
    ax.add_patch(circle_border)
    ax.plot([0, r], [0, 0], 'r-', linewidth=2, label=f'r = {r}')
    ax.plot(0, 0, 'ro', markersize=8)
    ax.text(0, 0, f'Luas = π × {r}²', fontsize=12, color='darkgreen', fontweight='bold', ha='center')
    ax.set_xlim(-r-1, r+1)
    ax.set_ylim(-r-1, r+1)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title('Luas Lingkaran', fontsize=14, fontweight='bold')
    return fig

def draw_circle_circumference(r):
    fig, ax = plt.subplots(figsize=(6, 6))
    circle = Circle((0, 0), r, fill=False, color='#FF9800', linewidth=4)
    ax.add_patch(circle)
    ax.plot(0, 0, 'ro', markersize=8)
    # Tambahkan panah untuk menunjukkan keliling
    theta = np.linspace(0, 2*np.pi, 100)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    ax.plot(x, y, 'orange', linewidth=4, label=f'Keliling = 2π × {r}')
    ax.text(0, -r-0.5, f'Keliling = 2 × π × {r}', fontsize=11, color='darkorange', fontweight='bold', ha='center')
    ax.set_xlim(-r-1.5, r+1.5)
    ax.set_ylim(-r-1.5, r+1.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title('Keliling Lingkaran', fontsize=14, fontweight='bold')
    return fig

def draw_juring(r, theta_deg):
    fig, ax = plt.subplots(figsize=(7, 7))
    theta_rad = math.radians(theta_deg)
    
    # Gambar juring (sektor)
    wedge = Wedge((0, 0), r, 0, theta_deg, facecolor='#FF7043', alpha=0.4, edgecolor='#D84315', linewidth=3)
    ax.add_patch(wedge)
    
    # Gambar lingkaran lengkap (border saja)
    circle = Circle((0, 0), r, fill=False, color='#1976D2', linewidth=2, linestyle='--')
    ax.add_patch(circle)
    
    # Gambar garis jari-jari
    ax.plot([0, r], [0, 0], 'b-', linewidth=2.5)
    ax.plot([0, r * math.cos(theta_rad)], [0, r * math.sin(theta_rad)], 'b-', linewidth=2.5)
    
    # Gambar busur
    arc = Arc((0, 0), r*2, r*2, angle=0, theta1=0, theta2=theta_deg, color='red', linewidth=3)
    ax.add_patch(arc)
    
    # Label sudut
    ax.text(r*0.3*math.cos(theta_rad/2), r*0.3*math.sin(theta_rad/2), f'θ = {theta_deg}°', 
            fontsize=11, color='purple', fontweight='bold', ha='center')
    
    ax.plot(0, 0, 'ko', markersize=8)
    ax.set_xlim(-r-1, r+1)
    ax.set_ylim(-r-1, r+1)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title(f'Juring Lingkaran (θ = {theta_deg}°)', fontsize=14, fontweight='bold')
    return fig

def draw_tembereng(r, theta_deg):
    fig, ax = plt.subplots(figsize=(7, 7))
    theta_rad = math.radians(theta_deg)
    
    # Gambar lingkaran
    circle = Circle((0, 0), r, fill=False, color='#1976D2', linewidth=2)
    ax.add_patch(circle)
    
    # Gambar tembereng (area yang diarsir)
    x_tembereng = [0]
    y_tembereng = [0]
    for angle in np.linspace(0, theta_rad, 50):
        x_tembereng.append(r * math.cos(angle))
        y_tembereng.append(r * math.sin(angle))
    x_tembereng.append(0)
    y_tembereng.append(0)
    
    # Isi tembereng
    tembereng = Polygon(list(zip(x_tembereng, y_tembereng)), facecolor='#AB47BC', alpha=0.4, edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(tembereng)
    
    # Gambar busur
    arc = Arc((0, 0), r*2, r*2, angle=0, theta1=0, theta2=theta_deg, color='red', linewidth=3)
    ax.add_patch(arc)
    
    # Gambar tali busur
    ax.plot([r, r * math.cos(theta_rad)], [0, r * math.sin(theta_rad)], 'g-', linewidth=2.5, label='Tali Busur')
    
    # Label
    ax.text(r*0.5*math.cos(theta_rad/2), r*0.5*math.sin(theta_rad/2), f'θ = {theta_deg}°', 
            fontsize=11, color='purple', fontweight='bold', ha='center')
    
    ax.plot(0, 0, 'ko', markersize=8)
    ax.set_xlim(-r-1, r+1)
    ax.set_ylim(-r-1, r+1)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title(f'Tembereng Lingkaran (θ = {theta_deg}°)', fontsize=14, fontweight='bold')
    return fig

def draw_busur(r, theta_deg):
    fig, ax = plt.subplots(figsize=(7, 7))
    
    # Gambar lingkaran (border saja)
    circle = Circle((0, 0), r, fill=False, color='#1976D2', linewidth=2)
    ax.add_patch(circle)
    
    # Gambar busur dengan penekanan
    theta_rad = math.radians(theta_deg)
    arc = Arc((0, 0), r*2, r*2, angle=0, theta1=0, theta2=theta_deg, color='#FF5722', linewidth=5)
    ax.add_patch(arc)
    
    # Gambar jari-jari
    ax.plot([0, r], [0, 0], 'b-', linewidth=2)
    ax.plot([0, r * math.cos(theta_rad)], [0, r * math.sin(theta_rad)], 'b-', linewidth=2)
    
    # Panah menunjukkan busur
    mid_angle = theta_rad / 2
    ax.annotate('', xy=(r*0.8*math.cos(mid_angle+0.1), r*0.8*math.sin(mid_angle+0.1)),
                xytext=(r*0.8*math.cos(mid_angle-0.1), r*0.8*math.sin(mid_angle-0.1)),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    
    ax.text(r*0.5*math.cos(mid_angle), r*0.5*math.sin(mid_angle)+0.5, 'Busur', 
            fontsize=12, color='red', fontweight='bold', ha='center')
    ax.text(r*0.3*math.cos(mid_angle), r*0.3*math.sin(mid_angle), f'θ = {theta_deg}°', 
            fontsize=11, color='purple', fontweight='bold', ha='center')
    
    ax.plot(0, 0, 'ko', markersize=8)
    ax.set_xlim(-r-1, r+1)
    ax.set_ylim(-r-1, r+1)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title(f'Busur Lingkaran (θ = {theta_deg}°)', fontsize=14, fontweight='bold')
    return fig

def draw_tali_busur(r, theta_deg):
    fig, ax = plt.subplots(figsize=(7, 7))
    theta_rad = math.radians(theta_deg)
    
    # Gambar lingkaran
    circle = Circle((0, 0), r, fill=False, color='#1976D2', linewidth=2)
    ax.add_patch(circle)
    
    # Gambar busur
    arc = Arc((0, 0), r*2, r*2, angle=0, theta1=0, theta2=theta_deg, color='orange', linewidth=2)
    ax.add_patch(arc)
    
    # Gambar tali busur (garis hijau tebal)
    x1, y1 = r, 0
    x2, y2 = r * math.cos(theta_rad), r * math.sin(theta_rad)
    ax.plot([x1, x2], [y1, y2], 'g-', linewidth=4, label='Tali Busur')
    
    # Titik ujung tali busur
    ax.plot(x1, y1, 'go', markersize=10)
    ax.plot(x2, y2, 'go', markersize=10)
    
    # Label sudut
    ax.text(r*0.3*math.cos(theta_rad/2), r*0.3*math.sin(theta_rad/2), f'θ = {theta_deg}°', 
            fontsize=11, color='purple', fontweight='bold', ha='center')
    
    # Label tali busur
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    ax.text(mid_x, mid_y + 0.5, 'Tali Busur', fontsize=11, color='green', fontweight='bold', ha='center')
    
    ax.plot(0, 0, 'ko', markersize=8)
    ax.set_xlim(-r-1, r+1)
    ax.set_ylim(-r-1, r+1)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title(f'Tali Busur Lingkaran (θ = {theta_deg}°)', fontsize=14, fontweight='bold')
    return fig

# ==================== HALAMAN MENU UTAMA ====================
if st.session_state.current_slide == 'menu':
    st.markdown('<h1 class="main-title">⭕ Komponen Komponen pada Lingkaran ⭕</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Pelajari 8 komponen penting dalam lingkaran dengan kalkulator interaktif!</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Layout 4x2 untuk tombol komponen
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📐 Luas Lingkaran", key="btn_luas", help="Klik untuk melihat rumus dan kalkulator luas lingkaran"):
            go_to_slide('luas')
            st.rerun()
        if st.button("📏 Jari-Jari", key="btn_jari", help="Klik untuk melihat penjelasan jari-jari lingkaran"):
            go_to_slide('jari_jari')
            st.rerun()
    
    with col2:
        if st.button("🔄 Keliling Lingkaran", key="btn_keliling", help="Klik untuk melihat rumus dan kalkulator keliling lingkaran"):
            go_to_slide('keliling')
            st.rerun()
        if st.button("➖ Diameter", key="btn_diameter", help="Klik untuk melihat penjelasan diameter lingkaran"):
            go_to_slide('diameter')
            st.rerun()
    
    with col3:
        if st.button("🍕 Juring Lingkaran", key="btn_juring", help="Klik untuk melihat rumus dan kalkulator juring lingkaran"):
            go_to_slide('juring')
            st.rerun()
        if st.button("〰️ Busur Lingkaran", key="btn_busur", help="Klik untuk melihat rumus dan kalkulator busur lingkaran"):
            go_to_slide('busur')
            st.rerun()
    
    with col4:
        if st.button("🎯 Tembereng Lingkaran", key="btn_tembereng", help="Klik untuk melihat rumus dan kalkulator tembereng lingkaran"):
            go_to_slide('tembereng')
            st.rerun()
        if st.button("➖ Tali Busur", key="btn_tali_busur", help="Klik untuk melihat rumus dan kalkulator tali busur"):
            go_to_slide('tali_busur')
            st.rerun()
    
    st.markdown("---")
    
    # Informasi umum tentang lingkaran
    st.markdown("""
    <div class="info-box">
   <h3 style="color:#000000;">📚 Tentang Lingkaran</h3>

<p style="color:#000000;">
<strong>Lingkaran</strong> adalah bangun datar yang terdiri dari semua titik 
yang berjarak sama dari suatu titik tetap yang disebut 
<strong>pusat lingkaran</strong>.
</p>

<p style="color:#000000;">
<strong>Nilai π (pi)</strong> ≈ 3.14159 atau 22/7
</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabel komponen
    st.markdown("### 📋 Daftar Komponen yang Akan Dipelajari:")
    
    data = {
        "No": [1, 2, 3, 4, 5, 6, 7, 8],
        "Komponen": ["Luas Lingkaran", "Keliling Lingkaran", "Juring Lingkaran", "Tembereng Lingkaran",
                     "Jari-Jari Lingkaran", "Diameter Lingkaran", "Busur Lingkaran", "Tali Busur Lingkaran"],
        "Simbol": ["L", "K", "-", "-", "r", "d", "-", "-"],
        "Satuan": ["cm², m²", "cm, m", "cm², m²", "cm², m²", "cm, m", "cm, m", "cm, m", "cm, m"]
    }
    
    st.table(data)

# ==================== 1. LUAS LINGKARAN ====================
elif st.session_state.current_slide == 'luas':
    st.markdown('<h2 class="component-title">📐 1. Luas Lingkaran</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="formula-box">
            <h4>📖 Rumus Luas Lingkaran:</h4>
            <h3 style="text-align: center; color: #1565C0;">
                L = π × r²
            </h3>
            <p>atau</p>
            <h3 style="text-align: center; color: #1565C0;">
                L = π × (d/2)²
            </h3>
            <p><strong>Keterangan:</strong></p>
            <ul>
                <li><strong>L</strong> = Luas lingkaran</li>
                <li><strong>π</strong> = 3.14 atau 22/7</li>
                <li><strong>r</strong> = Jari-jari lingkaran</li>
                <li><strong>d</strong> = Diameter lingkaran</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🧮 Kalkulator Luas Lingkaran")
        
        input_type = st.radio("Pilih input:", ["Jari-Jari (r)", "Diameter (d)"])
        
        if input_type == "Jari-Jari (r)":
            r = st.number_input("Masukkan jari-jari (r):", min_value=0.0, value=7.0, step=0.1)
            if r > 0:
                luas = math.pi * r**2
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>L = π × r²</p>
                    <p>L = {math.pi:.5f} × {r}²</p>
                    <p>L = {math.pi:.5f} × {r**2}</p>
                    <h3>L = {luas:.2f} satuan luas</h3>
                </div>
                """, unsafe_allow_html=True)
                st.pyplot(draw_circle_area(r))
        else:
            d = st.number_input("Masukkan diameter (d):", min_value=0.0, value=14.0, step=0.1)
            if d > 0:
                r = d / 2
                luas = math.pi * r**2
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>L = π × (d/2)²</p>
                    <p>L = {math.pi:.5f} × ({d}/2)²</p>
                    <p>L = {math.pi:.5f} × {r}²</p>
                    <h3>L = {luas:.2f} satuan luas</h3>
                </div>
                """, unsafe_allow_html=True)
                st.pyplot(draw_circle_area(r))
    
    # Navigasi
    st.markdown("---")
    col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])
    with col_nav1:
        if st.button("⬅️ Kembali ke Menu", key="back_luas"):
            go_back()
            st.rerun()
    with col_nav2:
        if st.button("🏠 Menu Utama", key="menu_luas"):
            reset_app()
            st.rerun()
    with col_nav3:
        if st.button("Lanjut ke Keliling ➡️", key="next_luas"):
            go_to_slide('keliling')
            st.rerun()

# ==================== 2. KELILING LINGKARAN ====================
elif st.session_state.current_slide == 'keliling':
    st.markdown('<h2 class="component-title">🔄 2. Keliling Lingkaran</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="formula-box">
            <h4>📖 Rumus Keliling Lingkaran:</h4>
            <h3 style="text-align: center; color: #1565C0;">
                K = 2 × π × r
            </h3>
            <p>atau</p>
            <h3 style="text-align: center; color: #1565C0;">
                K = π × d
            </h3>
            <p><strong>Keterangan:</strong></p>
            <ul>
                <li><strong>K</strong> = Keliling lingkaran</li>
                <li><strong>π</strong> = 3.14 atau 22/7</li>
                <li><strong>r</strong> = Jari-jari lingkaran</li>
                <li><strong>d</strong> = Diameter lingkaran</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🧮 Kalkulator Keliling Lingkaran")
        
        input_type = st.radio("Pilih input:", ["Jari-Jari (r)", "Diameter (d)"], key="keliling_input")
        
        if input_type == "Jari-Jari (r)":
            r = st.number_input("Masukkan jari-jari (r):", min_value=0.0, value=7.0, step=0.1, key="keliling_r")
            if r > 0:
                keliling = 2 * math.pi * r
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>K = 2 × π × r</p>
                    <p>K = 2 × {math.pi:.5f} × {r}</p>
                    <h3>K = {keliling:.2f} satuan panjang</h3>
                </div>
                """, unsafe_allow_html=True)
                st.pyplot(draw_circle_circumference(r))
        else:
            d = st.number_input("Masukkan diameter (d):", min_value=0.0, value=14.0, step=0.1, key="keliling_d")
            if d > 0:
                keliling = math.pi * d
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>K = π × d</p>
                    <p>K = {math.pi:.5f} × {d}</p>
                    <h3>K = {keliling:.2f} satuan panjang</h3>
                </div>
                """, unsafe_allow_html=True)
                st.pyplot(draw_circle_circumference(d/2))
    
    # Navigasi
    st.markdown("---")
    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([1, 1, 1, 1])
    with col_nav1:
        if st.button("⬅️ Kembali", key="back_keliling"):
            go_back()
            st.rerun()
    with col_nav2:
        if st.button("🏠 Menu", key="menu_keliling"):
            reset_app()
            st.rerun()
    with col_nav3:
        if st.button("⬅️ Luas", key="prev_keliling"):
            go_to_slide('luas')
            st.rerun()
    with col_nav4:
        if st.button("Juring ➡️", key="next_keliling"):
            go_to_slide('juring')
            st.rerun()

# ==================== 3. JURING LINGKARAN ====================
elif st.session_state.current_slide == 'juring':
    st.markdown('<h2 class="component-title">🍕 3. Juring Lingkaran</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="formula-box">
            <h4>📖 Rumus Juring Lingkaran:</h4>
            <h3 style="text-align: center; color: #1565C0;">
                Luas Juring = (θ/360°) × π × r²
            </h3>
            <p>atau</p>
            <h3 style="text-align: center; color: #1565C0;">
                Luas Juring = (θ/360°) × Luas Lingkaran
            </h3>
            <p><strong>Keterangan:</strong></p>
            <ul>
                <li><strong>Luas Juring</strong> = Luas sektor/juring lingkaran</li>
                <li><strong>θ (theta)</strong> = Sudut pusat dalam derajat</li>
                <li><strong>r</strong> = Jari-jari lingkaran</li>
                <li><strong>π</strong> = 3.14 atau 22/7</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>💡 Penjelasan:</h4>
            <p><strong>Juring</strong> adalah daerah yang dibatasi oleh dua jari-jari dan busur lingkaran yang menghubungkan ujung-ujung jari-jari tersebut.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🧮 Kalkulator Juring Lingkaran")
        
        r = st.number_input("Masukkan jari-jari (r):", min_value=0.0, value=10.0, step=0.1, key="juring_r")
        theta = st.number_input("Masukkan sudut (θ) dalam derajat:", min_value=0.0, max_value=360.0, value=60.0, step=1.0, key="juring_theta")
        
        if r > 0 and theta > 0:
            luas_juring = (theta / 360) * math.pi * r**2
            luas_lingkaran = math.pi * r**2
            st.markdown(f"""
            <div class="result-box">
                <h4>✅ Hasil Perhitungan:</h4>
                <p>Luas Juring = (θ/360°) × π × r²</p>
                <p>Luas Juring = ({theta}/360) × {math.pi:.5f} × {r}²</p>
                <p>Luas Juring = {(theta/360):.4f} × {luas_lingkaran:.2f}</p>
                <h3>Luas Juring = {luas_juring:.2f} satuan luas</h3>
                <hr>
                <p><strong>Luas Lingkaran Penuh:</strong> {luas_lingkaran:.2f}</p>
                <p><strong>Perbandingan:</strong> {theta}/360 = {(theta/360)*100:.1f}% dari lingkaran penuh</p>
            </div>
            """, unsafe_allow_html=True)
            st.pyplot(draw_juring(r, theta))
    
    # Navigasi
    st.markdown("---")
    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([1, 1, 1, 1])
    with col_nav1:
        if st.button("⬅️ Kembali", key="back_juring"):
            go_back()
            st.rerun()
    with col_nav2:
        if st.button("🏠 Menu", key="menu_juring"):
            reset_app()
            st.rerun()
    with col_nav3:
        if st.button("⬅️ Keliling", key="prev_juring"):
            go_to_slide('keliling')
            st.rerun()
    with col_nav4:
        if st.button("Tembereng ➡️", key="next_juring"):
            go_to_slide('tembereng')
            st.rerun()

# ==================== 4. TEMBERENG LINGKARAN ====================
elif st.session_state.current_slide == 'tembereng':
    st.markdown('<h2 class="component-title">🎯 4. Tembereng Lingkaran</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="formula-box">
            <h4>📖 Rumus Tembereng Lingkaran:</h4>
            <h3 style="text-align: center; color: #1565C0;">
                Luas Tembereng = Luas Juring - Luas Segitiga
            </h3>
            <p>atau</p>
            <h3 style="text-align: center; color: #1565C0;">
                L = (θ/360°) × π × r² - ½ × r² × sin(θ)
            </h3>
            <p><strong>Keterangan:</strong></p>
            <ul>
                <li><strong>L</strong> = Luas tembereng</li>
                <li><strong>θ</strong> = Sudut pusat dalam derajat</li>
                <li><strong>r</strong> = Jari-jari lingkaran</li>
                <li><strong>Luas Juring</strong> = (θ/360°) × π × r²</li>
                <li><strong>Luas Segitiga</strong> = ½ × r² × sin(θ)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>💡 Penjelasan:</h4>
            <p><strong>Tembereng</strong> adalah daerah yang dibatasi oleh busur lingkaran dan tali busur yang menghubungkan ujung-ujung busur tersebut.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🧮 Kalkulator Tembereng Lingkaran")
        
        r = st.number_input("Masukkan jari-jari (r):", min_value=0.0, value=10.0, step=0.1, key="tembereng_r")
        theta = st.number_input("Masukkan sudut (θ) dalam derajat:", min_value=0.0, max_value=360.0, value=60.0, step=1.0, key="tembereng_theta")
        
        if r > 0 and theta > 0:
            theta_rad = math.radians(theta)
            luas_juring = (theta / 360) * math.pi * r**2
            luas_segitiga = 0.5 * r**2 * math.sin(theta_rad)
            luas_tembereng = luas_juring - luas_segitiga
            
            st.markdown(f"""
            <div class="result-box">
                <h4>✅ Hasil Perhitungan:</h4>
                <p><strong>Langkah 1:</strong> Hitung Luas Juring</p>
                <p>Luas Juring = ({theta}/360) × π × {r}² = {luas_juring:.2f}</p>
                <br>
                <p><strong>Langkah 2:</strong> Hitung Luas Segitiga</p>
                <p>Luas Segitiga = ½ × {r}² × sin({theta}°)</p>
                <p>Luas Segitiga = ½ × {r**2} × {math.sin(theta_rad):.4f} = {luas_segitiga:.2f}</p>
                <br>
                <p><strong>Langkah 3:</strong> Hitung Luas Tembereng</p>
                <p>Luas Tembereng = {luas_juring:.2f} - {luas_segitiga:.2f}</p>
                <h3>Luas Tembereng = {luas_tembereng:.2f} satuan luas</h3>
            </div>
            """, unsafe_allow_html=True)
            st.pyplot(draw_tembereng(r, theta))
    
    # Navigasi
    st.markdown("---")
    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([1, 1, 1, 1])
    with col_nav1:
        if st.button("⬅️ Kembali", key="back_tembereng"):
            go_back()
            st.rerun()
    with col_nav2:
        if st.button("🏠 Menu", key="menu_tembereng"):
            reset_app()
            st.rerun()
    with col_nav3:
        if st.button("⬅️ Juring", key="prev_tembereng"):
            go_to_slide('juring')
            st.rerun()
    with col_nav4:
        if st.button("Jari-Jari ➡️", key="next_tembereng"):
            go_to_slide('jari_jari')
            st.rerun()

# ==================== 5. JARI-JARI LINGKARAN ====================
elif st.session_state.current_slide == 'jari_jari':
    st.markdown('<h2 class="component-title">📏 5. Jari-Jari Lingkaran</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="formula-box">
            <h4>📖 Definisi dan Rumus Jari-Jari:</h4>
            <p><strong>Jari-jari (r)</strong> adalah jarak dari pusat lingkaran ke tepi lingkaran.</p>
            <h3 style="text-align: center; color: #1565C0;">
                r = d / 2
            </h3>
            <p>atau</p>
            <h3 style="text-align: center; color: #1565C0;">
                r = √(L / π)
            </h3>
            <p>atau</p>
            <h3 style="text-align: center; color: #1565C0;">
                r = K / (2 × π)
            </h3>
            <p><strong>Keterangan:</strong></p>
            <ul>
                <li><strong>r</strong> = Jari-jari lingkaran</li>
                <li><strong>d</strong> = Diameter lingkaran</li>
                <li><strong>L</strong> = Luas lingkaran</li>
                <li><strong>K</strong> = Keliling lingkaran</li>
                <li><strong>π</strong> = 3.14 atau 22/7</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>💡 Fakta Menarik:</h4>
            <p>Jari-jari adalah <strong>setengah</strong> dari diameter. Semua jari-jari dalam satu lingkaran memiliki panjang yang sama!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🧮 Kalkulator Jari-Jari")
        
        input_type = st.radio("Hitung jari-jari dari:", ["Diameter (d)", "Luas (L)", "Keliling (K)"])
        
        if input_type == "Diameter (d)":
            d = st.number_input("Masukkan diameter (d):", min_value=0.0, value=14.0, step=0.1, key="jari_d")
            if d > 0:
                r = d / 2
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>r = d / 2</p>
                    <p>r = {d} / 2</p>
                    <h3>r = {r:.2f} satuan panjang</h3>
                </div>
                """, unsafe_allow_html=True)
                st.pyplot(draw_circle_with_radius(r))
                
        elif input_type == "Luas (L)":
            L = st.number_input("Masukkan luas (L):", min_value=0.0, value=154.0, step=0.1, key="jari_L")
            if L > 0:
                r = math.sqrt(L / math.pi)
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>r = √(L / π)</p>
                    <p>r = √({L} / {math.pi:.5f})</p>
                    <p>r = √{L/math.pi:.2f}</p>
                    <h3>r = {r:.2f} satuan panjang</h3>
                </div>
                """, unsafe_allow_html=True)
                st.pyplot(draw_circle_with_radius(r))
                
        else:  # Keliling
            K = st.number_input("Masukkan keliling (K):", min_value=0.0, value=44.0, step=0.1, key="jari_K")
            if K > 0:
                r = K / (2 * math.pi)
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>r = K / (2 × π)</p>
                    <p>r = {K} / (2 × {math.pi:.5f})</p>
                    <p>r = {K} / {2*math.pi:.5f}</p>
                    <h3>r = {r:.2f} satuan panjang</h3>
                </div>
                """, unsafe_allow_html=True)
                st.pyplot(draw_circle_with_radius(r))
    
    # Navigasi
    st.markdown("---")
    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([1, 1, 1, 1])
    with col_nav1:
        if st.button("⬅️ Kembali", key="back_jari"):
            go_back()
            st.rerun()
    with col_nav2:
        if st.button("🏠 Menu", key="menu_jari"):
            reset_app()
            st.rerun()
    with col_nav3:
        if st.button("⬅️ Tembereng", key="prev_jari"):
            go_to_slide('tembereng')
            st.rerun()
    with col_nav4:
        if st.button("Diameter ➡️", key="next_jari"):
            go_to_slide('diameter')
            st.rerun()

# ==================== 6. DIAMETER LINGKARAN ====================
elif st.session_state.current_slide == 'diameter':
    st.markdown('<h2 class="component-title">➖ 6. Diameter Lingkaran</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="formula-box">
            <h4>📖 Definisi dan Rumus Diameter:</h4>
            <p><strong>Diameter (d)</strong> adalah garis lurus yang menghubungkan dua titik pada lingkaran dan melalui pusat lingkaran.</p>
            <h3 style="text-align: center; color: #1565C0;">
                d = 2 × r
            </h3>
            <p>atau</p>
            <h3 style="text-align: center; color: #1565C0;">
                d = K / π
            </h3>
            <p>atau</p>
            <h3 style="text-align: center; color: #1565C0;">
                d = 2 × √(L / π)
            </h3>
            <p><strong>Keterangan:</strong></p>
            <ul>
                <li><strong>d</strong> = Diameter lingkaran</li>
                <li><strong>r</strong> = Jari-jari lingkaran</li>
                <li><strong>L</strong> = Luas lingkaran</li>
                <li><strong>K</strong> = Keliling lingkaran</li>
                <li><strong>π</strong> = 3.14 atau 22/7</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>💡 Fakta Menarik:</h4>
            <p>Diameter adalah <strong>garis terpanjang</strong> yang dapat ditarik dalam lingkaran. Diameter = 2 × Jari-jari</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🧮 Kalkulator Diameter")
        
        input_type = st.radio("Hitung diameter dari:", ["Jari-Jari (r)", "Luas (L)", "Keliling (K)"], key="diameter_input")
        
        if input_type == "Jari-Jari (r)":
            r = st.number_input("Masukkan jari-jari (r):", min_value=0.0, value=7.0, step=0.1, key="diameter_r")
            if r > 0:
                d = 2 * r
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>d = 2 × r</p>
                    <p>d = 2 × {r}</p>
                    <h3>d = {d:.2f} satuan panjang</h3>
                </div>
                """, unsafe_allow_html=True)
                st.pyplot(draw_circle_with_diameter(d))
                
        elif input_type == "Luas (L)":
            L = st.number_input("Masukkan luas (L):", min_value=0.0, value=154.0, step=0.1, key="diameter_L")
            if L > 0:
                d = 2 * math.sqrt(L / math.pi)
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>d = 2 × √(L / π)</p>
                    <p>d = 2 × √({L} / {math.pi:.5f})</p>
                    <p>d = 2 × √{L/math.pi:.2f}</p>
                    <p>d = 2 × {math.sqrt(L/math.pi):.2f}</p>
                    <h3>d = {d:.2f} satuan panjang</h3>
                </div>
                """, unsafe_allow_html=True)
                st.pyplot(draw_circle_with_diameter(d))
                
        else:  # Keliling
            K = st.number_input("Masukkan keliling (K):", min_value=0.0, value=44.0, step=0.1, key="diameter_K")
            if K > 0:
                d = K / math.pi
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>d = K / π</p>
                    <p>d = {K} / {math.pi:.5f}</p>
                    <h3>d = {d:.2f} satuan panjang</h3>
                </div>
                """, unsafe_allow_html=True)
                st.pyplot(draw_circle_with_diameter(d))
    
    # Navigasi
    st.markdown("---")
    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([1, 1, 1, 1])
    with col_nav1:
        if st.button("⬅️ Kembali", key="back_diameter"):
            go_back()
            st.rerun()
    with col_nav2:
        if st.button("🏠 Menu", key="menu_diameter"):
            reset_app()
            st.rerun()
    with col_nav3:
        if st.button("⬅️ Jari-Jari", key="prev_diameter"):
            go_to_slide('jari_jari')
            st.rerun()
    with col_nav4:
        if st.button("Busur ➡️", key="next_diameter"):
            go_to_slide('busur')
            st.rerun()

# ==================== 7. BUSUR LINGKARAN ====================
elif st.session_state.current_slide == 'busur':
    st.markdown('<h2 class="component-title">〰️ 7. Busur Lingkaran</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="formula-box">
            <h4>📖 Rumus Panjang Busur Lingkaran:</h4>
            <h3 style="text-align: center; color: #1565C0;">
                Panjang Busur = (θ/360°) × 2 × π × r
            </h3>
            <p>atau</p>
            <h3 style="text-align: center; color: #1565C0;">
                Panjang Busur = (θ/360°) × Keliling Lingkaran
            </h3>
            <p><strong>Keterangan:</strong></p>
            <ul>
                <li><strong>Panjang Busur</strong> = Panjang lengkung busur</li>
                <li><strong>θ (theta)</strong> = Sudut pusat dalam derajat</li>
                <li><strong>r</strong> = Jari-jari lingkaran</li>
                <li><strong>π</strong> = 3.14 atau 22/7</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>💡 Penjelasan:</h4>
            <p><strong>Busur</strong> adalah bagian lengkung dari keliling lingkaran yang dibatasi oleh dua titik pada lingkaran.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🧮 Kalkulator Busur Lingkaran")
        
        r = st.number_input("Masukkan jari-jari (r):", min_value=0.0, value=10.0, step=0.1, key="busur_r")
        theta = st.number_input("Masukkan sudut (θ) dalam derajat:", min_value=0.0, max_value=360.0, value=60.0, step=1.0, key="busur_theta")
        
        if r > 0 and theta > 0:
            panjang_busur = (theta / 360) * 2 * math.pi * r
            keliling_penuh = 2 * math.pi * r
            st.markdown(f"""
            <div class="result-box">
                <h4>✅ Hasil Perhitungan:</h4>
                <p>Panjang Busur = (θ/360°) × 2 × π × r</p>
                <p>Panjang Busur = ({theta}/360) × 2 × {math.pi:.5f} × {r}</p>
                <p>Panjang Busur = {(theta/360):.4f} × {keliling_penuh:.2f}</p>
                <h3>Panjang Busur = {panjang_busur:.2f} satuan panjang</h3>
                <hr>
                <p><strong>Keliling Lingkaran Penuh:</strong> {keliling_penuh:.2f}</p>
                <p><strong>Perbandingan:</strong> {theta}/360 = {(theta/360)*100:.1f}% dari keliling penuh</p>
            </div>
            """, unsafe_allow_html=True)
            st.pyplot(draw_busur(r, theta))
    
    # Navigasi
    st.markdown("---")
    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([1, 1, 1, 1])
    with col_nav1:
        if st.button("⬅️ Kembali", key="back_busur"):
            go_back()
            st.rerun()
    with col_nav2:
        if st.button("🏠 Menu", key="menu_busur"):
            reset_app()
            st.rerun()
    with col_nav3:
        if st.button("⬅️ Diameter", key="prev_busur"):
            go_to_slide('diameter')
            st.rerun()
    with col_nav4:
        if st.button("Tali Busur ➡️", key="next_busur"):
            go_to_slide('tali_busur')
            st.rerun()

# ==================== 8. TALI BUSUR LINGKARAN ====================
elif st.session_state.current_slide == 'tali_busur':
    st.markdown('<h2 class="component-title">➖ 8. Tali Busur Lingkaran</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="formula-box">
            <h4>📖 Rumus Panjang Tali Busur:</h4>
            <h3 style="text-align: center; color: #1565C0;">
                Panjang Tali Busur = 2 × r × sin(θ/2)
            </h3>
            <p>atau</p>
            <h3 style="text-align: center; color: #1565C0;">
                t = 2 × √(r² - a²)
            </h3>
            <p><em>(jika diketahui jarak dari pusat ke tali busur = a)</em></p>
            <p><strong>Keterangan:</strong></p>
            <ul>
                <li><strong>t</strong> = Panjang tali busur</li>
                <li><strong>r</strong> = Jari-jari lingkaran</li>
                <li><strong>θ</strong> = Sudut pusat dalam derajat</li>
                <li><strong>a</strong> = Jarak dari pusat ke tali busur</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>💡 Penjelasan:</h4>
            <p><strong>Tali Busur</strong> adalah garis lurus yang menghubungkan dua titik pada lingkaran. Tali busur tidak melalui pusat lingkaran (kecuali jika sudut = 180°, maka tali busur = diameter).</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🧮 Kalkulator Tali Busur")
        
        input_method = st.radio("Metode input:", ["Menggunakan Sudut (θ)", "Menggunakan Jarak dari Pusat (a)"])
        
        if input_method == "Menggunakan Sudut (θ)":
            r = st.number_input("Masukkan jari-jari (r):", min_value=0.0, value=10.0, step=0.1, key="tali_r")
            theta = st.number_input("Masukkan sudut (θ) dalam derajat:", min_value=0.0, max_value=180.0, value=60.0, step=1.0, key="tali_theta")
            
            if r > 0 and theta > 0:
                theta_rad = math.radians(theta)
                panjang_tali = 2 * r * math.sin(theta_rad / 2)
                
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>Panjang Tali Busur = 2 × r × sin(θ/2)</p>
                    <p>Panjang Tali Busur = 2 × {r} × sin({theta}°/2)</p>
                    <p>Panjang Tali Busur = 2 × {r} × sin({theta/2}°)</p>
                    <p>Panjang Tali Busur = 2 × {r} × {math.sin(theta_rad/2):.4f}</p>
                    <h3>Panjang Tali Busur = {panjang_tali:.2f} satuan panjang</h3>
                </div>
                """, unsafe_allow_html=True)
                st.pyplot(draw_tali_busur(r, theta))
                
        else:  # Menggunakan jarak dari pusat
            r = st.number_input("Masukkan jari-jari (r):", min_value=0.0, value=10.0, step=0.1, key="tali_r2")
            a = st.number_input("Masukkan jarak dari pusat ke tali busur (a):", min_value=0.0, value=5.0, step=0.1, key="tali_a")
            
            if r > 0 and a >= 0 and a <= r:
                panjang_tali = 2 * math.sqrt(r**2 - a**2)
                
                st.markdown(f"""
                <div class="result-box">
                    <h4>✅ Hasil Perhitungan:</h4>
                    <p>Panjang Tali Busur = 2 × √(r² - a²)</p>
                    <p>Panjang Tali Busur = 2 × √({r}² - {a}²)</p>
                    <p>Panjang Tali Busur = 2 × √({r**2} - {a**2})</p>
                    <p>Panjang Tali Busur = 2 × √{r**2 - a**2}</p>
                    <p>Panjang Tali Busur = 2 × {math.sqrt(r**2 - a**2):.4f}</p>
                    <h3>Panjang Tali Busur = {panjang_tali:.2f} satuan panjang</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Hitung sudut untuk visualisasi
                if a < r:
                    theta = 2 * math.degrees(math.acos(a / r))
                    st.pyplot(draw_tali_busur(r, theta))
            elif a > r:
                st.error("⚠️ Jarak dari pusat (a) tidak boleh lebih besar dari jari-jari (r)!")
    
    # Navigasi
    st.markdown("---")
    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([1, 1, 1, 1])
    with col_nav1:
        if st.button("⬅️ Kembali", key="back_tali"):
            go_back()
            st.rerun()
    with col_nav2:
        if st.button("🏠 Menu", key="menu_tali"):
            reset_app()
            st.rerun()
    with col_nav3:
        if st.button("⬅️ Busur", key="prev_tali"):
            go_to_slide('busur')
            st.rerun()
    with col_nav4:
        if st.button("🎉 Selesai!", key="finish"):
            go_to_slide('menu')
            st.rerun()

# Footer
def render_footer():
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #E3F2FD, #BBDEFB); border-radius: 10px;">
        <p style="font-size: 16px; color: #1565C0; margin: 0;">
            <strong>🎓 Dibuat dengan ❤️ untuk Pembelajaran Matematika</strong><br>
            <span style="font-size: 14px;">Komponen Komponen pada Lingkaran - Streamlit App</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

render_footer()
