# Aura Wireless Intelligence 📡

Aura Wireless Intelligence, kayıtlı Wi-Fi parolalarını görüntülemek, yönetmek ve paylaşmak için tasarlanmış modern, güvenli ve kullanıcı dostu bir Windows masaüstü uygulamasıdır.

[English Description below](#english)

---

## 🇹🇷 Özellikler

- **Gelişmiş Arayüz:** CustomTkinter ile oluşturulmuş, modern ve dinamik tasarım.
- **Dinamik Dil Desteği:** Tek tıkla Türkçe ve İngilizce arasında geçiş.
- **Parola Yönetimi:** Kayıtlı Wi-Fi parolalarını görüntüleme, arama ve kopyalama.
- **QR Kod Oluşturma:** Wi-Fi ağlarını anında paylaşmak için QR kod üretme ve kaydetme.
- **Dışa Aktarma:** Verilerinizi JSON veya CSV formatında yedekleme.
- **Sistem İstatikleri:** Aktif bağlantı durumu, sinyal gücü ve hız takibi.
- **Gizlilik Odaklı:** Parolaları maskeleme/gösterme seçeneği ve sistem tepsisine (tray) küçülme özelliği.
- **Yönetici Yetkisi:** Gerekli sistem bilgilerine erişim için otomatik yönetici (admin) kontrolü.

### Çalıştırılabilir Dosya (EXE) Oluşturma

Projeyi tek bir `.exe` dosyasına dönüştürmek için PyInstaller kullanabilirsiniz:

1. Gerekli araçları yükleyin:
   ```bash
   pip install pyinstaller
   ```
2. Derleme komutunu çalıştırın:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --icon="icon.png" --name "AuraWiFi" --add-data "$(python -c 'import customtkinter; import os; print(os.path.dirname(customtkinter.__file__))');customtkinter" wifi.py
   ```
   _Not: Oluşturulan dosya `dist/` klasöründe yer alacaktır._

### Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/Memati8383/Kayitli-WiFi-Parolalari.git
   ```
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Uygulamayı başlatın:
   ```bash
   python wifi.py
   ```

---

<a name="english"></a>

## 🇺🇸 Features

- **Advanced UI:** Modern and dynamic interface built with CustomTkinter.
- **Dynamic Language Support:** Switch between Turkish and English instantly.
- **Password Management:** View, search, and copy saved Wi-Fi passwords.
- **QR Code Generation:** Generate and save QR codes for instant Wi-Fi sharing.
- **Data Export:** Backup your connection data in JSON or CSV formats.
- **System Stats:** Live monitoring of connection status, signal strength, and speed.
- **Privacy Oriented:** Password masking/unmasking and system tray support.
- **Admin Privileges:** Automatic administrative check for secure system data access.

### Creating Executable (EXE)

You can convert the project into a standalone `.exe` file using PyInstaller:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Run the build command:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --icon="icon.png" --name "AuraWiFi" --add-data "$(python -c 'import customtkinter; import os; print(os.path.dirname(customtkinter.__file__))');customtkinter" wifi.py
   ```
   _Note: The executable will be generated in the `dist/` folder._

### Requirements

- Python 3.8+
- Windows OS (Required for `netsh` commands)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Memati8383/Kayitli-WiFi-Parolalari.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python wifi.py
   ```

---

## 📝 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.

## 🤝 İletişim

[Memati8383](https://github.com/Memati8383)
