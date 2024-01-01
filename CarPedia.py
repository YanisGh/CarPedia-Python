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


#Car data retrieval and displaying from entry search
#------------------------------
image_references = {}
def fetch_single_car_info():
    error_label.config(text="")
    #brand/model par defaut pck flm de les inputs a chaque fois dans les entry
    #A supprimer
    # brand = "Ford"
    # model = "Mustang"
    # year = ""
    year_provided = False
    brand_search = brand_entry.get().capitalize()
    model_search = model_entry.get().capitalize()
    year_search = year_entry.get()

    if year_search.isdigit():
        year_provided = True
    
    if not brand_search.strip() or not model_search.strip():
        error_label.config(text="Please enter a vehicle")
    else:
        # image = Image.open("r8test.jpg")
        # image_tk = ImageTk.PhotoImage(image)
        # image_references["img"] = image_tk  # Store image reference

        # label_img = Label(root, image=image_tk)
        # label_img.pack()

        url = f"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/all-vehicles-model/records?limit=-1&refine=make%3A\"{brand_search}\"&refine=model%3A\"{model_search}\"" 
        response = requests.get(url)
        
        #If successfull get data
        if response.status_code == 200:
            car_data = response.json()
            if 'results' in car_data and car_data['results']:
                make = car_data['results'][0].get('make', 'N/A')
                model = car_data['results'][0].get('model', 'N/A')
                vclass = car_data['results'][0].get('vclass', 'N/A')
                years = []
                engines = []
                transmissions = []
                drives = []
                #Car image displaying if it finds a car
                #------------------------------  
                # Set Chrome options to run in headless mode
                options = Options()
                options.add_argument("--headless=new")
                # Initialize Chrome driver with the specified options
                driver = webdriver.Chrome(options=options)
                # Open Google Images and search for the query

                #If user provided a year
                if year_provided:
                    url_img = f"https://www.google.com/search?q={year_search}+{make}+{model}"
                else:
                    url_img = f"https://www.google.com/search?q={make}+{model}"

                print(url_img)
                driver.get(url_img)
                accept_google_btn = driver.find_element('xpath','//*[@id="L2AGLb"]/div')
                accept_google_btn.click()
                google_img_btn = driver.find_element('xpath','//*[@id="bqHHPb"]/div/div/div[1]/a[1]/div')
                google_img_btn.click()

                img = driver.find_element('xpath','//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img').get_attribute("src")
                img_data = img.split(',')[1]
                decoded_img = base64.b64decode(img_data)
                image = Image.open(BytesIO(decoded_img))
                tk_image = ImageTk.PhotoImage(image)
                image_references["img"] = tk_image
                # Create a label and display the image
                label_img = tb.Label(root, image=tk_image)
                label_img.pack()
                #------------------------------
                #Car image displaying
                for car_info in car_data['results']:
                    year = car_info.get('year', 'N/A')
                    years.append(year)

                    cylinders = car_info.get('cylinders', 'N/A')
                    displacement = car_info.get('displ', 'N/A')
                    engine_description = f"{displacement}L engine with {cylinders} cylinders"
                    engines.append(engine_description)

                    transmission = car_info.get('trany', 'N/A')
                    transmission_description = f"{transmission} transmission"
                    transmissions.append(transmission_description)

                    drive = car_info.get('drive', 'N/A')
                    drive_description = f"{drive}"
                    drives.append(drive_description)

                sorted_years = sorted(list(set(years)))
                sorted_transmissions = sorted(list(set(transmissions)))
                sorted_drives = sorted(list(set(drives)))
                sorted_engines = sorted(list(set(engines)))

                # car_name_label = tb.Label(text=f"{make} {model} \n{vclass}", bootstyle="light")
                # car_name_label.pack(padx=300, pady=10)
                
                engines_combined = "\n ".join(sorted_engines)
                transmissions_combined = "\n ".join(sorted_transmissions)
                drives_combined = "\n ".join(sorted_drives)

                #Car displaying
                #------------------------------
                notebook_info = tb.Notebook(root, bootstyle="dark")
                notebook_info.pack()

                notebook_info_year = tb.Frame(notebook_info)
                notebook_info_engine = tb.Frame(notebook_info)
                notebook_info_transmission = tb.Frame(notebook_info)
                notebook_info_drive = tb.Frame(notebook_info)

                #fetch needed car details

                years = Label(notebook_info_year, text=f"{sorted_years}",width=30, height=15, wraplength=200)
                years.pack(padx=10, pady=10)

                engines = Label(notebook_info_engine, text=f"{engines_combined}",width=30, height=15, wraplength=200)
                engines.pack(padx=10, pady=10)

                transmission = Label(notebook_info_transmission, text=f"{transmissions_combined}",width=30, height=15, wraplength=200)
                transmission.pack(padx=10, pady=10)

                drive = Label(notebook_info_drive, text=f"{drives_combined}",width=30, height=15, wraplength=200)
                drive.pack(padx=10, pady=10)

                notebook_info.add(notebook_info_year, text="Year")
                notebook_info.add(notebook_info_engine, text="Engine")
                notebook_info.add(notebook_info_transmission, text="Transmission")
                notebook_info.add(notebook_info_drive, text="Drive")
                #------------------------------
                #Car displaying   

                def delete_vehicule():
                    label_img.destroy()
                    notebook_info.destroy()
                    delete_vehicule_button.destroy()
                delete_vehicule_button = tb.Button(root, text="Delete Vehicle", bootstyle="danger", command=delete_vehicule)
                delete_vehicule_button.pack(pady=10)   
        #Car data retrieval and displaying from entry search
        #-------------------------------
            else:
                error_label.config(text="No vehicle has been found in the database")

