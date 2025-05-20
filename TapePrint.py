#!/usr/bin/python3

import tempfile
import os
import win32print
import tkinter as tk
from tkinter import filedialog, messagebox
import argparse

# 🎛️ Argumenty wiersza poleceń
parser = argparse.ArgumentParser(
    description="Drukowanie etykiet z pliku .txt na drukarce Zebra",
    formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40)
)
parser.add_argument("-d", "--drukarka", help="Nazwa drukarki", default="ZEBRA")
parser.add_argument("-f", "--plik", help="Ścieżka do pliku .txt z numerami")
parser.add_argument("-k", "--obcinaj_kazda", action="store_true", help="Włącz obcinanie każdej etykiety")
parser.add_argument("-K", "--obcinaj_na_koncu", action="store_true", help="Odetnij po zakończeniu druku")
parser.add_argument("-r", "--odwrotnie", action="store_true", help="Drukuj etykiety w odwrotnej kolejności")
parser.add_argument("-n", "--co_ile_obcinac", metavar="N", type=int, default=100, help="Obcinanie co N etykiet (domyślnie 100)")
parser.add_argument("-t", "--test", action="store_true", help="Test bez wydruku")
parser.add_argument("-g", "--no_gui", action="store_true", help="Wyłączenie dialogów GUI")
args = parser.parse_args()

ZEBRA_PRINTER_NAME = args.drukarka
OBCINAJ_KAZDA = args.obcinaj_kazda
OBCINAJ_NA_KONCU = args.obcinaj_na_koncu
ODWROTNIE = args.odwrotnie
CO_ILE_OBCINAC = args.co_ile_obcinac
TEST = args.test
NO_GUI = args.no_gui

# 🖨️ Funkcja generująca kod ZPL z tekstem

def generuj_zpl_tekst(tekst, z_obcieciem=False):
    tryb = "^MMC" if z_obcieciem else "^MMT"
    return f"""
^XA
{tryb}
^CI28
^FO50,50
^A0N,50,50
^FD{tekst}^FS
^XZ
"""

def main():
    # 📂 Wybór pliku TXT
    plik_txt = args.plik
    if not plik_txt:
        if not NO_GUI:
            root = tk.Tk()
            root.withdraw()
            plik_txt = filedialog.askopenfilename(
                title="Wybierz plik z numerami inwentarzowymi",
                filetypes=[("Pliki tekstowe", "*.txt")]
            )
        if not plik_txt:
            if not NO_GUI:
                messagebox.showwarning("Brak pliku", "Nie wybrano żadnego pliku. Zamykanie programu.")
            exit(1)

    # 📤 Przetwarzanie i drukowanie
    with open(plik_txt, encoding='utf-8') as file:
        linie = [line.strip() for line in file if line.strip()] # Pomijanie pustych linii
        print(f"Ilość etykiet do wydruku: {len(linie)}")

    if len(linie) > 0:
        if not NO_GUI:
            root = tk.Tk()
            root.withdraw()
            if not messagebox.askokcancel("Ostrzeżenie", f"Plik zawiera {len(linie)} etykiet. Czy kontynuować drukowanie?"):
                print("Drukowanie przerwane przez użytkownika.")
                exit(0)

    if ODWROTNIE:
        linie.reverse()

    for i, tekst in enumerate(linie):
        ostatni = (i == len(linie) - 1) and OBCINAJ_NA_KONCU
        z_obcieciem = OBCINAJ_KAZDA or ostatni or ((CO_ILE_OBCINAC > 0) and ((i + 1) % CO_ILE_OBCINAC == 0))
        zpl = generuj_zpl_tekst(tekst, z_obcieciem=z_obcieciem)

        # Zapisz ZPL do pliku tymczasowego (opcjonalnie)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zpl", mode='w', encoding='utf-8') as tmp:
            tmp.write(zpl)
            tmp_path = tmp.name

        # Bezpośredni wydruk do drukarki Zebra
        if not TEST:
            try:
                hPrinter = win32print.OpenPrinter(ZEBRA_PRINTER_NAME)
            except Exception as e:
                print(f"Błąd podczas otwierania drukarki '{ZEBRA_PRINTER_NAME}': {e}")
                exit(1)

            try:
                hJob = win32print.StartDocPrinter(hPrinter, 1, ("Etykieta", None, "RAW"))
                win32print.StartPagePrinter(hPrinter)
                win32print.WritePrinter(hPrinter, zpl.encode('utf-8'))
                win32print.EndPagePrinter(hPrinter)
                win32print.EndDocPrinter(hPrinter)
            finally:
                win32print.ClosePrinter(hPrinter)
            print(f"[{i+1}/{len(linie)}] Wysłano do drukarki: {tekst}")
        else:
            print(f"[{i+1}/{len(linie)}] Wysłano do drukarki: {tekst}")
            print(f"ostatni:{ostatni}")
            print(f"z_obcieciem:{z_obcieciem}")
            print("ZPL:", zpl.strip())

        # Czyszczenie pliku tymczasowego
        try:
            os.remove(tmp_path)
        except Exception as e:
            print(f"Nie udało się usunąć pliku tymczasowego: {tmp_path} ({e})")
            
    print("Wszystkie napisy zostały wydrukowane.")

if __name__ == "__main__":
    main()