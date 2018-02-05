#! /usr/bin/env python3
# coding: utf-8

import os
import pandas               as pd
import logging              as lg
import numpy                as np
import matplotlib.pyplot    as plt

class SetOfParliamentMember:
    def __init__(self, name):
        self.name = name
        
    # ajouter des députer a partir d'un fichier csv    
    def data_from_csv(self, csv_file):
        self.dataframe = pd.read_csv(csv_file, sep=";")
        
    # ajouter des députer à prtir d'un dataframe    
    def dat_from_dataframe(self, dataframe):
        self.dataframe = dataframe
        
    # diagramme circulaire    
    def display_chart(self):
        data = self.dataframe
        female_mps = data[data.sexe == "F"]
        male_mps = data[data.sexe == "H"]
        
        counts = [len(female_mps), len(male_mps)]
        counts = np.array(counts)
        nb_mps = counts.sum()
        proportions = counts / nb_mps
        
        labels = ["Female ({})".format(counts[0]), "Male ({})".format(counts[1])]
        
        fig, ax = plt.subplots()
        ax.axis("equal")
        ax.pie(proportions, labels = labels, autopct="%1.1f pourcents")
        plt.title("{} ({} MPs)".format(self.name, nb_mps))
        plt.show()
        
    
    def split_by_political_party(self):
        result = {}  # le résultat sera un dictionnaire
        data = self.dataframe
        
        # récupère la liste des partis politiques
        # dropna() supprime les valeurs nulles
        # unique() affiche les valeurs distinctes
        all_parties = data["parti_ratt_financier"].dropna().unique()
        
        for party in all_parties:
            # utilisation d'un masque : data_subset est un DataFrame
            # n'affichant que les députés du parti "party"
            data_subset = data[data.parti_ratt_financier == party]
            
            # création à chaque itération d'un nouveau dataframe nommé subset
            # obtenu par filtrage du dataframe
            subset = SetOfParliamentMember('MPs from party"{}"'.format(party))
            subset.data_from_dataframe(data_subset)
            result[party] = subset
            
        return result
        
    

def launch_analysis(data_file, by_party = False):
    sopm = SetOfParliamentMember('All MPs')
    sopm.data_from_csv(os.path.join("data", data_file))
    sopm.display_chart()
    
    if by_party:
        for party, s in sopm.split_by_political_party().items():
            s.display_chart()
    

if __name__ == "__main__":
    launch_analysis('current_mps.csv')