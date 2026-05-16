import streamlit as st
from groq import Groq
import pandas as pd
import numpy as np

# --- 1. AYARLAR VE API ---
# Secrets'tan çekmeyi dener
try:
   # --- 1. AYARLAR VE API ---
    GROQ_API_KEY = "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"
except:
    GROQ_API_KEY = "" # Eğer hata alırsan buraya gsk_ ile başlayan kodu tırnak içine yazabilirsin

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Rüzgar Vatansever | Pro Terminal", layout="wide")

# --- 2. YAN PANEL ---
with st.sidebar:
    st.title("⚙️ Kontrol Paneli")
    st.subheader("🎨 Görsel Ayarlar")
    grafik_rengi = st.color_picker("Grafik Rengi Seç", "#00FFAA")
    st.markdown("---")
    st.subheader("📞 İletişim")
    st.write("📧 **E-posta:** 2010ruzgarvatansever2010@gmail.com")
    st.write("💻 **GitHub:** github.com/rukgar1923")
    if st.button("Sistem Durumu"):
        st.toast("Tüm sistemler aktif! 🚀")

# --- 3. ANA PANEL ---
st.title("🚀 İleri Seviye Mühendislik Terminali v6.2")

tab1, tab2, tab3 = st.tabs(["📊 Teknik Hesaplamalar", "📈 Performans Grafikleri", "⚡ AI Analiz"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛠️ Tasarım Parametreleri")
        with st.container(border=True):
            k_aciklik = st.slider("Kanat Açıklığı (cm)", 100, 400, 200)
            a_toplam = st.number_input("Toplam Ağırlık (g)", value=2500)
            p_kapasite = st.number_input("Pil Kapasitesi (mAh)", value=5000)
            a_cekis = st.number_input("Ortalama Akım Çekişi (A)", value=25)
            itki_hedef = st.slider("Hedef İtki/Ağırlık Oranı", 1.0, 5.0, 1.80)

    with col2:
        st.subheader("🔢 Mühendislik Çıktıları")
        # HESAPLAMALAR
        itki_gereken = (a_toplam * itki_hedef) / 1000
        sure_dakika = (p_kapasite / 1000) / a_cekis * 60
        k_alani = (k_aciklik / 100) * 0.3 
        k_yukleme = a_toplam / (k_alani * 10)
        verimlilik = (itki_gereken / (a_cekis * 11.1)) * 100 if a_cekis > 0 else 0
        
        c1, c2 = st.columns(2)
        c1.metric("Gereken Toplam İtki", f"{round(itki_gereken, 2)} kg")
        c1.metric("Tahmini Uçuş Süresi", f"{round(sure_dakika, 1)} dk")
        c2.metric("Kanat Yüklemesi", f"{round(k_yukleme, 1)} g/dm²")
        c2.metric("Verimlilik Puanı", f"{round(verimlilik, 2)}")

with tab2:
    st.subheader("📈 Dinamik Analiz Grafikleri")
    g_secim = st.selectbox("Analiz Türü", ["Hız ve Güç İhtiyacı", "Gaz ve İtki Dengesi", "Batarya Tüketimi"])
    x = np.linspace(0, 100, 50)
    if g_secim == "Hız ve Güç İhtiyacı":
        y = 0.5 * 1.225 * k_alani * (x / 3.6)**3
        df = pd.DataFrame({"Hız (km/sa)": x, "Güç (W)": y})
        st.line_chart(df, x="Hız (km/sa)", y="Güç (W)", color=grafik_rengi)
    elif g_secim == "Gaz ve İtki Dengesi":
        y = itki_gereken * (x/100)**2
        df = pd.DataFrame({"Gaz Seviyesi (%)": x, "İtki (kg)": y})
        st.area_chart(df, x="Gaz Seviyesi (%)", y="İtki (kg)", color=grafik_rengi)
    else: 
        y = np.clip(p_kapasite - (a_cekis * 1000 * (x/60)), 0, None)
        df = pd.DataFrame({"Uçuş Süresi (dk)": x, "Kapasite (mAh)": y})
        st.bar_chart(df, x="Uçuş Süresi (dk)", y="Kapasite (mAh)", color=grafik_rengi)

with tab3:
    st.subheader("🤖 Mühendislik Asistanı (Llama 3.1)")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_c = st.container(height=400)
    for m in st.session_state.messages:
        chat_c.chat_message(m["role"]).write(m["content"])

    if inp := st.chat_input("Sormak istediğin bir şey var mı?"):
        st.session_state.messages.append({"role": "user", "content": inp})
        chat_c.chat_message("user").write(inp)
        with chat_c.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": f"Sen Rüzgar'ın teknik asistanısın. Veriler: Ağırlık={a_toplam}g, Hedef İtki={itki_gereken}kg."},
                        {"role": "user", "content": inp}
                    ]
                ).choices[0].message.content
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Bağlantı Hatası: API Anahtarını Ayarlardan Kontrol Et!")

st.markdown("---")
st.caption("Rüzgar Vatansever Terminal v6.2 | 2026")
