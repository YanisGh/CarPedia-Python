from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import filedialog
import requests
import time
import base64
from io import BytesIO
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
from PIL import Image
import os



#Car data retrieval and displaying from entry search
#------------------------------
image_references = {}  
def fetch_single_car_info():
    car_name = ""
    search_status_label.config(text="")
    search_status_label.config(text="Searching for vehicle", bootstyle ="info")

    year_provided = False
    brand_search = brand_entry.get().replace(" ", "").capitalize()
    model_search = model_entry.get().replace(" ", "").capitalize()
    year_search = year_entry.get()

    if year_search.isdigit():
        year_provided = True
    
    if not brand_search.strip() or not model_search.strip():
       search_status_label.config(text="Please enter a vehicle", bootstyle ="danger")
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
                car_name = f"{make} {model} \n{vclass}"

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
                label_img = tb.Label(result_frame, image=tk_image)
                label_img.pack()
                car_label = tb.Label(result_frame, text=f"{car_name}")
                car_label.pack(pady=10)
                
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
                
                notebook_info = tb.Notebook(result_frame, bootstyle="dark")
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
                search_status_label.config(text="Vehicle found successfully !", bootstyle ="success")
                #------------------------------
                #Car displaying   

                def delete_vehicule():
                    car_label.destroy()
                    label_img.destroy()
                    notebook_info.destroy()
                    delete_vehicule_button.destroy()
                    search_status_label.config(text="")
                delete_vehicule_button = tb.Button(result_frame, text="Delete Vehicle", bootstyle="danger", command=delete_vehicule)
                delete_vehicule_button.pack(pady=10)   

            else:
                search_status_label.config(text="No vehicle has been found in the API", bootstyle="danger")
#------------------------------
#Car data retrieval and displaying from entry search


#License plate caracters to extract
#-------------------------------
def get_image_plate():
    filename = filedialog.askopenfilename()
    if filename:
        reader = easyocr.Reader(['en'])
        img = cv2.imread(f'{filename}')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
        #("gray",gray)
        # cv2.waitKey(0)
        bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
        edged = cv2.Canny(bfilter, 50, 250) #Edge detection
        plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
        #("edged",edged)
        # print(reader.readtext(edged))
        # cv2.waitKey(0)
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break
        print(location)
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0,255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)
        plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
        #("new img",new_image)
        # cv2.waitKey(0)
        (x,y) = np.where(mask==255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]
        plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        #("cropped",cropped_image)
        # cv2.waitKey(0)
        #reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)[0][1]
        print(result)
        retrieve_data_plate(result)
    else:
        search_status_license_label.config(text="Error getting the image", bootstyle = "danger")
        #return result 
#-------------------------------
#License plate caracters to extract


