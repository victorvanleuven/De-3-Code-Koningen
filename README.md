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
python3 main.py chip_a netlist_b algorithm
```
Kies een van de volgende algoritmes: baseline (baseline), greedy_random (gr), greedy_random_2.0 (gr_2)
(VERNEDERLANDSEN)
output and visualisation are optional and have default file names "test/chip_a_netlist_b_datetime.csv"
and "test/chip_a_netlist_b_datetime.png" respectively

### Structuur

Hieronder is een lijst van de verschillende mappen en files die voorkomen in dit project met een korte beschrijving.

* /code: bevat alle code van dit project.
  * /code/algorithms: bevat de code voor de verschillende algoritmes. (baseline, eerste en tweede algoritme)
  * /code/classes: bevat de benodigde classes voor deze case.
  * /code/visualisation: bevat de code voor de visualisatie van het grid.
  * /code/helpers: bevat de verschillende helper functies.
* /data: bevat de verschillende data bestanden om het programma in te laden en te visualiseren.
* main.py: de code waarbij alles samenkomt en die uiteindelijk wordt aangeroepen in de terminal. 


### De 3 Code-Koningen / Auteurs
- Jesse Mastenbroek, 12413437
- Pieter Out, 12474193
- Victor van Leuven, 11643978