from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


#  TODO 1 Encrypt (with a key) the passwords and copy saved passwords to a clipboard
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """ Generates a password with a random number of characters between 12 and 18.
        Specifically 8-10 Letters, 2-4 symbols, and 2-4 numbers.  The order of these
        characters is shuffled before being returned by the function to the Entry box.
        Copies generated passwords to a clipboard to allow the password to be pasted
        directly into the website.
    """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
               'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
               'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
               'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '~', '^', '[', ']', '{', '}', '']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    generated_password = "".join(password_list)
    password_input.insert(END, generated_password)
    pyperclip.copy(generated_password)


def save():
    """ Saves the website, username, and password
        to a json file.  Clears the website and password
        fields.
    """
    website = site_input.get()
    username = username_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "username": username,
            "password": password,
        }
    }

    if not all([website, username, password]):
        messagebox.showerror(title="Error", message="1 or more fields were left blank! \n Complete all fields to "
                                                    "continue.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            # Clear Entries
            site_input.delete(0, END)
            password_input.delete(0, END)


def find_password():
    """ Searches the json file to provide the username and password
        for the website entered.
    """
    website = site_input.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")
    else:
        if website in data:
            username = data[website]["username"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {username} \nPassword: {password}")
        else:
            messagebox.showerror(title="Error", message=f"No details for {website} exists.")


#  TODO 2 Change aesthetics of the Canvas and Window
# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
site_label = Label(text="Website:")
site_label.grid(column=0, row=1)
username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
site_input = Entry(width=16)
site_input.grid(column=1, row=1, sticky="EW")
site_input.focus()
username_input = Entry(width=35)
username_input.grid(column=1, row=2, columnspan=2, sticky="EW")
username_input.insert(END, "malcombbrown@gmail.com")
password_input = Entry(width=16)  # show="*" will display *'s instead of letters
password_input.grid(column=1, row=3, sticky="EW")

# Buttons
generate_btn = Button(text="Generate Password", command=generate_password)
generate_btn.grid(column=2, row=3, sticky="EW")
add_btn = Button(text="Add", width=36, command=save)
add_btn.grid(column=1, row=4, columnspan=2, sticky="EW")
search_btn = Button(text="Search", command=find_password)
search_btn.grid(column=2, row=1, sticky="EW")

window.mainloop()
