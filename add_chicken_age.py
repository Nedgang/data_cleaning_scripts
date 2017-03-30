#!/usr/bin/python3
"""
Explanations

Usage:
    ./add_chicken_age.py <data.py> <chicken_data> --output=<output.csv>

Options:
    -h, --help              Show this screen
    -o, --output=<file>     Output file name.
    -v, --version           Show version
"""

##########
# IMPORT #
##########
from datetime import datetime
import pandas as pd

from docopt import docopt

########
# MAIN #
########
def main(args):
    print("Loading files in RAM")
    data = pd.read_csv(args["<data.py>"])
    population = pd.read_csv(args["<chicken_data>"])

    if "Date d'éclosion" not in data:
        if "Lot" not in population:
            population["Lot"] = population.apply(define_lot, axis=1)
        print("Add chicken birth")
        data["Date d'éclosion"] = data.apply(lambda x:
                                              define_birth(x, population),
                                              axis = 1)

    print("Add chicken age")
    data["Age poule"] = data.apply(define_age, axis=1)

    print("Add chicken age group")
    data["Groupe d'age"] = data.apply(define_group, axis=1)

    print("Writing output: "+ args["--output"])
    data.to_csv(args["--output"], index=False)

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

def define_birth(row, pop):
    result = pop.loc[(pop["Ferme"] == row["Ferme"]) &
                     (pop["Cage"] == row["Cage"]) &
                     (pop["Lot"] == str(row["Lot"]))]["Date d'éclosion"]
    if result.tolist() != []:
        return result.tolist()[0]
    elif row["Lot"] == "2013.3":
        result = pop.loc[(pop["Ferme"] == row["Ferme"]) &
                     (pop["Cage"] == row["Cage"]) &
                     (pop["Lot"] == "2013.1")]["Date d'éclosion"]
        if result.tolist() != []:
            return result.tolist()[0]
        else:
            return -1
    else:
        print("pb")
        return -1

def define_age(row):
    date_eclosion = datetime.strptime(row["Date d'éclosion"], "%Y/%m/%d")
    date_ponte = datetime.strptime(row["Date Ponte"], "%Y/%m/%d")
    return (date_ponte-date_eclosion).days//7

def define_group(row):
    return str(row["Age poule"])[0]+"0"


##########
# LAUNCH #
##########
if __name__ == "__main__":
    arguments = docopt(__doc__, version="0.1")
    main(arguments)
