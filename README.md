# ⚡ zzfx — Resolume Multi-Performance Effect Plugin
**Dedicated VJ Master Rack untuk Ibadah Perdana UKK UNNES 2026**  
*Lokasi Project: `C:\ANDREAS\ip26-zzfx`*  
*Target Output: Novastar Video Processor (Auditorium UNNES 2400x720) & Universal Canvas (16:9, 1080p, 4K)*  
*Operator Resolume: Andreas*

---

## 🎯 Gambaran Plugin
`zzfx` adalah plugin efek terpadu (*All-in-One Master Rack*) untuk **Resolume Arena 7+** yang dirancang dengan sistem kalkulasi koordinat normal (`-1.0` s/d `+1.0`) dan mode resolusi adaptif. 

### ✨ Keunggulan Utama
1. **Bebas Potong Screen (Single Screen All-in-One):**
   - Tidak perlu lagi memotong screen menjadi 5 bagian terpisah di *Advanced Output* seperti workflow lama (*Chaser v4*).
   - Cukup pasang di 1 layer atau 1 screen, plugin otomatis menghitung pembagian panel LED.
2. **Fleksibel di Segala Resolusi (Universal Aspect Ratio):**
   - Mendukung penuh LED Center ultra-wide **`2400x720`**.
   - Otomatis adaptif jika dipakai di resolusi standar **`16:9` (1920x1080 / 4K)**, **`4:3`**, atau canvas custom lainnya tanpa distorsi!
3. **Grid Vertikal & Horizontal:**
   - Arah sapuan horizontal (Kiri, Kanan, Tengah, Membal) otomatis menggunakan **Grid Kolom Vertikal**.
   - Arah sapuan vertikal (Atas ke Bawah, Bawah ke Atas) otomatis membagi layar menjadi **Grid Baris Horizontal**.
4. **Trigger & Shortcut Terpisah (Piano / Toggle Ready):**
   - Setiap modul efek memiliki tombol **`Trigger`** instan sendiri:
     - Tekan tombol **`A`** ➔ Hentakan **Push**.
     - Tekan tombol **`B`** ➔ Flash burst **Strobe**.
     - Tekan tombol **`1`** ➔ Sapuan kilat **Chase**.
     - Tekan tombol **`Space`** ➔ Combo **Master Punch** (Push + Strobe).

---

## 📂 File yang Tersedia di Folder `C:\ANDREAS\ip26-zzfx`

| File | Format | Deskripsi |
| :--- | :--- | :--- |
| **`zzfx.cwired`** | Compiled Wire Plugin | Plugin biner siap pakai untuk **Resolume Arena 7+**. Terkunci aman, sangat ringan, siap dipakai di live show. |
| **`zzfx.wire`** | Wire Project File | Source patch berbasis node yang bisa dibuka dan diedit kembali menggunakan **Resolume Wire**. |
| **`build_zzfx.py`** | Python Builder Script | Script generator otomatis untuk me-rebuild `.wire` dan mengompilasinya menjadi `.cwired`. |
| **`README.md`** | Markdown Documentation | Panduan lengkap parameter, cara instalasi, dan mapping shortcut MIDI/Keyboard. |
| **`LICENSE`** | Open Source (MIT) | Lisensi resmi open source project. |

---

## 🚀 Cara Instalasi Manual ke Resolume Arena

