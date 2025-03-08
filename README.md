# ♟️ AI Chess Bot (Stockfish Tabanlı)

Bu proje, **Stockfish** motorunu kullanarak çalışan bir satranç botudur. **Pygame** ile görselleştirilmiş bir satranç tahtası içerir ve kullanıcıya karşı oynayabilir.

## 🚀 Özellikler

- **Stockfish Entegrasyonu** 🏆  
  Güçlü bir satranç motoru ile kullanıcıya karşı oynama imkanı sağlar.
  
- **Pygame Tabanlı Satranç Tahtası** 🎨  
  Kullanıcı dostu bir arayüze sahip olup, hamleleri görsel olarak takip edebilirsiniz.
  
- **Hamle Vurgulama ve Animasyonlar** 🔥  
  Seçilen taşların hareket alanları gösterilir ve taş hareketleri animasyonludur.
  
- **Şah Mat Algılama** ⚡  
  Oyun sona erdiğinde "Şah Mat" ekranı görüntülenir ve tekrar başlatılabilir.

## 📌 Kurulum

### 1️⃣ Gerekli Bağımlılıkları Yükleyin

Proje için **Python** yüklü olmalıdır. Gerekli bağımlılıkları aşağıdaki komutla yükleyebilirsiniz:

```bash
pip install pygame python-chess
```

Ayrıca **Stockfish** motorunu indirip uygun bir dizine yerleştirin. Daha sonra `STOCKFISH_PATH` değişkenini güncelleyin:

```python
STOCKFISH_PATH = "C:/path/to/stockfish.exe"  # Windows için
echo "export STOCKFISH_PATH=/path/to/stockfish" >> ~/.bashrc  # Linux/macOS için
```

### 2️⃣ Projeyi Çalıştırın

```bash
python chess_bot.py
```

## 🎯 Kullanım

- **Taşları seçmek için fareyle tıklayın.**
- **Stockfish, hamle yapmanızın ardından kendi hamlesini oynayacaktır.**
- **Şah mat olduğunda ekranda "Şah Mat" mesajı görüntülenecektir.**

## 🔮 Gelecek Güncellemeler

- ✅ **Stockfish tabanlı satranç botu (Mevcut sürüm)**
- 🔄 **Kendi satranç yapay zekamı eğiterek Stockfish yerine onu kullanmak** (Yakında!)


