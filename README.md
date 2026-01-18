# Aura Wireless Intelligence 📡

Aura Wireless Intelligence, kayıtlı Wi-Fi parolalarını görüntülemek, yönetmek ve paylaşmak için tasarlanmış modern, güvenli ve kullanıcı dostu bir Windows masaüstü uygulamasıdır.

---

## 🚀 Özellikler

- **Gelişmiş Arayüz:** CustomTkinter ile oluşturulmuş, modern ve dinamik tasarım.
- **Dinamik Dil Desteği:** Tek tıkla Türkçe ve İngilizce arasında geçiş.
- **Parola Yönetimi:** Kayıtlı Wi-Fi parolalarını görüntüleme, arama ve kopyalama.
- **QR Kod Oluşturma:** Wi-Fi ağlarını anında paylaşmak için QR kod üretme ve kaydetme.
- **Dışa Aktarma:** Verilerinizi JSON veya CSV formatında yedekleme.
- **Sistem İstatistikleri:** Aktif bağlantı durumu, sinyal gücü ve hız takibi.
- **Gizlilik Odaklı:** Parolaları maskeleme/gösterme seçeneği ve sistem tepsisine (tray) küçülme özelliği.
- **Yönetici Yetkisi:** Gerekli sistem bilgilerine erişim için otomatik yönetici (admin) kontrolü.

---

## 📦 Çalıştırılabilir Dosya (EXE) Oluşturma

Projeyi tek bir `.exe` dosyasına dönüştürmek için PyInstaller kullanabilirsiniz:

1. **Gerekli araçları yükleyin:**

   ```bash
   pip install pyinstaller
   ```

2. **Derleme komutunu çalıştırın:**
   ```bash
   pyinstaller --noconfirm --onefile --windowed --icon="icon.png" --name "AuraWiFi" --add-data "$(python -c 'import customtkinter; import os; print(os.path.dirname(customtkinter.__file__))');customtkinter" wifi.py
   ```
   _Not: Oluşturulan dosya `dist/` klasöründe yer alacaktır._

---

## 🛠 Kurulum ve Gereksinimler

- **İşletim Sistemi:** Windows (Netsh komutları için gereklidir).
- **Python:** 3.8 veya üzeri.

1. **Depoyu klonlayın:**
   ```bash
   git clone https://github.com/Memati8383/Kayitli-WiFi-Parolalari.git
   ```
2. **Gerekli kütüphaneleri yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Uygulamayı başlatın:**
   ```bash
   python wifi.py
   ```

---

## 📝 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.

## 🤝 İletişim

[Memati8383](https://github.com/Memati8383)
