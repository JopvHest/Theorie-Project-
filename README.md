# Protein pow(d)er
intro stukje protein powder.

## Aan de slag

### Vereisten

De Codebase is geschreven in python 3.7 en volledig compatible met 3.8. De requirements staan in requirements.txt en zijn met de volgende comment te installeren.
    pip install -r requirements.txt

### Gebruik
De applicatie wordt uitgeovoerd vanuit main/main.py, waarin de imports van alle bruikbare functies al staan. Ten eersten maak je een nieuw ongeorderde proteine aan met de volgende functie:
    
    protein1 = Protein(amino_string, dimension_mode)
amino_string: De string van het proteine dat je wil representeren en sorten. (voorbeeld: " CHHCPHPHPHP")
dimensions_mode: De string van de dimensie mode die je wil uitvoeren.("2D" of "3D")

Vervolgens kan je de chain van het proteine opbouwen met een search functie van jouw keuze. Zie XXX voor de algorithmes die beschikbaar zijn. Deze wordt opgeroepen op een protein object alsvolgens.
    
    search_type__function(protein1, parameter1, parameter2)

de paramaters verschillen met algorithme.

Nu de chain is opgebouwd kan je op verschillende manieren een output krijgen. Namelijk:
    
    print(protein1.get_score())
Dit print de score die dit proteine heeft gehaald.

    protein1.print_protein()
Dit print een representatie van het protein in 2d of 3d doormiddel van MatPlotLib

    protein.get_output_list()
Print een output zoals vereist vanuit de opdracht.

## Structuur
De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- /main/ : Bevat alle code van dit project.
    - /main/main.py : De applicatie wordt gerund vanuit deze file.
    - /main/classes/ : Bevat de classes voor de gebruikte objecten.
    - /main/functions/ : Bevat alle helper functies die worden hergebruikt in andere delen van code
    - /main/algorithms/ : Bevat de algorithms die de folds van de aminos bepalen.
    - /main/unfinished/ : Contains the current unfinished/ not working code of the project


# Algorithmes
We zullen van elke geimplementeerde search uitleggen wat die doet, en hoe deze aangeroepen moet worden. Ook wordt voor elke functie aangegeven of deze wordt gesupport in 2d EN 3d, of alleen in 2d.

### Depth search first
##### Lookahead
##### Iterative
## Branch bound
### Lookahead
### Random throwaway'
## Breadth_search
### Beam search
## iterative
### Hill climbing single
### Hill climbing multi
### Simulated annealing


# TODO
Where to go from here:

- Add 3D support to all functions
- Improve the score lower bound function for brand and bound.
- Instead of the manhatten distance, use a A* algorithm for figuring out which connections spots can still be reached in banch and bround.


# What we could have done better.
- Function abstraction by represeting them as classes.

