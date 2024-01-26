from tkinter import *
from tkinter import messagebox
import string
from random import randint, choice, shuffle
import os
import json
import pyperclip

FONT = "Courier"
BG_COLOR = "#FDF0D1"
BUTTON_COLOR = "#F79594"
password_file = "my_passwords.json"


# Password function
def password_gen(n: int, num: int, symbol: int):
	assert 8 <= n <= 15, f"Error! Password must be from 8 to 15 characters."
	assert 1 <= num <= 4, f"Error! From 1 to 4 digits recommended."
	assert 1 <= symbol <= 2, f"Error! Not more than two symbols recommended."

	# instantiate lists of characters to use in password
	uppers = list(string.ascii_lowercase)
	lowers = list(string.ascii_uppercase)
	numbers = [str(i) for i in range(0, 10)]
	symbols = "!@#$%^&*-_+=<>?/()"

	# Compute length of password alphabets
	alpha_len = n - (num + symbol)
	upper_len = randint(1, alpha_len - 1)
	lower_len = alpha_len - upper_len

	# instantiate list of randomly selected characters from initial lists
	num_list = [choice(numbers) for _ in range(num)]
	sym_list = [choice(symbols) for _ in range(symbol)]
	upper_list = [choice(uppers) for _ in range(upper_len)]
	lower_list = [choice(lowers) for _ in range(lower_len)]

	# Combine the lists of characters into single list and shuffle
	password_list = num_list + sym_list + upper_list + lower_list
	shuffle(password_list)

	# Join all characters in the list to form a single password
	password = "".join(password_list)

	return password


# A function to display the generated password
def retrieve_password():
	random_password = password_gen(15, 2, 2)
	password_entry.delete("0", END)
	password_entry.insert("insert", random_password)
	pyperclip.copy(password_entry.get())


# A function to raise warning for bad entries
def warn(num):
	win = Toplevel(
		width=200, height=400,
		bg=BG_COLOR,
		padx=20, pady=40
	)
	lab = Label(
		win, text="",
		font=(FONT, 20, "bold"),
		bg=BG_COLOR, fg="red"
	)
	if num == 1:
		lab.config(text="All details MUST be entered!")
	elif num == 2:
		lab.config(text="Password MUST contain:\none uppercase,\none number,\nand one symbol")
	elif num == 3:
		lab.config(text="Website already in use.")
	elif num == 4:
		lab.config(text="Invalid email!")
	lab.grid(row=1, column=1)


# A function to delete entries
def delete_entries():
	for widget in [website_entry, password_entry]:
		widget.delete(0, END)


# A function to check if entry exists in file
def check_file(data, entry):
	if any(key == entry for key in data.keys()):
		return True


# A function to manage data
def manage_data(new_entry):
	ask = messagebox.askokcancel(
		title=f"{website_entry}",
		message=f"You have entered\nWebsite: {website_entry.get()}\nUsername: {username_entry.get()}"
				f"\n Press 'Okay' to continue or 'Cancel' to cancel"
	)
	if ask:
		if os.path.isfile(password_file):  # Check if file exists
			# Read the file and update with new data
			with open(password_file, "r") as f:
				old_data = json.load(f)
				key = list(new_entry.keys())[0]  # Grab the website entry
				result = check_file(data=old_data, entry=key)  # Check if website already exits
			if not result:
				old_data.update(new_entry)
				# Write mew data to file
				with open(password_file, "w") as f:
					json.dump(old_data, f, indent=4)
			else:
				warn(3)
		else:  # If file does not exist, create the file
			with open(password_file, "w") as f:
				json.dump(new_entry, f, indent=4)
	else:
		delete_entries()


# A function to extract and save user details
def extract_details():
	# Extract the entries
	website = website_entry.get().strip()
	username = username_entry.get().strip()
	password = password_entry.get().strip()
	details = {
		website: {
			"Username": username,
			"Password": password,
		}
	}

	# Validate the entries
	if any(len(detail) == 0 for detail in [website, username, password]):
		warn(1)
	elif not (any(char.isupper() for char in password) and any(char.isnumeric() for char in password) and any(
			char in "!@#$%^&*-_+=<>?/" for char in password)):
		warn(2)
	elif "@" in username:
		if any((("." not in username), (username[-1] == "."), (username[::-1][1] == "."))):
			warn(4)
	else:
		manage_data(new_entry=details)
		delete_entries()


