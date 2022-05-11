# ProjectDatabase
Zpracovali: des. Lenka Blažková a des. Filip Raczek

## Zadání číslo 2
Definujte datové struktury (PostgreSQL + SQLAlchemy) pro ukládání dostupných (vypsaných) termínů ke zkoušce (zápočtu, či jiné formy zkoušky). Využijte již definovaných modelů. Připravte API (GraphQL).
## Postup
### grafické zpracování struktur
schematabulek.pdf (odkaz)
Pomocí stránky dbdiagram.io (https://dbdiagram.io/home) jsme si vytvořili vizualizaci datových strukutr. Definovali jsme si hlavní tabulky: Predmet, Zkouska, Studijni_skupina, Uzivatel, Opravneni. Mezi tabulkami, které mají mezi sebou vztah N:N, jsme vytvořili dodatečné tabulky, které nesou pouze primární klíče hlavních tabulek. 
### definování struktur
Vytvořili jsme modely datových entit za využití SQLAlchemy knihovny. Hlavní tabulky jsou deklarovány jako třídy (class), mezitabulky jsou vytvořeny pomocí funkce Table
### testování
Abych zjistila, jsetli mám tabulky správně definované, tak jsem si nejprve nahrála data na server. Pro propojení databáze se serverem jsem vytvořila pomocí connectionstringu. Naplnila jsem struktury náhodnými daty. K tomu jsem využila CRUD ops. V pgAdminu se mi poté zobrazily jednotlivé entity, které jsem nahrála. Tím se ověřila správnost definování struktur.
### navázání na databázové záznamy
-znovu vytváření struktur pro GraphQL, jak se definují vztahy? jak nahlédnout? explicitní/implicitní resolvery

#### Budoucí termíny
- 	8. 6. 2022 projektový den
- 	30. 6. 2022 uzavření projektu


