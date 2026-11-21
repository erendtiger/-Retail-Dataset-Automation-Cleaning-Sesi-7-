"""
clean_retail.py
Retail Dataset Automation & Cleaning (Sesi 7 - Python Automation Tool)

Jalankan dari terminal:
    python clean_retail.py
"""

import os
import sys

import pandas as pd


class DataCleaner:
    """Class untuk membersihkan dataset transaksi retail."""

    def __init__(self, input_path: str):
        self.input_path = input_path
        self.df = None

    # 1. Load data mentah
    def load_data(self):
        self.df = pd.read_csv(self.input_path)
        print(f"[LOAD] {self.input_path} -> {self.df.shape[0]} baris, {self.df.shape[1]} kolom")
        return self

    # 2. String normalization
    def clean_text(self, columns):
        """Hapus spasi di awal/akhir lalu ubah ke Title Case."""
        for col in columns:
            self.df[col] = self.df[col].astype("string").str.strip().str.title()
        print(f"[TEXT] Normalisasi teks (strip + Title Case): {columns}")
        return self

    # 3. Hapus duplikat
    def drop_duplicates(self):
        before = len(self.df)
        self.df = self.df.drop_duplicates().reset_index(drop=True)
        print(f"[DUPLIKAT] {before - len(self.df)} baris duplikat dihapus ({before} -> {len(self.df)})")
        return self

    # 4. Imputasi missing values
    def fill_missing(self, column, value=0):
        n_missing = int(self.df[column].isna().sum())
        self.df[column] = self.df[column].fillna(value).astype(int)  # jumlah beli = bilangan bulat
        print(f"[MISSING] {n_missing} nilai kosong di '{column}' diisi dengan {value}")
        return self

    # 5. Ekspor
    def save_data(self, output_path: str):
        self.df.to_csv(output_path, index=False)
        print(f"[SAVE] Data bersih disimpan ke {output_path} ({self.df.shape[0]} baris)")
        return self

    def run_all(self, output_path: str):
        """Jalankan seluruh pipeline pembersihan sekali panggil."""
        text_cols = ["nama_produk", "kategori", "metode_bayar", "kota_pembeli"]
        return (
            self.load_data()
            .clean_text(text_cols)
            .drop_duplicates()
            .fill_missing("jumlah_beli", 0)
            .save_data(output_path)
        )


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "dataset_retail_homework.csv")
    output_file = os.path.join(base_dir, "dataset_retail_clean.csv")

    if not os.path.exists(input_file):
        sys.exit(f"File tidak ditemukan: {input_file}")

    DataCleaner(input_file).run_all(output_file)
    print("Selesai.")
