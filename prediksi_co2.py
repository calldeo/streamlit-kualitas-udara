import pickle
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Prediksi Kualitas Udara",
    page_icon="🌍",
    layout="wide"
)

model = pickle.load(open('prediksi_co2.sav','rb'))

df = pd.read_excel("CO2 dataset.xlsx")
df['Year'] = pd.to_datetime(df['Year'], format='%Y')
df.set_index(['Year'], inplace=True)

st.markdown("<h1 style='text-align: center;'>🌍 Forecasting Kualitas Udara</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Aplikasi untuk memprediksi kadar CO2 di masa depan</p>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Pilih Menu", ["Hasil Pengecekan", "Prediksi"])

if menu == "Hasil Pengecekan":
    st.markdown("### 📊 Hasil Pengecekan Data Historis")
    
    st.dataframe(df.style.highlight_max(color='lightgreen'))
    
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Scatter(
        x=df.index,
        y=df['CO2'],
        name='Data Historis',
        line=dict(color='gray')
    ))
    
    fig_hist.update_layout(
        title='Data Historis Kadar CO2',
        xaxis_title='Tahun',
        yaxis_title='Kadar CO2',
        template='plotly_white'
    )
    
    st.plotly_chart(fig_hist, use_container_width=True)

elif menu == "Prediksi":
    st.markdown("### 📅 Pilih Rentang Tahun Prediksi")
    year = st.slider("Geser untuk menentukan tahun",1,30, step=1)

    pred = model.forecast(year)
    pred = pd.DataFrame(pred, columns=['CO2'])

    if st.button("🔮 Mulai Prediksi", help="Klik untuk melihat hasil prediksi"):
        
        st.markdown("### 📊 Hasil Prediksi")
        
        col1, col2 = st.columns([2,3])
        with col1:
            st.markdown("#### Data Prediksi CO2")
            st.dataframe(pred.style.highlight_max(color='lightgreen'))
            
        with col2:
            st.markdown("#### Visualisasi Prediksi")
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df.index, 
                y=df['CO2'],
                name='Data Historis',
                line=dict(color='gray', dash='dash')
            ))
            
            fig.add_trace(go.Scatter(
                x=pred.index,
                y=pred['CO2'],
                name='Prediksi',
                line=dict(color='#1f77b4')
            ))
            
            fig.update_layout(
                title='Tren Kadar CO2',
                xaxis_title='Tahun',
                yaxis_title='Kadar CO2',
                hovermode='x unified',
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            