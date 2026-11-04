# Testplan


Eine bereits eingelesene Wettermessung wird als Tupel dargestellt:

```python
(city, time, temperature)
```

Beispiel:

```python
("Köln", 861, 21.7)
```

- `city` ist ein String.
- `time` ist die Anzahl der Minuten seit Mitternacht.
- `temperature` ist die Temperatur in Grad Celsius als `float`.


- time sind Minuten als ganze Zahl: parse_time ist int
Möglicher Fehler: str oder float wird zurückgegeben

- temp ist float
Möglicher Fehler: wird zu str oder nur als int (und nicht als float möglich)

## parse_time

- Umrechnung in Minuten, Mögliche Fehler: Falsche Formel, Stunden und Minuten vertauscht (?)

Grenzwerte:

- Mögliche Uhrzeiten: 
    - Stunde 0 bis 23 möglich (also 23:59 --> 1439), Mögliche Fehler: 23 wird abgelehnt
    - Stunde 24 nicht möglich (also 1440), Mögliche Fehler: 24 wird erlaubt (und ergibt 1440)
    - Minute 60 nicht möglich (also ab:60), Mögliche Fehler: die 60 wird erlaubt und einberechnet
    - Wenn es 0 ist insgesamt möglich (also 00:00), Mögliche Fehler: Die 0 wird abgelehnt 
    - Führende Nullen sind optional (also 9:5), Mögliche Fehler: wird Value Error statt zusammengerechnet
    - Form ist 00:00, Mögliche Fehler: Falsche Anzahl an Doppelpunkten und Stellen wird verwendet o.ä.

Spezialfälle:

Generell:
    - Stunde muss Zahl sein vor dem Zusammenrechnen, Möglicher Fehler: ist keine Zahl, rechnet trotzdem zusammen
    - Minute muss Zahl sein vor dem Zusammenrechnen, Möglicher Fehler: ist keine Zahl, rechnet trotzdem zusammen

Ungültiger Wert:
    - Ungültig wäre: Stunde fehlt (Feld leer), Möglicher Fehler: wird trotzdem gerechnet 
    - Ungültig wäre: Minute fehlt (Feld leer), Möglicher Fehler: wird trotzdem gerechnet
    - Ungültig: Komplett Leerer Text (nur ":" oder " "), Möglicher Fehler: Rechnet mit 0 oder stürzt ab

## parse_measurement

Regelfall: Normal ist richtige Reihenfolge und richtig umgewandelt ("Köln", 861, 21.7)

Grenzwerte:
    - Extrem hohe Temperatur, Mögliche Fehler: Value Error statt richtige Tenperatur (z.B. 100.0)
    - Extrem niedrige Temperatur, Mögliche Fehler: Value Error statt Übertragung (z.B. -90.0)
    

Spezialfälle:

    - Leerzeichen um die Stadt, Möglicher Fehler: Stadt wird nicht bereinigt und Leerzeichen bleiben
    - Leerzeichen um die Uhrzeit, Möglicher Fehler: wird nicht bereinigt, führt zu Value Error
    - Leerzeichen IN der Stadt, Möglicher Fehler: werden entfernt 
    - Uhrzeit wird nicht mit parse_time geprüft, Möglicher Fehler: rechnet weiter, statt Value Error
    - Uhrzeit ohne Nullen, Möglicher Fehler: Value Error statt Nullen umgewandelt
    - Negative Temperatur, Mögliche Fehler: Minuszeichen wird nicht akzeptiert führt zu Value Error


Ungültige Werte:

    - Zahl statt Text, Möglicher Fehler: wird als Attribute Error ausgegeben (Value Error wäre richtig)
    - Fehlender Wert (None statt Text), Möglicher Fehler: Attribute Error statt Value Error
    - vier Felder statt drei, Möglicher Fehler: liefert die drei Felder statt direkt Value Error
    - zwei Felder statt drei, Möglicher Fehler: Fehlendes Feld führt zu IndexError statt Value Error
    - Stadt ist leer, Möglicher Fehler: Arbeitet mit leerem Feld statt Value Error
    - Stadt aus (mehreren) Leerzeichen, Möglicher Fehler: Leere Stadt statt Value Error
    - Temperatur als Text, Mögliche Fehler: return ist 0.0 oder sowas
    - Temperatur fehlt, Mögliche Fehler: wird mit 0 oder sowas ersetzt statt Value Error


