import requests
marchi={}
import csv
link='https://mivv.com/wp-content/themes/mivv/getModelli.php?lang=it&marca='
with open('filemoto.csv','r') as file: 
 for riga in file:
  marchio,id = riga.strip().split(';') 
  marchi[id]=marchio
for id, marchio in marchi.items():
 risposta = requests.get(link+id) 
 data=risposta.json()
 for elementi in data:
  id_modello=elementi['id']
  modello=elementi['value']  
  f=open('lista_modelli.csv','a')
  f.write(marchio + ';' + modello + ';' + str(id_modello) + "\n")
  f.close()