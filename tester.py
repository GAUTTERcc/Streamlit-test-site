import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Програма для аналізу твітів")

# Вибір методу завантаження
set_file = st.selectbox("Оберіть метод:", ["Обрати", "CSV", "JSON"])

if set_file in ["CSV", "JSON"]:
    upload_file = st.file_uploader(f"Завантажте {set_file}-файл", type=set_file.lower())

    if upload_file:
        st.success(f"✅ Файл {set_file} успішно завантажено!")

        if set_file == "CSV":
            df = pd.read_csv(upload_file)
        
        elif set_file == "JSON":
            df = pd.read_json(upload_file)

        st.subheader("📄 Перші 10 записів")
        st.write(df.head(10))

        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['month'] = df['date'].dt.to_period('M')
            activity = df.groupby('month').size()

            st.subheader("📈 Активність користувача (кількість твітів)")
            fig, ax = plt.subplots()
            activity.plot(kind='bar', ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.warning("⚠️ У файлі має бути колонка 'date' з датою публікації.")
    else:
        st.info("⬆️ Завантажте файл для аналізу.")
else:
    st.info("ℹ️ Ви не обрали метод!")