###Ob die Leerzeichen um die Temperatur entfernt werden, kann man nicht testen. float(" 21.7 ") ignoriert Leerzeichen sowieso, also verhält sich kaputter Code dort genau wie richtiger Code.

## filter_by_temperature

- Normaler Bereich (?) wird gefiltert

Grenzwerte:

    - Untere Grenze gehört dazu, Mögliche Fehler: wird rausgefiltert statt mitgenommen
    - Obere Grenze gehört dazu, Mögliche Fehler: wird rausgefiltert statt mitgenommen
    - Knapp drunter oder drüber gehört nicht dazu (also 14.9 oder 25.1), Mögliche Fehler: wird trotzdem mitgenommen
    - Untere und obere Grenze gleich ist möglich (also 20.0 bis 20.0), Mögliche Fehler: Value Error statt gefiltert

Ungültige Werte:

    - Untere Grenze größer als obere, Möglicher Fehler: gibt leere Liste zurück statt Value Error

Spezialfälle:

    - Reihenfolge bleibt gleich, Möglicher Fehler: wird sortiert o.ä.
    - Doppelte Messungen bleiben doppelt, Möglicher Fehler: Doppelte werden rausgeworfen

Seiteneffekte:

    - Liste bleibt wie sie ist, Möglicher Fehler: wird verändert oder Messungen werden rausgelöscht
    - Ergebnis ist eine neue Liste, Möglicher Fehler: gibt einfach die alte Liste zurück

## average_temp

- Normaler Mittelwert wird berechnet

Spezialfälle:

    - Andere Städte zählen nicht mit, Möglicher Fehler: rechnet alle Städte mit oder teilt durch alle Messungen
    - Ergebnis mit Komma (also 12.5), Möglicher Fehler: rundet ab und ergibt 12
    - Groß- und Kleinschreibung zählt (Köln und köln), Möglicher Fehler: rechnet beide zusammen
    - Stadtname muss genau stimmen (Köln und Köln-Ehrenfeld), Möglicher Fehler: rechnet Köln-Ehrenfeld mit

Ungültige Werte:

    - Stadt gibt es nicht, Möglicher Fehler: gibt 0 zurück statt Value Error
    - Liste ist leer, Möglicher Fehler: ZeroDivisionError statt Value Error

Seiteneffekte:

    - Liste bleibt wie sie ist, Möglicher Fehler: wird verändert

## hottest_measurement

- Normal ist die höchste Temperatur eindeutig (in der Mitte)

Grenzwerte:

    - Höchste ist ganz vorne, Möglicher Fehler: erste Messung wird übersprungen
    - Höchste ist ganz hinten, Möglicher Fehler: letzte Messung wird übersprungen
    - Nur eine Messung, Möglicher Fehler: stürzt ab statt die Messung zurückzugeben

Spezialfälle:

    - Nur Minusgrade, Möglicher Fehler: fängt bei 0 an und findet nichts
    - Gleiche Temperatur, frühere Uhrzeit steht hinten, Möglicher Fehler: Uhrzeit wird ignoriert, nimmt einfach die erste
    - Gleiche Temperatur, frühere Uhrzeit steht vorne, Möglicher Fehler: nimmt die spätere oder letzte
    - Gleiche Temperatur UND gleiche Uhrzeit, Möglicher Fehler: nimmt die letzte statt die erste
    - Uhrzeit zählt nur bei gleicher Temperatur, Möglicher Fehler: nimmt die frühere, obwohl sie kälter ist

Ungültige Werte:

    - Liste ist leer, Möglicher Fehler: IndexError statt Value Error

Seiteneffekte:

    - Liste bleibt wie sie ist, Möglicher Fehler: wird sortiert o.ä.

