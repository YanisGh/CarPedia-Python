from tkinter import *
import ttkbootstrap as tb
import requests
import time
import base64
from io import BytesIO
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

#To get rid of the "-" 
#plate_from_entry = license_plate_entry.get().replace("-","")
plate_from_entry = "AN684FH" #ED427BH #AN684FH #DT405RH #AG963SR
print(f"Car data submitted: Plate - {plate_from_entry}")
driver = webdriver.Chrome()   
url = "https://www.paruvendu.fr/fiches-techniques-auto/"
driver.get(url)
#Pour accepter les cookies si il y'a le prompt
accept_cookies_btn = driver.find_element('xpath','//*[@id="step1"]/div[3]/button[2]')
if accept_cookies_btn: 
    accept_cookies_btn.click()
#fill out plate number in field
license_field = driver.find_element('xpath','//*[@id="immatriculation"]')
license_field.send_keys(plate_from_entry)
#click on submit button
submit_license_btn = driver.find_element('xpath','//*[@id="btnValidImmat"]')
submit_license_btn.click()
time.sleep(1)
try:
    error_element = driver.find_element('xpath', '//*[@id="pap_err_cuImmat"]').text
    print(f"error element : {error_element}.")
    # If there is an error
    if error_element:
        print(f"error element detected: {error_element}")
        time.sleep(60)
        if error_element == "":
            print("No license found + error element empty")
            time.sleep(20)
    else:
        # If error_element is not found, or if it's an empty string, continue with the code
        # Get car pic
        car_img = driver.find_element('xpath', "/html/body/div[3]/div[1]/div[5]/div[1]/div[1]/div/p/img").get_attribute("src")
        print(f"car img : {car_img}")

except NoSuchElementException:
    # If the element was not found, continue with the rest of the code
    
    # response = requests.get(url)
    # image = Image.open(BytesIO(response.content))
    # car_image = ImageTk.PhotoImage(image)

    #Type du véhicule  
    try:
        submit_finition = driver.find_element('xpath','/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/form/div/input')
        # Execute JavaScript to click the button 
        if submit_finition: 
            driver.execute_script("arguments[0].click();", submit_finition)
            print("bouton finition appuyer")
    except NoSuchElementException:
            #Get car pic
            print("pas de bouton")
    car_type = driver.find_element('xpath',"/html/body/div[3]/div[1]/div[5]/div[3]/div[1]/ul/li[1]/span").text
    print(f"car type : {car_type}")
    #Mecanique
    car_engine = driver.find_element('xpath', '//*[@id="auto_pv_ongOn0TAB"]/div/div/table/tbody/tr[2]/td[2]/span').text
    car_displacement = driver.find_element('xpath', '//*[@id="auto_pv_ongOn0TAB"]/div/div/table/tbody/tr[3]/td[2]/span').text
    car_hp = driver.find_element('xpath', '/html/body/div[3]/div[1]/div[5]/div[3]/div[1]/ul/li[3]/span').text
    car_fuel = driver.find_element('xpath', '/html/body/div[3]/div[1]/div[5]/div[3]/div[1]/ul/li[2]/span').text
    print(f"Moteur {car_fuel} de {car_engine} de {car_displacement} développant {car_hp}")

    car_max_speed = driver.find_element('xpath', '/html/body/div[3]/div[1]/div[5]/div[3]/div[1]/ul/li[6]/span').text
    print(f"Vitesse max : {car_max_speed}")

    car_gearbox_gear = driver.find_element('xpath', '//*[@id="auto_pv_ongOn0TAB"]/div/div/table/tbody/tr[7]/td[2]/span').text
    car_gearbox_type = driver.find_element('xpath', '/html/body/div[3]/div[1]/div[5]/div[3]/div[1]/ul/li[4]/span').text
    print(f"Boite de vitesses : Boite {car_gearbox_type} à {car_gearbox_gear} rapports")

    car_0to100 = driver.find_element('xpath', '//*[@id="auto_pv_ongOn0TAB"]/div/div/table/tbody/tr[10]/td[2]/span').text
    print(f"0-100km/h : {car_0to100}")

    car_period_prod = driver.find_element('xpath', '//*[@id="auto_pv_ongOn0TAB"]/div/div/table/tbody/tr[18]/td[2]/span').text
    print(f"Periode de production : {car_period_prod}")

    car_price_new = driver.find_element('xpath', '//*[@id="auto_pv_ongOn0TAB"]/div/div/table/tbody/tr[19]/td[2]/span').text
    print(f"Prix neuf : {car_price_new}")
    driver.quit()