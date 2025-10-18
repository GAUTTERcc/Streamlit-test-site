import pandas as pd
import streamlit as st
import plotly.express as px
import os

st.title("Програма для аналізу твітів")


file_path = "tweets.csv" 

if os.path.exists(file_path):
    st.success(f"✅ Файл {file_path} знайдено!")


    df = pd.read_csv(file_path)

    st.subheader("📄 Перші 10 записів")
    st.write(df.head(10))

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['month'] = df['date'].dt.to_period('M')

        activity = df.groupby('month').size().reset_index(name='tweets_count')

        metrics = []
        if 'likes' in df.columns:
            avg_likes = df.groupby('month')['likes'].mean().reset_index(name='avg_likes')
            metrics.append(avg_likes)
        if 'retweets' in df.columns:
            avg_retweets = df.groupby('month')['retweets'].mean().reset_index(name='avg_retweets')
            metrics.append(avg_retweets)

        for m in metrics:
            activity = activity.merge(m, on='month', how='left')

        st.subheader("📈 Активність користувача по місяцях")
        fig = px.bar(activity, 
                     x='month', 
                     y='tweets_count', 
                     text='tweets_count',
                     title="Кількість твітів по місяцях")
        
        if 'avg_likes' in activity.columns:
            fig.add_scatter(x=activity['month'], y=activity['avg_likes'], mode='lines+markers', name='Середні лайки')
        if 'avg_retweets' in activity.columns:
            fig.add_scatter(x=activity['month'], y=activity['avg_retweets'], mode='lines+markers', name='Середні репости')

        fig.update_layout(xaxis_title="Місяць", yaxis_title="Кількість твітів / середнє")
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("⚠️ У файлі має бути колонка 'date' з датою публікації.")
else:
    st.error(f"❌ Файл {file_path} не знайдено в корневій папці.")



