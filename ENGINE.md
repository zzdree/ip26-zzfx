# ENGINE.md — Bedah Arsitektur, Analisis Referensi & Rekayasa Plugin IP26-ZZFX

Dokumentasi teknis mendalam hasil audit, dekompilasi, dan reverse-engineering terhadap plugin referensi di `X:\IP26\Assets\Softs\Resolume Plugins` (`FFGLBumper.dll`, `FFGLWiper.dll`, `FFGLOutliner.dll`, `FFGLChaser.dll`, dan koleksi patch `.cwired`), serta implementasi arsitektur **Pure Modular Resolume Wire** pada suite [`C:\ANDREAS\ip26-zzfx`](file:///C:/ANDREAS/ip26-zzfx).

---

## 1. Latar Belakang & Ruang Lingkup

### Masalah pada Sistem Legacy
Sebelumnya, produksi visual panggung (khususnya event besar seperti di Auditorium UNNES dengan LED wall Novastar 2400×720) mengandalkan plugin eksternal berbasis **FFGL 2.x C++ DLL** (seperti Chaser v3.1.3/v4.0.0, Wiper, Bumper, dan Outliner buatan pihak ketiga). 

Kelemahan fatal sistem legacy tersebut:
1. **Kerap Crash / Hang saat Live**: FFGL DLL lawas menggunakan dependensi runtime C++ (`MSVCR120.dll` / runtime Visual Studio 2013-2015) yang rentan konflik memori (*access violation*) saat Resolume Arena dijalankan berjam-jam di Windows 11.
2. **Ketergantungan Slice Advanced Output**: Plugin seperti Chaser v4 mewajibkan operator membuat 5 slices terpisah di menu *Advanced Output* Resolume. Jika konfigurasi slice bergeser atau dipakai di screen single-canvas biasa, chaser tidak berfungsi.
3. **Kaku pada Resolusi**: Transformasi dan ukuran shader di-hardcode ke aspek rasio 16:9, sehingga saat diproyeksikan ke LED wall ultrawide 2400×720 (aspek rasio 10:3), efek terdistorsi atau terpotong.
4. **All-in-One Bloatware**: Plugin gabungan monolitik membebani render thread GPU karena semua loop shader berjalan bersamaan meskipun hanya 1 efek yang dipakai.

### Solusi: Native Pure Modular Wire (.cwired)
Membuat ulang seluruh fungsionalitas esensial ke dalam format **Resolume Wire Native (`.cwired`)** versi 7.26.1.
* **100% Pure Modular**: 5 file terpisah independen (`zz_pusher`, `zz_chaser`, `zz_wiper`, `zz_stroke`, `zz_strobe`).
* **Zero External Dependencies**: Berjalan langsung di GPU render graph Resolume tanpa C++ DLL eksternal.
* **Fleksibel di Semua Resolusi**: Menggunakan sistem kalkulasi normalisasi koordinat $[-1.0, +1.0]$, otomatis presisi di 1920×1080 maupun 2400×720.
* **Dapat Ditaruh Bebas**: Bekerja stabil di level **Composition**, **Layer**, maupun **Clip**.

---

## 2. Hasil Bedah & Dekompilasi Plugin Referensi

Folder referensi: `X:\IP26\Assets\Softs\Resolume Plugins`
Isi folder:
* `dll/` & `exe/Chaser v4.0.0/Crack/dll/`: `FFGLBumper.dll`, `FFGLWiper.dll`, `FFGLOutliner.dll`, `FFGLChaser.dll`, `SliceTracer_FFGL21.dll`, dll.
* `cwired/`: `PUSHER.cwired`, `BOOMER.cwired`, `Glow_Borders.cwired`, `SLICE STROBE.cwired`, `Tracer.cwired`, dll.

---

### A. Bedah `FFGLBumper.dll` & `PUSHER.cwired` (Efek Zoom Kick & Flash Kejut)

* **Metadata Biner**:
  * PDB Symbol: `C:\Users\joris\Documents\Develop\hybridffgl\binaries\x64\Release\FFGLBumper.pdb`
  * Developer: Joris Hermans (Hybrid Visuals / Resolume Core Dev).
* **Parameter Internal**:
  * `Scale`: Faktor pembesaran tekstur (zoom).
  * `Bump harder and harder`: Input Trigger untuk memicu hentakan.
  * `Fade Speed`: Durasi pembusukan (*exponential release decay*).
  * `Blast Speed`: Intensitas kilatan solid flash.
  * `Opacity`: Pengatur transparansi mixing.
* **Logika Shader GLSL**:
  ```glsl
  uniform vec2 Scale;
  uniform float Opacity;
  uniform vec2 MaxUV;
  
  // Transform UV terpusat di titik tengah (0.5, 0.5)
  vec2 st = UV - vec2(0.5);
  st *= (1.0 / Scale) * (8.0 * Scale.y);
  st += vec2(0.5);
  
  vec4 color = texture(tex, st);
  // Flash blending
  color.rgb += vec3(Opacity * blastMultiplier);
  fragColor = color;
  ```
* **Kelemahan Referensi**: Pada versi DLL, trigger tidak memiliki visual button yang interaktif di inspector baru Resolume Arena 7 tanpa mapping shortcut manual.
* **Implementasi di `zz_pusher`**:
  * Menggunakan **`Trigger In`** bertuliskan **`Punch!`** yang memunculkan tombol klik fisik di inspector Resolume.
  * Menggunakan node **`Attack Release`** (`77697265-D980-43B3-9237-6683B154A5B0`) dengan `attack-time: 0.0s` (serangan instan saat hit pertama) dan `linear: True` / `restart-at-zero: True`.
  * Menambahkan jalur paralel **`Push`** (`Bool In`) melalui node `Smooth` untuk keperluan permainan piano (*hold key*).
  * Mengkombinasikan zoom terpusat via node **`Transform`** (`77697265-9225-4009-9D2D-5F898E94CC33`) dan solid flash kejut via node **`Video Mixer`** (Add Mode 11).

---

### B. Bedah `FFGLWiper.dll` (Efek Tirai Sapuan Gradien)

* **Metadata Biner**:
  * PDB Symbol: `C:\Users\joris\Documents\Develop\hybridffgl\binaries\x64\Release\FFGLWiper.pdb`
* **Parameter Internal**:
  * `Length`: Lebar rentang gradien tirai cahaya.
  * `LoopTime`: Periode waktu 1 kali siklus sapuan.
  * `Flip` / `Flip Direction` / `Swap Directions`: Pembalik arah sapuan.
  * `Phase`: Posisi fase gelombang berjalan.
* **Kode Shader GLSL Asli (diekstrak dari biner DLL)**:
  ```glsl
  in vec2 WipeUV;
  uniform float LoopTime;
  uniform float Length;
  uniform float Flip;
  
  localTime = mod(localTime, LoopTime);
  float scaledPhase = ((localTime - 0.5) * 2.0) / Length; // sapuan menutupi 2x panjang layar
  float fade = abs(WipeUV.y) / Length;
  fade = mix(fade, 1.0 - fade, Flip);
  fade = mix(fade, 1.0 - fade, doOddEvens);
  
  float wipe = fade - scaledPhase; // animasi pergeseran gradien
  wipe *= step(fade, scaledPhase + 1.0); // potong puncak gradien agar bersih
  fragColor = vec4(wipe) * color;
  ```
* **Kelemahan Referensi**: Pada implementasi FFGL, gradien hanya menyapu satu sumbu tetap dan sering menghasilkan artefak aliasing di tepi layar ultrawide.
* **Implementasi di `zz_wiper`**:
  * Menghasilkan **`Radiant Gradient`** (`77697265-FCE2-4EBE-8C81-99C578524A24`, Radial Mode) dengan puncak tengah putih solid dan *falloff* halus ke transparan.
  * Tirai gradien digeser melintasi canvas menggunakan node **`Transform`** yang dipacu oleh osilator Saw / Triangle (untuk opsi **`Bounce`**).
  * Menyediakan **6 Mode Arah**:
    1. Kiri ke Kanan (`L -> R`)
    2. Kanan ke Kiri (`R -> L`)
    3. Atas ke Bawah (`U -> D`)
    4. Bawah ke Atas (`D -> U`)
    5. Tengah ke Luar (`Center -> Out`)
    6. Luar ke Tengah (`Out -> Center`)
  * Slider **`Gradient Width`** untuk mengatur ketebalan tirai cahaya.

---

### C. Bedah `FFGLOutliner.dll` & `Glow_Borders.cwired` (Efek Snake Stroke Berputar)

* **Metadata Biner**:
  * PDB Symbol: `C:\Users\joris\Documents\Develop\hybridffgl\binaries\x64\Release\FFGLOutliner.pdb`
* **Parameter Internal**:
  * `Animate`: Menghidupkan animasi keliling perimeter bingkai.
  * `Length`: Panjang busur ekor laser snake.
  * `Phase`: Kecepatan / offset fase perputaran.
  * `Feather`: Kelembutan tepi (*edge blur*).
  * `Color`: Warna neon stroke.
* **Kode Shader GLSL Asli (diekstrak dari biner DLL)**:
  ```glsl
  uniform float Length;
  uniform float Phase;
  uniform vec4 Color;
  uniform bool Animate;
  
  if (Animate) {
      float edge = fract(fract(uvx * Count) - fract(Phase + Random * RandomVal + abs(NormalizedPosX) * Fan));
      float animVal = smoothstep(1.0 - Length, 1.0, edge);
      fragColor = vec4(line) * Color * animVal;
      fragColor += vec4(1.0) * Color * blurVal; // feather glow
  }
  ```
* **Kelemahan Referensi**:
  * Hanya menghasilkan bingkai tajam persegi murni (*sharp corners*), tidak bisa dibulatkan (*corner radius*).
  * Bingkai selalu menempel di tepi piksel terluar, sehingga pada panggung fisik yang memiliki bezel LED atau masking panggung, garis sering terpotong.
* **Implementasi di `zz_stroke`**:
  * **Procedural Rectangle Canvas**: Dibangun dengan node `Rectangle` (`77697265-4db6-4573-8aa7-42362bc44931`) dan `Edge` (`77697265-ab950887-37ee-4fd2-9487-c856b6b75c83`).
  * **Corner Radius Dinamis**: Input `Float` ($0.0 \dots 0.5$) diumpankan ke Float4 round corner untuk menghasilkan sudut membulat modern.
  * **Border Inset Dinamis**: Memungkinkan bingkai ditarik masuk menjauhi tepi layar ($0.0 \dots 0.2$), aman dari bezel fisik kabinet LED.
  * **Sweep Gradient Mask**: Menggunakan Conical/Angle Gradient (`type: 2`) 360° yang diputar oleh Sawtooth Oscillator, kemudian dimasking ke bingkai menggunakan native node **`Mask`** (`77697265-CB86-4A6F-AABA-009C4C8BB5C1`, v2).
  * Menghasilkan laser snake neon yang meluncur mengelilingi perimeter dengan ekor gradien fading super halus.

---

### D. Bedah `FFGLChaser.dll` & Chaser v3/v4 (Efek Chaser Kolom Presisi)

* **Parameter Internal Chaser Legacy**:
  * `Step`, `Fill`, `Sustain`, `Echoes`, `Bounce`.
* **Kelemahan Utama Chaser Legacy**:
  * Mengharuskan 5 slice terdaftar di *Advanced Output*.
  * Jika hanya ditaruh di Master Composition biasa, ia tidak mengenali koordinat kolom panggung.
* **Implementasi di `zz_chaser`**:
  * **1-Screen Murni**: Didesain khusus agar **TIDAK MEMERLUKAN SLICE DI ADVANCED OUTPUT**. Cukup drop di Composition / Layer / Clip 1 Screen tunggal.
  * **Matematika Koordinat Grid Presisi**:
    Sistem koordinat horizontal Resolume Wire terbentang dari $X = -1.0$ (ujung paling kiri) hingga $X = +1.0$ (ujung paling kanan), dengan total bentang $= 2.0$.
    Untuk jumlah grid kolom $N$:
    $$\text{Lebar Slice } W = \frac{2.0}{N}$$
    $$\text{Koordinat Tengah Slice Pertama } X_0 = -1.0 + \frac{W}{2}$$
    $$\text{Posisi Kolom ke-}i: \quad X_i = X_0 + \left(i \times W\right), \quad i \in \{0, 1, \dots, N-1\}$$
    
    Pada LED Wall Panggung UNNES dengan $N = 5$ panel:
    * $W = \frac{2.0}{5} = 0.40$
    * $X_0 = -1.0 + 0.20 = -0.80$
    * Panel 1: $\mathbf{-0.80}$ (Ujung Kiri)
    * Panel 2: $\mathbf{-0.40}$ (Kiri Tengah)
    * Panel 3: $\mathbf{\phantom{-}0.00}$ (Tepat Tengah)
    * Panel 4: $\mathbf{+0.40}$ (Kanan Tengah)
    * Panel 5: $\mathbf{+0.80}$ (Ujung Kanan)
  * **Quantization Engine**: Sinyal fase kontinu $p \in [0.0, 1.0)$ dikalikan 2.0 dan diumpankan ke node `Quantize` berstep $W$ ($0.4$), menghasilkan perpindahan kolom yang presisi (*snap to grid*), atau dapat dimatikan untuk mode pergerakan halus (*continuous glide*).
  * **Arah & Bounce**: 6 preset arah gerakan + toggle `Bounce` (bolak-balik ping-pong).

---

## 3. Struktur Biner `.cwired` vs `.wire`

Dalam ekosistem Resolume Wire:
* **`.wire`** adalah file proyek visual graph berbasis **JSON terstruktur**. Berisi definisi nodes, atribut, konstanta, port binding, koordinat UI canvas, dan metadata author.
* **`.cwired`** adalah file biner hasil kompilasi resmi dari perintah:
  ```powershell
  & "C:\Program Files\Resolume Wire\Wire.exe" compile <patch.wire>
  ```

### Header Biner `.cwired`
Dari hasil analisis byte hex `PUSHER.cwired` dan suite `zz_*.cwired`:
```hex
Offset 0x00: 00 01 00 00 00 01 00 00   -> Format Version (Major: 1, Minor: 1)
Offset 0x08: 00 14 01 d9 4f 6c d4 fd   -> 16-byte Cryptographic Hash / GUID Token
Offset 0x10: da 3f 22 00 00 00 00 00
Offset 0x18: 00 00 00 00 00 00 00 00   -> 48-byte Zero Padding
...
Offset 0x48: [Encrypted / Serialized Bytecode Graph & Embedded Resource Bundle]
```
Binary `.cwired` menjamin:
1. Tidak dapat rusak atau terkorupsi oleh editor teks.
2. Dibaca secara langsung oleh engine C++ Resolume Arena tanpa tahapan parsing JSON di runtime.
3. 100% kompatibel dengan ABI versi Resolume Arena `7.26.1.7833`.

---

## 4. Arsitektur 5 Plugin Modular IP26-ZZFX

```
C:\ANDREAS\ip26-zzfx\
├── cwired/                  # Binary siap pakai (Drop ke Resolume Arena)
│   ├── zz_pusher.cwired     # Elastic Zoom Kick & Solid Kejut Flash
│   ├── zz_chaser.cwired     # 1-Screen 5-Panel Precision Chaser & Bounce
│   ├── zz_strobe.cwired     # High-Speed Strobe Pulse Clock
│   ├── zz_stroke.cwired     # Animated Neon Snake Stroke Frame & Radius
│   └── zz_wiper.cwired      # Radiant Light Curtain Gradient Sweep
├── wire/                    # File source JSON Wire
│   ├── zz_pusher.wire
│   ├── zz_chaser.wire
│   ├── zz_strobe.wire
│   ├── zz_stroke.wire
│   └── zz_wiper.wire
├── build_suite.py           # Pipeline compiler & generator otomatis
└── ENGINE.md                # Dokumentasi arsitektur ini
```

### Matriks Spesifikasi Teknis

| Parameter / Fitur | `zz-pusher` | `zz-chaser` | `zz-wiper` | `zz-stroke` | `zz-strobe` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Kategori** | Effect | Effect | Effect | Effect | Effect |
| **Pemicu Utama** | Click `Punch!` & Piano `Push` | Toggle `Chase` / Piano | Toggle `Wiper` / Piano | Toggle `Stroke` / Piano | Piano `Strobe (Hold)` |
| **Default State** | Ready (0.0 idle) | **Active (True)** | **Active (True)** | **Active (True)** | Standby (False) |
| **Resolusi Relatif** | `[1.0, 1.0]` Auto | `[1.0, 1.0]` Auto | `[1.0, 1.0]` Auto | `[1.0, 1.0]` Auto | `[1.0, 1.0]` Auto |
| **Jumlah Node Wire** | 22 Nodes | 36 Nodes | 25 Nodes | 28 Nodes | 13 Nodes |
| **Koneksi Port** | 25 Koneksi | 46 Koneksi | 35 Koneksi | 33 Koneksi | 13 Koneksi |
| **Ukuran Biner** | 15.9 KB | 27.5 KB | 20.1 KB | 23.7 KB | 9.6 KB |
| **Blend Mode** | Add (11) + Alpha (0) | Add (11) + Alpha (0) | Add (11) + Alpha (0) | Add (11) + Alpha (0) | Add (11) + Alpha (0) |
| **Anti-Crash Level** | 100% Native Wire | 100% Native Wire | 100% Native Wire | 100% Native Wire | 100% Native Wire |

---

## 5. Panduan Port & Node Wire Vital (Engine Reference)

Saat merekayasa patch Wire melalui skrip Python (`build_suite.py`), perhatikan penamaan port outlet berikut yang sering memicu kegagalan jika salah ketik:

1. **Clamp Node** (`77697265-7557-4053-ABEC-73E2A9786804`, v2):
   * Outlet port: `'output0'` (BUKAN `'output'`).
2. **Transform Node** (`77697265-9225-4009-9D2D-5F898E94CC33`, v2):
   * Outlet port: `'output0'`.
   * Input port scale & translation: tipe `float2`.
3. **Smooth Node** (`77697265-86ce-4e85-a02d-34f915fca74e`, v1):
   * Outlet port: `'output0'`.
4. **Attack Release Node** (`77697265-D980-43B3-9237-6683B154A5B0`, v1):
   * Outlet port: `'output'`.
   * Input port: `'trigger'`, `'release-time'`, `'attack-time'`.
5. **Mask Node** (`77697265-CB86-4A6F-AABA-009C4C8BB5C1`, v2):
   * Input: `'input'` (tekstur utama), `'mask'` (tekstur penutup).
   * Outlet: `'output'`.
6. **Video Mixer Node** (`77697265-A270-4D60-911C-A88B1BE6369A`, v3):
   * Mode 0: `Alpha Blend` (cocok untuk Bypass routing).
   * Mode 11: `Add Blend` (cocok untuk overlay cahaya, flash, dan laser neon tanpa meredupkan video asli).

---

## 6. Prosedur Re-Kompilasi

Jika ingin melakukan modifikasi parameter atau menambah fitur di masa mendatang:
1. Buka dan sesuaikan generator di [`build_suite.py`](file:///C:/ANDREAS/ip26-zzfx/build_suite.py).
2. Jalankan perintah kompilasi:
   ```powershell
   python C:\ANDREAS\ip26-zzfx\build_suite.py
   ```
3. Skrip akan otomatis:
   * Mengenerate file `.wire` (JSON) ke folder `wire/`.
   * Memanggil `Wire.exe compile` untuk memproduksi biner `.cwired` ke folder `cwired/`.
   * Memvalidasi ukuran biner hasil kompilasi.

---
*Dokumen ini disusun sebagai blueprint resmi rekayasa balik plugin visual Resolume untuk IP26 Production.*
