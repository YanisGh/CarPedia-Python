import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests

# def submit_data():
#     brand = entry_brand.get()
#     model = entry_model.get()
#     print(f"Car data submitted: Brand - {brand}, Model - {model}")

def fetch_car_info(brand, model):
    # URL of the API you want to fetch data from
    url = f"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/all-vehicles-model/records?limit=1&refine=make%3A\"{brand}\"&refine=model%3A\"{model}\""

    print(url)  
    # Make the API request
    response = requests.get(url)

    if response.status_code == 200:
        print("Car data retrieved")
        car_data = response.json()  # Assuming the API returns JSON data

        # Extract 'make' and 'model' from the JSON response under the 'results' key
        if 'results' in car_data and car_data['results']:
            make = car_data['results'][0].get('make', 'N/A')
            model = car_data['results'][0].get('model', 'N/A')

            print(f"Make: {make}, Model: {model}")
            return make, model
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
    showCarInfo(model, brand)

#Window to show retrieved car data from submit_data
def showCarInfo(model, brand):
    carInfo = tk.Tk()
    carInfo.title("Retrieved car data") 
    carInfo.geometry("600x350")
    label_brand = tk.Label(carInfo, text=f"Brand - {brand}, Model - {model}")
    label_brand.pack()
    fetch_car_info(brand, model)

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
