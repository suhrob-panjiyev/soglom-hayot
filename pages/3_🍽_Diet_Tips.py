import streamlit as st

st.title("🍽 Diet Tips — aniq maslahatlar")
st.write("Maqsadni tanlang, sizga mos amaliy tavsiyalar chiqadi.")

goal = st.selectbox("🎯 Maqsad", ["ozish", "saqlash", "semirish"], index=1)

st.markdown("---")

# ---------- universal tips ----------
st.subheader("✅ Universal qoidalar (hamma uchun)")
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
**🥛 Suv**
- Kuniga 6–10 stakan (1.5–2.5 L)
- Choy/kofe suv o‘rnini bosmaydi

**🍽 Porsiya nazorati**
- Likopchani 2 qism sabzavot, 1 qism protein, 1 qism uglevod qiling
""")

with c2:
    st.markdown("""
**🥩 Protein**
- Har ovqatda protein bo‘lsin (tovuq, tuxum, tvorog, loviya)

**🥗 Tolali ovqat (fiber)**
- Ko‘proq: karam, sabzi, bodring, ko‘kat, dukkakli
""")

st.markdown("---")

# ---------- goal specific ----------
if goal == "ozish":
    st.subheader("🔥 Ozish uchun strategiya")
    st.success("Asosiy maqsad: kaloriya defitsit + protein + yurish.")

    st.markdown("""
### 📌 Amaliy reja
- **Kuniga 7–10 ming qadam** (yoki 30–45 daqiqa piyoda yurish)
- Shirin ichimliklarni kamaytiring (cola/sharbat) → suv/limonli suv
- Kechki ovqatni yengilroq qiling (protein + sabzavot)

### 🍽 Nima yeyish kerak (misollar)
- Nonushta: **2 tuxum + bodring/pomidor + 1 bo‘lak qora non**
- Tushlik: **tovuq ko‘kragi + salat + ozroq guruch/grechka**
- Kechki ovqat: **qatiq/kefir + salat** yoki **baliq + sabzavot**
- Snack: **olma / yogurt / bodom (oz miqdor)**

### 🚫 Ko‘p bo‘lsa kamaytiring
- qovurilgan ovqat, chips, shirinlik, fast food, ko‘p non
""")

elif goal == "saqlash":
    st.subheader("⚖️ Vaznni saqlash")
    st.info("Asosiy maqsad: balans, rejim, barqaror odatlar.")

    st.markdown("""
### 📌 Amaliy reja
- Haftasiga 3–4 marta engil mashq yoki yurish
- Ovqatlanish va uyqu rejimi: **7–8 soat uyqu**
- Kuniga 3 ta asosiy ovqat + 1–2 snack

### 🍽 Balansli likopcha
- 1/2: sabzavot va ko‘kat
- 1/4: protein (tovuq, tuxum, tvorog, baliq)
- 1/4: uglevod (guruch, grechka, kartoshka, makaron)

### ✅ Oson odatlar
- Har kuni 1 ta meva
- Har kuni salat
- Shakarni kamaytirish
""")

else:  # semirish
    st.subheader("💪 Semirish uchun strategiya")
    st.warning("Asosiy maqsad: kaloriya ortiqcha + kuch mashqlari + sifatli ovqat.")

    st.markdown("""
### 📌 Amaliy reja
- Kuniga 4–5 marta ovqat (kichik-kichik)
- Har ovqatda protein bo‘lsin
- Haftasiga 3 marta kuch mashqlari (push-up, squat, gantel)

### 🍽 Kaloriyasi yuqori, foydali ovqatlar
- **yong‘oq, bodom, pista** (oz-ozdan)
- **tvorog, pishloq, sut**
- **guruch, makaron, kartoshka**
- **banan, quruq meva (kuraga/mayiz)**

### ✅ Namuna menyu
- Nonushta: bo‘tqa + sut + banan
- Tushlik: osh (kichik porsiya) + salat
- Kechki ovqat: makaron + qiyma/tovuq
- Snack: yogurt + yong‘oq
""")

st.markdown("---")

# ---------- checklist ----------
st.subheader("📌 Kunlik checklist")
colA, colB, colC = st.columns(3)

with colA:
    st.checkbox("✅ Suv ichdim (≥ 1.5L)")
    st.checkbox("✅ 1 ta meva yedim")
with colB:
    st.checkbox("✅ Sabzavot/salat bor edi")
    st.checkbox("✅ Protein yedim")
with colC:
    st.checkbox("✅ Yurish/mashq qildim")
    st.checkbox("✅ Kechasi yaxshi uxlashga harakat qildim")

st.caption("Kichik odatlar katta natija beradi. Har kuni oz-ozdan davom eting 🙂")
