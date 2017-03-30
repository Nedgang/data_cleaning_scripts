#!/usr/bin/python3.5
"""
Récupère les identifiants du père des individus présents dans le fichier de
qualité d'œuf en utilisant le fichier de localisation des troupeaux.

Usage:
    ./id_father_poids.py <poids> <chicken_data> --output=<output_file>

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
    poids = pd.read_csv(args["<poids>"])
    population = pd.read_csv(args["<chicken_data>"])

    # Check if the variable "lot" does exist.
    print("Clustering depending of the chicken birth (\"Lot\")")
    if "Lot" not in poids:
        poids["Lot"] = poids.apply(define_lot, axis=1)

    print("Searching father ID")
    result = pd.merge(poids, population[["Bird ID", "ID Père"]], how="left", on=["Bird ID"])

    print("Writing result file")
    result.to_csv(args["--output"], index=False)


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


##########
# LAUNCH #
##########
if __name__ == "__main__":
    arguments = docopt(__doc__, version="1.0.0")
    main(arguments)
