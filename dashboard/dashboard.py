import os
import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

# Load Data
file_path = os.path.join(os.path.dirname(__file__), "all_data.csv")
df = pd.read_csv(file_path)

# Mapping season dan memastikan kolom ada
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_labels = {1: "Clear", 2: "Cloudy", 3: "Rain/Snow"}

df['season'] = df['season'].map(season_labels)
df['weathersit'] = df['weathersit'].map(weather_labels)

# Sidebar Navigation
st.sidebar.title("📌 Menu Navigasi")
page = st.sidebar.radio("Pilih Halaman:", ["Dashboard Utama", "Pengaruh Musim dan Cuaca", "Statistik Penyewaan per Jam"])

# Sidebar Filtering
st.sidebar.header("Filter Data")

# Select box untuk musim
seasons = ["All Season"] + list(df['season'].dropna().unique())
selected_season = st.sidebar.selectbox("Pilih Musim", seasons)

# Select box untuk cuaca
weathers = ["All Weathers"] + sorted(df['weathersit'].dropna().unique())
selected_weather = st.sidebar.selectbox("Pilih Cuaca", weathers)

# Select box untuk jam
hours = ["All Hours"] + sorted(df['hr'].dropna().unique())
selected_hour = st.sidebar.selectbox("Pilih Jam", hours)

# Filter data berdasarkan pilihan pengguna
filtered_df = df.copy()
if selected_season != "All Season":
    filtered_df = filtered_df[filtered_df['season'] == selected_season]
if selected_weather != "All Weathers":
    filtered_df = filtered_df[filtered_df['weathersit'] == selected_weather]
if selected_hour != "All Hours":
    filtered_df = filtered_df[filtered_df['hr'] == float(selected_hour)]

# Main Content
st.title("🚲 Dashboard Penyewaan Sepeda")

if page == "Dashboard Utama":
    st.subheader("Selamat datang di Dashboard Penyewaan Sepeda")
    st.write("Gunakan sidebar untuk navigasi dan melihat statistik penyewaan.")

elif page == "Pengaruh Musim dan Cuaca":
    st.subheader("📊 Pengaruh Musim dan Cuaca terhadap Penyewaan Sepeda")
    
    if filtered_df.empty:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih. Coba ubah filter.")
    else:
        bike_rentals_season_weather = filtered_df.groupby(["season", "weathersit"])["cnt"].sum().reset_index()
        plt.figure(figsize=(10, 6))
        sns.barplot(data=bike_rentals_season_weather, x="season", y="cnt", hue="weathersit", palette="coolwarm")
        plt.title("Pengaruh Musim dan Cuaca terhadap Jumlah Penyewaan Sepeda", fontsize=14)
        plt.xlabel("Musim", fontsize=12)
        plt.ylabel("Total Penyewaan", fontsize=12)
        plt.legend(title="Kondisi Cuaca")
        st.pyplot(plt)

elif page == "Statistik Penyewaan per Jam":
    st.subheader("📈 Statistik Penyewaan Sepeda Berdasarkan Jam")
    
    if filtered_df.empty:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih. Coba ubah filter.")
    else:
        bike_rentals_per_hour = filtered_df.groupby("hr")["cnt"].sum()
        max_hour = bike_rentals_per_hour.idxmax()
        max_rentals = bike_rentals_per_hour.max()
        min_hour = bike_rentals_per_hour.idxmin()
        min_rentals = bike_rentals_per_hour.min()
        
        plt.figure(figsize=(12, 6))
        sns.lineplot(x=bike_rentals_per_hour.index, y=bike_rentals_per_hour.values, marker="o", label="Penyewaan Sepeda")
        plt.scatter(max_hour, max_rentals, color='red', s=100, label=f"Max: {max_hour}:00 ({max_rentals})")
        plt.scatter(min_hour, min_rentals, color='blue', s=100, label=f"Min: {min_hour}:00 ({min_rentals})")
        plt.xlabel("Jam")
        plt.ylabel("Jumlah Penyewaan")
        plt.title("Jumlah Penyewaan Sepeda per Jam")
        plt.xticks(range(0, 24))
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)
        
