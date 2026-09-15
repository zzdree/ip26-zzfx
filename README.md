# ⚡ zzfx — Resolume Multi-Performance Effect Plugin
**Dedicated VJ Master Rack untuk Ibadah Perdana UKK UNNES 2026**  
*Lokasi Project: `C:\ANDREAS\ip26-zzfx`*  
*Target Output: Novastar Video Processor / LED Center Utama 2400x720 (Auditorium UNNES)*  
*Operator Resolume: Andreas*

---

## 🎯 Gambaran Plugin
`zzfx` adalah plugin efek terpadu (*All-in-One Master Rack*) untuk **Resolume Arena 7+** yang dirancang khusus untuk memenuhi kebutuhan live visual panggung lebar (ultra-wide LED 2400x720) tanpa perlu repot memotong screen manual.

Modul utama:
1. **Push (Beat Punch & Zoom Bump):** Hentakan ritmis saat kick drum / drop dengan decay envelope yang halus dan punchy.
2. **Chase (Dynamic Grid Slicer & Beam Sweep):**
   - **1 Screen All-in-One:** Tidak perlu lagi memotong screen menjadi 5 bagian terpisah seperti workflow lama! Cukup pasang di 1 layer/screen 2400x720, plugin otomatis membagi grid sesuai setting.
   - **Grid Slices (1–10, default: 5):** Pas untuk setup fisik 5 modul kabinet LED Center Auditorium UNNES.
   - **Snap to Grid (Toggle):**
     - `ON (True)`: Bilah melompat persis per-panel layar (gaya *Chaser v4.0.0*).
     - `OFF (False)`: Bilah bergerak meluncur mulus (*smooth laser/light sweep*).
   - **Chase Direction (4 Arah):**
     - `Left -> Right` (Kiri ke Kanan)
     - `Right -> Left` (Kanan ke Kiri)
     - `Center -> Out` (Dari Tengah membuka ke Kanan & Kiri bersamaan)
     - `Up -> Down` (Dari Atas menyapu ke Bawah)
3. **Strobe (High-Speed Flash & Burst):** Kilatan cahaya putih ritmis (2–30 Hz) yang bisa dipicu terus-menerus (*toggle*) atau lewat hentakan sesaat (*burst envelope*).
4. **Outline (Edge Detection & Neon Glow):** Garis tepi bercahaya neon (Sobel algorithm) di sekeliling siluet kamera, teks lirik, atau motion grafis. Sangat megah untuk sesi penyembahan (*Worship*).
5. **Master Punch (Combo Button):** 1 tombol pemicu sakti yang mengaktifkan hentakan Push dan kilatan Strobe secara bersamaan saat momen transisi atau drop lagu.
6. **Master Mix (Global Dry/Wet):** Slider peredam untuk mengatur intensitas efek secara menyeluruh atau bypass murni.

---

## 📂 File yang Tersedia di Folder `C:\ANDREAS\ip26-zzfx`

| File | Format | Deskripsi |
| :--- | :--- | :--- |
| **`zzfx.cwired`** | Compiled Wire Plugin | File plugin biner siap pakai untuk **Resolume Arena 7+**. Terkunci aman, ringan, siap langsung di-load di live show. |
| **`zzfx.wire`** | Wire Project File | Source patch berbasis node yang bisa dibuka dan diedit kembali kapan saja menggunakan aplikasi **Resolume Wire**. |
| **`build_zzfx.py`** | Python Builder Script | Script generator otomatis untuk me-rebuild file `.wire` dan mengompilasinya menjadi `.cwired`. |

---

## 🚀 Cara Instalasi Manual ke Resolume Arena

Sesuai permintaan Anda, file **tidak disalin otomatis** ke folder user/system. Silakan salin sendiri dengan salah satu cara berikut:

