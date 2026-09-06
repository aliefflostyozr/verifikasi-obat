"""
4_ℹ️_Tentang.py - Halaman informasi untuk pengunjung website: penjelasan sistem,
isi website, cara pakai, tujuan, dan keterbatasannya.
"""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from theme import page_setup, hero, section_title, icon, feature_card

page_setup("Tentang - Sistem Verifikasi Obat", "ℹ️")
hero("Informasi untuk Pengunjung", "ℹ️ Tentang Website Ini",
     "Penjelasan lengkap tentang apa itu Sistem Verifikasi Obat Otomatis, apa saja isinya, "
     "cara memakainya, tujuan pembuatannya, dan batasan yang perlu Anda ketahui.")

# ------------------------------------------------------------------
# 1. Apa itu sistem ini
# ------------------------------------------------------------------
section_title("hospital", "Apa Itu Sistem Verifikasi Obat Otomatis")
st.markdown("""
**Sistem Verifikasi Obat Otomatis** adalah website prototipe riset hasil kerja sama
**Institut Teknologi Sepuluh Nopember (ITS)** dan **Instalasi Farmasi RSUD Haji Surabaya**.

Website ini dibuat untuk membantu tenaga farmasi memeriksa apakah obat yang sudah disiapkan
di meja penyiapan sudah sesuai dengan resep pasien (e-resep), memakai teknologi
*computer vision* (AI pengenal gambar). Caranya:

1. Foto meja penyiapan obat diambil.
2. Sistem AI mendeteksi dan menghitung setiap pil/obat yang ada di foto, lalu (kalau
   modul jenis obatnya aktif) mengenali jenis obatnya juga.
3. Hasil hitungan itu dicocokkan secara otomatis dengan daftar e-resep.
4. Website menampilkan status: **SESUAI**, **TIDAK SESUAI**, **TIDAK YAKIN**, atau
   **GANGGUAN DATA**.

Prinsip utama sistem ini adalah ***human-in-the-loop***: AI hanya membantu mempercepat
pengecekan, sementara keputusan akhir soal kesesuaian obat tetap sepenuhnya berada di
tangan apoteker atau tenaga farmasi yang bertugas.
""")

# ------------------------------------------------------------------
# 2. Isi website
# ------------------------------------------------------------------
section_title("flask", "Isi Website Ini")
st.markdown("Website ini terdiri dari empat halaman, semuanya bisa diakses lewat menu di sidebar sebelah kiri:")

f1, f2 = st.columns(2)
with f1:
    feature_card("scan", "🔬 Verifikasi Foto",
                  "Untuk mengecek satu foto meja penyiapan obat. Upload foto, isi daftar "
                  "e-resep, lalu sistem langsung menampilkan hasil deteksi dan status kecocokannya.")
with f2:
    feature_card("chart", "📊 Dashboard Pengujian",
                  "Untuk menguji kemampuan sistem sekaligus pada banyak foto (pengujian batch), "
                  "lengkap dengan angka akurasi dan rincian hasil per foto.")
st.write("")
f3, f4 = st.columns(2)
with f3:
    feature_card("brain", "📈 Hasil Riset",
                  "Berisi seluruh hasil eksperimen ilmiah di balik sistem ini: perbandingan "
                  "beberapa model AI, uji ketahanan sistem, kecepatan pemrosesan, hingga "
                  "visualisasi bagian gambar yang jadi perhatian AI saat mengambil keputusan.")
with f4:
    feature_card("hospital", "ℹ️ Tentang",
                  "Halaman yang sedang Anda baca ini - penjelasan umum, cara pakai, tujuan, "
                  "dan keterbatasan website.")

# ------------------------------------------------------------------
# 3. Cara menggunakan website
# ------------------------------------------------------------------
section_title("scan", "Cara Menggunakan Website Ini")

with st.expander("🔬 Cara memakai halaman Verifikasi Foto", expanded=True):
    st.markdown("""
1. Buka halaman **🔬 Verifikasi Foto** dari sidebar.
2. Pada bagian **1. Upload Foto**, unggah satu foto meja penyiapan obat (format JPG, JPEG,
   PNG, atau BMP).
3. Pada bagian **2. Data E-Resep**, isi daftar obat sesuai resep pasien: nama obat dan
   jumlah yang seharusnya ada. Anda bisa menambah baris obat dengan tombol **➕ Tambah obat**,
   atau menghapus baris dengan tombol **🗑️ Hapus**.
4. Klik tombol **🚀 Jalankan Verifikasi**.
5. Dalam beberapa detik, sistem akan menampilkan foto hasil deteksi (kotak hijau berarti
   sesuai, merah berarti tidak sesuai, oranye berarti tidak yakin) beserta status akhir dan
   rincian jumlah per jenis obat.
""")

