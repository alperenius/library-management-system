# Kütüphane Yönetim Sistemi

Python 202 Bootcamp bitirme projesi - Nesne Yönelimli Programlama, Harici API Kullanımı ve FastAPI ile Web API geliştirme konularını birleştiren kapsamlı bir kütüphane yönetim sistemi.

## 📚 Proje Açıklaması

Bu proje, üç farklı aşamada geliştirilmiş bir kütüphane yönetim sistemidir:

1. **Aşama 1**: OOP prensiplerine dayalı terminal uygulaması
2. **Aşama 2**: Open Library API entegrasyonu ile otomatik kitap bilgisi çekme
3. **Aşama 3**: FastAPI ile RESTful web servisi

### ✨ Özellikler

- 📖 Kitap ekleme, silme, listeleme ve arama
- 🌐 ISBN numarası ile otomatik kitap bilgisi çekme (Open Library API)
- 💾 JSON dosyası ile veri kalıcılığı
- 🚀 FastAPI ile modern web API
- 📊 Kütüphane istatistikleri
- 🧪 Kapsamlı unit ve integration testleri

## 🛠️ Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

### Adım Adım Kurulum

1. **Projeyi klonlayın:**
```bash
git clone https://github.com/kullanici-adi/library-management-system.git
cd library-management-system
```

2. **Virtual environment oluşturun (önerilen):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

## 🚀 Kullanım

### Terminal Uygulaması (Aşama 1 & 2)

Terminal uygulamasını başlatmak için:

```bash
python main.py
```

Uygulama menüsü:
- **1. Kitap Ekle**: ISBN numarası girerek kitap ekleyin
- **2. Kitap Sil**: ISBN numarası ile kitap silin
- **3. Kitapları Listele**: Tüm kitapları görüntüleyin
- **4. Kitap Ara**: ISBN ile kitap arayın
- **5. Çıkış**: Uygulamadan çıkın

### Web API (Aşama 3)

API sunucusunu başlatmak için:

```bash
uvicorn api:app --reload
```

API şu adreste çalışacaktır: `http://localhost:8000`

#### 📋 API Dokümantasyonu

FastAPI'nin otomatik dokümantasyonuna erişmek için:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### 🔗 API Endpoint'leri

| Method | Endpoint | Açıklama | Request Body |
|--------|----------|----------|--------------|
| GET | `/` | API durumu | - |
| GET | `/books` | Tüm kitapları listele | - |
| POST | `/books` | Yeni kitap ekle | `{"isbn": "978-0451524935"}` |
| GET | `/books/{isbn}` | Belirli kitabı getir | - |
| DELETE | `/books/{isbn}` | Kitap sil | - |
| GET | `/stats` | Kütüphane istatistikleri | - |

#### 📝 Örnek API Kullanımı

**Kitap ekleme:**
```bash
curl -X POST "http://localhost:8000/books" \
     -H "Content-Type: application/json" \
     -d '{"isbn": "978-0451524935"}'
```

**Tüm kitapları listeleme:**
```bash
curl "http://localhost:8000/books"
```

**Kitap silme:**
```bash
curl -X DELETE "http://localhost:8000/books/978-0451524935"
```

## 🧪 Testleri Çalıştırma

Tüm testleri çalıştırmak için:

```bash
pytest
```

Detaylı test raporu için:

```bash
pytest -v
```

Test coverage için:

```bash
pytest --cov=. --cov-report=html
```

### Test Dosyaları

- `test_book.py`: Book sınıfı unit testleri
- `test_library.py`: Library sınıfı unit testleri  
- `test_api.py`: FastAPI integration testleri

## 📁 Proje Yapısı

```
library-management-system/
├── book.py              # Book sınıfı
├── library.py           # Library sınıfı
├── main.py              # Terminal uygulaması
├── api.py               # FastAPI web servisi
├── requirements.txt     # Python bağımlılıkları
├── README.md           # Bu dosya
├── library.json        # Veri dosyası (otomatik oluşur)
├── test_book.py        # Book testleri
├── test_library.py     # Library testleri
└── test_api.py         # API testleri
```

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler

- **Python 3.8+**: Ana programlama dili
- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **httpx**: HTTP client library
- **Pydantic**: Veri validasyonu
- **Pytest**: Test framework
- **Open Library API**: Kitap bilgileri

### Mimari

- **OOP Tasarım**: Book ve Library sınıfları
- **JSON Persistence**: Veri kalıcılığı
- **RESTful API**: HTTP standartlarına uygun
- **Error Handling**: Kapsamlı hata yönetimi
- **Input Validation**: Pydantic ile veri doğrulama


## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.

## 📞 İletişim

Proje Sahibi - [GitHub Profili](https://github.com/alperenius)

Proje Linki: [https://github.com/kullanici-adi/library-management-system](https://github.com/alperenius/library-management-system)

---
