Ez a fájlrendező alkalmazás lehetővé teszi, hogy különböző kiterjesztésű fájlokat mappákba rendszerezzen. 
Támogatja a Windows rendszereket, logolja a műveleteket, és egy GUI felületen keresztül vezérelhető.

Fő funkciói:
  Kiterjesztés alapú fájlrendezés:
    Áthelyezi a kiválasztott kiterjesztésű fájlokat egy külön almappába a megadott cél mappán belül.
  Logolás:
    Létrehoz dátummal és pontos idővel ellátott logfájlt a cél almappában.
    Naplózza a mozgatott fájlokat, futásidőt és a művelet kezdési idejét.
    A log tartalmazza:
    
      PID (a futó Python folyamat azonosítója)
    
      Felhasználónév
      
      A művelet kezdési ideje
      
      Forrás és cél mappa
      
      Áthelyezett fájlok listája
      
      Futásidő
        A log minden futtatás után automatikusan létrejön a cél almappában (a megadott kiterjesztés mappán belül).
  Fájlnév-ütközés kezelése:
    Ha már létezik az adott fájlnév a cél mappában, a program automatikusan sorszámozással hoz létre egyedi nevű másolatot (pl. file_1.pdf).
  GUI:
    Forrás mappa tallózása
    Cél mappa tallózása
    Kiterjesztés megadása
    „Rendezés”, „Log megnyitása” és „Kilépés” gombok
    Állapotjelző sáv a folyamat közbeni és utáni visszajelzéshez

Fájlok
  main.py – a program indító fájlja
  gui.py – a felhasználói felület kezelése
  file_manager.py – a fájlrendezés és logolás végrehajtása

GUI működés
  Forrás mappa tallózása: Kiválasztod a mappát, ahonnan a fájlokat áthelyezed.
  Cél mappa tallózása: Ide kerül az almappa, ahová a fájlok kerülnek.
  Kiterjesztés: Add meg a rendezendő fájlok kiterjesztését (pl. pdf, jpg, txt).
  Rendezés gomb: Elindítja a fájlmozgatást és a log létrehozását.
  Log megnyitása gomb: Megnyitja a legutolsó log fájlt Jegyzettömbben (Windows).
  Kilépés gomb: Bezárja az alkalmazást.

Követelmények
  Python 3.x
  Windows (a os.startfile() miatt)
  Nem igényel külső csomagokat
