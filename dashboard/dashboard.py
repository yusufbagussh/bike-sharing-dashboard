import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Import custom data loading function
import main_data as datasets

# Load dataset
data = datasets.load_datasets()

# Perform RFM analysis and additional calculations
@st.cache_data 
def perform_rfm_analysis(data):
    # Recency
    recency = data.groupby(['season', 'weathersit'])['dteday'].max().reset_index()
    recency['Recency (Days Ago)'] = (data['dteday'].max() - recency['dteday']).dt.days

    # Frequency
    frequency = data.groupby(['season', 'weathersit'])['cnt'].sum().reset_index()
    frequency.rename(columns={'cnt': 'Frequency (Total Rentals)'}, inplace=True)

    # Monetary
    monetary = data.groupby(['season', 'weathersit'])['cnt'].mean().reset_index()
    monetary.rename(columns={'cnt': 'Monetary (Avg Daily Rentals)'}, inplace=True)

    # Combine RFM
    rfm = recency.merge(frequency, on=['season', 'weathersit'])
    rfm = rfm.merge(monetary, on=['season', 'weathersit'])

    # Add Labels
    rfm['Season'] = rfm['season'].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
    rfm['Weather'] = rfm['weathersit'].map({1: "Clear", 2: "Mist", 3: "Light Rain", 4: "Heavy Rain"})

    return rfm

@st.cache_data 
def analyze_workingday_vs_holiday(data):
    # Frequency: Total Rentals by Working Day
    frequency = data.groupby(['workingday', 'holiday'])['cnt'].sum().reset_index()
    frequency.rename(columns={'cnt': 'Frequency (Total Rentals)'}, inplace=True)
    frequency['Type'] = frequency.apply(
        lambda row: 'Holiday' if row['holiday'] == 1 else 'Working Day' if row['workingday'] == 1 else 'Weekend', axis=1
    )

    # Monetary: Average Daily Rentals by Working Day
    monetary = data.groupby(['workingday', 'holiday'])['cnt'].mean().reset_index()
    monetary.rename(columns={'cnt': 'Monetary (Avg Daily Rentals)'}, inplace=True)
    monetary['Type'] = monetary.apply(
        lambda row: 'Holiday' if row['holiday'] == 1 else 'Working Day' if row['workingday'] == 1 else 'Weekend', axis=1
    )

    return frequency, monetary

# Perform analyses
rfm_data = perform_rfm_analysis(data)
freq_workingday, monetary_workingday = analyze_workingday_vs_holiday(data)

# Dashboard Header
st.title("Bike Sharing Data Dashboard")
st.markdown("""
Explore the patterns of bike rentals using **RFM Analysis**, focusing on **season**, **weather conditions**, and **day type**.
""")

# Sidebar Filters
st.sidebar.header("""Filter Options For Advanced Visualization""")
selected_season = st.sidebar.multiselect(
    "Select Season(s):",
    options=rfm_data['Season'].unique(),
    default=rfm_data['Season'].unique()
)
selected_weather = st.sidebar.multiselect(
    "Select Weather Condition(s):",
    options=rfm_data['Weather'].unique(),
    default=rfm_data['Weather'].unique()
)

# Apply filters for RFM data
filtered_rfm = rfm_data[(rfm_data['Season'].isin(selected_season)) &
                        (rfm_data['Weather'].isin(selected_weather))]

# Section 1: Visualizations
st.header("Visualizations")

st.subheader("Rentals by Season and Weather")
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=data[data['season'].isin([1, 2, 3, 4])], x='season', y='cnt', hue='weathersit', palette='Set2', ax=ax)
ax.set_title('Rentals by Season and Weather Condition')
ax.set_xlabel('Season (1=Spring, 2=Summer, 3=Fall, 4=Winter)')
ax.set_ylabel('Total Rentals')
ax.legend(title='Weather (1=Clear, 2=Mist, 3=Light Rain, 4=Heavy Rain)')
st.pyplot(fig)
    
st.subheader("Rentals by Day Type")
# Rentals by Day Type (Updated)
day_type_avg = data.groupby(['workingday', 'holiday'])['cnt'].mean().reset_index()
day_type_avg['Type'] = day_type_avg.apply(
    lambda row: 'Holiday' if row['holiday'] == 1 else 'Working Day' if row['workingday'] == 1 else 'Weekend', axis=1
)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=day_type_avg, x='Type', y='cnt', hue='Type', dodge=False, palette='Blues_d', ax=ax)
ax.set_title('Average Rentals by Day Type')
ax.set_xlabel('Day Type')
ax.set_ylabel('Average Rentals')
st.pyplot(fig)


# Section 2: RFM Analysis Visualizations
st.header("RFM Analysis Visualizations")

# Recency Visualization
st.subheader("Recency: Days Since Last Rental")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=filtered_rfm, x='Season', y='Recency (Days Ago)', hue='Weather', palette='coolwarm', ax=ax)
ax.set_title('Recency of Rentals by Season and Weather')
ax.set_xlabel('Season')
ax.set_ylabel('Days Since Last Rental')
ax.legend_.remove()
st.pyplot(fig)

# Frequency Visualization
st.subheader("Frequency: Total Rentals")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=filtered_rfm, x='Season', y='Frequency (Total Rentals)', hue='Weather', palette='muted', ax=ax)
ax.set_title('Frequency of Rentals by Season and Weather')
ax.set_xlabel('Season')
ax.set_ylabel('Total Rentals')
ax.legend_.remove()
st.pyplot(fig)

# Monetary Visualization
st.subheader("Monetary: Average Daily Rentals")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=filtered_rfm, x='Season', y='Monetary (Avg Daily Rentals)', hue='Weather', palette='pastel', ax=ax)
ax.set_title('Average Daily Rentals by Season and Weather')
ax.set_xlabel('Season')
ax.set_ylabel('Avg Daily Rentals')
ax.legend_.remove()
st.pyplot(fig)

# Frequency Visualization for Working Day
st.subheader("Frequency: Total Rentals by Day Type")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=freq_workingday, x='Type', y='Frequency (Total Rentals)', palette='Blues_d', ax=ax)
ax.set_title('Frequency of Rentals by Day Type')
ax.set_xlabel('Day Type')
ax.set_ylabel('Total Rentals')
st.pyplot(fig)

# Monetary Visualization for Working Day
st.subheader("Monetary: Average Daily Rentals by Day Type")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=monetary_workingday, x='Type', y='Monetary (Avg Daily Rentals)', palette='Greens_d', ax=ax)
ax.set_title('Average Daily Rentals by Day Type')
ax.set_xlabel('Day Type')
ax.set_ylabel('Avg Daily Rentals')
st.pyplot(fig)

# Footer
st.markdown("""
### About
This dashboard is built using **Streamlit** and incorporates **RFM Analysis** and comparisons of working days vs holidays to explore bike rental patterns.
Data source: Bike Sharing Dataset.
""")
