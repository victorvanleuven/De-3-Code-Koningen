# Chips & Circuits
Dit programma probeert een kort en goedkoop pad te vinden om verschillende gates op een chip in connectie met elkaar te brengen. Zo kort mogelijk houdt in dat de connectie tussen de gates zo min mogelijk afstand aflegt over de grid zonder overlap te hebben met andere connecties. Het totale pad wordt duurder als connectie met elkaar kruisen. 
De totale kosten (C) worden als volgt berekend:
```
 C = n + 300 * k
```
Waarbij n de totale lengte is van het gehele pad en k het aantal kruisingen is. 

### Gebruik
Het programma kan gebruikt worden door het volgende command aan te roepen in de terminal:
```  
python3 main.py gate_coordinates netlist output_csv output_png
```
Waarbij 'gate_coordinates' de naam is van de file waarin de coördinaten zijn gegeven van de gates. 'netlist' is de naam van file waar de netlist in staat, waar is aangegeven welke gates met elkaar in connectie zijn. De output_csv is de naam van een csv bestand waar de gebruiker wil dat de paden tussen de gaten worden opgeslagen. Die worden vervolgens gevisualiseerd en opgeslagen als een png bestand met de naam die wordt gegeven in het vierde argument. 

### De 3 Code-Koningen / Auteurs
- Jesse Mastenbroek, 
- Pieter Out,
- Victor van Leuven, 11643978


*outline:*
- _data_
- _grid.py (grid class)_
- _netlist.py (netlist class)_
- _circuit.py (class consisting of net with wires as in example/output.csv)_
    - _has Circuit.cost() as method_
- generate_net.py (_generates net given netlist and grid._)