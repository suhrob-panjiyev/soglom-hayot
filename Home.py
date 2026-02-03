import streamlit as st
from utils.db import init_db

init_db()

st.set_page_config(
    page_title="Sog‘lom Hayot",
    page_icon="🥗",
    layout="wide"
)

# ---------- Style ----------
st.markdown("""
<style>
.big-title {font-size: 56px; font-weight: 800;}
.sub {font-size: 18px; opacity: 0.85;}
.card {
    padding: 18px;
    border-radius: 16px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
}
</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="big-title">🥗 Sog‘lom Hayot</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub">Kaloriya • Ovqat • Vazn • Sog‘lom odatlar</div>', unsafe_allow_html=True)
    st.write("")

    st.success("Ilovani boshlash uchun pastdagi tugmani bosing 👇")

    # 🚀 BOSHLASH TUGMASI
    if st.button("🚀 Boshlash", use_container_width=True):
        st.switch_page("pages/1_🥗_Calculator.py")


with col2:
    st.markdown("""
    <div class="card">
        <h4>📌 Qanday foydalaniladi?</h4>
        <ol>
            <li>Calculator → kaloriya hisoblash</li>
            <li>Food Log → ovqat qo‘shish</li>
            <li>Tracker → vazn kuzatish</li>
            <li>Diet Tips → maslahatlar</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")


# ---------- FEATURE CARDS ----------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown('<div class="card">🔥 <b>Kaloriya hisoblash</b><br>BMR + TDEE</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">🥩 <b>Makro tavsiya</b><br>Protein/Yog‘/Carb</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card">🍔 <b>Food Log</b><br>Kunlik kaloriya nazorati</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="card">📈 <b>Vazn grafik</b><br>Progress kuzatish</div>', unsafe_allow_html=True)


st.markdown("---")
st.caption("⚠️ Ilova tibbiy maslahat bermaydi. Natijalar taxminiy hisob-kitoblarga asoslangan.")
