# D'PARIS EGSOTIS – Backend API

Python FastAPI backend untuk aplikasi **D'PARIS EGSOTIS** (Direktori Statistik Pariwisata Berbasis GPS & Infografis) Kota Pagar Alam.

---

## 🚀 Cara Menjalankan (XAMPP/Lokal)

### 1. Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Siapkan database MySQL di XAMPP

Buka phpMyAdmin di `http://localhost/phpmyadmin` lalu buat database:

```sql
CREATE DATABASE dparis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Konfigurasi `.env`

File `.env` sudah tersedia dengan konfigurasi default XAMPP. Edit jika perlu:

```env
DATABASE_URL=mysql+pymysql://root:@localhost:3306/dparis_db
SECRET_KEY=your-secret-key-here
```

### 4. Jalankan server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API akan tersedia di: **http://localhost:8000**  
Swagger Docs: **http://localhost:8000/docs**

---

## 📦 Scripts

### Buat admin user
```bash
python scripts/create_admin.py
# atau dengan argumen custom:
python scripts/create_admin.py --username myAdmin --email admin@myapp.id --password Rahasia@123
```

### Seed sample data
```bash
python scripts/seed_data.py
```

---

## 🧪 Testing

```bash
pytest tests/ -v
```

---

## 📂 Struktur API

| Method | Endpoint | Deskripsi | Auth |
|--------|----------|-----------|------|
| POST | `/api/v1/auth/login` | Login | Public |
| POST | `/api/v1/auth/register` | Daftar | Public |
| GET | `/api/v1/auth/me` | Info user | User |
| GET | `/api/v1/accommodations/` | List akomodasi | Public |
| POST | `/api/v1/accommodations/` | Tambah akomodasi | Admin |
| GET | `/api/v1/tourism/` | List wisata | Public |
| POST | `/api/v1/tourism/` | Tambah wisata | Admin |
| GET | `/api/v1/culinary/` | List kuliner | Public |
| POST | `/api/v1/culinary/` | Tambah kuliner | Admin |
| GET | `/api/v1/infographics/` | List infografis | Public |
| POST | `/api/v1/complaints/` | Kirim pengaduan | Public |
| POST | `/api/v1/complaints/track` | Lacak pengaduan | Public |
| GET | `/api/v1/complaints/` | Semua pengaduan | Admin |
| GET | `/api/v1/dashboard/` | Statistik ringkasan | Admin |

---

## 🐳 Docker (Opsional)

```bash
docker-compose up -d
```

Akses: API → `http://localhost:8000`, phpMyAdmin → `http://localhost:8080`

---

## 🔐 Default Admin

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `Admin@12345` |
| Email | `admin@dparis.id` |

> ⚠️ **Ganti password segera setelah deploy ke production!**
