import streamlit as st

st.title("ℹ️ Ilova haqida")
st.caption("Sog‘lom Hayot — kaloriyani boshqarish va odatlarni kuzatish uchun mini yordamchi.")

st.markdown("""
### 🎯 Maqsad
**Sog‘lom Hayot** ilovasi sizga:
- kunlik kaloriya ehtiyojini hisoblash,
- ovqatlarni kiritib kunlik limitni kuzatish,
- vazn o‘zgarishini grafikda ko‘rish,
- sog‘lom odatlarni shakllantirish

ishda yordam beradi.

---

### 🧠 Qanday ishlaydi?
- **Kaloriya kalkulyatori**: BMR → TDEE → maqsadga mos kaloriya (ozish/saqlash/semirish)
- **Food Log**: ovqatlarni qo‘shasiz va bugungi jami kaloriyani ko‘rasiz
- **Vazn kuzatuvchi**: kuniga bir nechta yozuv kiritib trendni kuzatasiz
- Ma’lumotlar **SQLite** bazada saqlanadi (refresh bo‘lsa ham yo‘qolmaydi)

---

### ⚠️ Muhim eslatma
Bu ilova tibbiy maslahat bermaydi. Natijalar **taxminiy** hisob-kitoblarga asoslangan.
Agar sog‘liq muammolari bo‘lsa, shifokor/dietolog bilan maslahat qiling.

---

## 👤 Muallif haqida
**Suhrob Panjiyev**  
- 🎓 Yo‘nalish: Axborot tizimlari va texnologiyalari (3-bosqich)  
- 💻 Qiziqishlar: Python, Data Science, Machine Learning, Web ilovalar  
- 📌 Maqsad: foydali va ommabop IT loyihalar qilish

📬 Aloqa:
- Telegram: **https://t.me/atlet_bro**
- GitHub: **https://github.com/suhrob-panjiyev**
- Email: **panjiyevsuhrob84@gmail.com**

---

### ⭐ Kelajakdagi rejalar
- ovqatlar bazasini kengaytirish (o‘zbekcha taomlar)
- dashboard (haftalik kaloriya/vazn tahlili)
- foydalanuvchi profili va cloud bazaga ulash (keyingi bosqich)
""")