# A function to search data and retrieve website details:
def search():
	website = website_entry.get().strip()
	try:
		with open(password_file, "r") as f:
			data = json.load(f)
	except FileNotFoundError:
		messagebox.showinfo(
			title="No File Error",
			message=f"File {password_file} not found in directory!"
		)
	except json.JSONDecodeError:
		messagebox.showinfo(
			title="File Empty Error",
			message=f"File {password_file} is currently empty!"
		)
	else:
		if len(website) == 0:
			messagebox.showinfo(
				title="Website info",
				message="The website entry is empty\nKindly provide a website name"
			)
		elif website in list(data.keys()):
			username = data[website]["Username"]
			password = data[website]["Password"]
			messagebox.showinfo(
				title="Website info",
				message=f"Website: {website}\nEmail/Username: {username}\nPassword: {password}"
			)
		else:
			messagebox.showinfo(
				title="Website info",
				message=f"No website: {website} found in database."
			)


# Create and configure the window
window = Tk()
window.title("Password Manager")
window.config(bg=BG_COLOR, padx=50, pady=50)

for n in range(1, 5):
	window.rowconfigure(n, weight=1)  # Let each row from 1 to 4 have equal weight

# Intatiate a photo image from file
logo = PhotoImage(file="password icon.png")

# A canvas to hold image in first row
canvas = Canvas(
	width=360, height=242,
	highlightthickness=0,
	bg=BG_COLOR
)
canvas.create_image(
	125, 121,
	image=logo
)
canvas.grid(row=1, column=1, columnspan=2)

# Lable for website entry
l1 = Label(
	window,
	text="Website",
	bg=BG_COLOR,
	font=(FONT, 13)
)
l1.grid(row=2, column=0, sticky="W")

# Frame contianing website entry and search button
f1 = Frame(window, width=46, bg=BG_COLOR)
f1.grid(pady=3, row=2, column=1)

# An entry for website name
website_entry = Entry(
	f1,
	justify="left",
	width=20,
	borderwidth=2,
	bg="white",
	font=("Arial", 14),
)
website_entry.grid(row=0, column=0, sticky="NS")

# The button to search records
b1 = Button(
	f1,
	text="Search records",
	font=(FONT, 13),
	height=2,
	width=17,
	bg=BUTTON_COLOR,
	command=search
)
b1.grid(row=0, column=1, sticky="E")

# Label for the username/e-mail entry
l2 = Label(
	window,
	text="Username/Email",
	bg=BG_COLOR,
	font=(FONT, 13)
)
l2.grid(row=3, column=0, sticky="W")

# Entry to retrieve username
username_entry = Entry(
	window,
	justify="left",
	width=40,
	borderwidth=2,
	bg="white",
	font=(FONT, 13),
)
username_entry.insert(0, "patrickonodje@gmail.com")
username_entry.grid(row=3, column=1)

# A label for the password entry
l3 = Label(
	window,
	text="Password",
	bg=BG_COLOR,
	font=(FONT, 13)
)
l3.grid(row=4, column=0, sticky="W")

# A frame to hold password entry and button to generate random password
f2 = Frame(window, width=46, bg=BG_COLOR)
f2.grid(pady=3, row=4, column=1)

# The password entry
password_entry = Entry(
	f2,
	justify="left",
	width=20,
	borderwidth=2,
	bg="white",
	font=("Arial", 14),
)
password_entry.grid(row=0, column=0, sticky="NS")

# Button to generate a random password
b2 = Button(
	f2,
	text="Generate Password",
	font=(FONT, 13),
	height=2,
	width=17,
	bg=BUTTON_COLOR,
	command=retrieve_password
)
b2.grid(row=0, column=1, sticky="E")

# A button to update/add records to file
b3 = Button(
	window,
	text="Add",
	font=(FONT, 13),
	height=2,
	width=17,
	bg=BUTTON_COLOR,
	command=extract_details
)
b3.grid(pady=5, row=5, column=1, columnspan=2)

# Loop the window to keep it running till closed
window.mainloop()
