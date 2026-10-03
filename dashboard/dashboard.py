from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Olist E-Commerce Dashboard",
    page_icon="📊",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "main_data.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df


def rupiah_like(value):
    # Dataset memakai satuan mata uang aslinya. Format ini hanya untuk pemisah ribuan.
    return f"{value:,.2f}"


df = load_data()

st.title("Dashboard Analisis Olist E-Commerce")
st.caption(
    "Fokus analisis: pertumbuhan transaksi dan hubungan ketepatan pengiriman dengan review pelanggan."
)

min_date = df["order_purchase_timestamp"].min().date()
max_date = df["order_purchase_timestamp"].max().date()

st.sidebar.header("Filter")
date_range = st.sidebar.date_input(
    "Periode transaksi",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

mask = (
    df["order_purchase_timestamp"].dt.date >= start_date
) & (
    df["order_purchase_timestamp"].dt.date <= end_date
)
filtered = df.loc[mask].copy()

st.subheader("Ringkasan Periode Terpilih")
col1, col2, col3, col4 = st.columns(4)

order_count = filtered["order_id"].nunique()
sales_total = filtered["sales_value"].sum()
avg_review = filtered["review_score"].mean()
valid_delivery = filtered[filtered["delivery_status"].notna()]
late_rate = (
    (valid_delivery["delivery_status"] == "Late").mean() * 100
    if not valid_delivery.empty else 0
)

col1.metric("Order Delivered", f"{order_count:,}")
col2.metric("Nilai Penjualan", rupiah_like(sales_total))
col3.metric("Avg. Review", f"{avg_review:.2f}" if pd.notna(avg_review) else "-")
col4.metric("Late Delivery Rate", f"{late_rate:.2f}%")

st.divider()
st.header("Pertanyaan 1 — Pertumbuhan Transaksi")
st.write(
    "Bagaimana perubahan nilai penjualan dan jumlah order delivered bulanan pada "
    "Januari–Agustus 2018 dibanding Januari–Agustus 2017?"
)

q1 = df[
    df["order_purchase_timestamp"].dt.year.isin([2017, 2018])
    & df["order_purchase_timestamp"].dt.month.between(1, 8)
].copy()
q1["year"] = q1["order_purchase_timestamp"].dt.year
q1["month_num"] = q1["order_purchase_timestamp"].dt.month
q1["month"] = q1["order_purchase_timestamp"].dt.strftime("%b")

monthly = (
    q1.groupby(["year", "month_num", "month"], as_index=False)
    .agg(sales_value=("sales_value", "sum"), orders=("order_id", "nunique"))
    .sort_values(["month_num", "year"])
)

left, right = st.columns(2)
with left:
    fig, ax = plt.subplots(figsize=(7, 4))
    for year in [2017, 2018]:
        temp = monthly[monthly["year"] == year]
        ax.plot(temp["month"], temp["sales_value"], marker="o", label=str(year))
    ax.set_title("Nilai Penjualan Jan–Ags 2017 vs 2018")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Sum of price")
    ax.ticklabel_format(style="plain", axis="y")
    ax.legend(title="Tahun")
    fig.tight_layout()
    st.pyplot(fig)

with right:
    fig, ax = plt.subplots(figsize=(7, 4))
    for year in [2017, 2018]:
        temp = monthly[monthly["year"] == year]
        ax.plot(temp["month"], temp["orders"], marker="o", label=str(year))
    ax.set_title("Jumlah Order Delivered Jan–Ags 2017 vs 2018")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Order")
    ax.legend(title="Tahun")
    fig.tight_layout()
    st.pyplot(fig)

sales_2017 = q1.loc[q1["year"] == 2017, "sales_value"].sum()
sales_2018 = q1.loc[q1["year"] == 2018, "sales_value"].sum()
orders_2017 = q1.loc[q1["year"] == 2017, "order_id"].nunique()
orders_2018 = q1.loc[q1["year"] == 2018, "order_id"].nunique()
sales_growth = (sales_2018 / sales_2017 - 1) * 100
order_growth = (orders_2018 / orders_2017 - 1) * 100

st.info(
    f"Jan–Ags 2018 menghasilkan nilai penjualan {sales_growth:.2f}% lebih tinggi "
    f"dan jumlah order {order_growth:.2f}% lebih tinggi dibanding Jan–Ags 2017."
)

st.divider()
st.header("Pertanyaan 2 — Pengiriman dan Kepuasan Pelanggan")
st.write(
    "Seberapa besar perbedaan review antara pesanan tepat waktu/lebih cepat "
    "dan pesanan terlambat selama Januari–Agustus 2018?"
)

q2 = df[
    (df["order_purchase_timestamp"] >= "2018-01-01")
    & (df["order_purchase_timestamp"] < "2018-09-01")
].dropna(subset=["delivery_status", "review_score"]).copy()
q2["low_rating"] = q2["review_score"] <= 2

summary = (
    q2.groupby("delivery_status", as_index=False)
    .agg(
        orders=("order_id", "nunique"),
        avg_review=("review_score", "mean"),
        low_rating_pct=("low_rating", "mean"),
    )
)
summary["low_rating_pct"] *= 100
status_order = ["On-time / early", "Late"]
summary = summary.set_index("delivery_status").reindex(status_order).reset_index()

left, right = st.columns(2)
with left:
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(summary["delivery_status"], summary["avg_review"])
    ax.set_title("Rata-rata Review Score")
    ax.set_xlabel("Status Pengiriman")
    ax.set_ylabel("Review Score")
    ax.set_ylim(0, 5)
    ax.bar_label(bars, fmt="%.2f")
    fig.tight_layout()
    st.pyplot(fig)

with right:
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(summary["delivery_status"], summary["low_rating_pct"])
    ax.set_title("Rating Rendah (1–2)")
    ax.set_xlabel("Status Pengiriman")
    ax.set_ylabel("Persentase (%)")
    ax.bar_label(bars, fmt="%.1f%%")
    fig.tight_layout()
    st.pyplot(fig)

on_time_review = summary.loc[
    summary["delivery_status"] == "On-time / early", "avg_review"
].iloc[0]
late_review = summary.loc[
    summary["delivery_status"] == "Late", "avg_review"
].iloc[0]
late_low = summary.loc[
    summary["delivery_status"] == "Late", "low_rating_pct"
].iloc[0]

st.info(
    f"Rata-rata review turun dari {on_time_review:.2f} pada pengiriman tepat waktu/lebih cepat "
    f"menjadi {late_review:.2f} pada pengiriman terlambat. "
    f"Pada order terlambat, {late_low:.2f}% review berada pada rating 1–2."
)

st.divider()
st.header("Rekomendasi")
st.write(
    "Prioritaskan monitoring order yang mendekati estimated delivery date dan evaluasi "
    "proses logistik yang sering menghasilkan keterlambatan. Untuk perencanaan kapasitas, "
    "gunakan volume transaksi absolut bersama pertumbuhan YoY agar tidak bias oleh baseline rendah."
)
