import requests
modelli={}
link='https://mivv.com/wp-content/themes/mivv/getModelli.php?lang=it&marca='
with open('lista_modelli.csv','r') as file:
 for riga in file:
  marchio,modello,id = riga.strip().split(';')
  modelli[id]=(marchio,modello)
for id,(marchio,modello) in modelli.items():
 risposta=requests.get(link+id)
 dato=risposta.json()
 for elementi in dato:
  anni=elementi['value'].replace('&gt;','-')
  id_anni=elementi['id']
  f=open('listacompleta_modelli.csv','a')
  f.write(id + ';' + marchio + ';' + modello + ';' + anni + ';' + str(id_anni) + "\n")
  f.close()