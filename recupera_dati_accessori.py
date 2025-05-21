import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback
listacodici=[]
opzioni=Options()
opzioni.add_argument('headless')
opzioni.add_argument('start-maximized')
with open('listasku.csv','r') as file:
 for riga in file:
  listacodici.append(riga.strip())     
browser=webdriver.Chrome(options=opzioni)
browser.get('https://mivv.com/')
time.sleep(5)
for codice in listacodici:
 dati_uniti=''
 modello_scarico=''
 foto_unite=''
 try:
  browser.find_elements(By.CLASS_NAME,'form-group')[0].find_elements(By.TAG_NAME,'input')[0].send_keys(codice + Keys.ENTER)
  articoli=WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.CLASS_NAME,'blog-item-title')))
  link_articolo=browser.find_elements(By.CLASS_NAME,'blog-item-title')[0].find_elements(By.TAG_NAME,'a')[0].get_attribute('href')
  browser.get(link_articolo)
  tipo_veicolo=WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.CLASS_NAME,'label-moto-box')))
  try:
   moto=browser.find_elements(By.CLASS_NAME,'label-moto-box')[0].get_attribute('innerText')
  except Exception:
   moto='ERRORE RECUPERO TIPO VEICOLO'
  try:
   modello_scarico=browser.find_elements(By.CLASS_NAME,'nome-scarico')[0].find_elements(By.CLASS_NAME,'linea-scarico')[0].get_attribute('innerText').replace('\n','').strip()
  except Exception:
   modello_scarico=''    
  try:
   materiale_scarico=browser.find_elements(By.CLASS_NAME,'nome-scarico')[0].find_elements(By.CLASS_NAME,'allestimento-scarico')[0].get_attribute('innerText').replace('\n','').strip()
  except Exception:
   materiale_scarico=''
  if modello_scarico != '' or materiale_scarico != '':
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
   f=open('foto-accessori.csv','a')
   f.write(dati_uniti + ';' + moto +';' + foto_unite + "\n")
   f.close() 
  try: #COSTO
   costo=browser.find_element(By.ID,'riquadro-prezzo').get_attribute('innerText').split('\n')[1].replace('€','').replace(' ','')   
  except Exception:
   costo=''   
  try:
   f=open('accessori.csv','a')
   f.write(dati_uniti + ';' + nome_articolo + ';' + moto + ';' + descrizione + ';' + costo + "\n")
   f.close()
  except Exception:
   traceback.print_exc()    
 except Exception:
  traceback.print_exc()
 browser.get('https://mivv.com/')
 time.sleep(5) 