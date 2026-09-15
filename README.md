# ⚡ zz-suite — Pure Modular Resolume Performance VJ Plugins
**Professional Pure Modular VJ Toolkit untuk Ibadah Perdana UKK UNNES 2026**  
*Lokasi Project: `C:\ANDREAS\ip26-zzfx`*  
*Target Output: Novastar Video Processor (Auditorium UNNES 2400x720) & Universal Canvas (16:9, 1080p, 4K)*  
*Operator Resolume: Andreas (IP26 Production)*

---

## 🌟 Filosofi Arsitektur: 100% Pure Modular

Project ini dirancang dengan pendekatan **Pure Modular Suite (`zz-suite`)**. Setiap efek merupakan plugin mandiri (*standalone plugin*) yang terpisah secara independen:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   ZZ-SUITE PURE MODULAR PLUGINS                        │
├──────────────────────┬─────────────────────────────────────────────────┤
│ zz_pusher.cwired     │ Elastic Zoom Kick & Beat Punch                  │
│ zz_chaser.cwired     │ 7-Direction Dedicated Piano Chaser (Keys 1–7)   │
│ zz_strobe.cwired     │ High-Speed Multi-Rate Flash Strobe              │
│ zz_outliner.cwired   │ Neon Sobel Edge Glow Overlay                    │
│ zz_wiper.cwired      │ Linear Scanner Light Beam & Curtain Wipe        │
└──────────────────────┴─────────────────────────────────────────────────┘
```

### 💡 Keuntungan Pure Modular:
1. **Fleksibilitas Stacking:** Kamu bebas drag hanya efek yang kamu inginkan ke Layer atau Composition.
2. **Urutan Efek Bebas:** Efek bisa diatur urutan render-nya (misal: *Outliner* dulu baru di-*Push*, atau *Chaser* di atas *Strobe*).
3. **Ultra Ringan & Hemat GPU:** Setiap modul hanya memuat shader node yang diperlukan, nol overhead dari efek yang tidak digunakan.
4. **Respon Piano Seketika:** Setiap parameter trigger diprogram untuk mode Piano tanpa latency.

---

## 📦 Struktur Folder & Daftar File (`C:\ANDREAS\ip26-zzfx`)

Repository terbagi menjadi 2 folder utama agar rapi dan mudah digunakan:
* **`cwired/`** ➔ Berisi 5 plugin biner siap pakai untuk **Resolume Arena**.
* **`wire/`** ➔ Berisi 5 file project/source patch untuk **Resolume Wire**.

### 1. Folder `cwired/` (Siap Pakai di Resolume Arena)
| File | Ukuran | Jenis | Deskripsi & Fungsi |
| :--- | :--- | :--- | :--- |
| **`cwired/zz_pusher.cwired`** | 8.1 KB | Modular | **Elastic Zoom Kick / Bumper.** Pembesaran hentakan beat drum dengan parameter *Push Amount* & *Push Decay*. |
| **`cwired/zz_chaser.cwired`** | 39.1 KB | Modular | **7-Direction Dedicated Chaser.** 7 trigger saklar terpisah (1-7), Grid Slices (1-10), Snap to Grid, Speed, Color, Intensity. |
| **`cwired/zz_strobe.cwired`** | 8.2 KB | Modular | **High-Speed Flash Strobe.** Flash kilatan putih/warna dengan frekuensi 2–30 Hz dan kontrol intensitas. |
| **`cwired/zz_outliner.cwired`** | 7.6 KB | Modular | **Neon Sobel Edge Glow.** Deteksi garis kontur siluet kamera/lirik dengan palet warna neon dan wet/dry mix. |
| **`cwired/zz_wiper.cwired`** | 18.2 KB | Modular | **Curtain & Scanner Wipe.** Bilah sapuan cahaya (4 arah: L->R, R->L, Up->Down, Down->Up) dengan ketebalan bar dinamis. |

### 2. Folder `wire/` (Source Patch Resolume Wire)
| File | Deskripsi |
| :--- | :--- |
| **`wire/zz_pusher.wire`** | Source node patch untuk modul Pusher. |
| **`wire/zz_chaser.wire`** | Source node patch untuk modul Chaser 7-arah. |
| **`wire/zz_strobe.wire`** | Source node patch untuk modul Strobe flash. |
| **`wire/zz_outliner.wire`** | Source node patch untuk modul Outliner neon. |
| **`wire/zz_wiper.wire`** | Source node patch untuk modul Wiper curtain/scanner. |

### 3. Builder Script
| File | Deskripsi |
| :--- | :--- |
| `build_suite.py` | Python script otomatis untuk men-generate 5 project ke `wire/` dan mengompilasinya ke `cwired/` via Wire CLI. |

---

## 🚀 Cara Instalasi ke Resolume Arena

1. Buka folder [`C:\ANDREAS\ip26-zzfx\cwired`](file:///C:/ANDREAS/ip26-zzfx/cwired).
2. **Double-click** file `.cwired` yang ingin digunakan (`zz_pusher.cwired`, `zz_chaser.cwired`, `zz_strobe.cwired`, `zz_outliner.cwired`, `zz_wiper.cwired`).  
   *(Resolume Arena akan otomatis mendaftarkannya ke panel Effects).*
3. *Alternatif folder effect Resolume:* Buka Resolume Arena $\rightarrow$ **Preferences** $\rightarrow$ **Effects** $\rightarrow$ Tambahkan path folder `C:\ANDREAS\ip26-zzfx\cwired`.
4. Seluruh plugin siap digunakan di panel **Effects**!

---

## 🎛️ Panduan Parameter Setiap Modul

### 1. `zz-pusher` (Zoom Beat Punch)
* **`Push (Toggle / Piano)`:** Saklar zoom punch. Cocok di-bind ke tombol keyboard untuk ketukan kick drum.
* **`Push Amount (Slider 0.0 – 1.0)`:** Kekuatan zoom hentakan (default: `0.35`).
* **`Push Decay (Slider 0.0 – 1.0s)`:** Waktu kembali elastis (default: `0.12s`; set `0.0s` untuk snap instan).

### 2. `zz-chaser` (7-Direction Slices Runner)
Tersedia **7 saklar trigger independen**:
* **`Chase 1: Left -> Right`:** Sapuan bar vertikal dari kiri ke kanan.
* **`Chase 2: Right -> Left`:** Sapuan bar vertikal dari kanan ke kiri.
* **`Chase 3: Center -> Out`:** Bar mekar dari tengah layar ke kedua sisi luar bersamaan.
* **`Chase 4: Out -> Center`:** Bar kuncup dari sisi luar menuju tengah layar.
* **`Chase 5: Up -> Down`:** Sapuan bar horizontal dari atas ke bawah.
* **`Chase 6: Down -> Up`:** Sapuan bar horizontal dari bawah ke atas.
* **`Chase 7: Bounce`:** Bar bolak-balik terus menerus (*ping-pong*).
* **`Grid Slices (Int 1 – 10, default: 5)`:** Jumlah kolom/baris slice. Set `5` untuk layar Auditorium UNNES.
* **`Snap to Grid (Toggle, default: ON)`:** ON = lompat per panel LED modular; OFF = sapuan mulus continuous.
* **`Chase Speed (Slider 0.1 – 8.0 Hz)`:** Kecepatan lari bar cahaya.
* **`Chase Color (Color Picker)`:** Warna bilah sinar (default: *Amber Gold*).
* **`Chase Intensity (Slider 0.0 – 1.0)`:** Kecerahan bar saat melintasi layar.

### 3. `zz-strobe` (High-Speed Multi-Rate Flash)
* **`Strobe (Toggle / Piano)`:** Saklar flash putih.
* **`Strobe Rate (Slider 2.0 – 30.0 Hz)`:** Frekuensi kedipan per detik (default: `14.0 Hz`).
* **`Strobe Intensity (Slider 0.0 – 1.0)`:** Kecerahan kilatan flash.
* **`Strobe Color (Color Picker)`:** Warna kilatan (default: Putih `1.0, 1.0, 1.0`).

### 4. `zz-outliner` (Neon Sobel Edge Detection)
* **`Outline (Toggle / Piano)`:** Saklar deteksi garis tepi neon.
* **`Outline Strength (Slider 0.5 – 8.0)`:** Ketajaman & ketebalan deteksi tepi Sobel (default: `2.5`).
* **`Outline Color (Color Picker)`:** Warna garis neon (default: *Neon Cyan*).
* **`Outline Mix (Slider 0.0 – 1.0)`:** Opacity overlay garis neon di atas video.

### 5. `zz-wiper` (Scanner Light Beam & Curtain Wipe)
* **`Wiper (Toggle / Piano)`:** Saklar bilah tirai/scanner.
* **`Wipe Direction (Dropdown / Int 0 – 3)`:**
  - `0`: Kiri ke Kanan (*Left -> Right*)
  - `1`: Kanan ke Kiri (*Right -> Left*)
  - `2`: Atas ke Bawah (*Up -> Down*)
  - `3`: Bawah ke Atas (*Down -> Up*)
* **`Wipe Speed (Slider 0.1 – 6.0 Hz)`:** Kecepatan siklus sapuan beam.
* **`Bar Width (Slider 0.05 – 1.0)`:** Ketebalan bilah sapuan (default: `0.35`).
* **`Bar Color (Color Picker)`:** Warna sinar wiper.
* **`Wipe Intensity (Slider 0.0 – 1.0)`:** Kecerahan sapuan wiper.

---

## 🎹 Panduan Setting Mode Piano & Shortcut Keyboard di Resolume Arena

Hanya butuh 1 menit untuk mengatur shortcut keyboard agar performa VJ maksimal:

1. Drag modul yang diinginkan ke **Composition** (atau layer video).
2. Tekan **`Ctrl + Shift + K`** (*Shortcuts $\rightarrow$ Edit Keyboard*).
3. Klik tombol parameter di inspector, lalu tekan tombol keyboard yang diinginkan:
   * **`A`** ➔ `Push` *(pada zz-pusher)*
   * **`B`** ➔ `Strobe` *(pada zz-strobe)*
   * **`W`** ➔ `Wiper` *(pada zz-wiper)*
   * **`O`** ➔ `Outline` *(pada zz-outliner)*
   * **`1` s/d `7`** ➔ `Chase 1` s/d `Chase 7` *(pada zz-chaser)*
4. **SET MODE PIANO (PENTING):**
   * Klik shortcut yang baru dibuat pada tampilan Resolume.
   * Di panel kanan bawah (**Shortcuts Inspector**), ubah dropdown **Mode** dari *Toggle* menjadi **`Piano`**.
5. Tekan **`Esc`** untuk keluar dari mode edit shortcut.
6. **Hasil:**
   - **Tahan tombol:** Efek langsung aktif dan bergerak mengikuti irama musik.
   - **Lepas tombol:** Efek mati seketika (*instant cut*), opacity kembali ke 0.0, GPU nol beban.

---

## 🔨 Cara Compile Ulang Source Patch

Jika melakukan perubahan node logic di `build_suite.py`, jalankan command:

```powershell
python build_suite.py
```

Script akan men-generate seluruh file `.wire` ke folder `wire/` dan otomatis mengompilasinya menjadi file `.cwired` ke folder `cwired/` menggunakan Resolume Wire CLI.

---

*Dibuat khusus untuk Divisi Multimedia & Live Production IP26 — Ibadah Perdana UKK UNNES 2026.*