with st.expander("📊 Cara memakai halaman Dashboard Pengujian"):
    st.markdown("""
Halaman ini untuk menguji sistem pada banyak foto sekaligus, bukan satu per satu. Ada dua
cara mengisi data ujinya (pilih salah satu di sidebar):

- **Folder lokal** - kalau Anda menjalankan website ini di komputer/server sendiri dan sudah
  punya kumpulan foto uji beserta data acuannya di dalam satu folder.
- **Upload dari browser** - unggah beberapa foto langsung dari perangkat Anda, lalu tempelkan
  data acuannya (format JSON) ke kotak teks yang disediakan.

Setelah data uji siap, klik **🚀 Jalankan Pengujian Batch** dan sistem akan memproses semua
foto sekaligus, menampilkan tingkat akurasi, tabel hasil per foto, dan ringkasan kesalahan
yang terjadi.
""")

with st.expander("📈 Cara membaca halaman Hasil Riset"):
    st.markdown("""
Halaman ini berisi bukti-bukti ilmiah di balik sistem ini, disajikan dalam beberapa tab:

- **🏆 Baseline/SOTA** - perbandingan performa beberapa arsitektur AI yang diuji.
- **🧪 Ablation Study** - pengujian pengaruh berbagai pengaturan (ukuran model, resolusi
  gambar, skema pelatihan, dll) terhadap hasil.
- **⚡ Latency** - seberapa cepat sistem memproses satu foto.
- **🩺 Data Asli RSUD** - hasil pengujian memakai foto asli dari rumah sakit (kalau sudah
  tersedia).
- **🔍 Error Analysis** - rincian kapan dan kenapa sistem cenderung salah mendeteksi atau
  mengklasifikasi.
- **🧠 Explainability** - visualisasi bagian gambar mana yang paling memengaruhi keputusan AI.
- **🔗 Simulasi E-Resep** - simulasi seberapa cepat seluruh alur (foto sampai status akhir)
  berjalan dari ujung ke ujung.

Anda tidak perlu memahami detail teknis di halaman ini untuk memakai fitur verifikasi obat -
halaman ini lebih ditujukan bagi yang tertarik pada sisi riset dan validasi ilmiah sistem.
""")

# ------------------------------------------------------------------
# 4. Tujuan pembuatan website
# ------------------------------------------------------------------
section_title("shield", "Tujuan Pembuatan Website Ini")
st.markdown("""
Website ini dibuat sebagai bagian dari riset untuk menjajaki apakah teknologi *computer
vision* dapat membantu proses verifikasi obat di instalasi farmasi rumah sakit, dengan
tujuan:

- **Mempercepat proses pengecekan** kesesuaian obat dengan resep, yang biasanya dilakukan
  secara manual oleh tenaga farmasi.
- **Mengurangi risiko kesalahan manusia** (human error) akibat kelelahan atau beban kerja
  tinggi, tanpa menghilangkan peran pengawasan manusia.
- **Menjadi bahan riset ilmiah** yang bisa dipublikasikan dan dikembangkan lebih lanjut,
  baik oleh tim ITS maupun peneliti lain di bidang serupa.
- **Menjadi purwarupa (prototipe) awal** yang bisa terus disempurnakan sebelum
  dipertimbangkan untuk dipakai secara nyata di lingkungan rumah sakit.
""")

# ------------------------------------------------------------------
# 5. Keterbatasan website (untuk publik)
# ------------------------------------------------------------------
section_title("brain", "Yang Perlu Anda Ketahui Sebelum Memakai Sistem Ini")
st.markdown("""
- Ini adalah **prototipe riset tahap awal**, bukan produk medis yang sudah disertifikasi
  untuk penggunaan klinis penuh.
- Model AI saat ini masih dilatih dari **dataset foto publik**, sehingga tingkat akurasinya
  pada foto obat asli di lapangan (misalnya kondisi pencahayaan atau kemasan obat yang
  berbeda-beda) masih dalam tahap penyempurnaan lebih lanjut.
- Sistem bisa saja salah mendeteksi jumlah maupun jenis obat, terutama pada foto dengan
  pencahayaan gelap, objek yang sangat kecil, atau obat yang ditata terlalu rapat/menumpuk.
- Status **TIDAK YAKIN** atau **GANGGUAN DATA** sengaja ditampilkan setiap kali sistem tidak
  cukup percaya diri dengan hasilnya, atau data e-reseonya tidak lengkap - ini justru
  bagian dari desain keamanan sistem, supaya sistem tidak pernah "asal menyatakan sesuai".
- Anggap hasil dari website ini sebagai **alat bantu**, bukan pengganti pemeriksaan manual.
  Keputusan akhir soal kesesuaian obat tetap harus dilakukan oleh tenaga farmasi yang
  berwenang.
- Kalau Anda menemukan hasil yang tampak keliru atau mengalami kendala saat memakai
  website ini, silakan hubungi pengembang untuk membantu proses perbaikan sistem ke
  depannya.
""")
