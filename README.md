# Protein pow(d)er

In de case proteine pow(d)er is het de bedoeling dat je een proteïne, een ketting van aminozuren, vouwt op een manier waarop de stabiliteit van die ketting zo hoog mogelijk is. Een hoge stabiliteit betekent een zo laag mogelijke stabiliteitsscore. Het blijkt dat een verkeerde vouwing van proteïnen kan zorgen voor kanker, Alzheimer, en taaislijmziekte. Hierdoor is het erg belangrijk om de precieze vouwing van een proteïne te kunnen bepalen. Elke vouwing is een 90 graden hoek, waardoor het probleem op een grid werkt. Er bestaan P, H, en C aminozuren. P (polaire) aminozuren voegen niks toe aan de stabiliteit. H (hydrofobe) aminozuren zorgen voor -1 stabiliteitsscore, wanneer ze naast elkaar liggen maar niet direct verbonden zijn in de ketting. C (cysteïne) aminozuren zorgen voor -5 stabiliteitsscore wanneer ze op deze zelfde manier naast elkaar liggen, terwijl een C en H aminozuur samen zorgen voor -1 stabiliteitsscore.

![Protein visualizaion](doc/proteins.png)


# Aan de slag

#### Vereisten

De Codebase is geschreven in python 3.7 en volledig compatible met 3.8. De requirements staan in requirements.txt en zijn met de volgende line te installeren:

    pip install -r requirements.txt

#### Gebruik
De applicatie wordt uitgevoerd vanuit main/main.py. Als deze file gerund wordt volgt een command line interface die de gebruiker een aantal vragen stelt, en vervolgens de juiste algoritmes toepast op de aangevraagde proteïne.

Eerst zal gevraagd worden of de gebruiker wil werken in 2D of 3D modus. Hierna selecteert de gebruiker één van de acht proteïnen gegeven in de case, of de custom optie. De custom optie laat de gebruiker een string invoeren, bestaand uit P/H/C voor de verschillende aminozuren. Vervolgens selecteert de gebruiker welk algoritme gebruikt moet worden om de folds van de chain te bepalen. Verdere uitleg over de algoritmes, en de parameters die deze algoritmes zal vragen van de gebruiker, staan in de algoritme sectie van deze readme. Nadat het algoritme klaar is, krijgt de gebruiker de final score van de chain en de runtime te zien. Tot slot kan de gebruiker kiezen uit verschillende outputs:
- Interactive protein visualisation
  - De standaard visualisatie, gemaakt met gebruik van matplotlib.
- Standard output list
  - De vereiste output, beschreven op de mprog pagina over deze case.
- Final score
  - Om nogmaals de final score aan te vragen.


# Structuur
De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- /code/ : Bevat alle code van dit project.
    - /code/main.py : De applicatie wordt gerund vanuit deze file.
    - /code/classes/ : Bevat de classes voor de gebruikte objecten.
    - /code/functions/ : Bevat alle helper functies die worden hergebruikt in andere delen van code.
    - /code/algorithms/ : Bevat de algorithms die de folds van de aminos bepalen.
    - /code/unfinished/ : Bevat niet afgeronde/niet werkende code.



# Algoritmes

Het volgende variabele wordt door praktisch elk algoritme gebruikt:

C-H score:
Dit variabele bepaalt de score van een C-H bond in de ogen van het algoritme. Een lagere score zorgt er voor dat een algoritme C-H bonds eerder vermijd, in de hoop dat er later een ander C aminozuur naast dit C aminozuur geplaatst kan worden. De score wordt automatisch omgezet naar een negatief nummer, vul dus een integer tussen 0 en 1 in. Het invullen van 1 zorgt voor de standaard versie.

## Depth first search (depth_search)
Dit is een implementatie van het Depth First algoritme die alle mogelijke combinaties van legal folds afgaat. Vindt altijd de beste score, gegeven genoeg tijd. Gebruikt geen aanvullende parameters.

##### Lookahead (depth_search_lookahead)

Dit is een variatie van de depth search die een x aantal stappen diep vooruit kijkt. De volgende stap zet hij naar de fold die over deze x stappen de beste score opleverde. Bij de volgende stap kijkt hij weer x stappen vooruit en kiest de fold die over deze x stappen de beste score opleverde. Vindt niet altijd de beste score. Dit algoritme gebruikt 1 aanvullend parameter:

max_lookahead:
Dit is een integer die aangeeft hoeveel stappen de lookahead vooruit moet kijken. Suggested range: (6-12).

## Branch & bound (branch_and_bound)

Het branch and bound algoritme is een aangepast depth first algoritme die voor elke chain bekijkt of deze de beste score nog kan verbeteren, doormiddel van de upper bound van de score. Hij houdt ook alle spots bij waar potentieel nog bonds kunnen connecten, en verwijdert deze weer als ze niet meer reachable zijn. Dit gebeurt doormiddel van de manhatten distance. Vindt altijd de beste score. Dit algoritme gebruikt 1 aanvullend parameter:

best_score_import:
Als je zeker weet dat de beste score onder een bepaalde score ligt, kan je deze specificeren om alle chains onder deze score te abandonen. Mocht je dit niet zeker weten, kun je hier 0 invullen.

#### Branch & bound random throwaway (branch_and_bound_random)

Zie branch & bound. Dit is een toevoeging aan dit algoritme. Hij houdt de gemiddelde score op elke depth bij, en stopt willekeurig met chains na ze te vergelijken met de gemiddelde score. De kans dat deze wordt geabandond is gebaseerd op het feit of de score onder of boven het gemiddelde ligt. Vindt niet altijd de beste score.

p1: De kans dat een chain wordt geabandoned als hij een score lager heeft dan het gemiddelde (dus beter). Waarde tussen 0 en 1.

p2: De kans dat een chain wordt geabandoned als hij een hogere score heeft dan het gemiddelde (dus slechter). Waarde tussen 0 en 1.

#### Lookahead

Aangezien een brand and bound algoritme veel sneller is dan een normale depth first search, wilde we nog een een lookahead algoritme maken met de B&B. Helaas hebben we niet genoeg tijd gehad om deze volledig te implementeren.

aanwezig in /unfinished/.

## Breadth_search (breadth_search)

De breadth search verlengt the chain steeds door één nieuwe amino te leggen. Hij begint met het leggen van de eerste Amino met een fold in vastgestelde richting (dit voorkomt dubbel werk omdat de eerste richting niet uitmaakt ivm spiegelingen). Hij voegt deze als chain object toe aan de queue. Hij haalt de eerst toegevoegde chain uit de queue, kijkt naar alle mogelijke folds, en maakt voor elke mogelijke fold een chain aan van de chain tot dan toe plus de nieuwe fold. Hierbij wordt een deepcopy gemaakt van de chain die net uit de queue is gehaald. Daarna stopt hij de nieuw gemaakte chains weer in de queue en zo gaat hij steeds door totdat hij alle aminos heeft gehad. Vindt altijd de beste score. Dit algoritme gebruikt geen aanvullende parameters.


#### Beam search
De beam search werkt volgens hetzelfde principe en initïele structuur als de breadth_search. Het verschil is dat dit algoritme op elke laag alle chains slechter dan de gemiddelde score pruned. Vindt niet altijd de beste score. Dit algoritme gebruikt geen aanvullende parameters.

## Iterative


#### Hill climbing single (hill_climbing)
Een hill climbing algoritme dat een enkele fold verlegt, en deze vervolgens houdt als het leidt tot een betere, of gelijke score. Hij kan een fold met verslechtering accepteren als hij al een bepaalt aantal turns niet is verbeterd. Dit algoritme gebruikt de volgende aanvullende parameters:

iterations:
Iterations is een integer die aangeeft hoe vaak een verandering aan de chain wordt uitgevoerd alvorens het programma stopt. Suggested: 20k iterations.

max_non_improvements:
Dit is een integer die aangeeft hoe vaak een random fold tot een verbetering moet leiden. Dus als de fold geen verbetering in score geeft wordt de oude staat van de chain hersteld. Als dit net zo vaak is gebeurd als max_non_improvements gaat hij verder met deze chain ongeacht dat het geen betere score geeft.

#### Hill climbing caterpillar (hill_climbing_caterpillar)
Dit algoritme verlegt de fold van een random geselecteerd amino en past de daarop volgende folds aan zodat de amino daarna of de amino 2 daarna weer op een plek in de begin chain uitkomt. Als er hierdoor ruimte in de chain ontstaat worden de aminos na deze van plek gewisseld zodat de chain weer aansluit. Dit algoritme gebruikt dezelfde aanvullende parameters als de eerste hill climber.

#### Simulated annealing
Het hill climbing single algoritme die is aangepast door een variabele kans op acceptatie die gebaseerd is op de score. Deze kans is gebaseerd op een variabele temperatuur. De temperatuur neemt lineair af van de start temperatuur naar de eind temperatuur naarmate je door de iteraties heen gaat. Dit algoritme gebruikt de volgende aanvullende parameters, boven op de parameters gebruikt in de eerste hill climber. 

start_temp: De temperatuur waar het algoritme mee begint. Suggested range: 5-10

end_temp: De temperatuur waar het algoritme mee eindigt. Suggested temp: 0.5

## Random
Dit algoritme bepaalt elke fold op een random wijze. Gebruikt geen aanvullende parameters.

# Advanced: 3D
Helaas hebben we niet de tijd gehad om elk algoritme compatible te maken met een 3d protein-structuur. De volgende algoritmes werken in 3d:
- Random
- Depth search
- Depth search Lookahead
- Hill climbing single
- Simulated annealing
