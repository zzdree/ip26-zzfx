# ⚡ zzfx (v3.0.0) — Resolume All-in-One Performance Rack
**Dedicated 1x Drag VJ Performance Rack untuk Ibadah Perdana UKK UNNES 2026**  
*Lokasi Project: `C:\ANDREAS\ip26-zzfx`*  
*Target Output: Novastar Video Processor (Auditorium UNNES 2400x720) & Universal Canvas (16:9, 1080p, 4K)*  
*Operator Resolume: Andreas*

---

## 🎯 Gambaran Plugin
`zzfx` v3.0 adalah plugin efek All-in-One siap pakai untuk **Resolume Arena 7+**. Tidak perlu lagi drag plugin berkali-kali untuk mode chase yang berbeda! Cukup **1x drag** ke Composition, semua efek aksi (7 arah chase, push zoom, strobe flash, outline neon, dan master punch) langsung berada di dalam satu panel inspektor yang rapi.

### ✨ Keunggulan Utama v3.0
1. **1x Drag All-in-One (7 Dedicated Chase Triggers):**
   - Di dalam 1 panel efek, tersedia **7 tombol saklar terpisah** untuk setiap variasi arah animasi:
     * `Chase 1: Left -> Right` (Shortcut `1`)
     * `Chase 2: Right -> Left` (Shortcut `2`)
     * `Chase 3: Center -> Out` (Shortcut `3`)
     * `Chase 4: Out -> Center` (Shortcut `4`)
     * `Chase 5: Up -> Down` (Shortcut `5`)
     * `Chase 6: Down -> Up` (Shortcut `6`)
     * `Chase 7: Bounce / Ping-Pong` (Shortcut `7`)
2. **Perilaku Piano Hold Murni (Sesuai Karakter Chaser v3.1.3 & v4.0.0):**
   - **Tahan tombol:** Efek looping terus berulang mengikuti tempo.
   - **Lepas tombol:** Efek langsung mati seketika (*instant clean cut*), opacity menjadi 0.0 sehingga GPU nol beban.
   - Tidak ada timer decay paksa yang mengambang saat tuts dilepas.
3. **Dedicated Action Shortcuts:**
   - **`Space`** ➔ `Master Punch` (Zoom Kick + Strobe Combo untuk Bass Drop)
   - **`A`** ➔ `Push` (Zoom Kick dengan smooth elastic decay)
   - **`B`** ➔ `Strobe` (High-speed White Flash)
   - **`1` s/d `7`** ➔ Pilihan arah chase langsung
4. **Bebas Potong Screen (Single Screen Grid System):**
   - Tidak perlu memotong output menjadi 5 slice di *Advanced Output*.
   - Parameter `Grid Slices` otomatis membagi layar secara proporsional.
   - Pilihan `Snap to Grid`: ON (lompat per modul LED) atau OFF (sapuan beam halus continuous).
5. **Universal Aspect Ratio Support:**
   - Mendukung penuh layar ultra-wide Auditorium UNNES **`2400x720`**.
   - Otomatis adaptif tanpa distorsi pada kanvas standar **`16:9` (1080p / 4K)** maupun LED custom lainnya.

---

## 📂 File di Folder `C:\ANDREAS\ip26-zzfx`

| File | Format | Deskripsi |
| :--- | :--- | :--- |
| **`zzfx.cwired`** | Compiled Wire Plugin (v3.0.0) | File biner siap pakai untuk **Resolume Arena 7+**. Ringan, terkompilasi resmi via Resolume Wire CLI. |
| **`zzfx.wire`** | Wire Project File | Source patch berbasis node yang dapat dibuka dan diedit kembali menggunakan **Resolume Wire**. |
| **`build_zzfx.py`** | Python Builder Script | Script generator otomatis untuk membangun graph node `.wire` dan mengompilasinya menjadi `.cwired`. |
| **`README.md`** | Markdown Documentation | Dokumentasi teknis parameter, petunjuk instalasi, dan mapping shortcut. |
| **`LICENSE`** | Open Source (MIT) | Lisensi resmi open source project. |

---

## 🚀 Cara Instalasi ke Resolume Arena

