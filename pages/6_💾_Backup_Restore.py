import streamlit as st
import pandas as pd
import json
from datetime import date, datetime

st.title("💾 Backup / Restore")
st.write("Ma’lumotlaringizni saqlab qo‘ying (backup) yoki qayta tiklang (restore).")

# ----------- helpers -----------
def make_json_safe(x):
    """date/datetime va boshqa tiplarni JSON-safe qiladi."""
    if isinstance(x, (date, datetime)):
        return x.isoformat()
    return x

def df_to_records(df: pd.DataFrame):
    if df is None or len(df) == 0:
        return []
    # hamma qiymatni json-safe qilamiz
    records = df.to_dict(orient="records")
    safe = []
    for r in records:
        safe.append({k: make_json_safe(v) for k, v in r.items()})
    return safe

def records_to_df(records, columns):
    if not records:
        return pd.DataFrame(columns=columns)
    df = pd.DataFrame(records)
    for c in columns:
        if c not in df.columns:
            df[c] = None
    return df[columns]

def ensure_defaults():
    if "food_log" not in st.session_state:
        st.session_state.food_log = pd.DataFrame(columns=["Sana", "Ovqat", "Porsiya", "Kaloriya"])

    if "weights_df" not in st.session_state:
        st.session_state.weights_df = pd.DataFrame(columns=["Vaqt", "Vazn (kg)"])

    if "daily_target" not in st.session_state:
        st.session_state.daily_target = 2000

    if "last_calc" not in st.session_state:
        st.session_state.last_calc = {}

ensure_defaults()

# ----------- backup payload -----------
st.subheader("⬇ Backup yuklab olish")

backup = {
    "version": 1,
    "created_at": date.today().isoformat(),
    "daily_target": int(st.session_state.daily_target),
    "food_log": df_to_records(st.session_state.food_log),
    "weights_df": df_to_records(st.session_state.weights_df),
    "last_calc": st.session_state.last_calc if isinstance(st.session_state.last_calc, dict) else {},
}

backup_json = json.dumps(backup, ensure_ascii=False, indent=2).encode("utf-8")

st.download_button(
    "⬇ Backup (JSON) yuklab olish",
    data=backup_json,
    file_name="calorie_app_backup.json",
    mime="application/json",
)

st.info("✅ Bu faylni saqlab qo‘ying. Keyin restore qilishda qayta yuklaysiz.")

st.markdown("---")

# ----------- restore -----------
st.subheader("⬆ Restore (backup faylni yuklash)")

uploaded = st.file_uploader("Backup JSON faylni tanlang", type=["json"])

if uploaded is not None:
    try:
        data = json.load(uploaded)

        if "version" not in data or "food_log" not in data:
            st.error("❌ Bu backup formati noto‘g‘ri yoki eski.")
            st.stop()

        # Restore daily_target
        if "daily_target" in data:
            st.session_state.daily_target = int(data["daily_target"])

        # Restore food_log
        st.session_state.food_log = records_to_df(
            data.get("food_log", []),
            columns=["Sana", "Ovqat", "Porsiya", "Kaloriya"]
        )

        # Restore weights_df
        st.session_state.weights_df = records_to_df(
            data.get("weights_df", []),
            columns=["Vaqt", "Vazn (kg)"]
        )

        # Restore last_calc
        lc = data.get("last_calc", {})
        st.session_state.last_calc = lc if isinstance(lc, dict) else {}

        st.success("✅ Restore muvaffaqiyatli! Endi boshqa sahifalarga o‘ting.")
        st.toast("Restore qilindi ✅")

    except Exception as e:
        st.error(f"❌ Restore paytida xatolik: {e}")
