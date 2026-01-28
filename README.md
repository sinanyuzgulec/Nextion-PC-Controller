# Nextion PC Controller & Stream Deck

Bu proje, bir **Nextion HMI** ekranını PC üzerinden kontrol edilebilen, sistem verilerini (CPU/GPU/RAM) canlı gösteren ve medya kontrolü (Stream Deck) sağlayan modüler bir sisteme dönüştürmeyi amaçlar.

> **⚠️ DİKKAT:** Bu proje henüz geliştirme aşamasındadır (Work in Progress). Bazı modüller stabil çalışmayabilir veya geliştirilmeye devam edilmektedir.

## 🚀 Mevcut Özellikler
- **Otomatik Port Tespiti:** USB-to-TTL dönüştürücüyü otomatik bulur.
- **Sistem İzleme:** CPU/GPU kullanım, sıcaklık, frekans (GHz) ve RAM takibi.
- **Medya Kontrolü:** Sistem ses seviyesi (Slider), mikrofon ve hoparlör mute kontrolü.
- **Modüler Mimari:** Her sayfa için ayrı bir Python script'i ile genişletilebilir yapı.

## 🛠️ Donanım Gereksinimleri
- Nextion HMI Ekran (Örn: NX3224T028)
- USB to TTL Dönüştürücü (CH340, CP2102 vb.)
- Bağlantı kabloları

## 📦 Kurulum ve Çalıştırma
1. **Python Kütüphanelerini Yükleyin:**
   ```bash
   pip install pyserial psutil pynvml wmi pywin32 pycaw comtypes requests