### Cara 1: Salin ke Folder Extra Effects (Paling Direkomendasikan)
1. Buka File Explorer.
2. Salin file **`zzfx.cwired`** (atau `zzfx.wire`).
3. Tempel (*paste*) ke folder plugin Resolume Anda:
   ```text
   C:\Users\<NamaUser>\Documents\Resolume Arena\Extra Effects\
   ```
   *(Atau di `C:\Users\<NamaUser>\OneDrive\Documents\Resolume Arena\Extra Effects\` jika OneDrive aktif).*
4. Buka **Resolume Arena**. Plugin **`zzfx`** akan langsung muncul di panel **Effects** pada kategori Video Effects.

### Cara 2: Salin ke Folder Patches Resolume Wire
1. Salin file **`zzfx.cwired`** atau **`zzfx.wire`**.
2. Tempel ke folder:
   ```text
   C:\Users\<NamaUser>\Documents\Resolume Wire\Patches\
   ```
3. Buka Resolume Arena. Efek otomatis terindeks di panel Effects.

---

## 🎛️ Panduan Parameter & Kontrol

```
[INPUT VIDEO (2400x720)] ──► [PUSH] ──► [OUTLINE] ──► [CHASE] ──► [STROBE] ──► [DRY/WET] ──► [OUTPUT]
                               ▲                        ▲           ▲
                               └─────── [MASTER PUNCH] ─┴───────────┘
```

### 1. Master Section
* **`Master Punch (Trigger Button)`:** Sekali tekan, langsung memicu hentakan Push + Strobe Burst bersamaan. Cocok di-map ke tombol keyboard `Space` atau drum pad MIDI!
* **`Master Mix (Slider 0.0 – 1.0)`:** Pengatur Dry/Wet global. Pada nilai `1.0`, efek aktif penuh; pada `0.0`, video kembali murni (*true bypass*).

### 2. Push Module (Zoom & Hentakan)
* **`Push Enable (Toggle)`:** Saklar on/off untuk modul Push.
* **`Push Trigger (Trigger Button)`:** Pemicu manual khusus hentakan push.
* **`Push Amount (Slider 0.0 – 1.0)`:** Kekuatan zoom hentakan (rekomendasi: `0.3 – 0.6`).
* **`Push Decay (Slider 0.05 – 1.0s)`:** Kecepatan kembali ke posisi normal (default `0.25s` untuk membal yang punchy dan musikal).

### 3. Chase Module (Multi-Direction Grid Slicer & Sweep)
* **`Chase Enable (Toggle)`:** Saklar on/off untuk bilah cahaya berjalan.
* **`Chase Speed (Slider 0.2 – 8.0 Hz)`:** Kecepatan sapuan bar melintasi layar.
* **`Grid Slices (Int 1 – 10, default: 5)`:** Jumlah pembagian panel LED. Set ke `5` untuk layar fisik 5 bagian di Auditorium UNNES.
* **`Snap to Grid (Toggle, default: ON)`:**
  - `ON`: Efek melompat tepat per-panel LED (1 -> 2 -> 3 -> 4 -> 5).
  - `OFF`: Efek menyapu halus seperti laser beam continuous.
* **`Chase Direction (Dropdown Pilihan)`:**
  - `0: Left -> Right` (Kiri ke Kanan)
  - `1: Right -> Left` (Kanan ke Kiri)
  - `2: Center -> Out` (Mekar dari tengah ke tepi luar)
  - `3: Up -> Down` (Sapuan vertikal atas ke bawah)
* **`Chase Width (Slider 0.03 – 0.5)`:** Ketebalan bilah cahaya (default `0.15`).
* **`Chase Color (Color Picker)`:** Warna sinar cahaya berjalan (default: *Warm Amber Gold*).
* **`Chase Intensity (Slider 0.0 – 1.0)`:** Kecerahan sinar saat melintas di atas video panggung.

### 4. Outline Module (Edge Neon Glow)
* **`Outline Enable (Toggle)`:** Saklar on/off untuk garis neon.
* **`Outline Strength (Slider 0.5 – 8.0)`:** Sensitivitas ketebalan deteksi tepi Sobel (rekomendasi: `2.0 – 3.5`).
* **`Outline Color (Color Picker)`:** Warna cahaya neon (default: *Neon Cyan* `[0, 217, 255]`, bisa diubah ke *Gold Worship* `[255, 217, 76]`).
* **`Outline Mix (Slider 0.0 – 1.0)`:** Opacity overlay garis glow di atas video asli (mode Additive blending).

### 5. Strobe Module (High-Speed Flash)
* **`Strobe Enable (Toggle)`:** Mengaktifkan kedipan strobe terus-menerus.
* **`Strobe Trigger (Trigger Button)`:** Memicu semburan flash sesaat (*burst flash* 3–4 kedipan).
* **`Strobe Rate (Slider 2.0 – 30.0 Hz)`:** Frekuensi kedipan strobe (default `14.0 Hz`).
* **`Strobe Intensity (Slider 0.0 – 1.0)`:** Kecerahan kilatan cahaya putih (default `0.9`).

---

## 💡 Rekomendasi Penggunaan saat Live Ibadah Perdana

| Sesi Ibadah | Setting yang Disarankan | Mood & Nuansa Visual |
| :--- | :--- | :--- |
| **Praise (Upbeat / Cepat)**<br>*Lagu Pembuka, Sorak-Sorai* | • `Push Enable: ON` (Amount `0.5`, Decay `0.2s`)<br>• `Chase Enable: ON` (`Grid Slices: 5`, `Snap: ON`, `Dir: Center -> Out` atau `Left -> Right`)<br>• `Strobe Enable: OFF` (Gunakan `Master Punch` saat intro/reff) | Memberikan energi dinamis tinggi, visual 5 panel LED panggung tampak hidup mengikuti ketukan drum band UKK. |
| **Worship (Khidmat / Syahdu)**<br>*Penyembahan, Doa Syafaat* | • `Outline Enable: ON` (Color: *Warm Gold / Soft White*, Mix `0.6`)<br>• `Push Enable: OFF`<br>• `Chase Enable: OFF`<br>• `Strobe Enable: OFF` | Siluet WL, singer, dan pemain musik di layar LED Center tampak anggun dengan aura glow keemasan tanpa silau berlebihan. |
| **Climax / Reff Drop** | • Tekan tombol **`Master Punch`** pada downbeat pertama reff! | Layar menghentak dengan zoom punch sekaligus kilatan strobe 3-flash yang sangat punchy dan megah. |

---

## ⌨️ Rekomendasi Shortcut & MIDI Mapping
* **Tombol `Space` atau MIDI Drum Pad 1:** Map ke parameter `Master Punch`.
* **Knob 1:** Map ke `Push Amount`.
* **Knob 2:** Map ke `Outline Mix`.
* **Knob 3:** Map ke `Chase Speed`.
* **Knob 4 / Tombol 2:** Map ke `Chase Direction`.
* **Fader Master:** Map ke `Master Mix` (Dry/Wet).

---
*Dibuat khusus untuk Divisi Multimedia & Live Production IP26 — Ibadah Perdana UKK UNNES 2026.*
