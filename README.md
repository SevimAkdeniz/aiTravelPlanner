# AI Travel Planner V1

AI Travel Planner, kullanıcı tercihlerini dikkate alarak kişiselleştirilmiş seyahat önerileri ve günlük gezi planı oluşturan bir seyahat planlama prototipidir.

Bu V1 sürümünde sistem Roma şehri üzerinde geliştirilmiştir. Kullanıcının ilgi alanı, bütçesi, seyahat temposu ve günlük zaman aralığına göre lokasyonlar skorlanır ve saatli gezi planı oluşturulur.

## V1 Kapsamı

- Roma için 40 turistik lokasyonluk veri seti oluşturuldu.
- OpenTripMap API ile lokasyon verileri çekildi.
- OpenTripMap verileri master lokasyon listesiyle eşleştirildi.
- Eksik lokasyonlar Wikidata ve manuel veri ile tamamlandı.
- Planlama için kategori, süre, ücret, ilgi skorları ve area group kolonları eklendi.
- Veri kaynakları ve güven seviyesi için confidence kolonları eklendi.
- Kullanıcı profiline göre suitability score hesaplandı.
- Farklı kullanıcı profilleriyle test yapıldı.
- Roma için 3 günlük saatli örnek gezi planı üretildi.

## Kullanılan Veri Kaynakları

- OpenTripMap API
- Wikidata
- Manual V1 Feature Engineering

Lokasyon kimliği, koordinatlar ve kaynak ID bilgileri OpenTripMap ve Wikidata üzerinden oluşturulmuştur.

Süre, ücret ve ilgi skorları V1 prototip için kural tabanlı başlangıç değerleri olarak atanmıştır. Bu alanlar sonraki sürümlerde resmi web siteleri, Google Places API ve kullanıcı geri bildirimleri ile geliştirilecektir.

## Proje Klasör Yapısı

datasets/
  raw/
    rome/
      opentripmap_rome_raw.csv

  master/
    rome/
      rome_master_dataset_v1.csv
      rome_master_dataset_v1.xlsx

  outputs/
    scores/
      rome_location_scores_history_architecture_user.csv
      rome_location_scores_art_museum_user.csv
      rome_location_scores_food_evening_user.csv
      rome_location_scores_nature_slow_user.csv
      rome_location_scores_low_budget_fast_user.csv
      rome_location_scores_profile_comparison.csv

    itineraries/
      rome_sample_itinerary.csv
      rome_sample_itinerary.xlsx

  archive/
    rome/
      intermediate files

scripts/
  fetch_opentripmap_rome.py
  create_rome_40_master_list.py
  enrich_master_with_opentripmap.py
  fetch_missing_opentripmap_by_name.py
  complete_manual_locations.py
  add_planning_features.py
  add_data_confidence.py
  score_locations.py
  add_area_groups.py
  create_sample_itinerary.py

## Ana Dataset

Final V1 ana dataset dosyası:

datasets/master/rome/rome_master_dataset_v1.csv

Bu dosya Roma için 40 lokasyon içerir.

Ana dataset içinde şu veri grupları bulunur:

- Lokasyon adı
- Şehir ve ülke bilgisi
- Koordinatlar
- OpenTripMap ve Wikidata ID bilgileri
- Kategori ve alt kategori
- Ortalama ziyaret süresi
- Giriş ücreti
- Bütçe seviyesi
- İlgi skorları
- Turistik önem skoru
- Hava durumu uygunluğu
- Veri kaynağı ve güven seviyesi

## Suitability Score Mantığı

Sistem her lokasyon için kullanıcının profiline göre 0-100 arasında uygunluk skoru hesaplar.

V1 formülünde kullanılan bileşenler:

- Interest match score
- Importance score
- Budget match score
- Time match score
- Tempo match score
- Weather match score

Formül:

suitability_score =
interest_match * 0.35
+ importance_score * 0.25
+ budget_match * 0.15
+ time_match * 0.10
+ tempo_match * 0.10
+ weather_match * 0.05

