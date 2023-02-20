# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:11:30 2023

@author: Chamakh Feriel
"""

from string import punctuation
import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import os
import json
from pandas.io.json import json_normalize
from tkinter import *
import urllib.request
import numpy as n
import math
import string
import datetime
import csv

root =Tk()

def enregistrement(txt):
    # Définir les données à écrire dans le fichier CSV
    now = datetime.datetime.now()
    data = [
        [txt, now]
        
    ]

    # Ouvrir le fichier CSV
    with open('donnees.csv', mode='a', newline='') as file:
        
        # Créer un objet écrivain CSV
        writer = csv.writer(file)
        
        # Écrire les données dans le fichier CSV
        writer.writerows(data)
        
        # Fermer le fichier CSV
        file.close()



def import_donnee_reel_time(): 
    #os.remove("Parking_temps_reel.csv")
    urllib.request.urlretrieve("https://download.data.grandlyon.com/files/rdata/lpa_mobilite.donnees/Parking_temps_reel.csv", "Parking_temps_reel.csv")
    data_real_time = pd.read_csv('Parking_temps_reel.csv',sep=",")
    return data_real_time

def import_donnee_detail(): 
    #os.remove("pvo_patrimoine_voirie.pvoparking.csv")
    urllib.request.urlretrieve("https://download.data.grandlyon.com/ws/grandlyon/pvo_patrimoine_voirie.pvoparking/all.csv?maxfeatures=-1", "pvo_patrimoine_voirie.pvoparking.csv")
    data_detaille = pd.read_csv('pvo_patrimoine_voirie.pvoparking.csv',sep=";")
    
    
    return data_detaille

def nettoyer_msg(txt):
     
     tokens = word_tokenize(txt)
     
     tokens=[w.lower() for w in tokens]
     
     k=' '.join(tokens)
     return k 

def fonction_code_postal(msg):
    new_df = pd.DataFrame()
    lengeur=len(msg)
    if lengeur == 2 :
        code_postal="690"+msg
    elif lengeur == 3 :
        code_postal="69"+msg
    elif lengeur == 5 :
        code_postal=msg  
    
    
    rep = "les parkings proposés avec ce code postal "+ code_postal +" sont :"
    
    for index, row in data_detaille.iterrows():
       
       if not math.isnan(row["insee"]) :
           
           if str(int(row["insee"])) == code_postal:
               rep = rep +"\n" +str(row["nom"])
               new_df = new_df.append(data_detaille.loc[index])
                       
    rep = rep + "\n"+ "Quel parking voulez vous choisir ?"
    return  new_df,rep

def fonction_Commune(msg):
    new_df = pd.DataFrame()
    answer=bool(False)
    msg = msg.lower()
    rep = "les parkings proposés dans cette commune sont :"
    for index, row in data_detaille.iterrows():
       l=str(row["commune"]).lower()     
       match = re.search(msg, l)
       if match:
           rep = rep +"\n" +str(row["nom"])
           answer=bool(True)
           new_df = new_df.append(data_detaille.loc[index])
    rep = rep + "\n"+ "Quel parking voulez vous choisir ?"
    
    return new_df,rep,answer    
  
def fonction_Parking(new_df,msg):
    global data
    id_four=""
    answer=bool(False)
    msg = msg.lower()
    
    for index, row in new_df.iterrows():
       l=str(row["nom"]).lower()     
       match = msg.find(l)
       
       if match != -1:   
           
           id_four=row["idfournisseur"]
           
           answer=bool(True)
           data=new_df.loc[index]
           
           break
     
    return data,id_four  

def fonction_id_Parking(new_df,msg):
    id_parking =""
    answer=bool(False)
    msg = msg.lower()
    
    for index, row in new_df.iterrows():
       l=str(row["nom"]).lower()     
       match = msg.find(l)
       
       if match != -1:   
           
           id_parking=row["idparking"]
           
           answer=bool(True)
           break
     
    return id_parking  
"""  
def fonction_Q_detaille(msg):
    print("Q_detaille")
    return 0
