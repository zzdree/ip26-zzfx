# ⚡ zzfx (v2.0.0) — Resolume Multi-Performance Effect Plugin
**Dedicated VJ Master Rack untuk Ibadah Perdana UKK UNNES 2026**  
*Lokasi Project: `C:\ANDREAS\ip26-zzfx`*  
*Target Output: Novastar Video Processor (Auditorium UNNES 2400x720) & Universal Canvas (16:9, 1080p, 4K)*  
*Operator Resolume: Andreas*

---

## 🎯 Gambaran Plugin
`zzfx` adalah plugin efek terpadu (*All-in-One Master Rack*) untuk **Resolume Arena 7+** yang dirancang dengan sistem kalkulasi koordinat normal (`-1.0` s/d `+1.0`) dan mode resolusi adaptif. 

### ✨ Keunggulan Utama v2.0
1. **Sistem On/Off Murni (Piano / Toggle Responsive):**
   - Tidak ada lagi timer decay paksaan atau tombol trigger yang membingungkan.
   - Setiap modul (`Push`, `Chase`, `Strobe`, `Outline`, `Master Punch`) memiliki saklar **On/Off** murni.
   - Di menu Shortcuts Resolume Arena, kamu bebas memilih:
     - **Mode Piano:** Efek aktif **hanya selama tuts tombol kamu tahan**, dan mati seketika saat jari kamu lepas.
     - **Mode Toggle:** Pencet sekali nyala terus, pencet sekali lagi mati.
2. **Stacking / Multi-Slot Ready (Bisa Ditumpuk Banyak Efek):**
   - Cukup 1 plugin `zzfx`, kamu bisa drag berkali-kali ke rack **Effects** di Composition:
     - Instance 1: Chase Kiri ➔ Kanan (Shortcut `1`, Piano)
     - Instance 2: Chase Tengah ➔ Luar (Shortcut `2`, Piano)
     - Instance 3: Chase Bounce (Shortcut `3`, Piano)
     - Instance 4: Push / Zoom (Shortcut `A`, Piano)
     - Instance 5: Strobe Flash (Shortcut `B`, Piano)
3. **Bebas Potong Screen (Single Screen All-in-One):**
   - Tidak perlu lagi memotong screen menjadi 5 bagian terpisah di *Advanced Output* seperti workflow lama (*Chaser v4*).
   - Cukup pasang di 1 layer atau 1 screen, plugin otomatis menghitung pembagian panel LED.
4. **Fleksibel di Segala Resolusi (Universal Aspect Ratio):**
   - Mendukung penuh LED Center ultra-wide **`2400x720`**.
   - Otomatis adaptif jika dipakai di resolusi standar **`16:9` (1920x1080 / 4K)**, **`4:3`**, atau canvas custom lainnya tanpa distorsi!
5. **Grid Vertikal & Horizontal:**
   - Arah sapuan horizontal (Kiri, Kanan, Tengah, Membal) otomatis menggunakan **Grid Kolom Vertikal**.
   - Arah sapuan vertikal (Atas ke Bawah, Bawah ke Atas) otomatis membagi layar menjadi **Grid Baris Horizontal**.

---

## 📂 File yang Tersedia di Folder `C:\ANDREAS\ip26-zzfx`

| File | Format | Deskripsi |
| :--- | :--- | :--- |
| **`zzfx.cwired`** | Compiled Wire Plugin | Plugin biner siap pakai untuk **Resolume Arena 7+**. Sangat ringan, terkompilasi resmi dari Resolume Wire. |
| **`zzfx.wire`** | Wire Project File | Source patch berbasis node yang bisa dibuka dan diedit kembali menggunakan **Resolume Wire**. |
| **`build_zzfx.py`** | Python Builder Script | Script generator otomatis untuk me-rebuild `.wire` dan mengompilasinya menjadi `.cwired`. |
| **`README.md`** | Markdown Documentation | Panduan lengkap parameter, cara instalasi, dan mapping shortcut MIDI/Keyboard. |
| **`LICENSE`** | Open Source (MIT) | Lisensi resmi open source project. |

---

## 🚀 Cara Instalasi ke Resolume Arena

