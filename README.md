# submission-analisis-data

Proyek ini berisi proses analisis data menggunakan Jupyter Notebook serta dashboard interaktif yang dibuat menggunakan **Streamlit**.

## Struktur Folder

```text
submission/
├── dashboard/
│   ├── main_data.csv
│   └── dashboard.py
├── data/
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   └── order_reviews_dataset.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Cara Menjalankan Dashboard

### 1. Buka terminal atau Command Prompt

Masuk ke folder utama proyek:

```bash
cd submission
```

### 2. Install library yang dibutuhkan

Pastikan Python sudah terpasang, kemudian jalankan:

```bash
pip install -r requirements.txt
```

Perintah tersebut akan menginstal library yang digunakan pada proyek, seperti `pandas`, `numpy`, `matplotlib`, `seaborn`, dan `streamlit`.

### 3. Jalankan dashboard Streamlit

Masih dari folder utama proyek, jalankan perintah berikut:

```bash
streamlit run dashboard/dashboard.py
```

### 4. Buka dashboard

Setelah perintah dijalankan, Streamlit akan menampilkan alamat lokal, biasanya:

```text
http://localhost:8501
```

Buka alamat tersebut melalui browser untuk melihat dashboard.

## Alternatif Jika Perintah `streamlit` Tidak Dikenali

Gunakan perintah berikut:

```bash
python -m streamlit run dashboard/dashboard.py
```

## Menghentikan Dashboard

Untuk menghentikan dashboard, kembali ke terminal lalu tekan:

```text
Ctrl + C
```

## Catatan

Pastikan file `main_data.csv` tetap berada di dalam folder `dashboard` bersama dengan `dashboard.py` agar dashboard dapat membaca data dengan benar.
