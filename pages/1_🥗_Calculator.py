import streamlit as st
import matplotlib.pyplot as plt

from utils.calculations import calc_bmr, calc_tdee, adjust_for_goal, calc_macros
from utils.db import set_setting, save_calculator, load_calculator

st.title("🥗 Kaloriya Kalkulyatori")

ACTIVITY = {
    "Kam harakat": 1.2,
    "O‘rtacha faol": 1.55,
    "Faol": 1.725
}

# ✅ DB dan oldingi qiymatlarni o‘qiymiz (bo‘lmasa default)
saved = load_calculator() or {
    "age": 20,
    "sex": "erkak",
    "weight": 70.0,
    "height": 170.0,
    "activity": "O‘rtacha faol",
    "goal": "saqlash"
}

activity_keys = list(ACTIVITY.keys())
goals = ["ozish", "saqlash", "semirish"]

with st.form("form"):
    age = st.number_input("Yosh", 10, 80, int(saved["age"]))

    sex_index = 0 if saved["sex"] == "erkak" else 1
    sex = st.selectbox("Jins", ["erkak", "ayol"], index=sex_index)

    weight = st.number_input("Vazn (kg)", 30.0, 200.0, float(saved["weight"]))
    height = st.number_input("Bo‘y (cm)", 120.0, 220.0, float(saved["height"]))

    # activity default index
    try:
        activity_index = activity_keys.index(saved["activity"])
    except ValueError:
        activity_index = 1  # O‘rtacha faol

    activity_key = st.selectbox("Faollik", activity_keys, index=activity_index)
    activity = ACTIVITY[activity_key]

    # goal default index
    try:
        goal_index = goals.index(saved["goal"])
    except ValueError:
        goal_index = 1  # saqlash

    goal = st.selectbox("Maqsad", goals, index=goal_index)

    submit = st.form_submit_button("🔮 Hisoblash")

if submit:
    bmr = calc_bmr(age, sex, weight, height)
    tdee = calc_tdee(bmr, activity)
    calories = adjust_for_goal(tdee, goal)

    protein, fat, carbs = calc_macros(calories, weight)

    # ✅ DB ga calculator inputlarini saqlaymiz (refreshda ham qoladi)
    save_calculator(age, sex, weight, height, activity_key, goal)

    # ✅ daily_target ni DB ga yozamiz (Food Log shu targetni o‘qiydi)
    set_setting("daily_target", str(int(round(calories))))

    # (ixtiyoriy) keyin dashboard uchun
    st.session_state.last_calc = {
        "calories": int(round(calories)),
        "protein": int(round(protein)),
        "fat": int(round(fat)),
        "carbs": int(round(carbs)),
    }

    st.markdown("---")
    st.subheader("📊 Siz uchun natijalar")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("🔥 Kaloriya", f"{int(round(calories))} kcal")
        st.metric("🥩 Protein", f"{int(round(protein))} g")
    with c2:
        st.metric("🧈 Yog‘", f"{int(round(fat))} g")
        st.metric("🍚 Uglevod", f"{int(round(carbs))} g")

    st.subheader("🥗 Makro taqsimoti")
    fig, ax = plt.subplots()
    ax.pie(
        [protein * 4, fat * 9, carbs * 4],
        labels=["Protein", "Yog‘", "Uglevod"],
        autopct="%1.1f%%",
        wedgeprops=dict(width=0.4)
    )
    ax.axis("equal")
    st.pyplot(fig)

    st.subheader("📏 BMI (Tana massasi indeksi)")
    bmi = weight / ((height / 100) ** 2)

    if bmi < 18.5:
        st.warning(f"BMI: {round(bmi, 1)} — Ozg‘in")
    elif bmi < 25:
        st.success(f"BMI: {round(bmi, 1)} — Normal")
    elif bmi < 30:
        st.warning(f"BMI: {round(bmi, 1)} — Ortiqcha vazn")
    else:
        st.error(f"BMI: {round(bmi, 1)} — Semizlik")
else:
    st.info("Formani to‘ldirib **Hisoblash** tugmasini bosing. Natijalar shu yerda chiqadi.")
