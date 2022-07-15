# ProjectDatabase
Zpracovali: des. Lenka Blažková a des. Filip Raczek

## Zadání číslo 2
Definujte datové struktury (PostgreSQL + SQLAlchemy) pro ukládání dostupných (vypsaných) termínů ke zkoušce (zápočtu, či jiné formy zkoušky). Využijte již definovaných modelů. Připravte API (GraphQL).
## Postup
### grafické zpracování struktur
##### [grafické schéma](ProjectDatabase-main/schematabulek.pdf)
Pomocí stránky dbdiagram.io (https://dbdiagram.io/home) jsme si vytvořili vizualizaci datových strukutr. Definovali jsme si hlavní tabulky: Predmet, Zkouska, Studijni_skupina, Uzivatel, Opravneni. Mezi tabulkami, které mají mezi sebou vztah M:N, jsme vytvořili dodatečné tabulky, které nesou pouze primární klíče hlavních tabulek. 
### definování struktur
##### [SQLAlchemy](ProjectDatabase-main/Zkousky/mainjl.ipynb#SQLAlchemy)
Vytvořili jsme modely datových entit za využití SQLAlchemy knihovny. Hlavní tabulky jsou deklarovány jako třídy (class), mezitabulky jsou vytvořeny pomocí funkce Table. Původně vytvářeno jako main.py (ve VisualStudio Code), ale kvůli problému s porpojením s Postgresem vytvářeno jako notebook mainjl.ipynb (v JupyterLabu)
### testování
Abych zjistila, jestli mám tabulky správně definované, tak jsem si nejprve nahrála data na server. Propojení databáze se serverem jsem vytvořila pomocí connectionstringu. Naplnila jsem struktury náhodnými daty. K tomu jsem využila CRUD ops. V pgAdminu se mi poté zobrazily jednotlivé entity, které jsem nahrála. Tím se ověřila správnost definování struktur.
### navázání na databázové záznamy
#### [GraphQL](ProjectDatabase-main/Zkousky/mainjl.ipynb#GraphQL)
V GrapgQL jsem si znovu nadefinovala modely, které navazují na datové struktury v SQLAlchemy. Díky tomu lze databázi spustit v aplikaci GraphiQL. Zde je možnost číst záznamy v databázy.
### kontejnerizace
Posledním krokem bylo vytvořit program, izolovat aplikace se všemi knihovnamy do kontejnerů. 
