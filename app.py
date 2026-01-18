import streamlit as st
import json
import os
from datetime import date
import matplotlib.pyplot as plt

st.markdown("""
<style>
/* Membesarkan tombol */
div.stButton > button {
    width: 100&;
    height: 50px;
    font-size: 24px;
    border-radius: 14px;
}   
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Sudahkah Anda Ngoding Hari Ini?",
    page_icon="💻",
    layout="centered"
)

DATA_FILE = "data.json"
today = str(date.today())


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_stats(data):
    sudah = list(data.values()).count("sudah")
    tidak = list(data.values()).count("tidak")
    total = sudah + tidak
    return sudah, tidak, total

def meme_text(percentage):
    if percentage >= 80:
        return "🔥 Rajin banget, calon suhu ni!"
    elif percentage >= 50:
        return "😎 Lumayan, consistent is key"
    elif percentage >= 20:
        return "😭 Besok pasti ngoding (katanya)"
    else:
        return "😅 Kamu pasti member IMPHNEN yaa"


data = load_data()


st.title("💻 Sudahkah Anda Ngoding Hari Ini?")

if today not in data:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Sudah doong!"):
            data[today] = "sudah"
            save_data(data)
            st.rerun()

    with col2:
        if st.button("❌ Tidak ah malasss"):
            data[today] = "tidak"
            save_data(data)
            st.rerun()

else:
    pilihan = data[today]
    if pilihan == "sudah":
        st.success("Mantap! Hari ini ngoding 🔥")
    else:
        st.warning("Tidak apa-apa, masih ada hari esok😭")

    st.info("Note: Kamu hanya bisa memilih satu kali per hari. Tunggu besok ya!")


st.divider()
st.subheader("📊 Statistik Ngoding")

sudah, tidak, total = get_stats(data)

if total > 0:
    persentase_sudah = (sudah / total) * 100

    fig, ax = plt.subplots()
    ax.pie(
        [sudah, tidak],
        labels=["Sudah", "Tidak"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")

    st.pyplot(fig)

    st.info(meme_text(persentase_sudah))
else:
    st.info("Belum ada data sama sekali.")

st.markdown(
    "<small>⭐ <a href='https://github.com/username/nama-repo' target='_blank'>Star on GitHub</a></small>",
    unsafe_allow_html=True
)
