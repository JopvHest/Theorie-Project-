# Protein pow(d)er
In de case proteine pow(d)er is het de bedoeling dat je een proteïne, een ketting van aminozuren, vouwt op een manier waarop de stabiliteit van die ketting zo hoog mogelijk is. Een hoge stabiliteit betekent een zo laag mogelijke stabiliteitsscore. Het blijkt dat een verkeerde vouwing van proteïnen kan zorgen voor kanker, Alzheimer, en taaislijmziekte. Hierdoor is het erg belangrijk om de precieze vouwing van een proteïne te kunnen bepalen. Elke vouwing is een 90 graden hoek, waardoor het probleem op een grid werkt. Er bestaan P, H, en C aminozuren. P (polaire) aminozuren voegen niks toe aan de stabiliteit. H (hydrofobe) aminozuren zorgen voor -1 stabiliteitsscore, wanneer ze naast elkaar liggen maar niet direct verbonden zijn in de ketting. C (cysteïne) aminozuren zorgen voor -5 stabiliteitsscore wanneer ze op deze zelfde manier naast elkaar liggen, terwijl een C en H aminozuur samen zorgen voor -1 stabiliteitsscore.

## Aan de slag

### Vereisten

De Codebase is geschreven in python 3.7 en volledig compatible met 3.8. De requirements staan in requirements.txt en zijn met de volgende comment te installeren.
    pip install -r requirements.txt

### Gebruik
De applicatie wordt uitgeovoerd vanuit main/main.py, waarin de imports van alle bruikbare functies al staan. Ten eersten maak je een nieuw ongeorderde proteine aan met de volgende functie:

    protein1 = Protein(amino_string, dimension_mode)
amino_string: De string van het proteine dat je wil representeren en sorten. (voorbeeld: " CHHCPHPHPHP")
dimensions_mode: De string van de dimensie mode die je wil uitvoeren.("2D" of "3D")

Vervolgens kan je de chain van het proteine opbouwen met een search functie van jouw keuze. Zie XXX voor de algorithmes die beschikbaar zijn. de paramaters verschillen met algorithme. Deze wordt opgeroepen op een protein object alsvolgens.

    search_type__function(protein1, parameter1, parameter2).

#### Output/ visualisatie

Nu de chain is opgebouwd kan je op verschillende manieren een output krijgen. Namelijk:

Print de score die dit proteine heeft gehaald:

    print(protein1.get_score())

Dit print een representatie van het protein in 2d of 3d doormiddel van MatPlotLib.

    protein1.print_protein()

Print een output zoals vereist vanuit de opdracht.

    protein.get_output_list()


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

### Depth search first.

    depth_search(protein, c-h_score)
beschrijving depth search.

##### Lookahead

    depth_search_lookahead(protein, c-h_score, max_lookahead)
beschrijving

max_lookahead:

### Branch & bound

    branch_and_bound(protein, c-h_score, best_score_import)
beschrijving

best_score_import:

#### Lookahead

beschrijving
located in /unfinished/.

#### Brand & bound random throwaway

    branch_and_bound_random(protein, c-h_score, best_score_import, p1, p2)

beschrijving.

best_score_import:

p1:

p2:

### Breadth_search

    breadth_search(protein, c-h_score)
beschrijving

#### Beam search

    beam_search(protein, c-h_score, selection_levels

beschrijving

selection_levels:

### iterative

describe iterative algos.

#### Hill climbing single

    hill_climbing_single_fold(protein, iterations)
beschrijving

iterations: 
#### Hill climbing caterpillar

    hill_climbing_caterpillar(protein, iterations)

beschrijving;
iterations:

#### Simulated annealing

    simulated_annealing(protein, iterations)

beschrijving:

iterations:

# TODO/ To improve
Where to go from here:

- Add 3D support to all functions
- Improve the score lower bound function for brand and bound.
- Instead of the manhatten distance, use a A* algorithm for figuring out which connections spots can still be reached in banch and bround.


# What we could have done better.
- Function abstraction by represeting them as classes.