"""  
def disponible(id):
    a=""
    for index, row in data_real_time.iterrows():
       
       if row["Parking_schema:identifier"]==id :
          
           a = " Ce parcking  a "+str(row["mv:currentValue"])+" places vides."

           
    if a =="":
        a = "Malheuresement, nous n'avons pas la disponibilité pour ce parking"
    return a

               
def answer_detaills(msg,df):
    rep=""
    
    les_mots = msg.split(" ")
    mots=["dispo","disponible","propretaire","prop","gestionnaire","voie entree","entree","sortie",
               "voie sortie","adresse","coordonnées gps" ,"gps","latitude","longitude","lat","lon",
               "capacite","capacite de voiture","voiture","capacite de place PMR","capacite de place pmr",
               "pmr","Mobilite reduite","annee fabrication","annee","fabrication","type de parking","type",
               "capacite de velo","velo","situation","vocation","usage","gratuit","reglement","prix","payant",
               "fermeture","horaire","temps","temp","nom","commune","ville","code postal","code","postal","cp",
               "capacite auto partage","capacite vehicule partage","partage" ]
        
    nb_mots=0
    a=""
    for i in les_mots:
        i=i.lower()
        if i in ["dispo","disponible"] :
            for index, row in data_real_time.iterrows():
               if row["Parking_schema:identifier"]==df["idfournisseur"] :
                   a = "\n"+"le parcking "+ df["nom"] + " a "+str(row["mv:currentValue"])+" places vides "
                   break
            if a =="":
                a = "\n"+"Malheuresement ,nous n'avons pas la disponibilité pour ce parking "
    
    mots_s_dispo=["propretaire","prop","gestionnaire","voie entree","entree","sortie",
               "voie sortie","adresse","coordonnées gps" ,"gps","latitude","longitude","lat","lon",
               "capacite","capacite de voiture","voiture","capacite de place PMR","capacite de place pmr",
               "pmr","Mobilite reduite","annee fabrication","annee","fabrication","type de parking","type",
               "capacite de velo","velo","situation","vocation","usage","gratuit","reglement","prix","payant",
               "fermeture","horaire","temps","temp","nom","commune","ville","code postal","code","postal","cp",
               "capacite auto partage","capacite vehicule partage","partage" ]
    for d in mots_s_dispo :
        d=d.lower()
        msg=msg.lower()
        nb_m = msg.find(d)
        if nb_m != -1 :
            if d in ["capacite auto partage","capacite vehicule partage","partage"]:
                rep = rep +"\n"+" \n la capacité auto partage de ce parking est "+str(df["capaciteautopartage"])
                break
            if d in ["code postal","code","postal","cp"]:
                rep = rep +"\n"+" \n la code postal de ce parking est "+str(df["insee"])
                break
            if d in ["commune","ville"]:
                rep = rep +"\n"+" \n la commune de ce parking est "+str(df["commune"])
                break
            if d in ["nom"]:
                rep = rep +"\n"+" \n le nom de ce parking est "+str(df["nom"])
                break
            if d in ["fermeture","horaire","temps","temp"]:
                rep = rep +"\n"+" \n l'horaire' de ce parking est "+str(df["fermeture"])
                break
            if d in ["reglement","prix","gratuit","payant"]:
                rep = rep +"\n"+" \n le type de règlement  de ce parking est "+str(df["reglementation"])
                break
            if d in ["usage"]:
                rep = rep +"\n"+" \n l'usage de ce parking est "+str(df["usage"])
                break
            if d in ["vocation"]:
                rep = rep +"\n"+" \n la vocation de ce parking est "+str(df["vocation"])
                break
            if d in ["capacite de velo","velo"]:
                rep = rep +"\n"+" \n la capacité de vélo de ce parking est "+str(df["capacitevelo"])
                break
            if d in ["capacite de velo","velo"]:
                rep = rep +"\n"+" \n la capacité de vélo de ce parking est "+str(df["capacitevelo"])
                break
            if d in ["type de parking","type","situation"]:
                rep = rep +"\n"+" \n le type de ce parking est "+str(df["typeparking"])+" ,"+ str(df["situation"])
                break
            if d in ["propretaire","prop"]:
                rep = rep +"\n"+" \n le propretaire de ce parking est "+str(df["propretaire"])
                break
            if d in ["gestionnaire"]:
                rep = rep +"\n"+" \n le gestionnaire de ce parking est "+str(df["gestionnaire"] )
                break
            if d in ["voie entree","entree"]:
                rep = rep +"\n"+" \n le voie d'entrée de ce parking est "+str(df["voieentree"]) 
                break
            if d in ["voie sortie","sortie"]:
                rep = rep +"\n"+" \n le voie de sortie de ce parking est "+str(df["voiesortie"])
                break
            if d in ["adresse","coordonnées gps" ,"gps","latitude","longitude","lat","lon"]:
                rep = rep +"\n"+" \n l'adresse de ce parking est : longitude  " +str(df["lon"]) +"  latitude  "+str(df["lat"])
                break
            if d in ["capacite","voiture","capacite de voiture"]:
                rep = rep +"\n"+" \n le capacité de voiture dans ce parking est "+str(df["capacite"] )
                break
            if d in ["capacite de place pmr","capacite de place PMR","pmr","Mobilite reduite"]:
                rep = rep +"\n"+" \n le capacité de de place PMR dans ce parking est "+str(df["capacite2rm"] )
                break
            if d in ["annee fabrication","annee","fabrication"]:
                rep = rep +"\n"+" \n l'année fabrication dans ce parking est "+str(df["annee"] )
                break
                

   
    reponse = str(rep) + str(a)
    return reponse
               
               
               
def answer(msg):
    
    
 
    reponse=""
    
    
    nettoyer_msg(msg)
    les_mots = msg.split(" ")
    
    new_df = pd.DataFrame()
    for i in les_mots:
        if i.isdigit():
            if len(i)>1 :
                
                new_df,reponse=fonction_code_postal(i)
                break;
                
    if reponse=="":
    
        new_df,rep,answer = fonction_Commune(msg)
        if answer is bool(False) :
            id_parking=""
            id_four=""
            if (new_df.empty):
                new_df=data_detaille
            data={}
            data,id_four = fonction_Parking(new_df,msg)
            
            id_parking = fonction_id_Parking(new_df,msg)
            
            nb=""
            nb=disponible(id_four)
            
            if nb != "":
                
                reponse = reponse + str(nb)
                
            
        else :
            
            reponse = rep
    
        mots=["dispo","disponible","propretaire","prop","gestionnaire","voie entree","entree","sortie",
                   "voie sortie","adresse","coordonnées gps" ,"gps","latitude","longitude","lat","lon",
                   "capacite","capacite de voiture","voiture","capacite de place PMR","capacite de place pmr",
                   "pmr","Mobilite reduite","annee fabrication","annee","fabrication","type de parking","type",
                   "capacite de velo","velo","situation","vocation","usage","gratuit","reglement","prix","payant",
                   "fermeture","horaire","temps","temp","nom","commune","ville","code postal","code","postal","cp",
                   "capacite auto partage","capacite vehicule partage","partage" ]
            
        nb_mots=0
        for i in les_mots:
            for k in mots:
                i=i.lower()
                k=k.lower()
                print (k)
                print(i)
                match2 = i.find(k)
                if match2 != -1:
                    nb_mots=nb_mots+1
                    
        if nb_mots != 0:
            reponse=answer_detaills(e.get(),data)
  
    return reponse
    
    
    
def envoie():
    res =""
    envoie = "Moi :" +e.get()
    res =res + envoie +" "
    txt.insert(END, "\n"+envoie)
    if 'bonjour' in e.get():           
        txt.insert(END,"\n"+ "ChatBot : Bonjour  ,vous voulez des information sur quel parking, "+ 
                   "vous pouvez nous donnez votre code postal afin de vous suggérer des parkings"
                   +"?")
        res =res + "ChatBot : Bonjour  ,vous voulez des information sur quel parking, vous pouvez nous donnez votre code postal afin de vous suggérer des parkings ?"
      
    elif  'bonjour' in e.get():           
        txt.insert(END,"\n"+ "ChatBot : Bonjour  ,vous voulez des information sur quel parking, "+ 
                       "vous pouvez nous donnez votre code postal afin de vous suggérer des parkings"
                       +"?")
        res =res + "ChatBot : Bonjour  ,vous voulez des information sur quel parking, vous pouvez nous donnez votre code postal afin de vous suggérer des parkings ?"
      
    elif 'Au revoir' in e.get():
        res =res + "ChatBot : A Bientôt"
      
        txt.insert(END,"\n"+ "ChatBot : A Bientôt")
        root.quit
        
    else :
        res =res + "ChatBot : "+ answer(e.get())
        reponse=answer(e.get())
        txt.insert(END,"\n"+ "ChatBot :" + reponse) 
        
    e.delete(0,END)
    enregistrement(res) 
    
    #return discussion
    
    
    
data_real_time=import_donnee_reel_time()
data_detaille=import_donnee_detail()

#enregistrement=""
txt =Text(root , font=("arial",12))
txt.insert(END, "\n"+ "ChatBot : Bonjour que puis-je faire pour vous ?")
#enregistrement=enregistrement+"ChatBot : Bonjour que puis-je faire pour vous ?"
txt.grid(row=0,column=0,columnspan=2)
e=Entry(root,width=100)
e.grid(row=1,column=0)
envoyer=Button(root,text="Envoyer",command=envoie).grid(row=1,column=1)
#enregistrement=enregistrement+envoie()

root.title("ChatBot")
root.mainloop()