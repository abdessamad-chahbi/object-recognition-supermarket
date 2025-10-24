import mysql.connector as cnx
import os,random

class Connexion : 
    def __init__(self) -> None:
        self.mydb = cnx.connect(
                            host="localhost",
                            user="root",
                            password="",
                            database="dbprodui"
                            )
        
    def getProduit(self,produit) : 
        mycursor = self.mydb.cursor()
        sql = "SELECT * FROM `produits` WHERE `produiLabel` ="+"'"+produit+"'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()[0]
        #resultat sous form tuple (produitLabel,quantite,prix)
        return myresult