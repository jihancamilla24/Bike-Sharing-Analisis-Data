import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# membuat fungsi banyaknya penyewaan sepeda
def total_sewa_day_df(day_df):
   cnt_day_df =  day_df.groupby(by="dteday").agg({
      "cnt": "sum"
    })
   cnt_day_df = cnt_day_df.reset_index()
   cnt_day_df.rename(columns={
        "cnt": "cnt_sum"
    }, inplace=True)
   return cnt_day_df

# membuat fungsi banyaknya penyewa registered
def total_registered_df(day_df):
   reg_df =  day_df.groupby(by="dteday").agg({
      "registered": "sum"
    })
   reg_df = reg_df.reset_index()
   reg_df.rename(columns={
        "registered": "registered_sum"
    }, inplace=True)
   return reg_df

# membuat fungsi banyaknya penyewa sepeda (digunakan khusus untuk analisis jam)
def total_sewa_df(hour_df):
    total_penyewaan_df = hour_df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    return total_penyewaan_df

# membuat fungsi banyaknya penyewa sepeda berdasarkan musim
def jenis_musim_df(day_df): 
    season_df = day_df.groupby(by="season").cnt.sum().reset_index() 
    return season_df

# mendefinisikan data
day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)   

hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

min_date_days = day_df["dteday"].min()
max_date_days = day_df["dteday"].max()

min_date_hour = hour_df["dteday"].min()
max_date_hour = hour_df["dteday"].max()

with st.sidebar:
    # memasukkan logo 
    st.image("https://github.com/jihancamilla24/Bike-Sharing-Analisis-Data/blob/main/logoo.jpg?raw=true")
    
    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_day = day_df[(day_df["dteday"] >= str(start_date)) & 
                        (day_df["dteday"] <= str(end_date))]

main_df_hour = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                        (hour_df["dteday"] <= str(end_date))]

sewa_day_df = total_sewa_day_df(main_df_day)
registered_df = total_registered_df(main_df_day)
sum_order_items_df = total_sewa_df(main_df_hour)
season_df = jenis_musim_df(main_df_day)

# membuat visualisasi data
st.header('Bike Sharing :sparkles:')
st.subheader('Daily Share')
 
col1, col2 = st.columns(2)

# menampilkan data banyaknya penyewa sepeda keseluruhan
with col1:
    total_orders = sewa_day_df.cnt_sum.sum()
    st.metric("Total Penyewaan Sepeda", value=total_orders)

# menampilkan data banyaknya penyewa registered keseluruhan
with col2:
    total_revenue = registered_df.registered_sum.sum()
    st.metric("Total Registered", value=total_revenue)

# pertanyaan 1
st.subheader("Performa Penyewaan Sepeda Dalam 2 Tahun Terakhir")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    day_df["dteday"],
    day_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# pertanyaan 2
st.subheader("Performa Penyewaan Sepeda Dalam 2 Tahun Terakhir per Bulan")

grouped_data = day_df.groupby(pd.Grouper(key='dteday', freq='M'))['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(20, 5))
ax.plot(
    grouped_data['dteday'], 
    grouped_data['cnt'], 
    marker='o', 
    linewidth=2,
    color="#90CAF9"
    )
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# pertanyaan 3
st.subheader("Korelasi Temperatur dan Penyewaan Sepeda")

# Memplot data sebagai scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x=day_df['temp'], 
           y=day_df['cnt'], 
           color='blue', 
           alpha=0.5,
           )
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Menghitung korelasi
correlation = day_df['temp'].corr(day_df['cnt'])
st.write(f"Korelasi antara temperatur dan jumlah penyewaan sepeda: {correlation:.2f}")

# Menghitung kovariansinya
covariance = day_df['temp'].cov(day_df['cnt'])
st.write(f"Kovarians antara temperatur dan jumlah penyewaan sepeda: {covariance:.2f}")

st.subheader("Korelasi Kelembaban dan Penyewaan Sepeda")

# Memplot data sebagai scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x=day_df['hum'], 
           y=day_df['cnt'], 
           color='blue', 
           alpha=0.5,
           )
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Menghitung korelasi
correlation = day_df['hum'].corr(day_df['cnt'])
st.write(f"Korelasi antara kelembaban dan jumlah penyewaan sepeda: {correlation:.2f}")

# Menghitung kovariansinya
covariance = day_df['hum'].cov(day_df['cnt'])
st.write(f"Kovarians antara kelembaban dan jumlah penyewaan sepeda: {covariance:.2f}")

# pertanyaan 4
st.subheader("Musim Pelanggan Paling Banyak Menyewa Sepeda")

colors1 = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"]
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(
        y="cnt", 
        x="season",
        data=season_df.sort_values(by="season", ascending=False),
        palette=colors1,
    )
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

st.pyplot(fig)

st.subheader("Jam Pelanggan Menyewa Sepeda")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,6))

colors11 = ["#D3D3D3", "#D3D3D3", "#72BCD4", "#D3D3D3", "#D3D3D3"]
colors22 = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4"]

sns.barplot(x="hr", y="cnt", data=sum_order_items_df.head(5), palette=colors11, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jam", fontsize=10)
ax[0].set_title("Jam Penyewaan Sepeda Terbaik", loc="center", fontsize=10)
ax[0].tick_params(axis='y', labelsize=10)
ax[0].tick_params(axis='x', labelsize=10)
 
sns.barplot(x="hr", y="cnt", data=sum_order_items_df.sort_values(by="hr", ascending=True).head(5), palette=colors22, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jam",  fontsize=10)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Jam Penyewaan Sepeda Terburuk", loc="center", fontsize=10)
ax[1].tick_params(axis='y', labelsize=10)
ax[1].tick_params(axis='x', labelsize=10)
 
st.pyplot(fig)
