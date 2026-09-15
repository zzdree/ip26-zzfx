# ⚡ zz-suite — Pure Modular Resolume Performance VJ Plugins
**Professional Pure Modular VJ Toolkit untuk Ibadah Perdana UKK UNNES 2026**  
*Lokasi Project: [`C:\ANDREAS\ip26-zzfx`](file:///C:/ANDREAS/ip26-zzfx)*  
*Repository GitHub: [https://github.com/zzdree/ip26-zzfx](https://github.com/zzdree/ip26-zzfx)*  
*Target Output: Novastar Video Processor (Auditorium UNNES 2400x720) & Universal Canvas (16:9, 1080p, 4K)*  
*Operator Resolume: Andreas (IP26 Production)*

---

## 🌟 Filosofi Arsitektur: 100% Pure Modular

Project ini dirancang dengan standar **Pure Modular Architecture (`zz-suite`)**. Setiap efek merupakan plugin mandiri (*standalone compiled binary*) yang independen dan terisolasi:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   ZZ-SUITE PURE MODULAR PLUGINS                        │
├──────────────────────┬─────────────────────────────────────────────────┤
│ zz_pusher.cwired     │ Efek Kejut: Beat Punch Zoom + Solid Glow Fade   │
│ zz_chaser.cwired     │ 1-Screen Precision Grid Runner (Slices & Bounce)│
│ zz_wiper.cwired      │ Smooth Continuous Scanner Curtain Wipe          │
│ zz_strobe.cwired     │ High-Speed Native Piano Flash Strobe            │
│ zz_stroke.cwired     │ Animated Snake Border Glow with Fading Tail     │
└──────────────────────┴─────────────────────────────────────────────────┘
```

### 💡 Keuntungan Pure Modular:
1. **Fleksibilitas Stacking:** Bebas drag hanya efek yang diperlukan ke Composition, Layer, atau Clip.
2. **Bebas Crash (*Crash-Proof & Zero Conflict*):** Setiap modul berdiri sendiri tanpa dependensi eksternal, compiled native menggunakan official Resolume Wire Engine.
3. **Ultra Ringan & Hemat GPU:** Modul hanya memproses shader saat aktif. Saat piano key dilepas, opacity langsung cut ke 0.0 (nol beban GPU).
4. **Urutan Efek Dinamis:** Urutan render bebas diatur (misal: *Stroke* di atas video, lalu di-*Push* bersamaan dengan *Wiper*).

---

## 📐 Fleksibilitas Resolusi & Fleksibilitas Penempatan

### 1. Dynamic Resolution (100% Fleksibel)
- Seluruh 5 plugin dibangun menggunakan sistem koordinat **Relative Texture & Procedural Canvas (`resolution-relative: [1, 1]`)**.
- **Hasil:**
  - ✅ **1920x1080 (FHD / Monitor Preview):** Tampilan proporsional dan tajam.
  - ✅ **2400x720 (Novastar LED Wall Auditorium UNNES):** Otomatis menyesuaikan aspek rasio ultrawide panggung tanpa distorsi.
  - ✅ **4K / Custom Resolution:** 100% adaptif mengikuti resolusi video buffer tanpa perlu setting ulang.

### 2. Penempatan: Composition vs Layer vs Clip
- **Di Composition (Global Master FX):**
  - **Sangat Aman!** Semua efek akan memengaruhi keseluruhan output visual (Video Background + Kamera + Lowerthird/Lirik). Sangat direkomendasikan untuk *Pusher* dan *Strobe* saat drop musik/reff lagu.
- **Di Layer (Specific Track FX):**
  - Efek hanya memengaruhi layer tersebut (misalnya hanya di Layer Background Motion Graphics, sementara Layer Lirik tetap bersih).
- **Di Clip (Individual Video FX):**
  - Efek melekat langsung pada video clip tertentu saat di-trigger.

---

## 📦 Struktur Folder & File (`C:\ANDREAS\ip26-zzfx`)

Repository terbagi menjadi 2 folder utama:
* **[`cwired/`](file:///C:/ANDREAS/ip26-zzfx/cwired)** ➔ Berisi 5 plugin biner siap pakai untuk **Resolume Arena**.
* **[`wire/`](file:///C:/ANDREAS/ip26-zzfx/wire)** ➔ Berisi 5 source patch untuk **Resolume Wire**.

### 1. Folder `cwired/` (Siap Pakai di Resolume Arena)
| File | Ukuran | Jenis | Deskripsi & Fitur Utama |
| :--- | :--- | :--- | :--- |
| **[`cwired/zz_pusher.cwired`](file:///C:/ANDREAS/ip26-zzfx/cwired/zz_pusher.cwired)** | 15.2 KB | Modular | **Efek Kejut (Beat Zoom Kick + Solid Flash).** Dilengkapi tombol klik `Punch!` di inspector & piano toggle, zoom membesar seketika lalu pudar halus bersama kilatan solid. |
| **[`cwired/zz_chaser.cwired`](file:///C:/ANDREAS/ip26-zzfx/cwired/zz_chaser.cwired)** | 25.0 KB | Modular | **1-Screen Precision Grid Runner.** Tanpa perlu slice screen / Advanced Output! Custom Grid 1–10 (default 5 panel), Snap to Grid, 6 arah gerakan, opsi Bounce (ping-pong vs looping). |
| **[`cwired/zz_wiper.cwired`](file:///C:/ANDREAS/ip26-zzfx/cwired/zz_wiper.cwired)** | 21.4 KB | Modular | **Smooth Continuous Scanner Curtain Wipe.** Bilah sapuan cahaya continuous (tanpa grid), 6 arah gerakan, opsi Bounce, kontrol Bar Width & Speed. |
| **[`cwired/zz_strobe.cwired`](file:///C:/ANDREAS/ip26-zzfx/cwired/zz_strobe.cwired)** | 10.3 KB | Modular | **High-Speed Flash Strobe.** Model stock Resolume Strobe dengan Piano hold, frekuensi 2–30 Hz, kontrol warna dan intensitas kilatan. |
| **[`cwired/zz_stroke.cwired`](file:///C:/ANDREAS/ip26-zzfx/cwired/zz_stroke.cwired)** | 18.4 KB | Modular | **Perimeter Snake Border Glow.** Efek ular cahaya berlari mengelilingi bingkai tepi layar LED dengan ekor memudar halus (*smooth gradient tail*), arah CW/CCW, dan ketebalan garis. |

---

## 🎛️ Panduan Parameter & Cara Pakai Setiap Modul

### 1. `zz-pusher` (Efek Kejut / Beat Punch Zoom)
* **`Punch!` (Click Trigger Button):** Tombol klik langsung di inspector untuk memicu efek hentakan seketika tanpa harus mapping piano manual.
* **`Push` (Toggle / Piano):** Saklar aktivasi untuk shortcut keyboard / MIDI.
* **`Push Amount` (0.0 – 1.0, default: `0.35`):** Besaran zoom hentakan kejut.
* **`Push Decay` (0.02 – 1.0s, default: `0.15s`):** Kecepatan pudar halus (*smooth exponential release*).
* **`Flash Intensity` (0.0 – 1.0, default: `0.40`):** Kecerahan kilatan solid yang muncul bersama hentakan dan pudar bersamaan.
* **`Flash Color` (Color Picker):** Warna kilatan kejut (default: Putih).
* **`Bypass` (Toggle):** Mem-bypass efek seketika.

### 2. `zz-chaser` (1-Screen Precision Grid Runner)
* **`Chase (Hold)` (Piano Hold):** Tahan untuk mengaktifkan chaser, lepas untuk instant cut.
* **`Direction` (0 – 5):**
  - `0`: Left $\rightarrow$ Right
  - `1`: Right $\rightarrow$ Left
  - `2`: Up $\rightarrow$ Down
  - `3`: Down $\rightarrow$ Up
  - `4`: Center $\rightarrow$ Out
  - `5`: Out $\rightarrow$ Center
* **`Bounce` (Toggle, default: OFF):**
  - `OFF`: Runner meluncur satu arah lalu melompat looping langsung dari awal.
  - `ON`: Runner bergerak bolak-balik terus menerus (*ping-pong*).
* **`Grid Slices X` (Int 1 – 10, default: `5`):** Pembagi kolom presisi. Set `5` untuk 5 panel LED Auditorium UNNES.
* **`Grid Slices Y` (Int 1 – 10, default: `1`):** Pembagi baris presisi horizontal.
* **`Snap to Grid` (Toggle, default: ON):**
  - `ON`: Melompat presisi per panel LED.
  - `OFF`: Bergerak meluncur mulus continuous melintasi grid.
* **`Chase Speed` (0.1 – 8.0 Hz, default: `1.5 Hz`):** Kecepatan lari chaser.
* **`Chase Color` (Color Picker):** Warna bilah chaser (default: Amber Gold).
* **`Chase Intensity` (0.0 – 1.0):** Kecerahan bilah chaser.

### 3. `zz-wiper` (Continuous Scanner Curtain Wipe)
* **`Wiper (Hold)` (Piano Hold):** Tahan untuk memicu sapuan cahaya.
* **`Direction` (0 – 5):** L->R, R->L, Up->Down, Down->Up, Center->Out, Out->Center.
* **`Bounce` (Toggle):** Sapuan satu arah atau bolak-balik (*ping-pong*).
* **`Wipe Speed` (0.1 – 6.0 Hz):** Kecepatan siklus sapuan tirai.
* **`Bar Width` (0.02 – 1.0, default: `0.35`):** Lebar bilah sapuan cahaya.
* **`Bar Color` (Color Picker):** Warna tirai scanner.
* **`Wipe Intensity` (0.0 – 1.0):** Opacity bilah sapuan.

### 4. `zz-strobe` (High-Speed Multi-Rate Flash)
* **`Strobe (Hold)` (Piano Hold):** Tahan tombol untuk memicu flash cepat.
* **`Strobe Rate` (2.0 – 30.0 Hz, default: `14.0 Hz`):** Kecepatan kedipan per detik.
* **`Strobe Color` (Color Picker):** Warna kilatan (default: Putih).
* **`Strobe Intensity` (0.0 – 1.0):** Kecerahan kilatan.

### 5. `zz-stroke` (Animated Snake Perimeter Border)
* **`Stroke (Hold)` (Piano Hold):** Tahan tombol untuk memunculkan ular bingkai neon.
* **`Stroke Width` (0.005 – 0.08, default: `0.025`):** Ketebalan garis tepi layar LED.
* **`Snake Speed` (0.1 – 4.0 Hz, default: `1.0 Hz`):** Kecepatan lari ular mengitari pinggir layar.
* **`Direction` (0 = Clockwise, 1 = Counter-Clockwise):** Arah putaran ular cahaya.
* **`Stroke Color` (Color Picker):** Warna neon ular (default: Cyan Glow).
* **`Stroke Intensity` (0.0 – 1.0):** Kecerahan efek stroke.

---

## 🚀 Cara Instalasi ke Resolume Arena

1. Buka folder [`C:\ANDREAS\ip26-zzfx\cwired`](file:///C:/ANDREAS/ip26-zzfx/cwired).
2. **Double-click** masing-masing file `.cwired` untuk mendaftarkannya langsung ke database Resolume Arena.
3. *Atau daftarkan folder secara permanen:*
   - Buka Resolume Arena $\rightarrow$ **Preferences** $\rightarrow$ **Effects**.
   - Klik **Add Directory** $\rightarrow$ Arahkan ke `C:\ANDREAS\ip26-zzfx\cwired`.
4. Seluruh plugin akan langsung muncul di panel **Effects** Resolume Arena!

---

## 🎹 Panduan Setting Mode Piano di Resolume Arena

Untuk performa VJ live yang responsif saat ibadah/konser:

1. Drag plugin yang diinginkan ke **Composition** (atau layer video).
2. Tekan **`Ctrl + Shift + K`** (*Shortcuts $\rightarrow$ Edit Keyboard*).
3. Klik parameter toggle efek (misal `Push`, `Chase (Hold)`, `Strobe (Hold)`), lalu tekan tombol keyboard yang diinginkan (misal `Space`, `A`, `S`, dll).
4. Di panel kanan bawah (**Shortcuts Inspector**), ubah dropdown **Mode** dari *Toggle* menjadi **`Piano`**.
5. Tekan **`Esc`** untuk keluar.
6. **Hasil:**
   - **Tahan tombol:** Efek langsung aktif dan bergerak sesuai tempo.
   - **Lepas tombol:** Efek mati seketika (*instant cut*), opacity 0.0, nol beban GPU!

---

## 🔨 Cara Compile Ulang Source Patch

Jika melakukan penyesuaian parameter di [`build_suite.py`](file:///C:/ANDREAS/ip26-zzfx/build_suite.py), jalankan:

```powershell
python build_suite.py
```

Script akan men-generate source `.wire` dan mengompilasinya otomatis menjadi file `.cwired` menggunakan Resolume Wire CLI.

---

*Dibuat khusus untuk Divisi Multimedia & Live Production IP26 — Ibadah Perdana UKK UNNES 2026.*