#Car data retrieval and displaying from license search
#------------------------------
def retrieve_data_plate():
    #To get rid of the "-" 
    #plate_from_entry = license_plate_entry.get().replace("-","")
    plate_from_entry = "ED427BH"
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
        error_element = driver.find_element('xpath', '//*[@id="pap_err_cuImmat"]')
        if error_element:
            error_license_label.config(text="No license plates found")
            time.sleep(20)
    except NoSuchElementException:
        pass  # Element was not found, continue with the rest of the code
        
        #Get car pic
        car_img = driver.find_element('xpath',"/html/body/div[3]/div[1]/div[5]/div[1]/div[1]/div/p/img").get_attribute("src")
        print(f"car img : {car_img}")
        # response = requests.get(url)
        # image = Image.open(BytesIO(response.content))
        # car_image = ImageTk.PhotoImage(image)
        
        #Type du véhicule  
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
#------------------------------ 
#Car data retrieval and displaying from license search
    

#darkly/cyborg
root = tb.Window(themename="darkly")
root.title("CarPedia")
root.iconbitmap("images/logo.ico")
root.geometry('1000x600')

#Car data submission
#------------------------------
brand_entry_label = tb.Label(text="Your car's brand :", bootstyle="info")
brand_entry_label.pack(pady=10)
brand_entry = tb.Entry(root, bootstyle="primary",
                            width=30)
brand_entry.pack()

model_entry_label = tb.Label(text="Your car's model :", bootstyle="info")
model_entry_label.pack(pady=10)
model_entry = tb.Entry(root, bootstyle="primary",
                            width=30)
model_entry.pack()

year_entry_label = tb.Label(text="Your car's year :", bootstyle="info")
year_entry_label.pack(pady=10)
year_entry = tb.Entry(root, bootstyle="primary",
                            width=30)
year_entry.insert(0, '(Optional)')
year_entry.pack()

error_label = tb.Label(text="", bootstyle="danger")
error_label.pack(pady=5)

submit_entries_button = tb.Button(text="Search for your vehicle", bootstyle="primary", command=fetch_single_car_info)
submit_entries_button.pack(pady=20)

license_plate_entry_label = tb.Label(text="Enter your license plate :", bootstyle="info")
license_plate_entry_label.pack(pady=10)
license_plate_entry = tb.Entry(root, bootstyle="primary",
                            width=30)
license_plate_entry.pack()
license_plate_entry_button = tb.Button(text="Search for your vehicle using a license plate", bootstyle="primary", command=retrieve_data_plate)
license_plate_entry_button.pack(pady=20)
error_license_label = tb.Label(text="", bootstyle="danger")
error_label.pack(pady=5)
#------------------------------
#Car data submission


root.mainloop()



