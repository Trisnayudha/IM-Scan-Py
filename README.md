# Face Check-In Backend

Sistem backend untuk check-in peserta event berbasis QR Code dan face detection menggunakan Flask + MySQL + DeepFace.

---

## 🔧 Requirements

- Python 3.9+
- MySQL database
- MacOS (ARM64) atau Linux (tested)
- Virtual environment aktif (`python3 -m venv venv && source venv/bin/activate`)

---

## 📦 Installation

```bash
git clone https://your-repo.git
cd face_checkin_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Edit file `config.py`:

```python
class Config:
    DB_HOST = 'localhost'
    DB_USER = 'youruser'
    DB_PASSWORD = 'yourpassword'
    DB_NAME = 'yourdb'
```

---

## 🚀 Run App

```bash
source venv/bin/activate
python app.py
```

---

## 📡 API Endpoints

### 0. Check Face

`POST /check-face`

Form-data parameters:

- `image`: file upload (required)

**Response (success):**

```json
{
  "status": 1,
  "message": "Face detected",
  "data": { "face_detected": true }
}
```

**Response (failure):**

```json
{
  "status": 0,
  "message": "No face detected: <error message>",
  "data": { "face_detected": false }
}
```

### 1. Scan QR Code

`POST /scan-qr`

Request JSON body:

- `code_payment`: string (required)
- `day`: string, ISO format (`YYYY-MM-DD`) atau Indonesian format (e.g. `2025 juni tanggal 10`) (required)

```json
{
  "code_payment": "EX123456",
  "day": "2025-06-10"
}
```

**Response:**

```json
{
  "status": 1,
  "message": "Scan QR successful",
  "data": {
    "name": "Winter Humphrey",
    "job_title": "Director",
    "company": "Fletcher Traders",
    "code_payment": "EX123456",
    "checkin_field": "checkin_day1",
    "ticket_type": "Delegate Pass"
  }
}
```

### 2. Check-In

`POST /checkin`

JSON body:

- `code_payment`: string (required)
- `link_webhook`: URL string (required)
- `day`: string, ISO format (`YYYY-MM-DD`) atau format Indonesia (`2025 juni tanggal 10`) (required)
- `name`: string (required)
- `job_title`: string (required)
- `company`: string (required)
- `image`: base64-encoded string (required)

**Raw JSON Body Example:**

```json
{
  "code_payment": "EX123456",
  "link_webhook": "https://yourdomain.com/webhook",
  "day": "2025-06-10",
  "name": "Winter Humphrey",
  "job_title": "Director",
  "company": "Fletcher Traders",
  "image": "/9j/4AAQSkZJRgABAQAAAQABAAD... (base64 string)"
}
```

**Response:**

```json
{
  "status": 1,
  "message": "Check-in berhasil",
  "data": {
    "name": "Winter Humphrey",
    "company": "Fletcher Traders",
    "job_title": "Director",
    "code_payment": "EX123456",
    "day": "2025-06-10",
    "ticket_type": "Delegate Pass",
    "ticket_color": "#1428DF"
  }
}
```

### 3. List Delegates

`GET /list-delegate?search=<term>`

Query parameters:

- `search`: string, minimum 4 characters (required)

**Response:**

```json
{
  "status": 1,
  "message": "Success",
  "data": [
    {
      "name": "Winter Humphrey",
      "company_name": "Fletcher Traders",
      "code_payment": "EX123456"
    }
    // more items...
  ]
}
```

---

## 🔒 Note

- Sistem ini tidak menyimpan wajah, hanya mendeteksi apakah gambar adalah wajah valid atau tidak.
- Untuk verifikasi wajah bisa ditambahkan later jika ada database wajah delegate.

---

## ✅ Done

- Scan QR
- Verifikasi wajah (True/False)
- Check-in + webhook print
- Reprint + webhook print

---

Happy check-in! 🎟️

# IM-Scan

# IM-Scan