1. Tutup Resolume Arena terlebih dahulu (jika sedang terbuka).
2. Buka File Explorer ke folder [`C:\ANDREAS\ip26-zzfx`](file:///C:/ANDREAS/ip26-zzfx).
3. **Double-click** file **`zzfx.cwired`** (Resolume akan otomatis memproses dan menginstalnya).
   *Atau salin manual `zzfx.cwired` ke: `C:\Users\Public\Documents\Resolume Wire\Patches\`*.
4. Buka kembali **Resolume Arena**. Efek **`zzfx`** langsung siap digunakan di panel **Effects**!

---

## 🎛️ Panduan Parameter & Kontrol

```
[INPUT VIDEO] ──► [PUSH] ──► [OUTLINE] ──► [CHASE] ──► [STROBE] ──► [MASTER MIX] ──► [OUTPUT]
                    ▲                                   ▲
                    └─────────── [MASTER PUNCH] ────────┘
```

### 1. Master Section
* **`Master Punch (Toggle / Piano)`:** Tombol saklar drop combo. Jika aktif, memicu hentakan Push + Strobe flash bersamaan.
* **`Master Mix (Slider 0.0 – 1.0)`:** Pengatur Dry/Wet global (`1.0` efek penuh, `0.0` bypass murni).

### 2. Push Module (Zoom & Beat Punch)
* **`Push (Toggle / Piano)`:** Saklar on/off pembesar (zoom punch). Sangat asik di-set mode **Piano** untuk ketukan kick drum.
* **`Push Amount (Slider 0.0 – 1.0)`:** Kekuatan zoom hentakan (default: `0.35`).
* **`Push Decay (Slider 0.0 – 1.0s)`:** Kecepatan kembali normal (default `0.12s` untuk membal elastis; set `0.0s` untuk instant snap).

### 3. Chase Module (Multi-Direction Grid Slicer & Beam Sweep)
* **`Chase (Toggle / Piano)`:** Saklar on/off sapuan bilah cahaya.
* **`Grid Slices (Int 1 – 10, default: 5)`:** Jumlah pembagian panel LED. Set ke `5` untuk layar fisik 5 modul kabinet di Auditorium UNNES.
* **`Snap to Grid (Toggle, default: ON)`:**
  - `ON (True)`: Bilah melompat tepat per-panel LED (gaya *Chaser v4.0.0*).
  - `OFF (False)`: Bilah meluncur mulus seperti sapuan *laser beam continuous*.
* **`Chase Direction (7 Mode Pilihan Animasi Lengkap)`:**
  1. **`0: Left to Right`**: Sapuan kolom vertikal dari kiri ke kanan.
  2. **`1: Right to Left`**: Sapuan kolom vertikal dari kanan ke kiri.
  3. **`2: Center to Out`**: Mekar dari tengah layar ke kedua sisi luar bersamaan.
  4. **`3: Out to Center`**: Kuncup dari kedua sisi luar menuju ke tengah layar.
  5. **`4: Up to Down`**: Sapuan baris horizontal dari atas ke bawah.
  6. **`5: Down to Up`**: Sapuan baris horizontal dari bawah ke atas.
  7. **`6: Bounce / Ping-Pong`**: Sapuan bolak-balik terus-menerus!
* **`Chase Speed (Slider 0.1 – 8.0 Hz)`:** Kecepatan gerak bilah cahaya.
* **`Chase Color (Color Picker)`:** Warna sinar (default: *Warm Gold Amber*).
* **`Chase Intensity (Slider 0.0 – 1.0)`:** Kecerahan sinar saat melintas di layar.

### 4. Strobe Module (High-Speed Flash)
* **`Strobe (Toggle / Piano)`:** Saklar on/off kilatan strobe putih.
* **`Strobe Rate (Slider 2.0 – 30.0 Hz)`:** Frekuensi kedipan flash per detik (default: `14.0 Hz`).
* **`Strobe Intensity (Slider 0.0 – 1.0)`:** Kecerahan kilatan cahaya putih.

### 5. Outline Module (Edge Neon Glow)
* **`Outline (Toggle / Piano)`:** Saklar on/off garis neon di sekeliling siluet subjek/teks.
* **`Outline Strength (Slider 0.5 – 8.0)`:** Sensitivitas ketebalan deteksi tepi Sobel (default: `2.5`).
* **`Outline Color (Color Picker)`:** Warna cahaya neon (default: *Neon Cyan*).
* **`Outline Mix (Slider 0.0 – 1.0)`:** Opacity overlay garis glow di atas video.

---

## 🎹 Panduan Praktis Setting Shortcut di Resolume Arena

### Cara Setting Piano Mode:
1. Drag plugin **`zzfx`** ke Composition.
2. Tekan **`Ctrl + Shift + K`** (Shortcuts $\rightarrow$ Edit Keyboard).
3. Klik tombol saklar pada panel **zzfx** (misal tombol `Push`, `Chase`, atau `Strobe`).
4. Tekan tombol keyboard pilihan kamu:
   - **`Push`** ➔ Tekan tombol **`A`**
   - **`Strobe`** ➔ Tekan tombol **`B`**
   - **`Chase`** ➔ Tekan tombol **`1`**
   - **`Master Punch`** ➔ Tekan tombol **`Space`**
5. Di panel kanan bawah (**Shortcut Inspector**), pastikan **Mode** diatur ke **`Piano`**.
6. Tekan tombol **`Esc`** untuk selesai.

### Cara Menumpuk Efek untuk 3 Chase Sekaligus (Slot Stacking):
Jika kamu ingin tombol `1` untuk Chase Kiri-Kanan, tombol `2` untuk Chase Tengah-Luar, dan tombol `3` untuk Chase Bounce:
1. Tarik **`zzfx`** pertama ke Composition:
   - Nyalakan hanya modul **Chase**, set Direction: **Left to Right**.
   - Beri shortcut tombol **`1`** (Mode: Piano).
2. Tarik **`zzfx`** kedua ke Composition:
   - Nyalakan hanya modul **Chase**, set Direction: **Center to Out**.
   - Beri shortcut tombol **`2`** (Mode: Piano).
3. Tarik **`zzfx`** ketiga ke Composition:
   - Nyalakan hanya modul **Chase**, set Direction: **Bounce**.
   - Beri shortcut tombol **`3`** (Mode: Piano).
4. Selesai! Saat live, kamu tinggal menahan tombol `1`, `2`, atau `3` untuk memicu chase yang berbeda secara independen!

---

*Dibuat khusus untuk Divisi Multimedia & Live Production IP26 — Ibadah Perdana UKK UNNES 2026.*
