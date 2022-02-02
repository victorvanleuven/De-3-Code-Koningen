# Chips & Circuits
Dit programma probeert een zo kort en goedkoop mogelijk pad te vinden om verschillende gates op een chip in connectie met elkaar te brengen. Zo kort mogelijk houdt in dat de connectie tussen de gates zo min mogelijk afstand aflegt over de grid zonder overlap te hebben met andere connecties. Het totale pad wordt duurder als connectie met elkaar kruisen. 
De totale kosten (C) worden als volgt berekend:
```
 C = n + 300 * k
```
Waarbij n de totale lengte is van het gehele pad en k het aantal kruisingen is. 

### Gebruik
Het programma kan gebruikt worden door het volgende command aan te roepen in de terminal: 
```  
python3 main.py chip_a netlist_b algorithm runtime batchruns
```
Kies een van de volgende algoritmes: baseline (`baseline`), greedy_random (`gr`), greedy_random_2.0 (`gr_2`), greedy_random_hill (`gr_hill`).
Kies voor `runtime` hoe lang je een run wil laten duren (in seconden) en voor `batchruns` hoeveel runs je wil doen.

**VB**:
```  
python3 main.py chip_0 netlist_1 gr 60 4
``` 

### Structuur

Hieronder is een lijst van de verschillende mappen en files die voorkomen in dit project met een korte beschrijving.

* /code: bevat alle code van dit project.
  * /code/algorithms: bevat de code voor de verschillende algoritmes. (baseline, eerste en tweede algoritme)
  * /code/classes: bevat de benodigde classes voor deze case.
  * /code/visualisation: bevat de code voor de visualisatie van het grid.
  * /code/helpers: bevat de verschillende helper functies.
* /data: bevat de verschillende data bestanden om het programma in te laden en te visualiseren.
* main.py: de code waarbij alles samenkomt en die uiteindelijk wordt aangeroepen in de terminal. 

### Algoritmes

Hieronder een korte beschrijving van de algoritmes die worden gebruikt.
##### Baseline
Het baseline algoritme probeert oplossingen te genereren door alleen maar willekeurige zetten te doen, dus zonder enige heuristieken.

##### Greedy Random
Dit algoritme onderscheidt per connectie de stappen die naar de bestemming toe gaan (greedy) en stappen die ervan afwijken (non-greedy). Als er greedy stappen zijn, wordt daar een willekeurige keuze gemaakt met voorkeur voor de x- en y-richting. Indien er geen greedy stappen mogelijk zijn, wordt een willekeurige keuze gemaakt uit de non-greedy stappen, met voorkeur voor de z-richting.

##### Greedy Random 2.0
Greedy Random 2.0 zet stappen op dezelfde manier als greedy random, maar forceert zichzelf na elke tien connecties een laag omhoog.
Tevens probeert dit algoritme een pad opnieuw als er geen geldige stappen meer zijn, en blijft dit honderd keer proberen, waarna het alle paden wist en opnieuw begint bij de connectie waar het vastliep. (De eerder gemaakte connecties worden dan juist als laatste geprobeerd.)

##### Greedy Random Hill Climber
given solution with overlap, tries connections with overlap again using greedy random 2.0
Begint met een oplossing genereerd door het greedy random algoritme, waarbij overlap niet in acht werd genomen, maar wel alle connecties zijn gemaakt. 
Gaat over de connecties met overlap heen en probeert hiervan connecties zonder overlap te maken met behulp van het greedy random 2.0-algoritme. 
_De Hillclimber minimaliseert hier dus overlap in plaats van kosten._

### De 3 Code-Koningen / Auteurs
- Jesse Mastenbroek, 12413437
- Pieter Out, 12474193
- Victor van Leuven, 11643978