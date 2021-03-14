# How to use python “bot”?
- install python : https://www.python.org/downloads/release/python-379/, use x86-64 executable
- open terminal (invite de commandes)
- install necessary python libraries: `pip install pandas openpyxl click xlsxwriter`
- Dans un dossier unique mettre tous les documents:
  - en particulier creer les 2 documents data et config
  - lancer l’invite de commandes depuis ce dossier en tapant “cmd” dans la barre d’indication de chemin
- execute bot: `python data_summary.py --data-file month_relecture.xlsx --config-file config.xlsx --results-file results.xlsx`
- Pour acceder plus facilement aux commandes passes, vous pouvez utiliser les fleches du clavier (vers le haut)
- be careful to close excel files after saving config or modifications in data
- be careful when indicating files path, to use “\” before spaces in file names. Or you can just rely on auto-completion by using Tab (Tabulation).

# Config:

- one line exactly
- In each cell under the header, you should have all the values you want to filter in separated by “;”
- you can add one column “Age” in which you can specify relationships to age, using binary relationship operators. Example: “>= 13” or “> 13; < 16”. Watch the space between op and numerical value