#Car data retrieval and displaying from license search
#------------------------------
image_references_plate = {}
def retrieve_data_plate(license_plate=None):
    #To get rid of the "-" 
    #if we took the license plate from the entry
    if license_plate is None:
        license_plate = license_plate_entry.get()
    #plate_from_entry = "ED427BH" #ED427BH #AN684FH #DT405RH #AG963SR
    symbols_to_replace = [' ', '-', ';', ',', '.', ':', '!', '*']
    for symbol in symbols_to_replace:
        license_plate = license_plate.replace(symbol, "")
    print(f"Car data submitted: Plate - {license_plate}")
    driver = webdriver.Chrome()   
    url = "https://www.paruvendu.fr/fiches-techniques-auto/"
    driver.get(url)
    #Pour accepter les cookies si il y'a le prompt
    accept_cookies_btn = driver.find_element('xpath','//*[@id="step1"]/div[3]/button[2]')
    if accept_cookies_btn: 
        accept_cookies_btn.click()
    #fill out plate number in field
    license_field = driver.find_element('xpath','//*[@id="immatriculation"]')
    license_field.send_keys(license_plate)
    #click on submit button
    time.sleep(1)
    submit_license_btn = driver.find_element('xpath','//*[@id="btnValidImmat"]')
    submit_license_btn.click()
    time.sleep(1)
    try:
        error_element = driver.find_element('xpath', '//*[@id="pap_err_cuImmat"]').text
        # If there is an error
        if error_element:
            print(f"error element detected: {error_element}")
            search_status_license_label.config(text=f"ERREUR : {error_element}", bootstyle ="danger")
            if error_element == "":
                print("No license found + error element empty")
                time.sleep(20)
        else:
            #for some reason when i delete the line below and just leave the print, 
            #it just stops there when trying a car with trim options, it doesn't even enter the fucking else statement 
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
        car_img_url = driver.find_element('xpath',"/html/body/div[3]/div[1]/div[5]/div[1]/div[1]/div/p/img").get_attribute("src")
        #print(f"car img : {car_img_url}")
        # response = requests.get(url)
        # image = Image.open(BytesIO(response.content))
        # car_image = ImageTk.PhotoImage(image)
        
        #Type du véhicule  
        car_type = driver.find_element('xpath',"/html/body/div[3]/div[1]/div[5]/div[3]/div[1]/ul/li[1]/span").text
        car_name = driver.find_element('xpath',"/html/body/div[3]/div[1]/div[3]/div[1]/div/div[1]/h1").text
        
        #Mecanique
        car_max_speed = driver.find_element('xpath', '/html/body/div[3]/div[1]/div[5]/div[3]/div[1]/ul/li[6]/span').text
        car_max_speed_details = (f"Vitesse max : {car_max_speed}")

        car_gearbox_gear = driver.find_element('xpath', '//*[@id="auto_pv_ongOn0TAB"]/div/div/table/tbody/tr[7]/td[2]/span').text
        car_gearbox_type = driver.find_element('xpath', '/html/body/div[3]/div[1]/div[5]/div[3]/div[1]/ul/li[4]/span').text
        car_gearbox_details = (f"Boite de vitesses : Boite {car_gearbox_type} à {car_gearbox_gear} rapports")

        car_0to100 = driver.find_element('xpath', '//*[@id="auto_pv_ongOn0TAB"]/div/div/table/tbody/tr[10]/td[2]/span').text
        car_0to100_details = (f"0-100km/h en {car_0to100}")
        car_engine = driver.find_element('xpath', '//*[@id="auto_pv_ongOn0TAB"]/div/div/table/tbody/tr[2]/td[2]/span').text
        car_displacement = driver.find_element('xpath', '//*[@id="auto_pv_ongOn0TAB"]/div/div/table/tbody/tr[3]/td[2]/span').text
        car_hp = driver.find_element('xpath', '/html/body/div[3]/div[1]/div[5]/div[3]/div[1]/ul/li[3]/span').text
        car_fuel = driver.find_element('xpath', '/html/body/div[3]/div[1]/div[5]/div[3]/div[1]/ul/li[2]/span').text
        car_technical_details = (f"Moteur {car_fuel} de {car_engine} de {car_displacement} développant {car_hp}. \n" 
                                f"{car_0to100_details} et {car_max_speed_details}. \n"
                                f"{car_gearbox_details}")

        car_period_prod = driver.find_element('xpath', '//*[@id="auto_pv_ongOn0TAB"]/div/div/table/tbody/tr[18]/td[2]/span').text
        #print(f"Periode de production : {car_period_prod}")

        car_price_new = driver.find_element('xpath', '//*[@id="auto_pv_ongOn0TAB"]/div/div/table/tbody/tr[19]/td[2]/span').text
        #print(f"Prix neuf : {car_price_new}")
        car_misc_details = (f"Periode de production : {car_period_prod}. \n" 
                            f"Prix neuf : {car_price_new}")
        

        car_name_label = tb.Label(result_frame, text=f"{car_name}", bootstyle="light")
        car_name_label.pack(pady=10)

        response = requests.get(car_img_url)
        img_data = response.content
        # Open the image using Pillow
        image = Image.open(BytesIO(img_data))

        # Convert the image to Tkinter PhotoImage
        tk_image = ImageTk.PhotoImage(image)
        image_references_plate["img"] = tk_image
        # Create a label and display the image
        label_img = tb.Label(result_frame, image=tk_image)
        label_img.pack(pady= 10)

        notebook_info = tb.Notebook(result_frame, bootstyle="dark")
        notebook_info.pack()

        notebook_info_technique = tb.Frame(notebook_info)
        notebook_info_misc = tb.Frame(notebook_info)

        #fetch needed car details

        detail = Label(notebook_info_technique, text=f"{car_technical_details}",width=30, height=15, wraplength=200)
        detail.pack(padx=10, pady=10)
        detail = Label(notebook_info_misc, text=f"{car_misc_details}",width=30, height=15, wraplength=200)
        detail.pack(padx=10, pady=10)
        search_status_license_label.config(text="Vehicule trouvée !", bootstyle="success")

        notebook_info.add(notebook_info_technique, text="Details techniques du véhicule")
        notebook_info.add(notebook_info_misc, text="Details généraux du véhicule")

        def delete_vehicule():
            search_status_license_label.config(text="")
            car_name_label.destroy()
            label_img.destroy()
            notebook_info.destroy()
            delete_vehicule_button.destroy()
            
        delete_vehicule_button = tb.Button(result_frame, text="Delete Vehicle", bootstyle="danger", command=delete_vehicule)
        delete_vehicule_button.pack(pady=10)
        driver.quit()
        print("Finished")
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

search_status_label = tb.Label(text="", bootstyle="danger")
search_status_label.pack(pady=5)

submit_entries_button = tb.Button(text="Search for your vehicle", bootstyle="primary", command=fetch_single_car_info)
submit_entries_button.pack(pady=20)

license_plate_entry_label = tb.Label(text="Enter your license plate :", bootstyle="info")
license_plate_entry_label.pack(pady=10)
license_plate_entry = tb.Entry(root, bootstyle="primary",
                            width=30)
license_plate_entry.pack()

license_plate_entry_button = tb.Button(text="Search for your vehicle using a license plate", bootstyle="primary", command=retrieve_data_plate)
license_plate_entry_button.pack(pady=20)

license_plate_photo_button = tb.Button(text="Or use a photo", bootstyle="secondary", command=get_image_plate)
license_plate_photo_button.pack()

search_status_license_label = tb.Label(text="", bootstyle="danger")
search_status_license_label.pack()

separator = tb.Separator(root, bootstyle="light")
separator.pack(fill="x", padx=400)

result_frame = ScrolledFrame(root, autohide=False)
result_frame.pack(fill=BOTH, expand=YES)


#------------------------------
#Car data submission


root.mainloop()



