import streamlit as st
import pandas as pd
from datetime import date, datetime

from utils.db import add_weight, load_weights, clear_weights

st.title("📈 Vazn kuzatuvchi")
st.write("Sana va vaqtni tanlang — kuniga bir nechta yozuv kiritishingiz mumkin.")

# Sana + vaqt
selected_date = st.date_input("Sana", value=date.today())
selected_time = st.time_input("Vaqt", value=datetime.now().time().replace(microsecond=0))

# Vazn
new_weight = st.number_input("Vazn (kg)", 30.0, 200.0, 70.0, step=0.1)

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("➕ Saqlash"):
        ts = datetime.combine(selected_date, selected_time).isoformat(timespec="seconds")
        add_weight(ts, float(new_weight))
        st.toast("Vazn saqlandi ✅")
        st.rerun()

with c2:
    if st.button("🗑 Tozalash"):
        clear_weights()
        st.toast("Tarix tozalandi ✅")
        st.rerun()

with c3:
    show_table = st.checkbox("Jadvalni ko‘rsatish", value=True)

# DB dan o‘qiymiz
df = load_weights()

if len(df) > 0:
    df["ts"] = pd.to_datetime(df["ts"])
    df = df.sort_values("ts")

    st.subheader("📉 Grafik")
    chart_df = df.set_index("ts")["weight"]
    st.line_chart(chart_df)

    if show_table:
        st.subheader("📋 Tarix")
        show_df = df.rename(columns={"ts": "Vaqt", "weight": "Vazn (kg)"})
        st.dataframe(show_df[["Vaqt", "Vazn (kg)"]], use_container_width=True)

    csv = df.rename(columns={"ts": "Vaqt", "weight": "Vazn (kg)"})[["Vaqt", "Vazn (kg)"]].to_csv(index=False).encode("utf-8")
    st.download_button("⬇ CSV yuklab olish", csv, "weight_history.csv", "text/csv")

else:
    st.info("Hali yozuv yo‘q. Sana, vaqt va vaznni kiriting va **Saqlash** tugmasini bosing.")
