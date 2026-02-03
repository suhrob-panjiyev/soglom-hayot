# 🥗 Sog‘lom Hayot — Smart Calorie & Fitness Tracker

Sog‘lom Hayot — bu **kaloriya hisoblash, ovqat nazorati va vazn kuzatish** uchun yaratilgan oddiy va qulay web ilova.

👉 Maqsad: odamlar sog‘lig‘iga e’tiborli bo‘lishiga yordam berish.

---

## 🚀 Demo
🔗 Live app: (https://soglom-hayot-suhrob.streamlit.app/)

---

## ✨ Asosiy imkoniyatlar

### 🔥 Kaloriya Kalkulyatori
- BMR (bazal metabolizm) hisoblash
- TDEE (kunlik energiya sarfi)
- Ozish / saqlash / semirish uchun kaloriya tavsiyasi
- Protein / Yog‘ / Uglevod (makro) hisoblash
- BMI aniqlash

### 🍔 Food Log
- Ovqatlarni qo‘shish
- Kunlik kaloriya nazorati
- O‘zbekcha taomlar bazasi
- Qidiruv (gosht / go‘sht / gosht — hammasi ishlaydi)
- CSV yuklab olish

### 📈 Vazn Tracker
- Sana + vaqt bilan yozuvlar
- Kuniga bir nechta kirish mumkin
- Grafikda progress
- CSV eksport

### 🍽 Diet Tips
- Ozish / saqlash / semirish uchun aniq maslahatlar
- Amaliy menyu misollari
- Kunlik checklist

### 💾 SQLite Database
- Ma’lumotlar saqlanib qoladi (refresh bo‘lsa ham)
- Food log + vazn + settings DB’da

---

## 🛠 Texnologiyalar

- Python
- Streamlit
- Pandas
- Matplotlib
- SQLite

---

## 📦 O‘rnatish (Local)

```bash
git clone https://github.com/USERNAME/soglom-hayot.git
cd soglom-hayot
pip install -r requirements.txt
streamlit run Home.py
```
📂 Loyiha tuzilishi

calorie_app/
│
├── Home.py
├── foods.csv
├── requirements.txt
│
├── pages/
│   ├── 1_🥗_Calculator.py
│   ├── 2_📈_Tracker.py
│   ├── 3_🍽_Diet_Tips.py
│   ├── 4_ℹ️_About.py
│   ├── 5_🍔_Food_Log.py
│   └── 6_💾_Backup_Restore.py
│
└── utils/
    ├── calculations.py
    └── db.py



👤 Muallif

Suhrob

🎓 Axborot tizimlari va texnologiyalari talabasi
💻 Python | Data Science | ML | Web Apps
📬 Telegram: @atlet_bro

⭐ Agar loyiha yoqqan bo‘lsa

Repo’ga ⭐ star bosishni unutmang 🙂
