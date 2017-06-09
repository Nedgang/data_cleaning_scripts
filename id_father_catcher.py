#!/usr/bin/python3
"""
Récupère les identifiants du père des individus présents dans le fichier de
qualité d'œuf en utilisant le fichier de localisation des troupeaux.

Usage:
    ./id_father_catcher.py <egg_qual> <pedigree> --output=<output_file>

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
    population = pd.read_csv(args["<pedigree>"])

    population["Ferme"] = population["Ferme"].astype(str)
    egg_qual["Ferme"] = egg_qual["Ferme"].astype(str)

    population["Batiment"] = population["Batiment"].astype(str)
    egg_qual["Batiment"] = egg_qual["Batiment"].astype(str)

    population["Cage"] = population["Cage"].astype(str)
    egg_qual["Cage"] = egg_qual["Cage"].astype(str)

    population["Cage"] = population.apply(clean_cage, axis=1)
    egg_qual["Cage"]= egg_qual.apply(clean_cage, axis=1)

    population["Lot"] = population["Lot"].astype(float)
    egg_qual["Lot"] = egg_qual["Lot"].astype(float)

    # Check if the variable "lot" does exist.
    print("Clustering depending of the chicken birth (\"Lot\")")
    if "Lot" not in egg_qual:
        egg_qual["Lot"] = egg_qual.apply(define_lot, axis=1)

    if "Lot" not in population:
        population["Lot"] = population.apply(define_lot, axis=1)

    print("Searching father ID")

    egg_qual["IDPere"] = egg_qual.apply(lambda x: get_father_id(x, population)
                                          , axis=1)

    result = egg_qual[egg_qual["IDPere"] > 0]
    print("Writing result file")
    result.to_csv(args["--output"], index=False)


#############
# FUNCTIONS #
#############
def clean_cage(row):
    return row["Cage"].split(".")[0]

def define_lot(row):
    if "Generation" in row:
        infos = row["Generation"].split("/")
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
    if "BirdID" in row and row["BirdID"] != "":
        result = pop.loc[pop["Bird_ID"]==row["BirdID"]]["ID_P"]
        if result.tolist() != []:
            return result.tolist()[0]
        else:
            return -1
    else:
        result = pop.loc[(pop["Ferme"] == row["Ferme"]) &
                         (pop["Batiment"] == row["Batiment"]) &
                         (pop["Cage"] == row["Cage"]) &
                         (pop["Lot"] == row["Lot"])]["ID_P"]
        # print(result.tolist())
        if len(set(result.tolist())) == 1:
            return result.tolist()[0]
        elif row["Lot"] == "2013.3":
            result = pop.loc[(pop["Ferme"] == row["Ferme"]) &
                         (pop["Batiment"] == row["Batiment"]) &
                         (pop["Cage"] == row["Cage"]) &
                         (pop["Lot"] == 2013.1)]["ID_P"]
            if len(set(result.tolist())) == 1:
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