## Test Edilen Kullanıcı Profilleri

- history_architecture_user
- art_museum_user
- food_evening_user
- nature_slow_user
- low_budget_fast_user

Profil skor çıktıları şu klasördedir:

datasets/outputs/scores/

## Örnek Gezi Planı

Final itinerary dosyası:

datasets/outputs/itineraries/rome_sample_itinerary.csv

Örnek rota:

1. Gün - Vatican Area

- Vatican Museums
- Sistine Chapel
- St. Peter's Basilica
- Castel Sant'Angelo

2. Gün - Ancient Rome

- Colosseum
- Roman Forum
- Palatine Hill
- Altare della Patria

3. Gün - Historic Center + Trastevere

- Pantheon
- Piazza Navona
- Trevi Fountain
- Piazza del Popolo
- Trastevere

## Script Çalıştırma Sırası

1. python scripts/fetch_opentripmap_rome.py
2. python scripts/create_rome_40_master_list.py
3. python scripts/enrich_master_with_opentripmap.py
4. python scripts/fetch_missing_opentripmap_by_name.py
5. python scripts/complete_manual_locations.py
6. python scripts/add_planning_features.py
7. python scripts/add_data_confidence.py
8. python scripts/score_locations.py
9. python scripts/add_area_groups.py
10. python scripts/create_sample_itinerary.py

## Ortam Değişkenleri

OpenTripMap API anahtarı `.env` dosyasında tutulur.

OPENTRIPMAP_API_KEY=your_api_key_here

`.env` dosyası GitHub'a yüklenmemelidir.

## V1 Limitasyonları

- Sadece Roma şehri desteklenmektedir.
- Bazı planlama feature değerleri kural tabanlıdır.
- Giriş ücretleri ve ziyaret süreleri V1 draft değerleridir.
- Açılış ve kapanış saatleri henüz resmi kaynaklardan otomatik doğrulanmamıştır.
- Gerçek rota süresi Google Maps gibi rota API'leriyle hesaplanmamaktadır.
- Kullanıcı profili şu an script içinden test edilmektedir.

## V2 Planı

- Yeni şehirlerin eklenmesi
- Şehir bağımsız veri pipeline yapısı
- Frontend form üzerinden kullanıcı tercihleri alma
- MySQL veritabanı entegrasyonu
- Google Places API ile rating, yorum sayısı ve opening hours verisi alma
- Daha gelişmiş rota optimizasyonu



\## V2 — Kişiselleştirilmiş Öneri Modeli ve Gezi Planlama Motoru



V2 sürümünde Roma lokasyonları için kişiselleştirilmiş bir makine öğrenmesi öneri sistemi, saatlik gezi planlama motoru ve FastAPI servis katmanı geliştirilmiştir.



\### V2 Özellikleri



\* Kullanıcı tercihlerine göre 40 Roma lokasyonunun puanlanması

\* Her lokasyon için 0–100 arası kişisel uygunluk puanı

\* “Neden önerildi?” açıklamaları

\* Tarih, sanat, müze, mimari, doğa, gastronomi, alışveriş ve fotoğrafçılık ilgi alanları

\* Bütçe, tempo, ziyaret zamanı, hava durumu ve aile tercihlerinin değerlendirilmesi

\* Çok günlük saatlik gezi planı oluşturma

\* Lokasyonlar arası yaklaşık mesafe ve ulaşım süresi hesaplama

\* Toplam giriş ücreti bütçe kontrolü

\* Öğle molası ve günlük lokasyon sınırı

\* CSV ve Excel plan çıktıları

\* FastAPI öneri ve plan endpoint’leri

\* Swagger API dokümantasyonu

\* Otomatik API testleri



\### Kullanılan Teknolojiler



\* Python

\* Pandas

\* NumPy

\* Scikit-learn

\* Gradient Boosting Regressor

\* Joblib

\* FastAPI

\* Uvicorn

