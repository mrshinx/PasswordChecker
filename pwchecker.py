import requests
import hashlib
import tkinter as tk
from PIL import Image, ImageTk


def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check api and try again')
    return res


def get_leaks_count(hashes, hash_to_check):
    # Separate hash and count
    hashes = (line.split(':') for line in hashes.text.splitlines())
    # Check if the same password has been leaked and return the number of times it has been leaked, else return 0
    for h, count in hashes:
        if h == hash_to_check:
            return result.config(text=f'This password has been leaked {count} times. Pick another password.')
    return result.config(text=f'This password has never been leaked!')


def pwned_api_check(password):
    # Convert password from string to SHA1 hash, displayed in hexadecimal with upper case
    sha1pw = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    # Get first 5 char for the API, also the rest of the hash for comparison
    first5_char, tail = sha1pw[:5], sha1pw[5:]
    # Create request and get response
    response = request_api_data(first5_char)
    get_leaks_count(response, tail)


# Define window object
root = tk.Tk()
root.geometry('600x300')
root.title("Password Checker")
# Logo
logo = Image.open('logo.png')  # Open Logo as png
logo = ImageTk.PhotoImage(logo)  # Convert to Tkinter Image
logo_label = tk.Label(root, image=logo).place(x=-40, y=-150)

# Password entry
user_password = tk.Label(root, text="Password").place(x=40, y=100)
user_password_entry_area = tk.Entry(root, width=30)
user_password_entry_area.place(x=110, y=100)
# Check button
check_button = tk.Button(root, text="Check", command=lambda: pwned_api_check(user_password_entry_area.get())).place(
    x=40, y=130)
# Result text
result = tk.Label(root, text="")
result.place(x=40, y=160)

root.mainloop()
