powershell -Command "Set-Content -Path README.md -Encoding UTF8 -Value @'

\# AI Travel Planner V1



AI Travel Planner, kullanici tercihlerini dikkate alarak kisisellestirilmis seyahat onerileri ve gunluk gezi plani olusturan bir seyahat planlama prototipidir.



V1 surumunde sistem Roma sehri uzerinde gelistirilmistir. Kullanicinin ilgi alani, butcesi, seyahat temposu ve gunluk zaman araligina gore lokasyonlar skorlanir ve saatli gezi plani olusturulur.



\## V1 Kapsami



\- Roma icin 40 turistik lokasyonluk veri seti olusturuldu.

\- OpenTripMap API ile lokasyon verileri cekildi.

\- OpenTripMap verileri master lokasyon listesiyle eslestirildi.

\- Eksik lokasyonlar Wikidata ve manuel veri ile tamamlandi.

\- Planlama icin kategori, sure, ucret, ilgi skorlari ve area group kolonlari eklendi.

\- Veri kaynaklari ve guven seviyesi icin confidence kolonlari eklendi.

\- Kullanici profiline gore suitability score hesaplandi.

\- Farkli kullanici profilleriyle test yapildi.

\- Roma icin 3 gunluk saatli ornek gezi plani uretildi.



\## Kullanilan Veri Kaynaklari



\- OpenTripMap API

\- Wikidata

\- Manual V1 Feature Engineering



Lokasyon kimligi, koordinatlar ve kaynak ID bilgileri OpenTripMap ve Wikidata uzerinden olusturulmustur.



Sure, ucret ve ilgi skorlari V1 prototip icin kural tabanli baslangic degerleri olarak atanmistir. Bu alanlar sonraki surumlerde resmi web siteleri, Google Places API ve kullanici geri bildirimleri ile gelistirilecektir.



\## Proje Klasor Yapisi



datasets/

&#x20; raw/

&#x20;   rome/

&#x20;     opentripmap\_rome\_raw.csv



&#x20; master/

&#x20;   rome/

&#x20;     rome\_master\_dataset\_v1.csv

&#x20;     rome\_master\_dataset\_v1.xlsx



&#x20; outputs/

&#x20;   scores/

&#x20;     rome\_location\_scores\_history\_architecture\_user.csv

&#x20;     rome\_location\_scores\_art\_museum\_user.csv

&#x20;     rome\_location\_scores\_food\_evening\_user.csv

&#x20;     rome\_location\_scores\_nature\_slow\_user.csv

&#x20;     rome\_location\_scores\_low\_budget\_fast\_user.csv

&#x20;     rome\_location\_scores\_profile\_comparison.csv



&#x20;   itineraries/

&#x20;     rome\_sample\_itinerary.csv

&#x20;     rome\_sample\_itinerary.xlsx



&#x20; archive/

&#x20;   rome/

&#x20;     intermediate files



scripts/

&#x20; fetch\_opentripmap\_rome.py

&#x20; create\_rome\_40\_master\_list.py

&#x20; enrich\_master\_with\_opentripmap.py

&#x20; fetch\_missing\_opentripmap\_by\_name.py

&#x20; complete\_manual\_locations.py

&#x20; add\_planning\_features.py

&#x20; add\_data\_confidence.py

&#x20; score\_locations.py

&#x20; add\_area\_groups.py

&#x20; create\_sample\_itinerary.py



\## Ana Dataset



Final V1 ana dataset dosyasi:



datasets/master/rome/rome\_master\_dataset\_v1.csv



Bu dosya Roma icin 40 lokasyon icerir.



Ana dataset icinde su veri gruplari bulunur:



\- Lokasyon adi

\- Sehir ve ulke bilgisi

\- Koordinatlar

\- OpenTripMap ve Wikidata ID bilgileri

\- Kategori ve alt kategori

\- Ortalama ziyaret suresi

\- Giris ucreti

\- Butce seviyesi

\- Ilgi skorlari

\- Turistik onem skoru

\- Hava durumu uygunlugu

\- Veri kaynagi ve guven seviyesi



\## Suitability Score Mantigi



Sistem her lokasyon icin kullanicinin profiline gore 0-100 arasinda uygunluk skoru hesaplar.



V1 formulunde kullanilan bilesenler:



\- Interest match score

\- Importance score

\- Budget match score

\- Time match score

\- Tempo match score

\- Weather match score



Formul:



suitability\_score =

interest\_match \* 0.35

\+ importance\_score \* 0.25

\+ budget\_match \* 0.15

\+ time\_match \* 0.10

\+ tempo\_match \* 0.10

\+ weather\_match \* 0.05



\## Test Edilen Kullanici Profilleri



\- history\_architecture\_user

\- art\_museum\_user

\- food\_evening\_user

\- nature\_slow\_user

\- low\_budget\_fast\_user



Profil skor ciktilari su klasordedir:



datasets/outputs/scores/



\## Ornek Gezi Plani



Final itinerary dosyasi:



datasets/outputs/itineraries/rome\_sample\_itinerary.csv



Ornek rota:



1\. Gun - Vatican Area

\- Vatican Museums

\- Sistine Chapel

\- St. Peter's Basilica

\- Castel Sant'Angelo



2\. Gun - Ancient Rome

\- Colosseum

\- Roman Forum

\- Palatine Hill

\- Altare della Patria



3\. Gun - Historic Center + Trastevere

\- Pantheon

\- Piazza Navona

\- Trevi Fountain

\- Piazza del Popolo

\- Trastevere



\## Script Calistirma Sirasi



1\. python scripts/fetch\_opentripmap\_rome.py

2\. python scripts/create\_rome\_40\_master\_list.py

3\. python scripts/enrich\_master\_with\_opentripmap.py

4\. python scripts/fetch\_missing\_opentripmap\_by\_name.py

5\. python scripts/complete\_manual\_locations.py

6\. python scripts/add\_planning\_features.py

7\. python scripts/add\_data\_confidence.py

8\. python scripts/score\_locations.py

9\. python scripts/add\_area\_groups.py

10\. python scripts/create\_sample\_itinerary.py



\## Ortam Degiskenleri



OpenTripMap API anahtari .env dosyasinda tutulur.



OPENTRIPMAP\_API\_KEY=your\_api\_key\_here



.env dosyasi GitHub'a yuklenmemelidir.



\## V1 Limitasyonlari



\- Sadece Roma sehri desteklenmektedir.

\- Bazi planlama feature degerleri kural tabanlidir.

\- Giris ucretleri ve ziyaret sureleri V1 draft degerleridir.

\- Acilis ve kapanis saatleri henuz resmi kaynaklardan otomatik dogrulanmamistir.

\- Gercek rota suresi Google Maps gibi rota API'leriyle hesaplanmamaktadir.

\- Kullanici profili su an script icinden test edilmektedir.



\## V2 Plani



\- Yeni sehirlerin eklenmesi

\- Sehir bagimsiz veri pipeline yapisi

\- Frontend form uzerinden kullanici tercihleri alma

\- MySQL veritabani entegrasyonu

\- Google Places API ile rating, yorum sayisi ve opening hours verisi alma

\- Daha gelismis rota optimizasyonu

'@"