\* Pydantic

\* Pytest

\* HTTPX

\* OpenPyXL



\### Proje Yapısı



```text

aiTravelPlanner/

├── api/

│   ├── \_\_init\_\_.py

│   └── main.py

├── datasets/

│   ├── master/

│   ├── processed/

│   │   └── rome\_locations\_ml\_ready.csv

│   └── training/

│       ├── rome\_user\_location\_training.csv

│       └── synthetic\_user\_profiles.csv

├── models/

│   ├── location\_recommender\_v2.joblib

│   ├── feature\_columns.json

│   └── model\_metadata.json

├── reports/

├── scripts/

├── src/

│   ├── \_\_init\_\_.py

│   ├── preprocessing.py

│   ├── feature\_engineering.py

│   ├── generate\_training\_data.py

│   ├── train\_models.py

│   ├── evaluate\_ranking.py

│   ├── predict.py

│   ├── create\_itinerary.py

│   ├── test\_user\_scenarios.py

│   └── test\_itinerary\_scenarios.py

├── tests/

│   ├── \_\_init\_\_.py

│   └── test\_api.py

├── requirements.txt

└── README.md

```



\## Kurulum



Projeyi bilgisayara indirdikten sonra proje klasörüne girin:



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



\## Veri Ön İşleme



Ana Roma veri setini model eğitimine uygun hale getirmek için:



```bash

python src/preprocessing.py

```



Bu işlem aşağıdaki dosyayı oluşturur:



```text

datasets/processed/rome\_locations\_ml\_ready.csv

```



İşlenmiş veri seti:



\* 40 lokasyon

\* 38 model özelliği

\* 0 eksik değer



içermektedir.



\## Eğitim Verisi Oluşturma



Sentetik kullanıcı profilleri ve kullanıcı-lokasyon eşleşmeleri oluşturmak için:



```bash

python src/generate\_training\_data.py

```



Bu işlem:



\* 1.000 sentetik kullanıcı profili

\* Her kullanıcı için 40 lokasyon

\* Toplam 40.000 kullanıcı-lokasyon eşleşmesi



oluşturur.



Çıktılar:



```text

datasets/training/synthetic\_user\_profiles.csv

datasets/training/rome\_user\_location\_training.csv

```



\## Model Eğitimi



Modelleri eğitmek ve karşılaştırmak için:



```bash

python src/train\_models.py

```



Karşılaştırılan modeller:



\* Linear Regression

\* Decision Tree Regressor

\* Random Forest Regressor

\* Gradient Boosting Regressor



Son değerlendirmede en iyi model olarak Gradient Boosting seçilmiştir.



Kaydedilen model:



```text

models/location\_recommender\_v2.joblib

```



Model sonuçları:



```text

reports/model\_comparison.csv

reports/model\_metrics.json

reports/test\_predictions.csv

```



\## Model Değerlendirmesi



Kullanıcı bazlı sıralama performansını değerlendirmek için:



```bash

python src/evaluate\_ranking.py

```



Hesaplanan metrikler:



\* Top-1 doğruluğu

\* Top-3 örtüşmesi

\* Top-5 örtüşmesi

\* Top-10 örtüşmesi

\* NDCG@5

\* NDCG@10

\* MRR



Çıktılar:



```text

reports/ranking\_metrics.json

reports/user\_ranking\_results.csv

reports/sample\_top\_recommendations.csv

```



\## Kullanıcı Senaryosu Testleri



Farklı kullanıcı profillerinin farklı öneriler alıp almadığını test etmek için:



```bash

python src/test\_user\_scenarios.py

```



Test edilen örnek profiller:



\* Tarih ve mimari

\* Müze ve sanat

\* Doğa ve fotoğraf

\* Gastronomi ve akşam

\* Ücretsiz ve düşük bütçe

\* Çocuklu aile

\* Hızlı ilk ziyaret

\* Yavaş ve rahat gezi

\* Yağmurlu hava

\* Alışveriş ve şehir yaşamı



