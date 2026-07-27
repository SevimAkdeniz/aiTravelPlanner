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
