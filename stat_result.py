#!/usr/bin/python3
"""
Inventaire du fichier obtenu.

Usage:
    ./stat_result.py <file>
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
    data = pd.read_csv(args["<file>"])

    #Inventaire des lots
    set_lot = set()
    for l in data["Lot"]:
        set_lot.add(l)
    print(sorted(set_lot))

    #Décompte des pères obtenus
    found = 0
    for p in data["ID Père"]:
        if p > 0:
            found +=1
    print(str(found)+" pères trouvés sur "+str(len(data["ID Père"])))

    # Décompte des pères absents
    abs_father         = {}
    daughter_by_father = {}
    nb_daughter        = 0
    seen_cage          = set()
    for i, row in data.iterrows():
        if not row["ID Père"] > 0:
            if row["Lot"] in abs_father:
                abs_father[row["Lot"]] += 1
            else:
                abs_father[row["Lot"]] = 1
        else:
            nb_daughter += 1
            if row["ID Père"] not in daughter_by_father:
                daughter_by_father[row["ID Père"]] = 1
                seen_cage.add(row["Cage"])
            else:
                if row["Cage"] not in seen_cage:
                    daughter_by_father[row["ID Père"]] += 1
                    seen_cage.add(row["Cage"])

    if abs_father == {}:
        print("Tout les pères potentiels ont été trouvés")
    else:
        print(abs_father)

    print("Nombre de cages par pères: ", daughter_by_father)
    print("Moyenne: ", nb_daughter/len(daughter_by_father), "cages par coq")


#############
# FUNCTIONS #
#############

##########
# LAUNCH #
##########
if __name__ == "__main__":
    arguments = docopt(__doc__, version="0.1")
    main(arguments)
