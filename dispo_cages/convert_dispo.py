#!/usr/bin/python3
"""
Converti le fichier xls de dispositon des cages, en plusieurs feuilles, en un
beau csv pratique à utiliser.

Usage:
    ./convert_dispo.py <dispo.xls> --output <dispo.csv>

Options:
    -h, --help              Show this screen.
    -o, --output=<file>     Output file name.
    -v, --version           Show version.
"""

##########
# IMPORT #
##########
import pandas as pd

from docopt import docopt

########
# MAIN #
########
def main(args):
    print("Loading files in RAM")
    data_localisation = pd.read_excel(args["<dispo.xls>"],sheetname=None)

    # Creation du dataframe resultat
    result = pd.DataFrame({"Lot": [], "Type_cage": [], "Cage": [], "Batterie": [],
                           "Etage": [], "Côté": [], "Position": []})

    print("Concatenation of the different pages")
    for date in data_localisation:
        infos = date.split(" ")

        if infos[-1] == "CI":
            data_localisation[date]["Type_cage"] = "individuelle"
        else:
            data_localisation[date]["Type_cage"] = "multiple"

        if len(infos) == 3:
            data_localisation[date]["Lot"] = infos[0]
            result = result.append(data_localisation[date])
            data_localisation[date]["Lot"] = infos[1][1:]
            result = result.append(data_localisation[date])

        else:
            data_localisation[date]["Lot"] = infos[0]
            result = result.append(data_localisation[date])

    result = result[result.Cage != "Total général"]
    print("Writing result file")
    result.to_csv(args["--output"], index=False)

##########
# LAUNCH #
##########
if __name__ == "__main__":
    arguments = docopt(__doc__, version="0.1")
    main(arguments)
