<div align="center">
  <img src="icon.png" alt="Aura Logo" width="120">
  <h1>Aura Wireless Intelligence</h1>
  <p><b>Windows için Modern Wi-Fi Yönetim Aracı</b></p>
</div>

---

**Aura Wireless Intelligence**, kayıtlı Wi-Fi parolalarını yönetmek, görüntülemek, dışa aktarmak ve paylaşmak için tasarlanmış, **CustomTkinter** tabanlı modern bir masaüstü uygulamasıdır. Zarif tasarımı ve güçlü özellikleriyle ağ yönetimini bir üst seviyeye taşır.

## 🚀 Öne Çıkan Özellikler

- **🎨 Modern ve Estetik Arayüz:** Karanlık mod destekli, akıcı ve kullanıcı dostu tasarım.
- **🌍 Çoklu Dil Desteği:** **Türkçe** ve **İngilizce** dilleri arasında anlık geçiş imkanı.
- **🔑 Akıllı Parola Yönetimi:**
  - Kayıtlı tüm ağları listeleyin.
  - Parolaları gizleyin/gösterin.
  - Tek tıkla panoya kopyalayın.
- **📱 QR Kod Paylaşımı:** Misafirleriniz için Wi-Fi ağınızı anında **QR Kod**'a dönüştürün ve `png` olarak kaydedin.
- **📊 Canlı Sistem Analizi:** Aktif ağın sinyal kalitesini, bağlantı durumunu ve arayüz detaylarını canlı takip edin.
- **💾 Veri Yedekleme:** Ağ bilgilerinizi **JSON** veya **CSV** formatında dışa aktarın.
- **🛡️ Güvenli ve Yetkili:** Sistem komutlarına erişim için uygulama otomatik olarak yönetici izni ister.

---

## 🛠 Kurulum ve Gereksinimler

Proje **Windows 10/11** işletim sistemlerinde çalışmak üzere tasarlanmıştır.

### Ön Hazırlık

Sisteminizde **Python 3.8+** ve **Git**'in yüklü olduğundan emin olun.

### 1. Projeyi İndirin

```bash
git clone https://github.com/Memati8383/Kayitli-WiFi-Parolalari.git
cd Kayitli-WiFi-Parolalari
```

### 2. Kütüphaneleri Yükleyin

```bash
pip install -r requirements.txt
```

### 3. Çalıştırın

```bash
python wifi.py
```

---

## 📦 EXE (Uygulama) Olarak Derleme

Uygulamayı bağımsız bir `.exe` dosyasına dönüştürmek için **PyInstaller** kullanıyoruz. Aşağıdaki komut, tüm bağımlılıkları ve `CustomTkinter` temasını tek bir dosyada toplar.

```bash
# PyInstaller yüklü değilse:
pip install pyinstaller

# Derleme komutu:
pyinstaller --noconfirm --onefile --windowed --icon="icon.png" --name "AuraWiFi" --add-data "$(python -c 'import customtkinter; import os; print(os.path.dirname(customtkinter.__file__))');customtkinter" wifi.py
```

> **Bilgi:** Derleme tamamlandığında `AuraWiFi.exe` dosyası **`dist/`** klasöründe oluşacaktır.

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Hata bildirimleri, özellik istekleri veya Pull Request'ler için lütfen GitHub deposunu kullanın.

---

## 📝 Lisans

Bu proje **MIT Lisansı** ile korunmaktadır.

<div align="center">
  <sub>Geliştirici: <a href="https://github.com/Memati8383">Memati8383</a></sub>
</div>
