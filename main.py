from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import pyperclip
import json

lower_letters = list("qwertyuiopasdfghjklzxcvbnm")
upper_letters = list("QWERTYUIOPASDFGHJKLZXCVBNM")
symbols = list("!@#%^&*-")
numbers = list("1234567890")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def gen_pass():
    entry_3.delete(0, END)
    password_as_list = []
    password_as_list += [choice(lower_letters) for _ in range(randint(8, 10))]
    password_as_list += [choice(upper_letters) for _ in range(randint(2, 4))]
    password_as_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_as_list += [choice(numbers) for _ in range(randint(2, 4))]
    shuffle(password_as_list)
    password = "".join(password_as_list)
    pyperclip.copy(password)
    entry_3.insert(END, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_pass():

    site_name = entry_1.get().title()
    email = entry_2.get()
    password = entry_3.get()

    # Error Check if file Exists or Not
    try:
        file = open("data.json", mode="r")
    except FileNotFoundError:
        file = open("data.json", mode="w")
        file.close()
        data_as_dict = {}
    else:
        # Error Check if file empty or not
        try:
            data_as_dict = json.load(file)
        except:
            with open("data.json") as file:
                if not file.read(1):
                    data_as_dict = {}
        finally:
            entry_1.delete(0, END)
            entry_3.delete(0, END)
            data = {
                site_name: {
                    "email": email,
                    "password": password
                }
            }

        file.close()

    # Update Pass or Not
    if site_name.title() in data_as_dict.keys():
        continue_ = messagebox.askyesno("", "This site's password has already been saved\n"
                                            "Do you want to update the password? ")
        if continue_:
            data_as_dict.update(data)
            with open("data.json", mode="w") as file:
                json.dump(data_as_dict, file, indent=4)
    # Add Data
    elif site_name and email and password != "":
        confirmed = messagebox.askokcancel(title="Conformation", message=f"Website: {site_name}\n"
                                                                         f"Email: {email}\n"
                                                                         f"Password: {password}\n"
                                                                         f"Do you want to save this data?")
        if confirmed:
            data_as_dict.update(data)
            with open("data.json", mode="w") as file:
                json.dump(data_as_dict, file, indent=4)
    # Unfilled Fields
    else:
        messagebox.showwarning(title="", message="Fill in all the fields!")


# ------------------------ PASSWORD RETRIEVAL ------------------------- #

def retrieve_pass():

    # Error check if file DNE/Empty
    try:
        with open("data.json") as file:
            data = json.load(file)
    except:
        messagebox.showwarning("", "There are no entries in the password manager yet!")
    else:

        # Check if website data available or not
        try:
            site_info = data[entry_1.get().title()]
        except KeyError:
            messagebox.showwarning("", "No data associated with this site was found")
        else:
            email = site_info["email"]
            password = site_info["password"]
            messagebox.showinfo("", f"Email: {email}\nPassword: {password}")

# ---------------------------- UI SETUP ------------------------------- #

# Window
window = Tk()
window.title("Password Manager")
window.minsize(width=240, height=240)
window.config(padx=50, pady=40)

# Entries
entry_1 = Entry(width=50)
entry_1.focus()
entry_1.grid(column=1, row=1, columnspan=2)
entry_2 = Entry(width=50)
entry_2.insert(END, "ranvirsran.here@gmail.com")
entry_2.grid(column=1, row=2, columnspan=2)
entry_3 = Entry()
entry_3.grid(column=1, row=3, sticky="EW")

# Buttons
button_1 = Button(text="Generate Password", pady=0, padx=0, command=gen_pass)
button_1.grid(column=2, row=3, sticky="EW")
button_2 = Button(text="Add", command=save_pass)
button_2.grid(column=1, row=4, columnspan=2, sticky="EW")
button_3 = Button(text="Search", padx=0, pady=0, command=retrieve_pass)
button_3.grid(column=2, row=1, sticky="EW")

# Labels
label_1 = Label(text="Website")
label_1.grid(column=0, row=1)
label_2 = Label(text="Email Address")
label_2.grid(column=0, row=2)
label_3 = Label(text="Password")
label_3.grid(column=0, row=3)

# Image
canvas = Canvas(width=200, height=190, highlightthickness=0)
my_img = PhotoImage(file="logo.png")
canvas.create_image(100, 95, image=my_img)
canvas.grid(column=0, row=0, columnspan=3)

window.mainloop()
