# =====================================================================
# SYSTEM FINANSOWY: Budżet Domowy (v2.1 Excel Edition - Finał)
# Stała aplikacja internetowa | Autor: Marcin
# =====================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import json

# 1. KONFIGURACJA INTERFEJSU STRONY
st.set_page_config(page_title="Budżet Domowy", page_icon="🏠", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 38px !important; font-weight: bold; color: #2E7D32; }
    .author-tag { font-size: 16px; color: #6B7280; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🏠 SYSTEM FINANSOWY: Budżet Domowy v2.1</p>', unsafe_allow_html=True)
st.markdown('<p class="author-tag">Twórca i Główny Programista: Marcin</p>', unsafe_allow_html=True)
st.write("---")

# 2. SYSTEM ZAPISU I ODCZYTU DANYCH (PAMIĘĆ PROGRAMU)
st.sidebar.header("💾 ZAPISZ / WCZYTAJ BUDŻET")
wgrany_plik = st.sidebar.file_uploader("Wgraj swój plik budżetu:", type=["json"])

# Domyślna lista wydatków w stylu Excela na start
domyslne_wydatki = [
    {"Nazwa wydatku": "Telefon", "Kwota (PLN)": 30.0},
    {"Nazwa wydatku": "Mieszkanie i opłaty", "Kwota (PLN)": 2300.0},
    {"Nazwa wydatku": "Jedzenie", "Kwota (PLN)": 1400.0},
]
domyslny_przychod = 6000.0
domyslne_imie = "Marcin"

if wgrany_plik is not None:
    try:
        dane_z_pliku = json.load(wgrany_plik)
        domyslny_przychod = dane_z_pliku.get("przychod", 6000.0)
        domyslne_imie = dane_z_pliku.get("imie", "Marcin")
        domyslne_wydatki = dane_z_pliku.get("wydatki", domyslne_wydatki)
        st.sidebar.success("✅ Budżet wczytany!")
    except:
        st.sidebar.error("🚨 Błąd wczytywania pliku!")

# 3. PANEL BOCZNY - PODSTAWOWE USTAWIENIA
st.sidebar.write("---")
st.sidebar.subheader("⚙️ PARAMETRY GŁÓWNE")
imie_user = st.sidebar.text_input("Imię właściciela portfela:", value=domyslne_imie)
przychod = st.sidebar.number_input("Twój miesięczny przychód na rękę (PLN):", min_value=0.0, value=float(domyslny_przychod), step=100.0)

# 4. PANEL GŁÓWNY - EDYTOR W STYLU EXCELA
st.subheader("📋 Twoja Lista Wydatków (jak w Excelu)")
st.caption("💡 Instrukcja: Klikaj w komórki, aby zmienić opisy lub kwoty. Aby dodać nowy wydatek (np. kolejną pozycję), kliknij ikonę '+' na samym dole tabeli.")

# Tworzymy obiekt DataFrame z domyślnych wydatków
df_startowe = pd.DataFrame(domyslne_wydatki)

# Uproszczony i bezpieczny edytor tabeli
edytowana_tabela = st.data_editor(
    df_startowe,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)

# Konwersja edytowanych danych z powrotem do obliczeń
lista_wydatkow_wynik = edytowana_tabela.to_dict(orient="records")
suma_wydatkow = edytowana_tabela["Kwota (PLN)"].sum() if not edytowana_tabela.empty else 0.0

# Obliczenia końcowe
wolne_srodki = przychod - suma_wydatkow
procent_oszczednosci = (wolne_srodki / przychod) * 100 if przychod > 0 else 0

# Przygotowanie przycisku pobierania zaktualizowanego budżetu w panelu bocznym
dane_do_zapisu = {"imie": imie_user, "przychod": przychod, "wydatki": lista_wydatkow_wynik}
json_string = json.dumps(dane_do_zapisu)
st.sidebar.write("---")
st.sidebar.download_button(
    label="📥 Zapisz ten budżet (Pobierz plik)",
    data=json_string,
    file_name="moj_budzet.json",
    mime="application/json"
)

# ⚙️ SEKCYJKA ZAPŁATY KAWY W PANELU BOCZNYM (TUTAJ WPISAŁEM TWÓJ LINK)
st.sidebar.write("---")
st.sidebar.subheader("☕ WESPRZYJ PROJEKT")
st.sidebar.markdown("[👉 Postaw kawę Marcinowi](https://buycoffee.to)", unsafe_allow_html=True)

st.write("---")

# 5. PANEL METRYK (PODSUMOWANIE CASHFLOW)
st.subheader(f"📊 Stan Finansów: {imie_user}")
col1, col2, col3 = st.columns(3)
with col1: st.metric(label="💰 Stały Dochód", value=f"{przychod:,.2f} PLN")
with col2: st.metric(label="💸 Suma Wydatków z Tabeli", value=f"{suma_wydatkow:,.2f} PLN")
with col3:
    if wolne_srodki >= 0: st.metric(label="✅ Wypracowane Oszczędności", value=f"{wolne_srodki:,.2f} PLN", delta=f"{procent_oszczednosci:.1f}% pensji")
    else: st.metric(label="🚨 Deficyt Budżetowy!", value=f"{wolne_srodki:,.2f} PLN", delta="⚠️ Przekroczono budżet!", delta_color="inverse")

st.write("---")

# 6. DYNAMICZNY WYKRES KOLUMNOWY DLA TABELI
if not edytowana_tabela.empty and suma_wydatkow > 0:
    st.subheader("📈 Wykres Twoich Kosztów")
    fig = px.bar(
        edytowana_tabela, 
        x="Nazwa wydatku", 
        y="Kwota (PLN)", 
        title="Zestawienie kwotowe wprowadzonych pozycji",
        color="Nazwa wydatku",
        color_discrete_sequence=px.colors.qualitative.Dark2
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("💡 Dodaj chociaż jeden wydatek z kwotą większą od zera w tabeli powyżej, aby zobaczyć wykres.")

st.write("---")

# 7. CYFROWY DORADCA MARGINA
st.subheader("🤖 Asystent Finansowy Budżet Domowy")
if wolne_srodki > 0:
    if procent_oszczednosci >= 20: st.info(f"💡 **Rekomendacja:** Zarządzasz budżetem rewelacyjnie! Odkładasz aż {procent_oszczednosci:.1f}% swoich dochodów.")
    else: st.warning(f"💡 **Rekomendacja:** Twoje oszczędności to {procent_oszczednosci:.1f}% pensji. Przejrzyj tabelę i sprawdź, które pozycje możesz ograniczyć.")
else: st.error("💡 **Rekomendacja:** Deficyt! Suma pozycji w tabeli przewyższa Twój miesięczny przychód. Zredukuj koszty.")
