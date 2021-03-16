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
- Pour acceder plus facilement aux commandes passes, vous pouvez utiliser les fleches du clavier (vers le haut)
- Attention a bien fermer les fichiers excel apres avoir sauvegarde les modifications sur la configuration ou les donnees
- Attention lors de l'ecriture des chemins de fichiers a bien echapper les espaces a l'aide guillemets (voir [ici](https://www.howtogeek.com/694949/how-to-escape-spaces-in-file-paths-on-the-windows-command-line/) pour plus de precisions). Vous pouvez sinon utiliser Tab (Tabulation) pour avoir une auto-completion des fichiers. Le plus simple est certainement des nommer les fichiers sans espace.

## Config
- une ligne exactement dans le fichier (apres l'en-tete)
- dans chaque cellule sous l'en-tete vous pouvez mettre les valeurs que vous voulez selectionner, separees par des ";".
- vous pouvez ajouter une colonne "Age" dans laquelle vous pouvez specifier les relations d'ordre a l'age, en utilisant des operateurs binaires. Par exemple: “>= 13” or “> 13; < 16”. Attention a l'espace entre l'operateur et la valeur numerique.
- pour le filtrage selon la date, vous pouvez utiliser 1 ou 2 dates separees par ";". Chaque date doit etre ecrite dans un format non-ambigu en suivant le formattage anglo-saxon. Par exemple: "13 Jan 2019" or "23 Feb 2019; 31 Mar 2019". Si 1 seule date est presente dans la config, les visites selectionnees seront celles plus recentes que cette date. Les filtres de date sont inclusifs.



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

# Config:

- one line exactly
- In each cell under the header, you should have all the values you want to filter in separated by “;”
- you can add one column “Age” in which you can specify relationships to age, using binary relationship operators. Example: “>= 13” or “> 13; < 16”. Watch the space between op and numerical value
- For the date filtering, you can use 1 or 2 dates separated by ";". Each date should be written in a non-ambiguous format, following anglo-saxon formatting. Example: "13 Jan 2019" or "23 Feb 2019; 31 Mar 2019". If only 1 date is present the visits selected will be the ones more recent than this date. Dates filters are inclusive.
