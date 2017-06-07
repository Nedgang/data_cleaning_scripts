#!/usr/bin/python3
"""
Explanations

Usage:
    ./merge_dispo_cage.py <data.py> <dispo_cage.py> --output=<output.csv>

Options:
    -h, --help              Show this screen
    -o, --output=<file>     Output file name.
    -v, --version           Show version
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
    data = pd.read_csv(args["<data.py>"])
    dispo_cage = pd.read_csv(args["<dispo_cage.py>"])

    print("Merging files")
    data["Type_cage"] = data.apply(define_type_cage, axis=1)

    data["Cage"] = data["Cage"].astype(int)
    dispo_cage["Cage"] = dispo_cage["Cage"].astype(int)

    data["Lot"] = data["Lot"].astype(float)
    dispo_cage["Lot"] = dispo_cage["Lot"].astype(float)

    data["Type_cage"] = data["Type_cage"].astype(str)
    dispo_cage["Type_cage"] = dispo_cage["Type_cage"].astype(str)

    result = pd.merge(data, dispo_cage, how='inner', on=["Cage", "Lot", "Type_cage"])
    #print(result)

    print("Writing output: "+ args["--output"])
    result.to_csv(args["--output"], index=False)

#############
# FUNCTIONS #
#############
def define_type_cage(row):
    if row["Ferme"] == "Collorec":
        return "individuelle"
    else:
        return "multiple"

##########
# LAUNCH #
##########
if __name__ == "__main__":
    arguments = docopt(__doc__, version="0.1")
    main(arguments)
