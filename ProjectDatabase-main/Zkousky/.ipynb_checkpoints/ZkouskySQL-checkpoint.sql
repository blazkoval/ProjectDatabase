CREATE TABLE "Zkouska" (
  "id_zkousky" int PRIMARY KEY,
  "id_predmetu" int,
  "jmeno_zkousky" varchar,
  "id_zkousejiciho" int,
  "datum_zkousky" datetime,
  "max_kapacita" int,
  "prihlaseni_studenti" varchar,
  "poznamka" varchar
);

CREATE TABLE "Uzivatel" (
  "id_uzivatele" int PRIMARY KEY,
  "id_studijni_skupiny" int,
  "id_opravneni" int,
  "jmeno" varchar,
  "prijmeni" varchar,
  "titul" varchar,
  "email" varchar,
  "tel_cislo" varchar
);

CREATE TABLE "Zkouska_Zkousejici" (
  "id_zkousky" int,
  "id_zkousejiciho" int,
  PRIMARY KEY ("id_zkousky", "id_zkousejiciho")
);

CREATE TABLE "Zkouska_Student" (
  "id_zkousky" int,
  "id_studenta" int,
  PRIMARY KEY ("id_zkousky", "id_studenta")
);

CREATE TABLE "Opravneni" (
  "id_opravneni" int PRIMARY KEY,
  "web_admin" bool,
  "student" bool,
  "zkousejici" bool
);

CREATE TABLE "Studijni_skupina" (
  "id_studijni_skupiny" int PRIMARY KEY,
  "jmeno" varchar
);

CREATE TABLE "Predmet" (
  "id_predmetu" int PRIMARY KEY,
  "id_studijni_skupiny" int,
  "jmeno" varchar
);

CREATE TABLE "Studijni_skupina_Predmet" (
  "id_predmetu" int,
  "id_studijni_skupiny" int,
  PRIMARY KEY ("id_predmetu", "id_studijni_skupiny")
);

ALTER TABLE "Zkouska_Student" ADD FOREIGN KEY ("id_zkousky") REFERENCES "Zkouska" ("prihlaseni_studenti");

ALTER TABLE "Zkouska_Zkousejici" ADD FOREIGN KEY ("id_zkousky") REFERENCES "Zkouska" ("id_zkousejiciho");

ALTER TABLE "Zkouska_Zkousejici" ADD FOREIGN KEY ("id_zkousejiciho") REFERENCES "Uzivatel" ("id_uzivatele");

ALTER TABLE "Zkouska_Student" ADD FOREIGN KEY ("id_studenta") REFERENCES "Uzivatel" ("id_uzivatele");

ALTER TABLE "Uzivatel" ADD FOREIGN KEY ("id_opravneni") REFERENCES "Opravneni" ("id_opravneni");

ALTER TABLE "Uzivatel" ADD FOREIGN KEY ("id_studijni_skupiny") REFERENCES "Studijni_skupina" ("id_studijni_skupiny");

ALTER TABLE "Zkouska" ADD FOREIGN KEY ("id_predmetu") REFERENCES "Predmet" ("id_predmetu");

ALTER TABLE "Studijni_skupina_Predmet" ADD FOREIGN KEY ("id_predmetu") REFERENCES "Predmet" ("id_studijni_skupiny");

ALTER TABLE "Studijni_skupina_Predmet" ADD FOREIGN KEY ("id_studijni_skupiny") REFERENCES "Studijni_skupina" ("id_studijni_skupiny");
