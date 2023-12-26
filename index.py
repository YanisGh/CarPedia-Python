import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def submit_data():
    brand = entry_brand.get()
    model = entry_model.get()
    print(f"Car data submitted: Brand - {brand}, Model - {model}")

# def submit_data_plate():
#     url = "https://www.paruvendu.fr/fiches-techniques-auto/"
#     webbrowser.open(url)
#     plate = entry_plate.get()
#     print(f"Car data submitted: Plate - {plate}")

def submit_data_plate():
    #To get rid of the "-" 
    plate_from_entry = entry_plate.get().replace("-","")
    print(f"Car data submitted: Plate - {plate_from_entry}")
    driver = webdriver.Chrome()   
    url = "https://www.paruvendu.fr/fiches-techniques-auto/"
    driver.get(url)
    time.sleep(2)
    license_field = driver.find_element('xpath','//*[@id="immatriculation"]')
    license_field.send_keys(plate_from_entry)
    time.sleep(2)
    submit_license_btn = driver.find_element('xpath','//*[@id="btnValidImmat"]')
    submit_license_btn.click()
    time.sleep(20)

# Create a blank window
windowIndex = tk.Tk()
windowIndex.title("CarPedia")  # Set window title
windowIndex.geometry("400x300")  # Sets window size to width 400px and height 300px

# Create labels
label_brand = tk.Label(windowIndex, text="Enter Car Brand:")
label_brand.pack()

# Entry for Car Brand
entry_brand = tk.Entry(windowIndex)
entry_brand.pack()

# Create label for Car Model
label_model = tk.Label(windowIndex, text="Enter Car Model:")
label_model.pack()

# Entry for Car Model
entry_model = tk.Entry(windowIndex)
entry_model.pack()

# Submit button
submit_button = tk.Button(windowIndex, text="Submit", command=submit_data)
submit_button.pack()

# Create label for Car Model
label_plate = tk.Label(windowIndex, text="Enter license plate:")
label_plate.pack()

# Entry for license plate
entry_plate = tk.Entry(windowIndex)
entry_plate.pack()

# Submit button
submit_button_plate = tk.Button(windowIndex, text="Submit", command=submit_data_plate)
submit_button_plate.pack()

# Run the main loop
windowIndex.mainloop()
