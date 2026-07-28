# AI Travel Planner

AI Travel Planner, kullanıcı tercihlerini dikkate alarak kişiselleştirilmiş seyahat önerileri ve günlük gezi planları oluşturan yapay zekâ destekli bir seyahat planlama prototipidir.

Projenin mevcut sürümü Roma şehri üzerinde geliştirilmiştir. Sistem; kullanıcının ilgi alanları, bütçesi, seyahat temposu, günlük zaman aralığı, hava durumu tercihleri ve aile dostu mekân ihtiyacı gibi kriterlere göre turistik lokasyonları puanlar.

V1 sürümünde kural tabanlı puanlama ve örnek gezi planı oluşturma altyapısı geliştirilmiştir.

V2 sürümünde ise makine öğrenmesi tabanlı kişiselleştirilmiş öneri modeli, çok günlük gezi planlama motoru, FastAPI servis katmanı ve otomatik test altyapısı eklenmiştir.

---

# V1 — Kural Tabanlı Seyahat Planlama Sistemi

## V1 Kapsamı

* Roma için 40 turistik lokasyonluk veri seti oluşturuldu.
* OpenTripMap API ile lokasyon verileri çekildi.
* OpenTripMap verileri master lokasyon listesiyle eşleştirildi.
* Eksik lokasyonlar Wikidata ve manuel veri ile tamamlandı.
* Planlama için kategori, süre, ücret, ilgi skorları ve area group kolonları eklendi.
* Veri kaynakları ve güven seviyesi için confidence kolonları eklendi.
* Kullanıcı profiline göre suitability score hesaplandı.
* Farklı kullanıcı profilleriyle test yapıldı.
* Roma için 3 günlük saatli örnek gezi planı üretildi.

## V1 Kullanılan Veri Kaynakları

* OpenTripMap API
* Wikidata
* Manuel veri tamamlama
* V1 Feature Engineering

Lokasyon kimliği, koordinatlar ve kaynak ID bilgileri OpenTripMap ve Wikidata üzerinden oluşturulmuştur.

Süre, ücret ve ilgi skorları V1 prototipi için kural tabanlı başlangıç değerleri olarak atanmıştır.

Bu alanların sonraki sürümlerde resmi web siteleri, Google Places API ve gerçek kullanıcı geri bildirimleriyle geliştirilmesi planlanmaktadır.

## V1 Ana Veri Seti

Final V1 ana veri seti:

```text
datasets/master/rome/rome_master_dataset_v1.csv
```

Bu dosya Roma için 40 turistik lokasyon içermektedir.

Ana veri setinde şu veri grupları bulunmaktadır:

* Lokasyon adı
* Şehir ve ülke bilgisi
* Enlem ve boylam bilgisi
* OpenTripMap ve Wikidata kimlikleri
* Kategori ve alt kategori
* Ortalama ziyaret süresi
* Minimum ve maksimum ziyaret süresi
* Giriş ücreti
* Bütçe seviyesi
* İlgi alanı skorları
* Turistik önem skoru
* Hava durumu uygunluğu
* Aile dostu olma durumu
* Ulaşım ve yürüme zorluğu bilgileri
* Veri kaynağı
* Veri güven seviyesi

## V1 Suitability Score Mantığı

Sistem, her lokasyon için kullanıcının profiline göre 0 ile 100 arasında uygunluk skoru hesaplar.

V1 formülünde kullanılan bileşenler:

* Interest match score
* Importance score
* Budget match score
* Time match score
* Tempo match score
* Weather match score

Formül:

```text
suitability_score =
interest_match * 0.35
+ importance_score * 0.25
+ budget_match * 0.15
+ time_match * 0.10
+ tempo_match * 0.10
+ weather_match * 0.05
```

## V1 Test Edilen Kullanıcı Profilleri

* history_architecture_user
* art_museum_user
* food_evening_user
* nature_slow_user
* low_budget_fast_user

Profil skor çıktıları:

```text
datasets/outputs/scores/
```

## V1 Örnek Gezi Planı

Final itinerary dosyası:

```text
datasets/outputs/itineraries/rome_sample_itinerary.csv
```