1. Tutup Resolume Arena terlebih dahulu (jika sedang terbuka).
2. Buka File Explorer ke folder [`C:\ANDREAS\ip26-zzfx`](file:///C:/ANDREAS/ip26-zzfx).
3. **Double-click** file **`zzfx.cwired`** (Resolume akan otomatis mendaftarkannya ke database efek).
   *Atau salin file `zzfx.cwired` ke: `C:\Users\Public\Documents\Resolume Wire\Patches\`*.
4. Buka kembali **Resolume Arena**. Efek **`zzfx`** siap digunakan di panel **Effects**!

---

## 🎛️ Panduan Parameter & Kontrol di Inspector

Cukup tarik **1x** efek `zzfx` ke **Composition** (atau layer video):

```
[INPUT VIDEO] ──► [PUSH] ──► [OUTLINE] ──► [CHASE] ──► [STROBE] ──► [MASTER MIX] ──► [OUTPUT]
                    ▲                                   ▲
                    └─────────── [MASTER PUNCH] ────────┘
```

### 1. Master Section
* **`Master Punch (Toggle / Piano)`:** Tombol kombo pamungkas. Sekali ditekan/tahan, langsung memicu Push Zoom + Strobe Flash bersamaan saat drop lagu.
* **`Master Mix (Slider 0.0 – 1.0)`:** Kontrol Dry/Wet global (`1.0` efek penuh, `0.0` bypass).

### 2. Push Module (Zoom Beat Kick)
* **`Push (Toggle / Piano)`:** Saklar zoom punch. Sangat cocok di-set mode **Piano** untuk ketukan kick drum.
* **`Push Amount (Slider 0.0 – 1.0)`:** Intensitas pembesaran hentakan (default: `0.35`).
* **`Push Decay (Slider 0.0 – 1.0s)`:** Waktu kembali normal (default: `0.12s` membal elastis; set `0.0s` untuk instant snap).

### 3. Strobe Module (High-Speed Flash)
* **`Strobe (Toggle / Piano)`:** Saklar kilatan strobe putih.
* **`Strobe Rate (Slider 2.0 – 30.0 Hz)`:** Frekuensi kedipan flash per detik (default: `14.0 Hz`).
* **`Strobe Intensity (Slider 0.0 – 1.0)`:** Kecerahan kilatan flash.

### 4. Outline Module (Edge Neon Glow)
* **`Outline (Toggle / Piano)`:** Saklar deteksi garis neon di sekeliling siluet kamera/lirik.
* **`Outline Strength (Slider 0.5 – 8.0)`:** Ketebalan deteksi tepi Sobel (default: `2.5`).
* **`Outline Color (Color Picker)`:** Warna garis neon (default: *Neon Cyan*).
* **`Outline Mix (Slider 0.0 – 1.0)`:** Opacity overlay garis neon di atas video.

### 5. Chase Module (7 Dedicated Triggers & Grid Controller)
Tersedia 7 tombol saklar terpisah di inspector:
* **`Chase 1: Left -> Right`:** Sapuan bar vertikal dari kiri ke kanan.
* **`Chase 2: Right -> Left`:** Sapuan bar vertikal dari kanan ke kiri.
* **`Chase 3: Center -> Out`:** Bar mekar dari tengah layar ke kedua sisi luar bersamaan.
* **`Chase 4: Out -> Center`:** Bar kuncup dari kedua sisi luar menuju ke tengah layar.
* **`Chase 5: Up -> Down`:** Sapuan bar horizontal dari atas ke bawah.
* **`Chase 6: Down -> Up`:** Sapuan bar horizontal dari bawah ke atas.
* **`Chase 7: Bounce`:** Sapuan bolak-balik terus menerus (*ping-pong*).

**Pengaturan Chase Bersama:**
* **`Grid Slices (Int 1 – 10, default: 5)`:** Jumlah pembagian grid. Set ke `5` untuk Auditorium UNNES.
* **`Snap to Grid (Toggle, default: ON)`:**
  - `ON (True)`: Bar melompat terkuantisasi tepat per-panel LED (karakter *Chaser v4*).
  - `OFF (False)`: Bar meluncur mulus tanpa batas grid (*continuous laser sweep*).
* **`Chase Speed (Slider 0.1 – 8.0 Hz)`:** Kecepatan siklus lari bilah cahaya.
* **`Chase Color (Color Picker)`:** Warna sinar (default: *Warm Gold Amber*).
* **`Chase Intensity (Slider 0.0 – 1.0)`:** Kecerahan bar saat melintasi layar.

---

## 🎹 Panduan Praktis Setting Keyboard Shortcut di Resolume Arena

Hanya butuh 1 menit untuk mengatur shortcut keyboard agar performa VJ maksimal:

1. Drag plugin **`zzfx`** ke Composition (1x saja).
2. Tekan **`Ctrl + Shift + K`** (Shortcuts $\rightarrow$ Edit Keyboard).
3. Petakan tombol-tombol berikut pada panel **zzfx**:
   * Klik tombol **`Master Punch`** ➔ Tekan **`Space`**
   * Klik tombol **`Push`** ➔ Tekan **`A`**
   * Klik tombol **`Strobe`** ➔ Tekan **`B`**
   * Klik tombol **`Chase 1: Left -> Right`** ➔ Tekan **`1`**
   * Klik tombol **`Chase 2: Right -> Left`** ➔ Tekan **`2`**
   * Klik tombol **`Chase 3: Center -> Out`** ➔ Tekan **`3`**
   * Klik tombol **`Chase 4: Out -> Center`** ➔ Tekan **`4`**
   * Klik tombol **`Chase 5: Up -> Down`** ➔ Tekan **`5`**
   * Klik tombol **`Chase 6: Down -> Up`** ➔ Tekan **`6`**
   * Klik tombol **`Chase 7: Bounce`** ➔ Tekan **`7`**
4. **PENTING (Mode Piano):**
   * Klik salah satu shortcut tadi, lalu lihat di panel kanan bawah (**Shortcuts Inspector**).
   * Pastikan pilihan **Mode** diatur ke **`Piano`**.
5. Tekan tombol **`Esc`** untuk keluar dari mode edit shortcut.
6. **Selesai!** 
   - Tahan tombol `1` ➔ Chase Kiri-Kanan berjalan berulang. Lepas `1` ➔ Langsung mati bersih.
   - Tahan tombol `7` ➔ Chase Bolak-Balik berjalan. Lepas `7` ➔ Langsung mati bersih.
   - Tekan `Space` saat drop musik ➔ Layar menghentak dengan kilatan strobe secara instan!

---

*Dibuat khusus untuk Divisi Multimedia & Live Production IP26 — Ibadah Perdana UKK UNNES 2026.*