1. Buka File Explorer ke folder [`C:\ANDREAS\ip26-zzfx`](file:///C:/ANDREAS/ip26-zzfx).
2. Salin (*copy*) file **`zzfx.cwired`** (atau `zzfx.wire`).
3. Tempel (*paste*) ke folder plugin Resolume Anda:
   ```text
   C:\Users\<NamaUser>\Documents\Resolume Arena\Extra Effects\
   ```
   *(Atau di `C:\Users\<NamaUser>\OneDrive\Documents\Resolume Arena\Extra Effects\` jika OneDrive aktif).*
4. Buka **Resolume Arena**. Plugin **`zzfx`** akan langsung muncul di tab panel **Effects** pada kategori Video Effects!

---

## 🎛️ Panduan Parameter & Kontrol

```
[INPUT VIDEO] ──► [PUSH] ──► [OUTLINE] ──► [CHASE] ──► [STROBE] ──► [MASTER MIX] ──► [OUTPUT]
                    ▲                        ▲           ▲
                    └─────── [MASTER PUNCH] ─┴───────────┘
```

### 1. Master Section
* **`Master Punch (Trigger Button)`:** Sekali tekan memicu hentakan Push + Strobe Burst bersamaan. Pilihan tepat untuk transisi song / beat drop!
* **`Master Mix (Slider 0.0 – 1.0)`:** Pengatur Dry/Wet global. Nilai `1.0` efek aktif penuh; nilai `0.0` video kembali murni (*true bypass*).

### 2. Push Module (Zoom & Beat Punch)
* **`Push Enable (Toggle)`:** Saklar on/off modul Push.
* **`Push Trigger (Trigger Button)`:** Pemicu manual hentakan zoom (Attack instan 0.01s, decay halus).
* **`Push Amount (Slider 0.0 – 1.0)`:** Kekuatan zoom hentakan (rekomendasi: `0.3 – 0.5`).
* **`Push Decay (Slider 0.05 – 1.0s)`:** Kecepatan kembali normal (default `0.25s` untuk membal yang punchy).

### 3. Chase Module (Multi-Direction Grid Slicer & Beam Sweep)
* **`Chase Enable (Toggle)`:** Saklar untuk menyalakan sapuan cahaya secara terus-menerus (*continuous loop*).
* **`Chase Trigger (Trigger Button)`:** Pemicu hentakan sapuan sesaat (*momentary 1-shot burst*). Sangat asik ditekan per ketukan lagu!
* **`Grid Slices (Int 1 – 10, default: 5)`:** Jumlah pembagian panel LED. Set ke `5` untuk layar fisik 5 modul kabinet di Auditorium UNNES.
* **`Snap to Grid (Toggle, default: ON)`:**
  - `ON (True)`: Bilah melompat tepat per-panel LED (gaya *Chaser v4.0.0*).
  - `OFF (False)`: Bilah meluncur mulus seperti sapuan *laser beam continuous*.
* **`Chase Direction (7 Mode Pilihan Animasi Lengkap)`:**
  1. **`0: Left to Right`**: Sapuan kolom vertikal dari kiri ke kanan.
  2. **`1: Right to Left`**: Sapuan kolom vertikal dari kanan ke kiri.
  3. **`2: Center to Out`**: Mekar dari tengah layar ke kedua sisi luar (kiri & kanan) bersamaan.
  4. **`3: Out to Center`**: Kuncup dari kedua sisi luar menuju ke tengah layar.
  5. **`4: Up to Down`**: Sapuan baris horizontal dari atas ke bawah.
  6. **`5: Down to Up`**: Sapuan baris horizontal dari bawah ke atas.
  7. **`6: Bounce / Ping-Pong`**: Sapuan bolak-balik (kiri ➔ kanan ➔ kiri ➔ kanan) secara kontinyu!
* **`Chase Speed (Slider 0.2 – 8.0 Hz)`:** Frekuensi kecepatan gerak bilah cahaya.
* **`Chase Color (Color Picker)`:** Warna sinar (default: *Warm Gold Amber*).
* **`Chase Intensity (Slider 0.0 – 1.0)`:** Kecerahan sinar saat melintas di atas panggung.

### 4. Outline Module (Edge Neon Glow)
* **`Outline Enable (Toggle)`:** Saklar on/off garis neon di sekeliling WL, singer, atau teks lirik.
* **`Outline Strength (Slider 0.5 – 8.0)`:** Sensitivitas ketebalan deteksi tepi Sobel.
* **`Outline Color (Color Picker)`:** Warna cahaya neon (default: *Neon Cyan*, sangat indah jika diubah ke *Warm Gold* saat Worship).
* **`Outline Mix (Slider 0.0 – 1.0)`:** Opacity overlay garis glow di atas video (Additive blending).

### 5. Strobe Module (High-Speed Flash & Burst)
* **`Strobe Enable (Toggle)`:** Kedipan strobe terus-menerus.
* **`Strobe Trigger (Trigger Button)`:** Semburan flash sesaat (burst 3–4 kedipan kilat).
* **`Strobe Rate (Slider 2.0 – 30.0 Hz)`:** Frekuensi kedipan flash per detik.
* **`Strobe Intensity (Slider 0.0 – 1.0)`:** Kecerahan kilatan cahaya putih.

---

## 🎹 Panduan Praktis Setting Shortcut di Resolume Arena

Untuk mengatur tombol keyboard atau MIDI terpisah sesuai kebutuhan Anda (*misal Push di tombol A, Strobe di B, Chase di 1*):

1. Buka Resolume Arena, drag plugin **`zzfx`** ke Composition atau Layer target.
2. Tekan **`Ctrl + Shift + K`** (Menu: `Shortcuts -> Edit Keyboard`) atau **`Ctrl + Shift + M`** (jika menggunakan MIDI Controller).
3. Klik parameter pada panel **zzfx**:
   - Klik tombol **`Push Trigger`** ➔ Tekan tombol **`A`** pada keyboard.
   - Klik tombol **`Strobe Trigger`** ➔ Tekan tombol **`B`** pada keyboard.
   - Klik tombol **`Chase Trigger`** ➔ Tekan tombol **`1`** pada keyboard.
   - Klik tombol **`Master Punch`** ➔ Tekan tombol **`Space`** pada keyboard.
4. **Tips Mode Tombol (Toggle vs Piano/Hold):**
   - Jika Anda meng-klik **`Push Enable`**, **`Strobe Enable`**, atau **`Chase Enable`**:
   - Di panel sebelah kanan (*Shortcut Inspector*), ubah modenya dari **Toggle** menjadi **Piano**.
   - Dengan mode **Piano**: Efek hanya akan menyala **selama tombol ditekan**, dan langsung mati begitu tombol dilepas!
5. Tekan tombol **`Esc`** untuk keluar dari mode mapping. Sekarang Anda sudah siap live!

---

## 💡 Rekomendasi Setup saat Live Ibadah Perdana

| Sesi Ibadah | Setting yang Disarankan | Mood & Nuansa Visual |
| :--- | :--- | :--- |
| **Praise (Lagu Upbeat / Hentak Drum)** | • `Push Enable: ON` (`Decay: 0.2s`)<br>• `Chase Enable: ON` (`Grid: 5`, `Snap: ON`, Mode `Bounce` atau `Center to Out`)<br>• Mainkan `Push Trigger` (Tombol `A`) atau `Chase Trigger` (Tombol `1`) | Layar 5 modul LED Center tampak energik dan sinkron dengan ketukan drum band UKK. |
| **Worship (Penyembahan & Khidmat)** | • `Outline Enable: ON` (Color: *Warm Gold / Soft White*, Mix `0.6`)<br>• Modul lain: `OFF` | Siluet WL, singer, dan pemain musik di panggung tampil anggun dengan aura glow keemasan. |
| **Transisi / Song Drop** | • Tekan tombol **`Space`** (`Master Punch`) pada downbeat intro/reff! | Layar menghentak dengan zoom bump sekaligus kilatan strobe 3-flash megah. |

---
*Dibuat khusus untuk Divisi Multimedia & Live Production IP26 — Ibadah Perdana UKK UNNES 2026.*