Örnek rota:

### 1. Gün — Vatican Area

* Vatican Museums
* Sistine Chapel
* St. Peter's Basilica
* Castel Sant'Angelo

### 2. Gün — Ancient Rome

* Colosseum
* Roman Forum
* Palatine Hill
* Altare della Patria

### 3. Gün — Historic Center ve Trastevere

* Pantheon
* Piazza Navona
* Trevi Fountain
* Piazza del Popolo
* Trastevere

## V1 Script Çalıştırma Sırası

```bash
python scripts/fetch_opentripmap_rome.py
python scripts/create_rome_40_master_list.py
python scripts/enrich_master_with_opentripmap.py
python scripts/fetch_missing_opentripmap_by_name.py
python scripts/complete_manual_locations.py
python scripts/add_planning_features.py
python scripts/add_data_confidence.py
python scripts/score_locations.py
python scripts/add_area_groups.py
python scripts/create_sample_itinerary.py
```

## V1 Limitasyonları

* Sadece Roma şehri desteklenmektedir.
* Bazı planlama özellikleri kural tabanlıdır.
* Giriş ücretleri ve ziyaret süreleri başlangıç seviyesinde hazırlanmıştır.
* Açılış ve kapanış saatleri resmi kaynaklardan otomatik doğrulanmamaktadır.
* Gerçek rota süreleri Google Maps gibi servislerden alınmamaktadır.
* Kullanıcı profili script içinden tanımlanmaktadır.

---

# V2 — Makine Öğrenmesi Tabanlı Öneri Sistemi

V2 sürümünde, V1 veri seti kullanılarak kişiselleştirilmiş bir makine öğrenmesi öneri sistemi geliştirilmiştir.

Sistem, kullanıcı tercihlerini lokasyon özellikleriyle karşılaştırarak her lokasyon için kişisel bir uygunluk puanı üretir.

## V2 Kapsamı

* Roma lokasyon verilerinin makine öğrenmesine uygun hale getirilmesi
* Kullanıcı ve lokasyon özelliklerinin birleştirilmesi
* Sentetik kullanıcı profilleri oluşturulması
* 40.000 kullanıcı-lokasyon eğitim satırı oluşturulması
* Birden fazla regresyon modelinin eğitilmesi
* En iyi modelin otomatik seçilmesi
* Kullanıcıya özel lokasyon sıralaması
* Her öneri için açıklama üretimi
* Bütçe ve gezi temposu kontrolü
* Çok günlük saatlik gezi planı oluşturma
* Yaklaşık mesafe ve ulaşım süresi hesaplama
* FastAPI servis katmanı
* Swagger dokümantasyonu
* Otomatik API testleri

## Kullanılan Teknolojiler

* Python
* Pandas
* NumPy
* Scikit-learn
* Joblib
* FastAPI
* Uvicorn
* Pydantic
* Pytest
* HTTPX
* OpenPyXL

## Proje Klasör Yapısı

