#!/usr/bin/python3
"""
Récupère les identifiants du père des individus présents dans le fichier de
qualité d'œuf en utilisant le fichier de localisation des troupeaux.

Usage:
    ./id_father_catcher.py <egg_qual> <chicken_data> --output=<output_file>

Options:
    -h, --help              Show this screen.
    -o, --output=<file>     Output file name.
    -v, --version           Show version.
"""

##########
# IMPORT #
##########
import os
from datetime import datetime as dt

import pandas as pd

from docopt import docopt

########
# MAIN #
########
def main(args):
    print("Loading files in RAM")
    egg_qual = pd.read_csv(args["<egg_qual>"])
    population = pd.read_csv(args["<chicken_data>"])

    # Check if the variable "lot" does exist.
    print("Clustering depending of the chicken birth (\"Lot\")")
    if "Lot" not in egg_qual:
        egg_qual["Lot"] = egg_qual.apply(define_lot, axis=1)

    if "Lot" not in population:
        population["Lot"] = population.apply(define_lot, axis=1)

    print("Searching father ID")

    egg_qual["ID Père"] = egg_qual.apply(lambda x: get_father_id(x, population)
                                          , axis=1)

    print("Writing result file")
    egg_qual.to_csv(args["--output"], index=False)


#############
# FUNCTIONS #
#############
def define_lot(row):
    if "Génération" in row:
        infos = row["Génération"].split("/")
        try:
            infos[1]=str(int(infos[1]))
            return ".".join(infos[0:2])
        except:
            infos = row["Génération"].replace(",", ".")
            return infos

    elif "Date d'éclosion" in row:
        date = row["Date d'éclosion"].split("/")
        if int(date[0]) == 2014:
            if int(date[1]) <= 3:
                return "2013.3"
        if int(date[1]) <= 6:
            return date[0]+".1"
        else:
            return date[0]+".2"
    else:
        return -1

def get_father_id(row, pop):
    # If ID column exist and is not empty
    if "Bird ID" in row and row["Bird ID"] != "":
        result = pop.loc[pop["Bird ID"]==row["Bird ID"]]["ID Père"]
        if result.tolist() != []:
            return result.tolist()[0]
        else:
            return -1
    else:
        result = pop.loc[(pop["Ferme"] == row["Ferme"]) &
                         (pop["Bâtiment"] == row["Bâtiment"]) &
                         (pop["Cage"] == row["Cage"]) &
                         (pop["Lot"] == row["Lot"])]["ID Père"]
        if result.tolist() != []:
            return result.tolist()[0]
        elif row["Lot"] == "2013.3":
            result = pop.loc[(pop["Ferme"] == row["Ferme"]) &
                         (pop["Bâtiment"] == row["Bâtiment"]) &
                         (pop["Cage"] == row["Cage"]) &
                         (pop["Lot"] == 2013.1)]["ID Père"]
            if result.tolist() != []:
                return result.tolist()[0]
            else:
                return -1
        else:
            return -1

##########
# LAUNCH #
##########
if __name__ == "__main__":
    arguments = docopt(__doc__, version="1.0.0")
    main(arguments)
