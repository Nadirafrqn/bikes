import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt


sns.set(style='white')

day_data = pd.read_csv("submission/dashboard/day.csv")
day_data.head()


day_data['weekday'] = day_data['weekday'].map({
    0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'
})
day_data['weathersit'] = day_data['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Fungsi untuk mengelompokkan data berdasarkan weekday
def create_weekday_rent_df(df):
    return df.groupby(by='weekday').agg({'cnt': 'sum'}).reset_index()

# Fungsi untuk mengelompokkan data berdasarkan hari libur
def create_holiday_rent_df(df):
    return df.groupby(by='holiday').agg({'cnt': 'sum'}).reset_index()

# Fungsi untuk mengelompokkan data berdasarkan kondisi cuaca
def create_weather_rent_df(df):
    return df.groupby(by='weathersit').agg({'cnt': 'sum'}).reset_index()

# Fungsi untuk mengelompokkan data berdasarkan bulan
def create_monthly_rent_df(df):
    df['dteday'] = pd.to_datetime(df['dteday'])  # pastikan kolom 'dteday' diubah ke datetime
    return df.groupby(df['dteday'].dt.to_period('M')).agg({'cnt': 'sum'}).reset_index()

min_date = pd.to_datetime(day_data['dteday']).dt.date.min()
max_date = pd.to_datetime(day_data['dteday']).dt.date.max()

# Komponen input untuk rentang waktu
start_date, end_date = st.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

main_df = day_data[(day_data['dteday'] >= str(start_date)) & 
                   (day_data['dteday'] <= str(end_date))]

# Membuat dataframe berdasarkan grup data
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)

# Membuat dataframe dummy untuk daily rent (contoh karena belum didefinisikan di kode asli)
daily_casual_rent_df = main_df[['casual']].copy()
daily_registered_rent_df = main_df[['registered']].copy()
daily_rent_df = main_df[['cnt']].copy()

# Membuat Dashboard
st.header('Bike Rental Dashboard')

# Bagian untuk Daily Rentals
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual User', value=daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered User', value=daily_rent_registered)

with col3:
    daily_rent_total = daily_rent_df['cnt'].sum()  
    st.metric('Total User', value=daily_rent_total)

# Bagian untuk Weatherly Rentals
st.subheader('Weatherly Rentals')

fig, ax = plt.subplots(figsize=(16, 8))
colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]

sns.barplot(
    x='weathersit',
    y='cnt',
    data=weather_rent_df,
    palette=colors,
    ax=ax
)

for index, row in weather_rent_df.iterrows():
    ax.text(index, row['cnt'] + 1, str(row['cnt']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel('Weather Condition', fontsize=15)
ax.set_ylabel('Number of Rentals', fontsize=15)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Bagian untuk Weekday and Holiday Rentals
st.subheader('Weekday and Holiday Rentals')

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 12))
colors = ["tab:blue", "tab:orange"]

# Plot untuk Holiday
sns.barplot(
    x='holiday',
    y='cnt',
    data=holiday_rent_df,
    palette=colors,
    ax=axes[0]
)

for index, row in holiday_rent_df.iterrows():
    axes[0].text(index, row['cnt'] + 1, str(row['cnt']), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Number of Rents based on Holiday', fontsize=15)
axes[0].set_xlabel('Holiday (0 = No, 1 = Yes)', fontsize=12)
axes[0].set_ylabel('Number of Rentals', fontsize=12)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

# Plot untuk Weekday
sns.barplot(
    x='weekday',
    y='cnt',
    data=weekday_rent_df,
    palette=colors,
    ax=axes[1]
)

for index, row in weekday_rent_df.iterrows():
    axes[1].text(index, row['cnt'] + 1, str(row['cnt']), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Number of Rents based on Weekday', fontsize=15)
axes[1].set_xlabel('Weekday', fontsize=12)
axes[1].set_ylabel('Number of Rentals', fontsize=12)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)
