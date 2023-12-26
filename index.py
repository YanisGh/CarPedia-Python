import tkinter as tk

def submit_data():
    brand = entry_brand.get()
    model = entry_model.get()
    print(f"Car data submitted: Brand - {brand}, Model - {model}")

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

# Run the main loop
windowIndex.mainloop()
