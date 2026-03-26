---
title: D'PARIS EGSOTIS
emoji: 🌄
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# 🌄 D’PARIS EGSOTIS
[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/prayphnadeak/dparis-egsotis)
## Direktori Statistik Pariwisata Berbasis GPS & Infografis  
Progressive Web App (PWA) – VueJS + Python Backend

---

## 📌 Deskripsi Aplikasi

**D’PARIS EGSOTIS (Direktori Statistik Pariwisata dengan Pemanfaatan GPS dan Unsur Infografis)** adalah aplikasi berbasis **Progressive Web Apps (PWA)** yang menyediakan direktori statistik pariwisata Kota Pagar Alam.

Aplikasi ini dirancang untuk:
- Menyediakan informasi akomodasi, wisata, dan kuliner
- Menampilkan infografis statistik pariwisata
- Terintegrasi dengan layanan WhatsApp CADAS Besemah
- Menyediakan kanal pengaduan publik
- Memanfaatkan koordinat GPS untuk navigasi lokasi

Sistem dibangun menggunakan:
- **Frontend:** VueJS 3 (PWA)
- **Backend:** Python (FastAPI / Django REST)
- **Database:** SQLite (dparis.db)

---

# 🏗️ Arsitektur & Deployment

### 🌐 Skema Hosting
```mermaid
graph TD
    A[Admin/Dev] -->|Update SQLite| B(Local Repo)
    B -->|git commit & push| C{Hugging Face Space}
    C -->|Docker Build| D[Full Stack App]
    D -->|Read/Write| E[(SQLite: dparis.db)]
```

### 🚀 Akses Aplikasi
| Service | Link |
| --- | --- |
| **Hugging Face Space** | [🔗 dparis-egsotis](https://huggingface.co/spaces/prayphnadeak/dparis-egsotis) |

---

## 💻 WORKFLOW UPDATE DATA
1. Pastikan database `backend/dparis.db` sudah terupdate.
2. Lakukan Push ke Hugging Face:
   ```bash
   git add .
   git commit -m "Update data/aplikasi"
   git push hf main
   ```
3. Hugging Face akan otomatis melakukan **Building Docker** dan **Redeploy**.

---

# 🖥️ FRONTEND REQUIREMENTS

## 🛠️ Teknologi

- VueJS 3 (Composition API)
- Vue Router
- Pinia (State Management)
- Axios
- Vite
- vite-plugin-pwa
- TailwindCSS / Vuetify
- Leaflet.js / Google Maps API

---

# 🧠 BACKEND REQUIREMENTS

## 🛠️ Teknologi

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Uvicorn
- Docker

---

# 📦 ENVIRONMENT VARIABLES

### Frontend (`frontend/.env`)
```
VITE_API_URL=https://prayphnadeak-dparis-egsotis.hf.space
```

### Backend (`backend/.env` / Space Secrets)
```
DATABASE_URL=sqlite:///./dparis.db
SECRET_KEY=your-secret-key
```

---

# 🎯 KESIMPULAN

D’PARIS EGSOTIS adalah sistem:

✔️ Direktori Pariwisata  
✔️ Berbasis Statistik  
✔️ Terintegrasi GPS  
✔️ Berbasis Progressive Web App  
✔️ Siap dikembangkan menjadi Smart Tourism Platform  

---