```text
aiTravelPlanner/
├── api/
│   ├── __init__.py
│   └── main.py
│
├── datasets/
│   ├── raw/
│   │   └── rome/
│   │
│   ├── master/
│   │   └── rome/
│   │       ├── rome_master_dataset_v1.csv
│   │       └── rome_master_dataset_v1.xlsx
│   │
│   ├── processed/
│   │   └── rome_locations_ml_ready.csv
│   │
│   ├── training/
│   │   ├── rome_user_location_training.csv
│   │   └── synthetic_user_profiles.csv
│   │
│   ├── outputs/
│   │   ├── scores/
│   │   └── itineraries/
│   │
│   └── archive/
│
├── models/
│   ├── location_recommender_v2.joblib
│   ├── feature_columns.json
│   └── model_metadata.json
│
├── reports/
│   ├── model_comparison.csv
│   ├── model_metrics.json
│   ├── ranking_metrics.json
│   ├── user_ranking_results.csv
│   ├── sample_top_recommendations.csv
│   ├── latest_recommendations.csv
│   ├── latest_itinerary.csv
│   ├── latest_itinerary.xlsx
│   └── latest_itinerary_skipped.csv
│
├── scripts/
│   ├── fetch_opentripmap_rome.py
│   ├── create_rome_40_master_list.py
│   ├── enrich_master_with_opentripmap.py
│   ├── fetch_missing_opentripmap_by_name.py
│   ├── complete_manual_locations.py
│   ├── add_planning_features.py
│   ├── add_data_confidence.py
│   ├── score_locations.py
│   ├── add_area_groups.py
│   └── create_sample_itinerary.py
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── generate_training_data.py
│   ├── train_models.py
│   ├── evaluate_ranking.py
│   ├── predict.py
│   ├── create_itinerary.py
│   ├── test_user_scenarios.py
│   └── test_itinerary_scenarios.py
│
├── tests/
│   ├── __init__.py
│   └── test_api.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Kurulum

Projeyi bilgisayarınıza indirin:

```bash
git clone PROJE_GITHUB_ADRESI
```

Proje klasörüne girin:

```bash
cd aiTravelPlanner
```

Gerekli Python paketlerini yükleyin:

```bash
pip install -r requirements.txt
```

Python sürümünü kontrol edin:

```bash
python --version
```

Proje Python 3 ile çalışmaktadır.

---

# Ortam Değişkenleri

OpenTripMap API anahtarı `.env` dosyasında tutulur.

```env
OPENTRIPMAP_API_KEY=your_api_key_here
```

`.env` dosyası GitHub'a yüklenmemelidir.

`.gitignore` dosyasında aşağıdaki satır bulunmalıdır:

```text
.env
```

---

# V2 Veri Ön İşleme

Ana Roma veri setini makine öğrenmesi modeline uygun hale getirmek için:

```bash
python src/preprocessing.py
```

Bu işlem aşağıdaki dosyayı oluşturur:

```text
datasets/processed/rome_locations_ml_ready.csv
```

İşlenmiş veri seti:

* 40 lokasyon
* 38 model özelliği
* Eksik değeri olmayan temiz veri yapısı

içermektedir.

Modelde kullanılan başlıca lokasyon özellikleri:

* Koordinatlar
* OpenTripMap puanı
* Popülerlik skoru
* Ortalama ziyaret süresi
* Minimum ve maksimum ziyaret süreleri
* Giriş ücreti
* Önem skoru
* İlgi alanı skorları
* Toplu taşıma skoru
* Yürüme zorluğu skoru
* Rezervasyon gereksinimi
* Aile dostu olma durumu
* Ücretsiz olma durumu
* Yağmurlu ve sıcak hava uygunluğu
* Kategori
* Alt kategori
* Indoor veya outdoor durumu
* Area group

---

# Feature Engineering

Kullanıcı özellikleriyle lokasyon özelliklerini birleştirmek için:

```bash
python src/feature_engineering.py
```

Kullanıcı profili ile lokasyon verileri birleştirilerek modelin tahmin yapacağı özellik matrisi oluşturulur.

Kullanıcı profilinde kullanılan alanlar:

* history_interest
* museum_interest
* art_interest
* architecture_interest
* photography_interest
* nature_interest
* gastronomy_interest
* shopping_interest
* religious_interest
* budget_level
* max_entry_fee
* tempo
* preferred_visit_time
* rainy_weather
* hot_weather
* family_friendly_required
* free_place_preference

---

# Eğitim Verisi Oluşturma

Sentetik kullanıcı profilleri ve kullanıcı-lokasyon eşleşmeleri oluşturmak için:

```bash
python src/generate_training_data.py
```

Bu işlem:

* 1.000 sentetik kullanıcı profili
* Kullanıcı başına 40 lokasyon
* Toplam 40.000 kullanıcı-lokasyon satırı
* 106 kolonlu eğitim veri seti

oluşturur.

Çıktılar:

```text
datasets/training/synthetic_user_profiles.csv
datasets/training/rome_user_location_training.csv
```

Hedef uygunluk puanı oluşturulurken şu bileşenler kullanılır:

* İlgi alanı uyumu
* Lokasyon önemi
* Bütçe uyumu
* Gezi temposu uyumu
* Zaman tercihi
* Hava durumu
* Aile dostu olma durumu

V2 hedef puan ağırlıkları:

```text
Interest Match: 0.45
Importance: 0.12
Budget Match: 0.15
Tempo Match: 0.10
Time Match: 0.07
Weather Match: 0.06
Family Match: 0.05
```

---

# Model Eğitimi

Regresyon modellerini eğitmek ve karşılaştırmak için:

```bash
python src/train_models.py
```

Kullanıcı bazlı veri ayrımı uygulanmıştır:

```text
Eğitim kullanıcıları: 800
Test kullanıcıları: 200
Eğitim satırı: 32.000
Test satırı: 8.000
```

Karşılaştırılan modeller:

* Linear Regression
* Decision Tree Regressor
* Random Forest Regressor
* Gradient Boosting Regressor

En iyi model olarak Gradient Boosting Regressor seçilmiştir.

Model performansı:

```text
MAE: 2.3456
RMSE: 2.9368
R²: 0.8955
```

Kaydedilen model:

```text
models/location_recommender_v2.joblib
```

Modelle birlikte aşağıdaki dosyalar da kaydedilir:

```text
models/feature_columns.json
models/model_metadata.json
```

Model raporları:

```text
reports/model_comparison.csv
reports/model_metrics.json
reports/test_predictions.csv
```

---

# Sıralama Performansı

Kullanıcı bazlı öneri sıralamasını değerlendirmek için:

```bash
python src/evaluate_ranking.py
```

Elde edilen sıralama sonuçları:

```text
Top-1 Accuracy: 0.6850
Top-3 Overlap: 0.6917
Top-5 Overlap: 0.7910
Top-10 Overlap: 0.8280
NDCG@5: 0.9908
NDCG@10: 0.9919
MRR: 0.8128
```

Çıktılar:

```text
reports/ranking_metrics.json
reports/user_ranking_results.csv
reports/sample_top_recommendations.csv
```

---

# Kullanıcı Senaryosu Testleri

Farklı kullanıcı profillerinin farklı öneriler alıp almadığını kontrol etmek için:

```bash
python src/test_user_scenarios.py
```

Test edilen profiller:

* Tarih ve mimari odaklı kullanıcı
* Müze ve sanat odaklı kullanıcı
* Doğa ve fotoğraf odaklı kullanıcı
* Gastronomi ve akşam odaklı kullanıcı
* Ücretsiz ve düşük bütçeli kullanıcı
* Çocuklu aile
* Hızlı gezi temposuna sahip kullanıcı
* Yağmurlu hava profili
* Alışveriş ve şehir yaşamı profili
* Genel ilk ziyaret profili

Senaryo testlerinde farklı profiller için farklı ilk öneriler üretilmiştir.

Örnek sonuçlar:

```text
Tarih ve mimari: St. Peter's Basilica
Müze ve sanat: Borghese Gallery
Doğa: Villa Borghese
Gastronomi: Trastevere
Aile: Villa Borghese
Alışveriş: Campo de' Fiori
```

---

# Öneri Üretme

Varsayılan kullanıcı profili için öneri oluşturmak amacıyla:

```bash
python src/predict.py
```

Çıktı:

```text
reports/latest_recommendations.csv
```

Her öneri için şu bilgiler üretilir:

* Öneri sırası
* Lokasyon adı
* Kategori
* Alt kategori
* Enlem ve boylam
* Tahmini uygunluk puanı
* Giriş ücreti
* Ortalama ziyaret süresi
* Ziyaret zamanı
* Rezervasyon gereksinimi
* Aile dostu olma durumu
* Ulaşım skoru
* Yürüme zorluğu
* Öneri nedeni

Örnek öneri açıklaması:

```text
Tarih ilginizle yüksek uyumlu;
mimari ilginizle yüksek uyumlu;
fotoğraf çekimi için uygun;
belirlediğiniz giriş ücreti sınırına uygun.
```

---

# Çok Günlük Gezi Planlama Motoru

Makine öğrenmesi önerilerine göre çok günlük ve saatlik plan oluşturmak için:

```bash
python src/create_itinerary.py
```

Çıktılar:

```text
reports/latest_itinerary.csv
reports/latest_itinerary.xlsx
reports/latest_itinerary_skipped.csv
```

Planlama motoru şu kriterleri değerlendirir:

* Kullanıcının ML uygunluk puanı
* Minimum uygunluk skoru
* Toplam giriş ücreti bütçesi
* Günlük başlangıç saati
* Günlük bitiş saati
* Ziyaret süreleri
* Lokasyonlar arası mesafe
* Yaklaşık ulaşım süresi
* Günlük maksimum lokasyon sayısı
* Öğle molası
* Seyahat temposu
* Başlangıç koordinatı
* Rezervasyon durumu

Lokasyonlar arası mesafe Haversine formülü ile hesaplanır.

Gerçek yol mesafesine yaklaşmak için rota mesafesi belirli bir katsayıyla çarpılır.

Örnek 3 günlük plan sonucu:

```text
Planlanan gün: 3
Planlanan lokasyon: 14
Toplam giriş ücreti: 113 / 120 €
Toplam rota mesafesi: 10,25 km
Toplam ulaşım süresi: 247 dakika
Ortalama uygunluk puanı: 73,28
```

---

# Planlama Senaryosu Testleri

Farklı kullanıcı ve seyahat ayarlarıyla planlama sistemini test etmek için:

```bash
python src/test_itinerary_scenarios.py
```

Test edilen senaryolar:

* Tarih ve mimari
* Ücretsiz gezi
* Doğa ve fotoğraf
* Gastronomi ve akşam
* Çocuklu aile
* Hızlı ilk ziyaret

Toplam 6 senaryonun tamamı başarılı şekilde plan oluşturmuştur.

---

# FastAPI Servisi

V2 modelinin frontend veya başka sistemler tarafından kullanılabilmesi için FastAPI servis katmanı geliştirilmiştir.

API sunucusunu başlatmak için:

```bash
python -m uvicorn api.main:app --reload
```

Sunucu adresi:

```text
http://127.0.0.1:8000
```

Swagger dokümantasyonu:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoint'leri

## Ana Endpoint

```http
GET /
```

API hakkında temel bilgi döndürür.

## Sağlık Kontrolü

```http
GET /api/health
```

Örnek cevap:

```json
{
  "status": "healthy",
  "model": "location_recommender_v2",
  "city": "Rome"
}
```

## Kişiselleştirilmiş Öneriler

```http
POST /api/recommendations
```

Örnek istek:

```json
{
  "user_profile": {
    "history_interest": 2,
    "museum_interest": 1,
    "art_interest": 2,
    "architecture_interest": 3,
    "photography_interest": 8,
    "nature_interest": 2,
    "gastronomy_interest": 10,
    "shopping_interest": 6,
    "religious_interest": 1,
    "budget_level": "medium",
    "max_entry_fee": 20,
    "tempo": "normal",
    "preferred_visit_time": "evening",
    "rainy_weather": false,
    "hot_weather": false,
    "family_friendly_required": false,
    "free_place_preference": 5
  },
  "top_n": 5
}
```

Bu profil için örnek ilk öneriler:

```text
1. Trastevere
2. Piazza Navona
3. Campo de' Fiori
4. St. Peter's Basilica
5. Spanish Steps
```

## Çok Günlük Gezi Planı

```http
POST /api/itineraries
```

Bu endpoint:

* Kullanıcı profilini alır.
* Seyahat ayarlarını alır.
* Lokasyonları kişiselleştirilmiş olarak puanlar.
* Bütçe ve zaman kontrollerini yapar.
* Günlere ve saatlere ayrılmış plan döndürür.
* Günlük plan özetlerini oluşturur.
* Atlanan lokasyonları listeler.
* Sistem limitasyonlarını bildirir.

---

# Otomatik API Testleri

API testlerini çalıştırmak için:

```bash
python -m pytest tests/test_api.py -v
```

Test edilen alanlar:

* Ana endpoint
* Sağlık endpoint'i
* Öneri endpoint'i
* Öneri sayısı doğrulaması
* İlgi puanı doğrulaması
* Gezi planı endpoint'i
* Ücretsiz gezi senaryosu
* Saat formatı doğrulaması
* Seyahat günü doğrulaması

Mevcut test sonucu:

```text
9 passed
```

Testler aşağıdaki durumları kontrol eder:

* API'nin doğru cevap vermesi
* Önerilerin azalan puana göre sıralanması
* Gastronomi profiline uygun lokasyonların gelmesi
* Bütçenin aşılmaması
* Ücretsiz planda ücretli lokasyon bulunmaması
* Hatalı kullanıcı verilerinin reddedilmesi
* Hatalı gün ve saat bilgilerinin reddedilmesi

---

# Requirements

Projede kullanılan temel Python paketleri:

```text
fastapi
uvicorn
pydantic
pandas
numpy
scikit-learn
joblib
openpyxl
pytest
httpx
```

Tüm paketleri yüklemek için:

```bash
pip install -r requirements.txt
```

---

# Mevcut Limitasyonlar

* Sistem şu anda yalnızca Roma şehrini desteklemektedir.
* Açılış ve kapanış saatleri resmi kaynaklardan doğrulanmamaktadır.
* Ulaşım süreleri gerçek yol servisi yerine yaklaşık mesafe hesabıyla oluşturulmaktadır.
* Trafik ve toplu taşıma yoğunluğu hesaba katılmamaktadır.
* Günlük ilk lokasyona ulaşım, başlangıç koordinatı verilmezse hesaplanmamaktadır.
* Eğitim verileri sentetik kullanıcı profilleriyle oluşturulmuştur.
* Gerçek kullanıcı puanları henüz sisteme dahil edilmemiştir.
* Gastronomi ve alışveriş kategorilerinin veri çeşitliliği artırılmalıdır.
* Giriş ücretleri zaman içinde değişebileceği için resmi kaynaklarla güncellenmelidir.
* Aynı anda gelen çok sayıda plan isteği için API yapısı ileride yeniden düzenlenmelidir.

---

# V2 Sonucu

V2 sonunda sistem aşağıdaki akışla çalışmaktadır:

```text
Kullanıcı tercihleri
        ↓