\## Öneri Üretme



Varsayılan kullanıcı profili için öneri üretmek amacıyla:



```bash

python src/predict.py

```



Çıktı:



```text

reports/latest\_recommendations.csv

```



\## Saatlik Gezi Planı Oluşturma



Kullanıcı profiline göre çok günlük saatlik plan oluşturmak için:



```bash

python src/create\_itinerary.py

```



Çıktılar:



```text

reports/latest\_itinerary.csv

reports/latest\_itinerary.xlsx

reports/latest\_itinerary\_skipped.csv

```



Planlama motoru şu koşulları değerlendirir:



\* ML uygunluk puanı

\* Toplam giriş ücreti

\* Günlük başlangıç ve bitiş saati

\* Ziyaret süreleri

\* Lokasyonlar arası yaklaşık mesafe

\* Yaklaşık ulaşım süresi

\* Günlük maksimum lokasyon sayısı

\* Öğle molası

\* Kullanıcı temposu



\## Planlama Senaryosu Testleri



Farklı kullanıcı ve seyahat ayarlarıyla planlama motorunu test etmek için:



```bash

python src/test\_itinerary\_scenarios.py

```



Test edilen senaryolar:



\* Tarih ve mimari

\* Ücretsiz gezi

\* Doğa ve fotoğraf

\* Gastronomi ve akşam

\* Çocuklu aile

\* Hızlı ilk ziyaret



Her senaryo için ayrı CSV ve Excel plan çıktısı oluşturulur.



\## FastAPI Sunucusunu Çalıştırma



API sunucusunu başlatmak için:



```bash

python -m uvicorn api.main:app --reload

```



Sunucu varsayılan olarak şu adreste çalışır:



```text

http://127.0.0.1:8000

```



Swagger dokümantasyonu:



```text

http://127.0.0.1:8000/docs

```



API sağlık kontrolü:



```text

GET /api/health

```



Öneri endpoint’i:



```text

POST /api/recommendations

```



Saatlik gezi planı endpoint’i:



```text

POST /api/itineraries

```



\## API Testleri



Otomatik testleri çalıştırmak için:



```bash

python -m pytest tests/test\_api.py -v

```



Mevcut test kapsamı:



\* Ana endpoint

\* Sağlık kontrolü

\* Öneri endpoint’i

\* Öneri sayısı doğrulaması

\* İlgi puanı doğrulaması

\* Çok günlük plan endpoint’i

\* Sıfır bütçeli plan

\* Saat formatı doğrulaması

\* Seyahat günü doğrulaması



Mevcut sonuç:



```text

9 passed

```



\## Mevcut Kısıtlamalar



\* Açılış ve kapanış saatleri henüz doğrulanmış gerçek verilerle kontrol edilmemektedir.

\* Ulaşım süreleri gerçek yol servisi yerine Haversine mesafesi üzerinden yaklaşık hesaplanmaktadır.

\* Her günün ilk lokasyonuna konaklama noktasından ulaşım, başlangıç koordinatı verilmezse hesaplanmamaktadır.

\* Eğitim verileri başlangıç aşamasında sentetik kullanıcı profillerinden oluşturulmuştur.

\* Gerçek kullanıcı geri bildirimleri toplandığında model yeniden eğitilmelidir.

\* Gastronomi ve alışveriş lokasyonlarının veri çeşitliliği artırılmalıdır.



\## V2 Sonucu



V2 sonunda sistem:



1\. Kullanıcı tercihlerini alır.

2\. Roma’daki 40 lokasyonu kişisel olarak puanlar.

3\. En uygun lokasyonları sıralar.

4\. Her öneri için açıklama üretir.

5\. Bütçe ve zaman koşullarını kontrol eder.

6\. Yakın lokasyonları rota mantığıyla sıralar.

7\. Saatlik ve çok günlük gezi planı oluşturur.

8\. Sonuçları JSON, CSV ve Excel biçimlerinde sunar.



