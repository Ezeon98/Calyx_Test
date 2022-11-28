from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import xlsxwriter

#Opciones de Navegacion
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

driver_path = 'chromedriver.exe'

driver = webdriver.Chrome(driver_path, chrome_options=options)

#Inicia el navegador
driver.get('https://www.bna.com.ar/Personas')

#Buscar Dato
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                       '/html/body/main/div/div/div[4]/div[1]/div/div/div[1]/table')))

table_text = driver.find_element(By.XPATH,'/html/body/main/div/div/div[4]/div[1]/div/div/div[1]/table')


#Procesar texto
table_text = table_text.text

info = table_text.split()
info = [w.replace(',','.') for w in info]

dolar_mean = (float(info[5]) + float(info[6])) / 2
eur_mean = (float(info[8]) + float(info[9])) / 2
real_mean = (float(info[12]) + float(info[13])) / 2

#Armar Excel
workbook = xlsxwriter.Workbook('Cotizaciones.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(0,0, 'Dia')
worksheet.write(0,1, info[0])
worksheet.write(1,0, 'Moneda')
worksheet.write(1,1, 'Compra')
worksheet.write(1,2, 'Venta')
worksheet.write(1,3, 'Promedio')
worksheet.write(2,0, 'Dolar')
worksheet.write(3,0, 'Euro')
worksheet.write(4,0, 'Real')
worksheet.write(2,1, info[5])
worksheet.write(2,2, info[6])
worksheet.write(2,3, dolar_mean)
worksheet.write(3,1, info[8])
worksheet.write(3,2, info[9])
worksheet.write(3,3, eur_mean)
worksheet.write(4,1, info[12])
worksheet.write(4,2, info[13])
worksheet.write(4,3, real_mean)

workbook.close()

driver.quit()
