# Szöuli kerékpárkölcsönzés · adatvizualizációs workshop

Futtatható Python-kezdőprojekt. A dashboard az előkészített adatokat kapja meg,
és négy kitöltendő panelt jelenít meg. A panelek és a szűrők helyét az
`app.py` fájlban a `TODO` megjegyzések jelölik.

## Indítás PyCharmból

1. Csomagold ki a ZIP-et, majd a PyCharm **File → Open** menüjében nyisd meg
   a `bike_sharing_workshop` mappát.
2. Ha a PyCharm interpretert kér, válaszd ki a gépeden telepített **Python 3.12**-t.
3. A felső futtatási listából válaszd a **Workshop dashboard** konfigurációt,
   majd kattints a zöld **Run ▶** gombra.

Az első futtatás létrehozza a projekt saját `.venv` környezetét, és telepíti
a mellékelt követelménylistában szereplő csomagokat. Ehhez internetkapcsolat
szükséges. Az indítás után a dashboard megnyílik a böngészőben. A pontos helyi
címet a PyCharm **Run** panelje is kiírja.

A PyCharm **Stop ■** gombjával leállíthatod a dashboardot. A következő
indítás a meglévő környezetet használja.

## Hol dolgozz?

| Fájl | Szerep |
| --- | --- |
| `run_workshop.py` | A PyCharm futtatási beállításának indítója. Előkészíti a helyi környezetet és elindítja az alkalmazást. |
| `app.py` | A dashboard váza, a szűrők helye és a négy kitöltendő panel. Az előkészített DataFrame a `data` változóban érhető el. |
| `data_preparation.py` | A CSV beolvasása, az adattípusok beállítása és a naptári mezők képzése. |
| `data/SeoulBikeData.csv` | Az eredeti UCI-adatfájl, változatlan formában. |
| `requirements.txt` | A futtatáshoz szükséges csomagok és a vizualizációhoz használható Plotly. |

A workshopmunka a diagramok megtervezése, az adatok kérdéshez illő
csoportosítása és a szűrők, illetve a kijelölések bekötése.

## Az előkészített adatok

A CSV egy sora Szöul városi kerékpárkölcsönzési rendszerének egy óráját írja le.
A teljes állomány 8 760 megfigyelést tartalmaz 2017. december 1. és
2018. november 30. között. A betöltő az eredeti fájlt CP1252 kódolással
olvassa, a dátumot nap/hónap/év formátumban értelmezi, és időrendbe teszi
a rekordokat.

| Mezők | Jelentés |
| --- | --- |
| `timestamp`, `date`, `hour` | Az órai időbélyeg, a nap dátuma és a 0–23 közötti óra. Az időbélyeg az eredeti szöuli helyi időt követi. |
| `weekday`, `is_weekend`, `month` | A hét napja hétfőtől vasárnapig, hétvégejelző és a hónap első napja. |
| `rentals` | Az adott órában rögzített kölcsönzések száma. |
| `season`, `is_holiday`, `is_operating` | Évszak, ünnepnapjelző és üzemelési jelző. Az ünnepnap és a hétvége külön változó. |
| `temperature_c`, `humidity_pct`, `wind_speed_m_s`, `visibility_10m` | Hőmérséklet, relatív páratartalom, szélsebesség és látótávolság 10 méteres egységekben. |
| `dew_point_c`, `solar_radiation_mj_m2`, `rainfall_mm`, `snowfall_cm` | Harmatpont, napsugárzás, eső és havazás. A mértékegységet az oszlopnév tartalmazza. |

Az üzemen kívüli órák is bekerülnek a DataFrame-be a forrásban szereplő nulla
kölcsönzéssel. Ha az üzemelő szolgáltatás kölcsönzésszáma érdekel, az
`is_operating` mezővel szűkítsd a vizsgált órákat.

## Adatforrás

Easwaramoorthy, S. (2020). *Seoul Bike Sharing Demand* [adatkészlet].
UCI Machine Learning Repository. [DOI 10.24432/C5F62R](https://doi.org/10.24432/C5F62R).
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
