import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("mxmh_survey_results.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Clean + convert numeric columns
df = df.dropna(subset=['fav_genre', 'anxiety', 'depression', 'age', 'hours_per_day'])
df['age'] = pd.to_numeric(df['age'], errors='coerce')
df['hours_per_day'] = pd.to_numeric(df['hours_per_day'], errors='coerce')

# Streamlit Page Setup
st.set_page_config(page_title="Music & Mental Health", page_icon="🎧")
st.title("🎧 The Healing Power of Music")
st.markdown("""
Welcome to a data exploration of how music genres relate to mental well-being.  
This dashboard is built using real-world survey data to uncover:

- 🎵 Which music genres are associated with lower anxiety or depression?
- 💡 Can our listening habits say something about our emotional health?
- 🔍 What patterns can we discover in how people use music as a coping tool?

Scroll down and interact with the dashboard to uncover meaningful insights.
""")

# --- Interactivity: Age and Hours Filters ---
st.sidebar.header("🔍 Filter Options")

# Age Filter
min_age = int(df['age'].min())
max_age = int(df['age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(18, 30))

# Hours Per Day Filter
min_hours = float(df['hours_per_day'].min())
max_hours = float(df['hours_per_day'].max())
hours_range = st.sidebar.slider("Select Listening Hours per Day", min_value=0.0, max_value=10.0, value=(1.0, 5.0), step=0.5)

# Filter the data based on user input
filtered_df = df[
    (df['age'] >= age_range[0]) & 
    (df['age'] <= age_range[1]) & 
    (df['hours_per_day'] >= hours_range[0]) &
    (df['hours_per_day'] <= hours_range[1])
]

# Genre Selector
genres = sorted(df['fav_genre'].dropna().unique())
selected_genre = st.selectbox("Choose a genre to highlight:", genres)

# Average Anxiety by Genre
st.subheader("Average Anxiety Score by Genre")
genre_anxiety = filtered_df.groupby('fav_genre')['anxiety'].mean().sort_values()

fig1, ax1 = plt.subplots()
sns.barplot(x=genre_anxiety.values, y=genre_anxiety.index, palette='coolwarm', ax=ax1)
ax1.axvline(genre_anxiety[selected_genre], color='black', linestyle='--', label=f"{selected_genre}")
ax1.legend()
st.pyplot(fig1)

# Average Depression by Genre
st.subheader("Average Depression Score by Genre")
genre_depression = filtered_df.groupby('fav_genre')['depression'].mean().sort_values()

fig2, ax2 = plt.subplots()
sns.barplot(x=genre_depression.values, y=genre_depression.index, palette='mako', ax=ax2)
ax2.axvline(genre_depression[selected_genre], color='black', linestyle='--', label=f"{selected_genre}")
ax2.legend()
st.pyplot(fig2)

# Key Insights
st.markdown(f"""
### 🔍 Insight for {selected_genre}
- **Avg Anxiety Score:** {round(genre_anxiety[selected_genre], 2)}
- **Avg Depression Score:** {round(genre_depression[selected_genre], 2)}
""")

# Footer
st.markdown("---")
st.markdown("""
🔗 **Created by Siri Meghana Annamdevula**  
📊 Powered by Python, Pandas, Seaborn, and Streamlit  
📁 Dataset: [MXMH Music & Mental Health Survey (Kaggle)](https://www.kaggle.com/datasets/catherinerasgaitis/mxmh-survey-results)

> 🎓 This project explores the quiet power of music in mental wellness — where every beat, lyric, and rhythm tells a story about the listener.

""")

