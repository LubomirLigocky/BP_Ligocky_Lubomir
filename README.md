# BP_Ligocky_Lubomir
kompletný zdrojový kód programu implementácie multimodálnej LLM do robota NAO

Časti, ktoré sú označené DP_Imrich_discantiny sú hlavný zdroj a východiskový bod mojej práce. Je tam zahrnutá celá logika cvičenia s robotom bez verbálnej interakcie - pevné stanovené hlášky a cvičenia.
Sekundárny zdroj praktickej časti mojej práce sa nachádza na tomto github repozitári https://github.com/jperdek/dpImrichSetup/tree/exerciseApiCreation, kde sú pridané už aj pokročilejšie cvičenia a celkovo sú lepšie ošetrené pohyby robota.

# Inštalácia
Vzhľadom na špecifiká robota NAO vyžaduje projekt dve oddelené prostredia.

1. Riadiaca aplikácia (PC - Python 3.10+)
Toto prostredie slúži na spustenie hlavného rozhrania app.py.

Klonovanie repozitára
git clone https://github.com/LubomirLigocky/BP_Ligocky_Lubomir.git

cd BP_Ligocky_Lubomir

Vytvorenie virtuálneho prostredia
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

Inštalácia závislostí
pip install -r requirements.txt
Poznámka: Pre prácu so zvukom (PyAudio) na Windows môže byť potrebné nainštalovať pipwin install pyaudio.

2. Robotický modul (NAO - Python 2.7)
Súbor _robot_app.py musí bežať v prostredí s nainštalovaným NAOqi SDK.
Vyžaduje Python 2.7.

Musí byť zabezpečená sieťová viditeľnosť medzi PC a robotom.

# Spustenie
Najskôr spustite skript na strane robota (Python 2.7 prostredie) a následne hlavnú aplikáciu(uistite sa pritom že sa nachádzate v správnych adresároch):
- v podadresári \robot\robot    "C:\Python27\python.exe"_robot_app.py
- v podadresári \trainer        python app.py

# Kalibrácia senzorov 
Počkajte na inicializáciu kamery. Uistite sa, že sa nachádzate v zornom poli kamery (vzdialenosť cca 2,5 metra).

# Interakcia 
Akonáhle sa na obrazovke zobrazí rozhranie GUI, je to znak toho, že systém je aktívny. Hlasová komunikácia s robotom je možná okamžite. Cvičenie sa začína, keď dáte robotovi povel tým, že stlačíte niektoré z tlačidiel v GUI rozhraní.
POZOR: robot nemá funkciu barge-in, nefunguje prerušenie reči. Ak robot rozpráva, nepočúva, čo mu hovoríte vy.

# Riešenie problémov
- Robot nereaguje na hlas: Skontrolujte stav nabitia mikrofónu DJI Mic a overte, či je v systéme nastavený ako predvolené vstupné zariadenie.
- Chyba pripojenia (Connection Timeout): Overte, či nedošlo k zmene IP adresy robota (možno zistiť stlačením tlačidla na hrudi robota).
- Nízka snímková frekvencia (FPS): Uistite sa, že počítač je pripojený k napájaniu a grafická karta spracováva hĺbkovú mapu z kamery RealSense. Zároveň sa uistite, že kamera je k počítaču pripojená prostredníctvom vysokorýchlostného portu USB 3.0 (typ A alebo C), ktorý je nevyhnutný pre dostatočnú priepustnosť dát.

  Počas behu programu je takisto potrebné mať pripojenú k PC externú kameru(schopnú hĺbkového snímania) a ideálne aj externý mikrofón(za predpokladu že mikrofón vstavaný do PC nie je požadovanej kvality)
