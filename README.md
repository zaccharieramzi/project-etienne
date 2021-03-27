# Comment utiliser le "bot" python?

*English version below*

Ceci est une doc pour l'usage du bot sous Windows.

- installer Python: https://www.python.org/downloads/release/python-379/, en choisissnat le fichier x86-64 executable
- ouvrir le terminal (invite de commandes)
- installer les bibliotheques python necessaires: `pip install pandas openpyxl click xlsxwriter`
- Dans un dossier unique mettre tous les documents:
  - en particulier creer les 2 documents data et config
  - lancer l’invite de commandes depuis ce dossier en tapant “cmd” dans la barre d’indication de chemin
- executer le bot: `python data_summary.py --data-file month_relecture.xlsx --config-file config.xlsx --results-file results.xlsx`
- Pour acceder plus facilement aux commandes passees, vous pouvez utiliser les fleches du clavier (vers le haut)
- Attention a bien fermer les fichiers excel apres avoir sauvegarde les modifications sur la configuration ou les donnees
- Attention lors de l'ecriture des chemins de fichiers a bien echapper les espaces a l'aide de guillemets (voir [ici](https://www.howtogeek.com/694949/how-to-escape-spaces-in-file-paths-on-the-windows-command-line/) pour plus de precisions). Vous pouvez sinon utiliser Tab (Tabulation) pour avoir une auto-completion des fichiers. Le plus simple est certainement des nommer les fichiers sans espace.
- Astuce: a la place des noms d'arguments longs, vous pouvez utiliser `-c`, `-d`, `-r`.

## Config
- une ou deux lignes exactement dans le fichier (apres l'en-tete) par defaut
- dans chaque cellule sous l'en-tete vous pouvez mettre les valeurs que vous voulez selectionner, separees par des ";". Pour selectionner des cellules ou plusieurs elements doivent etre presents, il faut utiliser "+".
- vous pouvez ajouter une colonne "Age" dans laquelle vous pouvez specifier les relations d'ordre a l'age, en utilisant des operateurs binaires. Par exemple: “>= 13” or “> 13; < 16”. Attention a l'espace entre l'operateur et la valeur numerique.
- pour le filtrage selon la date, vous pouvez utiliser 1 ou 2 dates separees par ";". Chaque date doit etre ecrite dans un format non-ambigu en suivant le formattage anglo-saxon. Par exemple: "13 Jan 2019" or "23 Feb 2019; 31 Mar 2019". Si 1 seule date est presente dans la config, les visites selectionnees seront celles plus recentes que cette date. Les filtres de date sont inclusifs.
- une deuxieme ligne de configuration peut etre ajoutee pour une requete negative. Les lignes correspondant a la 2eme ligne seront exclues du resume.

### Config multi-lignes
- Vous pouvez avoir plus de 2 lignes dans votre fichier de configuration pour decrire des requetes plus complexes.
- Il faut alors ajouter une colonne dans le fichier de configuration, dont l'en-tete est "Request", celle-ci permet de specifier le type de requete pour chaque ligne : 0 pour une requete negative, 1 pour une requete positive.
Il faut specifier la requete pour chaque ligne.
- Une ligne du fichier de donnees sera inclue dans le resultat de l'execution si elle verifie l'une des requetes positives **et** qu'elle ne verifie **aucune** des requetes negatives.
- Autrement dit, la relation entre les lignes du fichier de config est une relation "ou" pour chaque type de requete, et la relation entre les requetes negatives et positives est une relation "et".


Attention: la correspondance entre la config et le contenu des cellules n'est pas exacte.
Les accents et la casse sont par exemple ignores.
Une cellule contenant la valeur de configuration sera consideree comme repondant a la configuration.
Exemple: une config "Keratine" selectionnera les cellules "KERATINE", "Keratineambienne", etc...


# How to use python “bot”?
- install python : https://www.python.org/downloads/release/python-379/, use x86-64 executable
- open terminal (invite de commandes)
- install necessary python libraries: `pip install pandas openpyxl click xlsxwriter`
- Put all files in a single folder:
  - In particular create 2 files: data and config
  - launch the terminal from this folder by typing "cmd" in the path location search bar
- execute bot: `python data_summary.py --data-file month_relecture.xlsx --config-file config.xlsx --results-file results.xlsx`
- To access more easily past commands in the terminal, you use the keyboard arrows (upwards)
- be careful to close excel files after saving config or modifications in data
- be careful when indicating files path, to use escape spaces in file names. Or you can just rely on auto-completion by using Tab (Tabulation).
- Tip: instead of long arguments name, you can use `-c`, `-d`, `-r`.

## Config:

- one or two lines exactly (after the header) by default
- In each cell under the header, you should have all the values you want to filter in separated by “;”. To select cells where many elements must be present, you need to use "+".
- you can add one column “Age” in which you can specify relationships to age, using binary relationship operators. Example: “>= 13” or “> 13; < 16”. Watch the space between op and numerical value
- For the date filtering, you can use 1 or 2 dates separated by ";". Each date should be written in a non-ambiguous format, following anglo-saxon formatting. Example: "13 Jan 2019" or "23 Feb 2019; 31 Mar 2019". If only 1 date is present the visits selected will be the ones more recent than this date. Dates filters are inclusive.
- a second line of config can be added for a negative request. Lines corresponding to the 2nd config line will be excluded from the summary.

### Multi-line config
- You can have more than 2 lines in your configuration file to describe more complex requests.
- You must then add a column in the configuration file, for which the header is "Request", which allows to specify the type of request for each line: 0 for a negative request, 1 for a positive request.
You need to specify the request type for each line.
- A line in the data file will be included in the execution results if it verifies one of the positive requests **and** it verifies **none** of the negative requests.
- Put differently, the relationship between the lines of the config file is an "or" relationship for each type of request, and the relationship between the negative and positive requests is an "and" relationship.



Warning: The match between config and cell content is not exact.
Accents and case are for example ignored.
A cell containing the config value will be considered as matching the configuration.
Example: a config "Keratine" will be matched by cells "KERATINE", "Keratineambienne", etc...
