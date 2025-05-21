import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import traceback
import time
import re
dati_uniti=''
lista_link={}
conta=int(0)
fileinput='listalink.csv'
fileoutput='dati.csv'
filefoto='foto.csv'
file_dati_tecnici='dati-tecnici.csv'
with open(fileinput,'r') as file:
 for riga in file:
  marchio,modello,link=riga.strip().split(';')
  lista_link[conta]=(marchio,modello,link)
  conta=conta+1
opzioni=Options()
opzioni.add_argument('start-maximized')
opzioni.add_argument('headless')
browser=webdriver.Chrome(options=opzioni)
for conta,(marchio,modello,link) in lista_link.items():
 try:
  link_prestazioni=''
  foto_unita=''
  costo=''
  colorazione=''
  colorazioni_unite=''
  dati_uniti=''
  omologazione_unita=''
  tipo_veicolo=''
  tabella_miglioramento=''
  browser.get(link)
  time.sleep(5)
  try:
   tipo_veicolo=browser.find_elements(By.CLASS_NAME,'vehicle-type__label')[0].get_attribute('innerText')
  except Exception:
   tipo_veicolo='ERRORE RECUPERO TIPO VEICOLO'      
  try:
   moto=browser.find_elements(By.CLASS_NAME,'label-moto-box')[0].get_attribute('innerText')
  except Exception:
   moto=''      
  try:
   modello_scarico=browser.find_elements(By.CLASS_NAME,'nome-scarico')[0].find_elements(By.CLASS_NAME,'linea-scarico')[0].get_attribute('innerText').replace('\n','').strip()
  except Exception:
   modello_scarico=''    
  try:
   materiale_scarico=browser.find_elements(By.CLASS_NAME,'nome-scarico')[0].find_elements(By.CLASS_NAME,'allestimento-scarico')[0].get_attribute('innerText').replace('\n','').strip()
  except Exception:
   materiale_scarico=''    
  if modello_scarico != '' and materiale_scarico != '':
   nome_articolo=modello_scarico + ' ' + materiale_scarico
  else:
   nome_articolo='NOME MANCANTE'   
  try:
   numero_dati=len(browser.find_element(By.ID,'dati-scarico').find_elements(By.XPATH,".//div[@class='singolo-dato-scarico']"))
  except Exception:
   numero_dati = 0   
  for i in range(numero_dati):
   dato=browser.find_element(By.ID,'dati-scarico').find_elements(By.XPATH,".//div[@class='singolo-dato-scarico']")[i].find_elements(By.CLASS_NAME,'etichetta-dato')[0].get_attribute('innerText').replace('\n','').strip()
   valore=browser.find_element(By.ID,'dati-scarico').find_elements(By.XPATH,".//div[@class='singolo-dato-scarico']")[i].find_elements(By.CLASS_NAME,'valore-dato')[0].get_attribute('innerText').replace('\n','').strip()
   if dati_uniti == '':
    dati_uniti=dato+': '+valore
   else:
    dati_uniti=dati_uniti+'$'+dato+': '+valore   
  try:
   numero_omologazioni=len(browser.find_element(By.ID,'dati-scarico').find_elements(By.CLASS_NAME,'fa.fa-thumbs-o-up'))
   for j in range(numero_omologazioni):
    omologazione=browser.find_element(By.ID,'dati-scarico').find_elements(By.CLASS_NAME,'fa.fa-thumbs-o-up')[j].find_element(By.XPATH,'..').get_attribute('innerText')
    omologazione_unita=omologazione_unita+'$'+omologazione   
  except Exception:
   omologazione_unita=''
  try:
   descrizione=browser.find_element(By.ID,'testo-prodotto').get_attribute('innerText').replace('\n','').strip()
  except Exception:
   descrizione='' 
  try: #BLOCCO FOTO
   numero_foto=len(browser.find_elements(By.CLASS_NAME,'cycle-slideshow')[0].find_elements(By.TAG_NAME,'img'))
   foto_prima=browser.find_elements(By.CLASS_NAME,'cycle-slideshow')[0].find_elements(By.TAG_NAME,'img')[numero_foto-1].get_attribute('src')+';1$'
   for x in range(1,numero_foto-1):
    foto=browser.find_elements(By.CLASS_NAME,'cycle-slideshow')[0].find_elements(By.TAG_NAME,'img')[x].get_attribute('src')
    foto_unita=foto_unita+foto+';'+str((x+1))+'$'
   foto_unite=foto_prima+foto_unita
  except Exception:
   try:
    foto_unite=browser.find_element(By.ID,'foto-scarico').find_elements(By.TAG_NAME,'img')[0].get_attribute('src')
   except Exception:
    foto_unite=''
  f=open(filefoto,'a')
  f.write(dati_uniti + ';' + moto +';' + foto_unite + "\n")
  f.close()  
  try: #CORRELATI COLORAZIONI 
   numero_colorazioni=len(browser.find_element(By.ID,'altri-scarichi-wrapper').find_elements(By.CLASS_NAME,'card-prodotto')[0].find_elements(By.CLASS_NAME,'codice-scarico'))
   if numero_colorazioni == 1:   
    colorazioni_unite=browser.find_element(By.ID,'altri-scarichi-wrapper').find_elements(By.CLASS_NAME,'card-prodotto')[0].find_elements(By.CLASS_NAME,'codice-scarico')[0].get_attribute('innerText')
   if numero_colorazioni >1 :
    for conta_colori in range(numero_colorazioni):
     colorazione=browser.find_element(By.ID,'altri-scarichi-wrapper').find_elements(By.CLASS_NAME,'card-prodotto')[conta_colori].find_elements(By.CLASS_NAME,'codice-scarico')[0].get_attribute('innerText')
     colorazioni_unite=colorazioni_unite+'$'+colorazione          
  except Exception:
   pass
   colorazione=''      
  try:
   omologazione_catalizzatore=len(browser.find_elements(By.CLASS_NAME,'badge-omologazione')[0].find_elements(By.XPATH,".//button[contains(@title, 'sia omologato è necessario montare il catalizzatore opzionale')]"))  
  except Exception:
   omologazione_catalizzatore=''
  try:
   numero_accessori=len(browser.find_element(By.ID,'accessori-scarico-wrapper').find_elements(By.CLASS_NAME,'card-prodotto'))
   if numero_accessori == 1:
    accessori_uniti=browser.find_element(By.ID,'accessori-scarico-wrapper').find_elements(By.CLASS_NAME,'card-prodotto')[0].find_elements(By.CLASS_NAME,'codice-scarico')[0].get_attribute('innerText')
   if numero_accessori > 1:
    for conta_accessori in range(numero_accessori):        
     accessorio=browser.find_element(By.ID,'accessori-scarico-wrapper').find_elements(By.CLASS_NAME,'card-prodotto')[conta_accessori].find_elements(By.CLASS_NAME,'codice-scarico')[0].get_attribute('innerText')
     accessori_uniti=accessori_uniti+'$'+accessorio
  except Exception:
   accessori_uniti=''       
  try: #ESPLOSO TECNICO
   link_esploso=browser.find_element(By.ID,'docs-scarico').find_elements(By.XPATH,".//span[@class='docs-label' and ./text()='Schematic']")[0].find_element(By.XPATH,'..').get_attribute('href')     
  except Exception:
   link_esploso=''
  try: #PDF PRESTAZIONI
   link_prestazioni=browser.find_element(By.ID,'docs-scarico').find_elements(By.XPATH,".//span[@class='docs-label' and ./text()='Dynochart']")[0].find_element(By.XPATH,'..').get_attribute('href')  
  except Exception:
   link_prestazioni=''      
  try: #TABELLA MIGLIORAMENTO
   tabella_miglioramento=browser.find_element(By.ID,'tabella-scarico').find_elements(By.TAG_NAME,'table')[0].get_attribute('innerHTML').replace('\n','').replace('<br>','').strip().replace('  ','')
   tabella_miglioramento=re.sub('<!--.*?-->', '',tabella_miglioramento)
   tabella_miglioramento="<div class='mega-table-mivv'><table>"+tabella_miglioramento+'</table></div>'
   tabella_miglioramento=tabella_miglioramento.replace('Max Power','Potenza massima').replace('Max Torque','Coppia massima')   
  except Exception:
   tabella_miglioramento=''      
  try: #COSTO
   costo=browser.find_element(By.ID,'riquadro-prezzo').get_attribute('innerText').split('\n')[1].replace('€','').replace(' ','')   
  except Exception:
   costo=''      
  try: #VIDEO YOUTUBE
   video_youtube=browser.find_element(By.ID,'movie_player').find_elements(By.CLASS_NAME,'ytp-impression-link')[0].get_attribute('href').split(';embeds')[0]   
  except Exception:
   video_youtube=''      
 except Exception:
  traceback.print_exc()
 '''
 try:
  f=open(fileoutput,'a')
  f.write(dati_uniti + ';' + omologazione_unita + ';' + descrizione + ';' + moto + "\n")
  f.close() 
 except Exception:
  traceback.print_exc()
 '''
 try:
  f=open(file_dati_tecnici,'a')
  f.write(dati_uniti + ';' + moto + ';' + str(costo) + ';' + omologazione_unita + ';' + str(omologazione_catalizzatore) + ';' + colorazioni_unite + ';' + accessori_uniti + ';' + video_youtube + ';' + tipo_veicolo + ';' + tabella_miglioramento + ';' + link_esploso + ';' + link_prestazioni + "\n")
  f.close() 
 except Exception:
  traceback.print_exc()     