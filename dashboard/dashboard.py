import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# Konfigurasi awal streamlit
st.set_page_config(
    page_title="Dashboard Kualitas Udara",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fungsi untuk memuat data
def load_data():
    try:
        # Ganti 'nama_file.csv' dengan nama file data Anda
        df = pd.read_excel('C:/Code/Project-Data-Analisis_Dicoding/clean_data.xlsx')
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
        df['day_of_week'] = df['date'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Fungsi untuk membuat plot PM2.5 per jam
def create_hourly_pm25_plot(df, selected_year, selected_station):
    filtered_df = df[
        (df['year'] == selected_year) & 
        (df['station'].isin(selected_station))
    ]
    hourly_avg = filtered_df.groupby('hour')['PM2.5'].mean()
    
    fig = px.bar(
        x=hourly_avg.index,
        y=hourly_avg.values,
        labels={'x': 'Jam', 'y': 'Rata-rata PM2.5'},
        title='Rata-rata PM2.5 per Jam'
    )
    return fig, hourly_avg.idxmax(), hourly_avg.max()

# Fungsi untuk membuat plot pengaruh hujan
def create_rain_effect_plots(df, selected_year, selected_station):
    filtered_df = df[
        (df['year'] == selected_year) & 
        (df['station'].isin(selected_station))
    ]
    
    def categorize_rain(rain):
        if rain == 0:
            return 'Tidak Hujan'
        elif rain <= 20:
            return 'Hujan Ringan'
        elif rain <= 50:
            return 'Hujan Sedang'
        else:
            return 'Hujan Lebat'
    
    filtered_df['Rain_Category'] = filtered_df['RAIN'].apply(categorize_rain)
    rain_effect = filtered_df.groupby('Rain_Category')[['PM2.5', 'SO2']].mean().reset_index()
    
    fig1 = px.bar(
        rain_effect,
        x='Rain_Category',
        y='PM2.5',
        title='Pengaruh Hujan terhadap PM2.5'
    )
    
    fig2 = px.bar(
        rain_effect,
        x='Rain_Category',
        y='SO2',
        title='Pengaruh Hujan terhadap SO2'
    )
    
    return fig1, fig2

# Fungsi untuk membuat plot PM10 per stasiun
def create_station_pm10_plot(df, selected_year, selected_station):
    filtered_df = df[
        (df['year'] == selected_year) & 
        (df['station'].isin(selected_station))
    ]
    pm10_avg = filtered_df.groupby('station')['PM10'].mean().sort_values(ascending=False)
    
    fig = px.bar(
        x=pm10_avg.index,
        y=pm10_avg.values,
        labels={'x': 'Stasiun', 'y': 'Rata-rata PM10'},
        title=f'Rata-rata PM10 per Stasiun ({selected_year})'
    )
    return fig, pm10_avg.index[0], pm10_avg.iloc[0]

# Fungsi untuk membuat plot perbandingan hari kerja vs akhir pekan
def create_weekday_weekend_plot(df, selected_year, selected_station, selected_pollutant):
    filtered_df = df[
        (df['year'] == selected_year) & 
        (df['station'].isin(selected_station))
    ]
    
    daily_avg = filtered_df.groupby(['date', 'is_weekend'])[selected_pollutant].mean().reset_index()
    
    fig = px.box(
        daily_avg,
        x='is_weekend',
        y=selected_pollutant,
        labels={
            'is_weekend': 'Tipe Hari (0=Hari Kerja, 1=Akhir Pekan)',
            selected_pollutant: f'Konsentrasi {selected_pollutant}'
        },
        title=f'Perbandingan {selected_pollutant} antara Hari Kerja dan Akhir Pekan'
    )
    
    weekday_data = daily_avg[daily_avg['is_weekend'] == 0][selected_pollutant]
    weekend_data = daily_avg[daily_avg['is_weekend'] == 1][selected_pollutant]
    t_stat, p_value = stats.ttest_ind(weekday_data, weekend_data)
    
    return fig, t_stat, p_value

def main():
    # Judul dashboard
    st.title("📊 Dashboard Analisis Kualitas Udara")
    
    # Load data
    df = load_data()
    
    if df is not None:
        # Sidebar filters
        st.sidebar.header("Filter Data")
        selected_year = st.sidebar.selectbox(
            "Pilih Tahun",
            sorted(df['year'].unique())
        )
        selected_station = st.sidebar.multiselect(
            "Pilih Stasiun",
            df['station'].unique(),
            default=[df['station'].unique()[0]]
        )
        
        if not selected_station:
            st.warning("Silakan pilih minimal satu stasiun.")
            return
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "Analisis PM2.5 per Jam",
            "Pengaruh Hujan",
            "Analisis PM10 per Stasiun",
            "Perbandingan Hari Kerja vs Akhir Pekan"
        ])
        
        # Tab 1: Analisis PM2.5 per Jam
        with tab1:
            st.header("📈 Analisis PM2.5 per Jam")
            fig, max_hour, max_pm25 = create_hourly_pm25_plot(df, selected_year, selected_station)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Jam dengan PM2.5 Tertinggi", f"{max_hour}:00")
            with col2:
                st.metric("Nilai PM2.5 Tertinggi", f"{max_pm25:.2f}")
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Tab 2: Pengaruh Hujan
        with tab2:
            st.header("🌧️ Pengaruh Hujan terhadap Polutan")
            fig1, fig2 = create_rain_effect_plots(df, selected_year, selected_station)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                st.plotly_chart(fig2, use_container_width=True)
        
        # Tab 3: Analisis PM10 per Stasiun
        with tab3:
            st.header("📍 Analisis PM10 per Stasiun")
            fig, highest_station, highest_pm10 = create_station_pm10_plot(df, selected_year, selected_station)
            
            st.plotly_chart(fig, use_container_width=True)
            st.metric(
                "Stasiun dengan PM10 Tertinggi",
                highest_station,
                f"Rata-rata: {highest_pm10:.2f}"
            )
        
        # Tab 4: Perbandingan Hari Kerja vs Akhir Pekan
        with tab4:
            st.header("📅 Perbandingan Hari Kerja vs Akhir Pekan")
            
            pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
            selected_pollutant = st.selectbox("Pilih Polutan", pollutants)
            
            fig, t_stat, p_value = create_weekday_weekend_plot(
                df, selected_year, selected_station, selected_pollutant
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("t-statistic", f"{t_stat:.4f}")
            with col2:
                st.metric("p-value", f"{p_value:.4f}")
        
        # Footer
        st.markdown("---")
        st.markdown("Dashboard dibuat dengan ❤️ menggunakan Streamlit")

if __name__ == "__main__":
    main()