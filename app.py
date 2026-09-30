# =====================================================================
# SYSTEM FINANSOWY: BudżetAlfa (v1.6 PRO z Pamięcią Plików)
# Stała aplikacja internetowa | Autor: Marcin
# =====================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import json

# 1. KONFIGURACJA INTERFEJSU STRONY
st.set_page_config(page_title="BudżetAlfa PRO", page_icon="💰", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 38px !important; font-weight: bold; color: #1E3A8A; }
    .author-tag { font-size: 16px; color: #6B7280; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">💰 SYSTEM FINANSOWY: BudżetAlfa v1.6 PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="author-tag">Twórca i Główny Programista: Marcin</p>', unsafe_allow_html=True)
st.write("---")

# 2. GADŻET: SYSTEM ZAPISU I ODCZYTU DANYCH (PAMIĘĆ PROGRAMU)
st.sidebar.header("💾 ZAPISZ / WCZYTAJ BUDŻET")
wgrany_plik = st.sidebar.file_uploader("Masz zapisany budżet? Wgraj go tutaj:", type=["json"])

# Domyślne wartości, jeśli plik nie jest wgrany
domyslne = {
    "imie": "Marcin", "przychod": 6000, "mieszkanie": 2300, 
    "jedzenie": 1400, "rozrywka": 500, "transport": 400, "inne": 300
}

# Jeśli użytkownik wgrał plik, nadpisujemy domyślne wartości danymi z pliku
if wgrany_plik is not None:
    try:
        dane_z_pliku = json.load(wgrany_plik)
        domyslne.update(dane_z_pliku)
        st.sidebar.success("✅ Budżet wczytany pomyślnie!")
    except:
        st.sidebar.error("🚨 Błąd wczytywania pliku!")

# 3. PANEL BOCZNY - WPROWADZANIE DANYCH WEJŚCIOWYCH
st.sidebar.write("---")
st.sidebar.subheader("⚙️ USTAWIENIA KWOT")
imie_user = st.sidebar.text_input("Imię właściciela portfela:", value=domyslne["imie"])
przychod = st.sidebar.number_input("Twój miesięczny przychód na rękę (PLN):", min_value=0, value=int(domyslne["przychod"]), step=100)

st.sidebar.write("---")
st.sidebar.subheader("💸 TWOJE MIESIĘCZNE WYDATKI:")
w_mieszkanie = st.sidebar.slider("🏠 Mieszkanie i opłaty:", 0, 10000, tragedy := int(domyslne["mieszkanie"]), step=50)
w_jedzenie = st.sidebar.slider("🛒 Jedzenie i chemia:", 0, 5000, int(domyslne["jedzenie"]), step=50)
w_rozrywka = st.sidebar.slider("🎉 Rozrywka i przyjemności:", 0, 3000, int(domyslne["rozrywka"]), step=50)
w_transport = st.sidebar.slider("🚗 Transport i paliwo:", 0, 3000, int(domyslne["transport"]), step=50)
w_inne = st.sidebar.slider("🔮 Inne / Niespodziewane:", 0, 3000, int(domyslne["inne"]), step=50)

# Przygotowanie danych do pobrania
dane_do_zapisu = {
    "imie": imie_user, "przychod": przychod, "mieszkanie": w_mieszkanie,
    "jedzenie": w_jedzenie, "rozrywka": w_rozrywka, "transport": w_transport, "inne": w_inne
}
json_string = json.dumps(dane_do_zapisu)

st.sidebar.write("---")
st.sidebar.download_button(
    label="📥 Pobierz i zapisz ten budżet",
    data=json_string,
    file_name="moj_budzet.json",
    mime="application/json"
)

# 4. RDZEŃ OBLICZENIOWY (MATEMATYKA PROGRAMU)
suma_wydatkow = w_mieszkanie + w_jedzenie + w_rozrywka + w_transport + w_inne
wolne_srodki = przychod - suma_wydatkow
procent_oszczednosci = (wolne_srodki / przychod) * 100 if przychod > 0 else 0

# 5. PANEL GŁÓWNY - PODSUMOWANIE (METRYKI)
st.subheader(f"📊 Kondycja Finansowa Użytkownika: {imie_user}")
col1, col2, col3 = st.columns(3)
with col1: st.metric(label="💰 Stały Dochód", value=f"{przychod:,} PLN")
with col2: st.metric(label="💸 Generowane Koszty", value=f"{suma_wydatkow:,} PLN")
with col3:
    if wolne_srodki >= 0: st.metric(label="✅ Oszczędności", value=f"{wolne_srodki:,} PLN", delta=f"{procent_oszczednosci:.1f}% pensji")
    else: st.metric(label="🚨 Deficyt!", value=f"{wolne_srodki:,} PLN", delta="⚠️ Przekroczono limity!", delta_color="inverse")

st.write("---")

# 6. WIZUALIZACJE DANYCH
kolumna_lewa, kolumna_prawa = st.columns(2)
with kolumna_lewa:
    st.subheader("🍩 Struktura Podziału Wydatków")
    df = pd.DataFrame({"Kategoria": ["Mieszkanie", "Jedzenie", "Rozrywka", "Transport", "Inne"], "Kwota (PLN)": [w_mieszkanie, w_jedzenie, w_rozrywka, w_transport, w_inne]})
    fig = px.pie(df, values="Kwota (PLN)", names="Kategoria", hole=0.45, color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig, use_container_width=True)

with kolumna_prawa:
    st.subheader("🎯 Tracker Celów Oszczędnościowych")
    nazwa_celu = st.text_input("Na jaki cel odkładasz wolne środki?", value="Poduszka finansowa")
    kwota_celu = st.number_input("Docelowa kwota do zgromadzenia (PLN):", min_value=1, value=5000)
    if wolne_srodki > 0:
        miesiace = kwota_celu / wolne_srodki
        st.success(f"🎯 Cel: **{nazwa_celu}**. Uzbierasz to za **{miesiace:.1f} mies.**!")
        st.progress(min(100, int((wolne_srodki / kwota_celu) * 100)) / 100)
    else: st.error("🚨 Brak wolnych środków na realizację celów!")

st.write("---")
# 7. PORADY SYSTEMOWE
st.subheader("🤖 Cyfrowy Doradca Finansowy BudżetAlfa")
if wolne_srodki > 0:
    if procent_oszczednosci >= 20: st.info(f"💡 **Rekomendacja:** Zarządzasz budżetem świetnie! Odkładasz aż {procent_oszczednosci:.1f}% kapitału.")
    else: st.warning(f"💡 **Rekomendacja:** Zoptymalizuj koszty rozrywki ({w_rozrywka} PLN), aby szybciej odłożyć na cel.")
else: st.error("💡 **Rekomendacja:** Krytyczna alokacja środków! Zredukuj wydatki zmienne.")
