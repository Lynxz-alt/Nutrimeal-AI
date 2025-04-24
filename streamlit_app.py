import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="NutriMeal AI", page_icon="🥗", layout="centered")

@st.cache_data
def load_data():
    df = pd.read_csv("foods.csv")
    df['Calories'] = df['Energy (kJ)'] * 0.239006
    df.rename(columns={
        'Menu': 'Food',
        'Carbohydrates (g)': 'Carbs'
    }, inplace=True)
    df.drop(columns=['Unnamed: 0', 'Energy (kJ)'], inplace=True)
    return df

df = load_data()

st.title("🥗 NutriMeal AI")
st.markdown("### Menu Sehat Otomatis Berdasarkan Tujuan Gizi Kamu")

st.sidebar.header("🧍 Profil Kamu")
goal = st.sidebar.selectbox("🎯 Tujuan Gizi", ["Diet", "Bulking", "Maintain"])
max_cal = st.sidebar.slider("🔥 Batas Kalori Maksimum", 100, 1500, 500, step=50)
min_protein = st.sidebar.slider("💪 Minimal Protein (gram)", 0, 100, 20)

df_filtered = df[(df['Calories'] <= max_cal) & (df['Protein (g)'] >= min_protein)]

st.markdown("---")
st.subheader("🍽️ Rekomendasi Menu Harian")
if st.button("Tampilkan Rekomendasi"):
    if df_filtered.empty:
        st.warning("Tidak ada makanan yang sesuai dengan filter kamu. Coba ubah filter!")
    else:
        st.success(f"Menampilkan {len(df_filtered)} makanan yang sesuai:")
        st.dataframe(df_filtered[["Food", "Calories", "Protein (g)", "Fat (g)", "Carbs"]])

st.markdown("---")
st.subheader("📊 Komposisi Gizi Rata-rata")
if not df_filtered.empty:
    avg_nutrients = df_filtered[["Protein (g)", "Fat (g)", "Carbs"]].mean()
    fig, ax = plt.subplots()
    ax.pie(avg_nutrients, labels=avg_nutrients.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

st.markdown("---")
st.subheader("💡 Tips Gizi Harian")
st.info("Minumlah air putih minimal 8 gelas per hari untuk membantu metabolisme dan menjaga hidrasi tubuh.")

st.markdown("---")
st.caption("Dibuat oleh NutriMeal AI · 2025")