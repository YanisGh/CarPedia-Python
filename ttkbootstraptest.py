from tkinter import *
import ttkbootstrap as tb
import requests
from io import BytesIO
from PIL import Image, ImageTk

def get_image_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = ImageTk.PhotoImage(img)
        return img
    else:
        print("Failed to retrieve the image")
        return None

#Car data retrieval and displaying
#------------------------------
def fetch_single_car_info():
    #brand/model par defaut pck flm de les inputs a chaque fois dans les entry
    #A supprimer
    brand = "Audi"
    model = "R8"
    # brand = brand_entry.get().capitalize()
    # model = model_entry.get().capitalize()

    url = f"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/all-vehicles-model/records?limit=-1&refine=make%3A\"{brand}\"&refine=model%3A\"{model}\"" 
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
    

        years = Label(notebook_info_year, text=f"{sorted_years}",width=50, height=5, wraplength=200)
        years.pack(padx=10, pady=10)

        engines = Label(notebook_info_engine, text=f"{engines_combined}",width=50, height=5, wraplength=200)
        engines.pack(padx=10, pady=10)

        transmission = Label(notebook_info_transmission, text=f"{transmissions_combined}",width=50, height=5, wraplength=200)
        transmission.pack(padx=10, pady=10)

        drive = Label(notebook_info_drive, text=f"{drives_combined}",width=50, height=5, wraplength=200)
        drive.pack(padx=10, pady=10)

        notebook_info.add(notebook_info_year, text="Year")
        notebook_info.add(notebook_info_engine, text="Engine")
        notebook_info.add(notebook_info_transmission, text="Transmission")
        notebook_info.add(notebook_info_drive, text="Drive")
        #------------------------------
        #Car displaying   
#Car data retrieval
#-------------------------------

#darkly/cyborg
root = tb.Window(themename="darkly")
root.title("CarPedia")
root.iconbitmap("images/logo.ico")
root.geometry('1000x600')

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

#Car data submission
#------------------------------
submit_entries_button = tb.Button(text="Search for your vehicle", bootstyle="primary", command=fetch_single_car_info)
submit_entries_button.pack(pady=20)
#------------------------------
#Car data submission


root.mainloop()



