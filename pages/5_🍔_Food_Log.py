import streamlit as st
import pandas as pd
from datetime import date
import re

from utils.db import (
    add_food,
    load_foods_for_day,
    delete_last_food_for_day,
    delete_foods_for_day,
    set_setting,
    get_setting
)

st.title("🍔 Bugungi ovqatlar (Food Log)")
st.write("Ovqat tanlang → qo‘shing → bugungi kaloriyangizni kuzating.")

# ---------- Helper: normalize ----------
def normalize_text(s: str) -> str:
    s = str(s).lower().strip()

    # barcha apostroflarni butunlay olib tashlaymiz (go'sht / go‘sht / gosht -> gosht)
    for ch in ["’", "'", "`", "ʻ", "ʼ", "‘"]:
        s = s.replace(ch, "")

    # o‘ → o, g‘ → g (har ehtimolga)
    s = s.replace("o‘", "o").replace("g‘", "g")

    # faqat harf/raqam/bo'sh joy qoldiramiz
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


# ---------- Load foods.csv ----------
try:
    foods = pd.read_csv("foods.csv")
except FileNotFoundError:
    st.error("❌ foods.csv topilmadi. Uni loyiha root (calorie_app/) ichiga qo‘ying.")
    st.stop()

# ---------- Clean foods ----------
foods = foods.dropna(subset=["name"]).copy()
foods["name"] = foods["name"].astype(str).str.strip()
foods["portion"] = foods["portion"].astype(str).str.strip()
foods["calories"] = pd.to_numeric(foods["calories"], errors="coerce")
foods = foods.dropna(subset=["calories"]).copy()
foods["calories"] = foods["calories"].round(0).astype(int)

foods["name_norm"] = foods["name"].apply(normalize_text)

# ---------- Target settings (DB) ----------
st.subheader("🎯 Kunlik kaloriya maqsadi")

saved = int(get_setting("daily_target", "2000"))
target = st.number_input("Maqsad (kcal)", 800, 6000, saved, step=50)

set_setting("daily_target", str(int(target)))
daily_target = int(target)

st.markdown("---")

# ---------- Add food ----------
today = st.date_input("Sana", value=date.today())
st.subheader("🍽 Ovqat qo‘shish")

query = st.text_input("🔎 Ovqat qidirish", placeholder="Masalan: osh, lagmon, go'sht, somsa...")

if query.strip():
    q = normalize_text(query)

    filtered_df = foods[foods["name_norm"].str.contains(q, na=False)]

    if len(filtered_df) == 0:
        parts = q.split()
        tmp = foods.copy()
        for p in parts:
            tmp = tmp[tmp["name_norm"].str.contains(p, na=False)]
        filtered_df = tmp

    if len(filtered_df) == 0:
        st.warning("Hech narsa topilmadi. Boshqa so‘z yozib ko‘ring.")
        st.stop()

    options = filtered_df["name"].tolist()[:50]
else:
    options = foods["name"].tolist()[:50]

selected_food = st.selectbox("Ovqat tanlang", options)

row = foods.loc[foods["name"] == selected_food].iloc[0]
portion = row["portion"]
cal_per_portion = int(row["calories"])

qty = st.number_input(f"Miqdor (porsiya) — ({portion})", 0.5, 10.0, 1.0, step=0.5)
total_cal = cal_per_portion * qty

c1, c2 = st.columns(2)
with c1:
    st.info(f"🍽 Porsiya: **{portion}**")
    st.info(f"🔥 1 porsiya: **{cal_per_portion} kcal**")

with c2:
    st.success(f"✅ Qo‘shilganda: **{int(total_cal)} kcal**")

if st.button("➕ Ovqatni qo‘shish"):
    add_food(
        day=str(today),
        food=selected_food,
        portion=f"{qty} x {portion}",
        calories=int(total_cal),
    )
    st.toast("Ovqat qo‘shildi ✅")
    st.rerun()  # qo‘shgandan keyin jadval yangilansin


# ---------- Daily summary (DB) ----------
st.markdown("---")
st.subheader("📊 Bugungi holat")

today_df = load_foods_for_day(str(today))  # columns: id, day, food, portion, calories

eaten = int(today_df["calories"].sum()) if len(today_df) else 0
remaining = int(max(0, daily_target - eaten))

st.metric("🍽 Bugun yegan kaloriya", f"{eaten} kcal")
st.metric("🎯 Qolgan limit", f"{remaining} kcal")

progress = min(1.0, eaten / daily_target) if daily_target > 0 else 0
st.progress(progress)

if eaten > daily_target:
    st.warning("⚠️ Siz bugungi limitdan oshib ketdingiz.")
else:
    st.success("✅ Ajoyib! Limit ichida ketyapsiz.")

# ---------- Table + actions ----------
st.subheader("📋 Bugungi ovqatlar ro‘yxati")

if len(today_df) == 0:
    st.info("Hozircha bugun uchun ovqat qo‘shilmadi.")
else:
    st.dataframe(
        today_df[["food", "portion", "calories"]].rename(
            columns={"food": "Ovqat", "portion": "Porsiya", "calories": "Kaloriya"}
        ),
        use_container_width=True
    )

    colA, colB = st.columns(2)
    with colA:
        if st.button("↩️ Oxirgi yozuvni o‘chirish"):
            delete_last_food_for_day(str(today))
            st.toast("Oxirgi yozuv o‘chirildi 🗑")
            st.rerun()

    with colB:
        if st.button("🗑 Bugungi hammasini tozalash"):
            delete_foods_for_day(str(today))
            st.toast("Bugungi ovqatlar tozalandi ✅")
            st.rerun()

# ---------- Download CSV (from DB) ----------
st.markdown("---")
if len(today_df) > 0:
    csv = today_df[["day", "food", "portion", "calories"]].to_csv(index=False).encode("utf-8")
else:
    csv = "day,food,portion,calories\n".encode("utf-8")

st.download_button("⬇ Bugungi ovqatlarni CSV qilib yuklab olish", csv, "today_food_log.csv", "text/csv")
