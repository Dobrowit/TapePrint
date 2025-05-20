# TapePrint
Drukowanie etykiet z pliku .txt na drukarce ZEBRA.

Plik tekstowy musi zawierać po jednej linijce tekstu na etykietę. Przydatne przy inwentaryzacji - drukujesz oznaczenia i naklejasz na sprzęty.

Etykiety drukowane są za pomocą języka [ZPL](https://en.wikipedia.org/wiki/Zebra_Programming_Language).

Wygląd etykiet można modyfikować zmieniając funkcję generuj_zpl_tekst(). Przy tym może być pomocny [edytor](https://labelary.com/viewer.html).
```
usage: TapePrint.py [-h] [-d DRUKARKA] [-f PLIK] [-k] [-K] [-r] [-n N] [-t] [-g]

Drukowanie etykiet z pliku .txt na drukarce Zebra

options:
  -h, --help                        Pomocna ściąga
  -d DRUKARKA, --drukarka DRUKARKA  Nazwa drukarki
  -f PLIK, --plik PLIK              Ścieżka do pliku .txt z numerami
  -k, --obcinaj_kazda               Włącz obcinanie każdej etykiety
  -K, --obcinaj_na_koncu            Odetnij po zakończeniu druku
  -r, --odwrotnie                   Drukuj etykiety w odwrotnej kolejności
  -n N, --co_ile_obcinac N          Obcinanie co N etykiet (domyślnie 100)
  -t, --test                        Test bez wydruku
  -g, --no_gui                      Wyłączenie dialogów GUI
```