Feature Engineering
        ↓
Makine Öğrenmesi Modeli
        ↓
Lokasyon Uygunluk Puanları
        ↓
Kişiselleştirilmiş Öneriler
        ↓
Bütçe ve Zaman Kontrolü
        ↓
Mesafe ve Rota Hesabı
        ↓
Saatlik Çok Günlük Gezi Planı
        ↓
JSON, CSV ve Excel Çıktıları
```

Sistem:

1. Kullanıcı tercihlerini alır.
2. Roma'daki 40 lokasyonu kullanıcıya özel puanlar.
3. Lokasyonları uygunluk puanına göre sıralar.
4. Her öneri için açıklama üretir.
5. Bütçe ve zaman koşullarını kontrol eder.
6. Yakın lokasyonları rota mantığıyla sıralar.
7. Öğle molalarını plana ekler.
8. Saatlik ve çok günlük gezi planı oluşturur.
9. Sonuçları JSON, CSV ve Excel biçimlerinde sunar.
10. FastAPI üzerinden frontend kullanımına hazır hale getirir.

---

# Gelecek Çalışmalar

* Next.js frontend formunun geliştirilmesi
* Kullanıcı kayıt ve giriş sistemi
* MySQL veritabanı entegrasyonu
* Plan kaydetme ve geçmiş planları görüntüleme
* Google Places API entegrasyonu
* Gerçek açılış ve kapanış saatleri
* Google Maps veya OpenRouteService rota entegrasyonu
* Gerçek yol ve ulaşım süresi hesaplama
* Kullanıcı geri bildirimleriyle modelin yeniden eğitilmesi
* Yeni şehirlerin sisteme eklenmesi
* Şehir bağımsız veri pipeline yapısı
* Gerçek kullanıcı puanlarından öğrenen öneri sistemi
* Model açıklanabilirliğinin geliştirilmesi
* Docker desteği
* Bulut ortamına deployment
* Mobil uyumlu kullanıcı arayüzü
