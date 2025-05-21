import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import traceback
opzioni=Options()
opzioni.add_argument('start-maximized')
#opzioni.add_argument('headless')
browser=webdriver.Chrome(options=opzioni)
browser.get('https://mivv.com/')
time.sleep(3)
numero_marche=len(browser.find_element(By.ID,'marca_moto').find_elements(By.TAG_NAME,'option'))
for i in range(24,numero_marche): # CAMBIA CON 1 SE VUOI FARE RIPARTIRE --> SI ERA BLOCCATO A MV AUGUSTA
 try:
  marchio_moto=browser.find_element(By.ID,'marca_moto').find_elements(By.TAG_NAME,'option')[i].get_attribute('innerText')
  id_moto=browser.find_element(By.ID,'marca_moto').find_elements(By.TAG_NAME,'option')[i].get_attribute('value')
  #f=open('filemoto.csv','a')
  #f.write(marchio_moto + ';' + id_moto + "\n")
  #f.close()
  browser.execute_script("document.getElementsByClassName('btn dropdown-toggle menu-btn btn-label')[0].click()")
  time.sleep(2)
  browser.find_elements(By.CLASS_NAME,'dropdown-menu.open')[0].find_elements(By.TAG_NAME,'a')[i].click()
  time.sleep(2)
  browser.execute_script("document.getElementsByClassName('btn dropdown-toggle menu-btn btn-label')[1].click()")
  time.sleep(2)
  numero_modelli=len(browser.find_elements(By.CLASS_NAME,'dropdown-menu.open')[1].find_elements(By.TAG_NAME,'a'))
  for j in range(1,numero_modelli):
   numero_articoli=0
   if j > 1:
    browser.execute_script("document.getElementsByClassName('btn dropdown-toggle menu-btn btn-label')[1].click()")   
    print('aperto')
   modello_moto=browser.find_elements(By.CLASS_NAME,'dropdown-menu.open')[1].find_elements(By.TAG_NAME,'a')[j].find_elements(By.TAG_NAME,'span')[0].get_attribute('innerText')
   browser.find_elements(By.CLASS_NAME,'dropdown-menu.open')[1].find_elements(By.TAG_NAME,'a')[j].click()
   time.sleep(2)
   browser.find_elements(By.CLASS_NAME,'btn.search-btn')[0].click()
   time.sleep(5)
   print(marchio_moto + ';' + modello_moto)
   try:
    numero_articoli=len(browser.find_element(By.ID,'cards-scarichi').find_elements(By.CLASS_NAME,'grid-element'))
   except Exception:   
    numero_articoli=0
   for k in range(numero_articoli):
    link=browser.find_element(By.ID,'cards-scarichi').find_elements(By.CLASS_NAME,'grid-element')[k].find_elements(By.TAG_NAME,'a')[0].get_attribute('href')
    f=open('listalink.csv','a')
    f.write(marchio_moto + ';' + modello_moto + ';' + link + "\n")
    f.close()
   browser.get('https://mivv.com/')
   time.sleep(2)
   browser.execute_script("document.getElementsByClassName('btn dropdown-toggle menu-btn btn-label')[0].click()")
   time.sleep(2)
   browser.find_elements(By.CLASS_NAME,'dropdown-menu.open')[0].find_elements(By.TAG_NAME,'a')[i].click()
   time.sleep(2)
 except Exception:
  browser.get('https://mivv.com/')
  time.sleep(15)  