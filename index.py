import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests
from io import BytesIO
from PIL import Image, ImageTk

# def submit_data():
#     brand = entry_brand.get()
#     model = entry_model.get()
#     print(f"Car data submitted: Brand - {brand}, Model - {model}")



def fetch_single_car_info(brand, model):
    # URL of the API you want to fetch data from
    brand = "Audi"
    model = "R8"

    url = f"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/all-vehicles-model/records?limit=-1&refine=make%3A\"{brand}\"&refine=model%3A\"{model}\""

    print(url)  
    # Make the API request
    response = requests.get(url)

    if response.status_code == 200:
        car_data = response.json()
        carInfo = tk.Tk()
        carInfo.title("Retrieved Car Data")
        carInfo.geometry("600x350")
        # retrieved_image = get_image_from_url("https://i.pinimg.com/736x/10/96/de/1096de000517b30cd2c97ca4744c1f2e.jpg")
        # if retrieved_image:
        #     label = tk.Label(windowIndex, image=retrieved_image)
        #     label.pack()
        canvas = tk.Canvas(carInfo)
        canvas.place(relx=0.65, rely=1, anchor='center')

        scrollbar = tk.Scrollbar(carInfo, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


        if 'results' in car_data and car_data['results']:
            make = car_data['results'][0].get('make', 'N/A')
            model = car_data['results'][0].get('model', 'N/A')
            vclass = car_data['results'][0].get('vclass', 'N/A')

            make_label = tk.Label(frame, text=f"Make: {make}")
            make_label.pack(anchor='center')

            model_label = tk.Label(frame, text=f"Model: {model}")
            model_label.pack(anchor='center')

            vclass_label = tk.Label(frame, text=f"Vehicle type: {vclass}")
            vclass_label.pack(anchor='center')

            for car_info in car_data['results']:
                year = car_info.get('year', 'N/A')
                cylinders = car_info.get('cylinders', 'N/A')
                displacement = car_info.get('displ', 'N/A')
                transmission = car_info.get('trany', 'N/A')
                drive = car_info.get('drive', 'N/A')

                info_frame = tk.Frame(frame, relief=tk.GROOVE, borderwidth=2)
                info_frame.pack(padx=5, pady=5, anchor='center', fill=tk.X)

                year_label = tk.Label(info_frame, text=f"Year: {year}")
                year_label.pack(anchor='center')

                cylinders_label = tk.Label(info_frame, text=f"{cylinders} cylinders")
                cylinders_label.pack(anchor='center')

                displacement_label = tk.Label(info_frame, text=f"{displacement}L of displacement")
                displacement_label.pack(anchor='center')

                transmission_label = tk.Label(info_frame, text=f"{transmission} transmission")
                transmission_label.pack(anchor='center')

                drive_label = tk.Label(info_frame, text=f"Drive: {drive}")
                drive_label.pack(anchor='center')

        else:
            print("Make and model not found in the response")
            return None, None
    else:
        print("Failed to fetch car data from the API")
        return None, None

def submit_data():
    brand = entry_brand.get().capitalize()
    model = entry_model.get().capitalize()
    print(f"Car data submitted: Brand - {brand}, Model - {model}")
    fetch_single_car_info(brand, model)

def retrieve_data_plate():
    #To get rid of the "-" 
    plate_from_entry = entry_plate.get().replace("-","")
    print(f"Car data submitted: Plate - {plate_from_entry}")
    driver = webdriver.Chrome()   
    url = "https://www.paruvendu.fr/fiches-techniques-auto/"
    driver.get(url)
    #fill out plate number in field
    license_field = driver.find_element('xpath','//*[@id="immatriculation"]')
    license_field.send_keys(plate_from_entry)
    #click on submit button
    submit_license_btn = driver.find_element('xpath','//*[@id="btnValidImmat"]')
    submit_license_btn.click()
    time.sleep(20)



# Create a blank window
windowIndex = tk.Tk()
windowIndex.title("CarPedia")  # Set window title
windowIndex.geometry("600x350")

# Create labels
label_brand = tk.Label(windowIndex, text="Enter Car Brand:")
label_brand.pack()

# TextBox for Car Brand
entry_brand = tk.Entry(windowIndex)
entry_brand.pack()

# Create label for Car Model
label_model = tk.Label(windowIndex, text="Enter Car Model:")
label_model.pack()

# TextBox for Car Model
entry_model = tk.Entry(windowIndex)
entry_model.pack()

# Submit button
submit_button = tk.Button(windowIndex, text="Submit", command=submit_data)
submit_button.pack()

# Create label for Car Model
label_plate = tk.Label(windowIndex, text="Enter license plate:")
label_plate.pack()

# TextBox for license plate
entry_plate = tk.Entry(windowIndex)
entry_plate.pack()

# Submit button
retrieve_button_plate = tk.Button(windowIndex, text="Submit", command=retrieve_data_plate)
retrieve_button_plate.pack()

# Run the main loop
windowIndex.mainloop()
