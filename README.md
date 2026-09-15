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
│ zz_chaser.cwired     │ 1-Screen Precision Grid Runner (Full L-to-R)    │
│ zz_wiper.cwired      │ Moving Radiant Gradient Curtain Wipe            │
│ zz_strobe.cwired     │ High-Speed Native Piano Flash Strobe            │
│ zz_stroke.cwired     │ Animated Perimeter Snake (Radius & Inset Frame) │
└──────────────────────┴─────────────────────────────────────────────────┘
```

---

## 🎛️ Panduan Parameter & Pembaruan Setiap Modul

### 1. [`zz_pusher.cwired`](file:///C:/ANDREAS/ip26-zzfx/cwired/zz_pusher.cwired) (Efek Kejut + Tombol Trigger Langsung)
* **`Punch!` (Click Trigger Button):** Tombol klik langsung di inspector untuk memicu efek hentakan seketika tanpa harus mapping piano manual.
* **`Push` (Toggle / Piano):** Saklar aktivasi untuk shortcut keyboard / MIDI pad.
* **`Push Amount` (0.0 – 1.5, default: `0.45`):** Besaran zoom hentakan kejut dari titik tengah layar.
* **`Push Decay` (0.05 – 1.5s, default: `0.25s`):** Waktu pudar elastis (*smooth release decay*).
* **`Flash Intensity` (0.0 – 1.0, default: `0.50`):** Kecerahan kilatan solid yang muncul bersama hentakan dan pudar bersamaan.
* **`Flash Color` (Color Picker):** Warna kilatan kejut (default: Putih).
* **`Bypass` (Toggle):** Mem-bypass efek seketika.

### 2. [`zz_chaser.cwired`](file:///C:/ANDREAS/ip26-zzfx/cwired/zz_chaser.cwired) (1-Screen Full Left-to-Right Precision Chaser)
* **Cakupan Penuh Layar (*Full L-to-R*):** Pembagian matematis presisi dari ujung kiri paling luar ($-0.80$) melintasi seluruh panel tengah ($0.00$) hingga ujung kanan paling luar ($+0.80$) untuk 5 panel LED Auditorium UNNES.
* **`Chase (Hold)` (Piano Hold):** Tahan untuk menyalakan chaser, lepas untuk *instant cut*.
* **`Direction` (0 – 5):**
  - `0`: Kiri ke Kanan (*Left $\rightarrow$ Right*)
  - `1`: Kanan ke Kiri (*Right $\rightarrow$ Left*)
  - `2`: Atas ke Bawah (*Up $\rightarrow$ Down*)
  - `3`: Bawah ke Atas (*Down $\rightarrow$ Up*)
  - `4`: Tengah ke Luar (*Center $\rightarrow$ Out*)
  - `5`: Luar ke Tengah (*Out $\rightarrow$ Center*)
* **`Bounce` (Toggle, default: OFF):**
  - `OFF`: Meluncur satu arah lalu langsung me-loop dari awal (*sawtooth*).
  - `ON`: Memantul bolak-balik terus menerus (*ping-pong triangle*).
* **`Grid Slices X` (Int 1 – 10, default: `5`):** Jumlah kolom panel horizontal.
* **`Grid Slices Y` (Int 1 – 10, default: `1`):** Jumlah baris panel vertikal.
* **`Snap to Grid` (Toggle, default: ON):**
  - `ON`: Melompat presisi panel per panel.
  - `OFF`: Meluncur mulus continuous melintasi layar.
* **`Chase Speed` (0.1 – 8.0 Hz, default: `1.5 Hz`):** Kecepatan lari chaser.
* **`Chase Color` (Color Picker):** Warna bilah chaser (default: Amber Gold).
* **`Chase Intensity` (0.0 – 1.0):** Kecerahan bilah chaser.

### 3. [`zz_wiper.cwired`](file:///C:/ANDREAS/ip26-zzfx/cwired/zz_wiper.cwired) (Radiant Moving Gradient Curtain Wipe)
* **Bentuk Gradien Digeser:** Menghasilkan tirai cahaya lembut (*radiant light beam*) dengan falloff gradien silky-smooth yang meluncur menyapu layar video.
* **`Wiper (Hold)` (Piano Hold):** Tahan untuk memicu sapuan cahaya.
* **`Direction` (0 – 5):** L->R, R->L, Up->Down, Down->Up, Center->Out, Out->Center.
* **`Bounce` (Toggle):** Sapuan satu arah atau bolak-balik (*ping-pong*).
* **`Wipe Speed` (0.1 – 6.0 Hz):** Kecepatan sapuan tirai.
* **`Gradient Width` (0.2 – 3.0, default: `1.0`):** Lebar sebaran gradien cahaya.
* **`Wipe Color` (Color Picker):** Warna gradien tirai scanner.
* **`Wipe Intensity` (0.0 – 1.0):** Opacity bilah sapuan.

### 4. [`zz_strobe.cwired`](file:///C:/ANDREAS/ip26-zzfx/cwired/zz_strobe.cwired) (Stock Strobe Reimagined)
* **`Strobe (Hold)` (Piano Hold):** Tahan tombol untuk memicu flash cepat.
* **`Strobe Rate` (2.0 – 30.0 Hz, default: `14.0 Hz`):** Kecepatan kedipan per detik.
* **`Strobe Color` (Color Picker):** Warna kilatan (default: Putih).
* **`Strobe Intensity` (0.0 – 1.0):** Kecerahan kilatan.

### 5. [`zz_stroke.cwired`](file:///C:/ANDREAS/ip26-zzfx/cwired/zz_stroke.cwired) (Perimeter Snake Border dengan Animasi & Fleksibilitas)
* **Animasi Ular Nyata (*Animated Snake*):** Ular neon berlari mengelilingi bingkai tepi layar dengan ekor gradien memudar (*smooth fading tail*) yang 100% terang dan dinamis!
* **`Stroke (Hold)` (Piano Hold):** Tahan untuk memunculkan ular bingkai neon.
* **`Stroke Width` (0.005 – 0.08, default: `0.025`):** Ketebalan garis tepi.
* **`Corner Radius` (0.0 – 0.5, default: `0.0`):** Sudut lengkung modern (*rounded corners*) untuk frame panggung yang elegan.
* **`Border Inset` (0.0 – 0.2, default: `0.0`):** Jarak batas frame dari tepi fisik layar (*floating inner frame*).
* **`Snake Speed` (0.1 – 4.0 Hz, default: `1.2 Hz`):** Kecepatan putaran ular neon mengelilingi layar.
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

*Dibuat khusus untuk Divisi Multimedia & Live Production IP26 — Ibadah Perdana UKK UNNES 2026.*
