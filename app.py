import random
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pyperclip # type: ignore
import re

# Główne założenia aplikacji
root = Tk()
root.title("Safe Pass")

window_width = 800
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

root.call('wm', 'iconphoto', root._w, PhotoImage(file='image/logo.png'))

root.config(background = "#EEEEF0")



# Icons
menu_icon = PhotoImage(file="image/menu.png")
menu_open_icon = PhotoImage(file="image/menu_open.png")
copy_icon = PhotoImage(file="image/copy.png")
hide_icon = PhotoImage(file="image/hide.png")
check_icon = PhotoImage(file="image/check.png")
refresh_icon = PhotoImage(file="image/refresh.png")
loop_icon = PhotoImage(file="image/loop.png")
show_icon = PhotoImage(file="image/eye.png")




# Dictionaries - słowniki potrzebne do szyfrowania haseł
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
          'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
lettersUpper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
special = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
full = list(letters)
full.extend(lettersUpper)
full.extend(numbers)
full.extend(special)

# User file - plik użytkownika 
user_file = "files/passwords/"

# Password file - plik z kontami jakie są w apce
password_file = "files/password.txt"





# Global table - tabela globalna z hasłami użytkownika
password_table = None


# Toggle password - funkcja odsłaniająca hasło
def toggle_password(password_entry):
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
    else:
        password_entry.config(show='*')


# Random number - Generowanie losowej liczby z przedziału
def rand(min,max):
    random_number = random.randint(min, max)
    return random_number


# Random True/False - Generowanie prawda lub fałsz
def rand_logic():
    random_number = random.randint(1, 2)
    if random_number == 1:
        return True
    else:
        return False


# Save to file - Zapis do pliku
def save_to_file(password, name, file_path):
    text = name + " " + password
    try:
        with open(file_path, "a") as file:
            file.write(text + "\n")
        print("Password saved successfully.")
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except PermissionError:
        print(f"Error: Permission denied to write to {file_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Code Password - Szyfrowanie hasła
def code_password(password):
    try:
        if not password:
            print("Error: Password cannot be empty.")
            return ""
        full_reverse = full[::-1]
        password_coded = []
        for char in password:
            if char in full:
                index = full.index(char)
                password_coded.append(full_reverse[index])
            else:
                print(f"Warning: Character '{char}' is not in the encoding list. It will be skipped.")
        return "".join(password_coded)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ""


# Recode Password - Odszyfrowanie hasła
def recode_password(password_coded):
    try:
        if not password_coded:
            print("Error: The coded password cannot be empty.")
            return ""
        full_reverse = full[::-1]
        password = []
        for char in password_coded:
            if char in full_reverse:
                index = full_reverse.index(char)
                password.append(full[index])
            else:
                print(f"Warning: Character '{char}' is not in the decoding list. It will be skipped.")
        
        return "".join(password)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ""



# Get Passwords - Odczyt haseł z pliku
def get_passwords(file_path):
    passwords = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                parts = line.strip().split(" ")
                if len(parts) >= 2:  # Upewnij się, że linia ma co najmniej dwie części
                    passwords.append(parts)
                else:
                    print(f"Warning: Skipping line due to unexpected format: '{line.strip()}'")
        return passwords
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied to read the file '{file_path}'.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []



# Cover - Zakrycie hasła gwiazdkami "******"
def cover_string(string):
    return "*" * len(string)


# Check Strong Password - Sprawdzanie siły hasła
def check_strong_password(password):
    try:
        if not password or len(password) < 8:
            return "Słabe hasło - Hasło musi mieć co najmniej 8 znaków."
        length = len(password)
        is_small_letter = re.search(r"[a-z]", password)
        is_big_letter = re.search(r"[A-Z]", password)
        is_numbers = re.search(r"[0-9]", password)
        is_special_characters = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

        if length >= 8 and is_small_letter and is_big_letter and is_numbers and is_special_characters:
            return "Silne hasło"
        elif length >= 6 and (is_small_letter or is_big_letter) and is_numbers:
            return "Średnie hasło"
        else:
            return "Słabe hasło"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "Błąd - Nie udało się sprawdzić siły hasła."



# Copy text - kopiuj do schowka (ctrl + v)
def copy(text):
    pyperclip.copy(text)


# Find Name - Znajdź hasło po nazwie pod jakim jest zapisane
def find(name):
    try:
        if not name:
            print("Error: The name cannot be empty.")
            return        
        global user_file
        passwords = get_passwords(user_file)
        password = "Nie znaleziono hasła"
        for i in passwords:
            if i[0] == name:
                password = recode_password(i[1])
                break
        # Create message box
        message_box = Toplevel(root)
        message_box.title("Twoje hasło")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - 250 / 2)
        center_y = int(screen_height/2 - 100 / 2)
        message_box.geometry(f'250x100+{center_x}+{center_y}')
        # Message content
        message = f"Twoje hasło: {password}"
        label = Label(message_box, text=message)
        label.pack(pady=10)
        # Create button frame
        mini_box = Frame(message_box)
        mini_box.pack(padx=10, pady=10)
        # Copy button
        copy_button = Button(mini_box, text=" Kopiuj", command=lambda: copy(password), image=copy_icon, compound=LEFT, foreground="#252F48", background="#E0E7F7")
        copy_button.pack(side=LEFT, padx=5)
        # Close button
        hide_button = Button(mini_box, text=" Zamknij", command=message_box.destroy, image=hide_icon, compound=LEFT, foreground="white", background="red")
        hide_button.pack(side=LEFT, padx=5)
    except FileNotFoundError:
        print(f"Error: The file '{user_file}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied to read the file '{user_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



# Show Password - Generowanie okna z wygenerowanym hasłem
def show_password(password):
    message_box = Toplevel(root)
    message_box.title("Wygenerowane hasło")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - 250 / 2)
    center_y = int(screen_height/2 - 200 / 2)
    message_box.geometry(f'250x200+{center_x}+{center_y}')
    message = "Twoje hasło: "+password
    label = Label(message_box, text=message)
    label.pack(pady=10)
    copy_button = Button(message_box, text=" Kopiuj", command=lambda:copy(password), image=copy_icon, compound=LEFT, foreground="#252F48", background="#E0E7F7")
    copy_button.pack(pady=10)
    refresh_button = Button(message_box, text=" Generuj ponownie", command=
    lambda: [message_box.destroy(), show_password(generate_password(generate_password_div_charamonut_entry.get(),
        generate_password_div_upper_letters_value.get(),
        generate_password_div_numbers_value.get(),
        generate_password_div_special_letters_value.get()))], image=refresh_icon, compound=LEFT, foreground="#252F48", background="#E0E7F7")
    refresh_button.pack(pady=10)
    mini_box = Frame(message_box)
    close_button = Button(mini_box, text=" Zamknij", command=message_box.destroy, image=hide_icon, compound=LEFT, foreground="white", background="red")
    close_button.pack(side=LEFT,padx=5)
    save_button = Button(mini_box, text=" Zapisz", command=lambda:new_pass(password), image=check_icon, compound=LEFT, foreground="white", background="green")
    save_button.pack(side=LEFT,padx=5)
    mini_box.pack(pady=10)


# Generate Password - Generowanie hasła o określonych wartościach
def generate_password(length,big_letters_value,numbers_value,special_value):
    if length.isdigit()==True and int(length)!=0 and length!='':
        password = []
        dictionary = list(letters) 
        if numbers_value == 1:
            dictionary.extend(numbers)
        if special_value == 1:
            dictionary.extend(special)
        for i in range(int(length)):
            if big_letters_value == 1:
                if rand_logic()==True:
                    password.extend(dictionary[rand(0,len(dictionary)-1)].upper())
                else:
                    password.extend(dictionary[rand(0,len(dictionary)-1)])
            else:
                password.extend(dictionary[rand(0,len(dictionary)-1)])
        return "".join(password)
    else:
        return "Error"


# Kliknięcie przycisku generuj
def generate_button_click(ilosc,wielkie_litery_value,cyfry_value,znaki_specjalne_value):
    password = generate_password(ilosc,wielkie_litery_value,cyfry_value,znaki_specjalne_value)
    show_password(password)


# kliknięcie przycisku zapisz
def save_button_click(password_string,name):
    global user_file
    password = code_password(password_string)
    passwords = get_passwords(user_file)
    is_good = True
    for i in passwords:
        if i[0] == name:
            is_good = False
    if is_good == True:
        save_to_file(password,name,user_file)
        find_pass()
    else:
        messagebox.showerror("Błąd", "Hasło o podanej nazwie już jest zapisane!")


# Przyciski w Menu - obsługa kliknięć przycisków w menu


# Login button in register segment
def register_div_login_button_click():
    hide()
    login_div.pack(fill=tk.BOTH, expand=True)
    root.config(menu=Menu(root))
    login_div_password_entry.delete(0, END)
    login_div_login_entry.delete(0, END)

# Hide every frame - ukrywa wszystkie ramki
def hide():
    login_div.pack_forget()
    register_div.pack_forget()
    find_div.pack_forget()
    save_password_div.pack_forget()
    generate_password_div.pack_forget()

# Funkcja stwórz hasło
def create_pass():
    hide()
    generate_password_div.pack(fill=tk.BOTH, expand=True)
    generate_password_div_charamonut_entry.delete(0,END)


# Segment zapisywania hasła
def new_pass(password):
    hide()
    save_password_div.pack(fill=tk.BOTH, expand=True)
    save_password_div_password_entry.delete(0, END)
    save_password_div_password_entry.insert(0, password)
    save_password_div_name_entry.delete(0,END)

def find_pass():
    global password_table
    global user_file
    hide()
    find_div.pack(fill=tk.BOTH, expand=True)
    find_div_name_find_entry.delete(0,END)
    if password_table:
        password_table.destroy()
    password_table = ttk.Treeview(find_div,columns=("Nazwa","Hasło","Siła hasła"),show="headings")
    password_table.heading("Nazwa", text="Nazwa")
    password_table.heading("Hasło", text="Hasło")
    password_table.heading("Siła hasła", text="Siła hasła")
    passwords = get_passwords(user_file)
    for password in passwords:
        password_table.insert("", END, values=(password[0],cover_string(password[1]), check_strong_password(recode_password(password[1]))))
    password_table.pack(padx=10,pady=10)


# Zaloguj się
def check_login(username, password):
    isUser = False
    with open("files/password.txt", "r") as file:
        for line in file:
            passwords = line.strip().split(" ")
            if username==passwords[0]:
                isUser = True
                if password == recode_password(passwords[1]):
                    global user_file
                    user_file = "files/passwords/"+username+".txt"
                    setMenu()
                    find_pass()
                else:
                    messagebox.showerror("Błąd", "Wpisano niepoprawne hasło!")
        if isUser==False:
            messagebox.showerror("Błąd", "Nie ma użytkownika o podanej nazwie")


# Zarejestruj się
def check_register(username, password, password2):
    if password.strip() == password2.strip():
        passwords = list()
        with open("files/password.txt", "r") as file:
            for line in file:
                passwords.append(line.strip().split(" "))
        is_good = True
        for i in passwords:
            if (i[0].lower()) == username.lower():
                is_good = False
        if is_good == True:
            text = username+" "+code_password(password)
            with open("files/password.txt", "a") as file:
                file.write(text+"\n")
            register_div.pack_forget()
            login_div.pack(fill=tk.BOTH, expand=True)
            new_file = "files/passwords/"+username+".txt"
            with open(new_file, "w") as file:
               messagebox.showinfo("Zapisano", "Dodano użytkownika!") 
        else:
            messagebox.showerror("Błąd", "Hasło o podanej nazwie już jest zapisane!")
    else:
        messagebox.showerror("Błąd", "Podane hasła nie są identyczne!")


# Nie mam konta przycisk
def dont_have_account():
    login_div.pack_forget()
    register_div_password2_entry.delete(0,END)
    register_div_password_entry.delete(0,END)
    register_div_login_entry.delete(0,END)
    register_div.pack(fill=tk.BOTH, expand=True)



# Validate function - sprawdza, czy wprowadzone znaki to cyfry
def validate_numeric_input(char):
    return char.isdigit()
vcmd = (root.register(validate_numeric_input), '%S') 


# Label - paragraf predefiniowany
def label(div,message):
    new_label = Label(div, text=message,bg=None, fg="black", font=("Arial", 12, "normal"))
    new_label.pack(pady=5)


# Okno pierwsze bazowe - okno do logowania
login_div = Frame(root)
login_div_image = tk.PhotoImage(file="image/logo.png")
login_div_image = login_div_image.subsample(6, 6) 
login_div_image_label = tk.Label(login_div, image=login_div_image)
login_div_image_label.pack(pady=10, anchor=tk.CENTER)
login_div_mini_box = Frame(login_div)
login_div_mini_box.pack(padx=10,pady=10)
login_div_login_label = Label(login_div_mini_box, text="Login: ", bg=None, fg="black", font=("Arial", 12, "normal"))
login_div_login_label.pack(side=LEFT,padx=5)
login_div_login_entry = Entry(login_div_mini_box, width=30)
login_div_login_entry.pack(side=LEFT,padx=5)
login_div_mini_box2 = Frame(login_div)
login_div_mini_box2.pack(padx=10,pady=10)
login_div_password_label = Label(login_div_mini_box2, text="Hasło: ", bg=None, fg="black", font=("Arial", 12, "normal"))
login_div_password_label.pack(side=LEFT,padx=5)
login_div_password_entry = Entry(login_div_mini_box2, width=30, show="*")
login_div_password_entry.pack(side=LEFT,padx=5)
login_div_password_entry_button = Button(login_div_mini_box2,width=15, image=show_icon, command=lambda:toggle_password(login_div_password_entry))
login_div_password_entry_button.pack(side=LEFT,padx=5)
login_div_mini_box3 = Frame(login_div)
login_div_mini_box3.pack(padx=10,pady=10)
login_div_register_button = Button(login_div_mini_box3, text="Nie masz konta?", foreground="#252F48", background="#E0E7F7", command=lambda: dont_have_account())
login_div_register_button.pack(side=LEFT,padx=5)
login_div_login_button = Button(login_div_mini_box3, text="Zaloguj", foreground="#252F48", background="#E0E7F7", command=
                      lambda: check_login(
                          login_div_login_entry.get(),
                          login_div_password_entry.get()
                      ))
login_div_login_button.pack(side=LEFT,padx=5)
login_div.pack(fill=tk.BOTH, expand=True)


# Okno Register - okno do tworzenia konta
register_div = Frame(root)
register_div_image = tk.PhotoImage(file="image/logo.png")
register_div_image = register_div_image.subsample(6, 6) 
register_div_image_label = tk.Label(register_div, image=register_div_image)
register_div_image_label.pack(pady=10, anchor=tk.CENTER)
register_div_mini_box = Frame(register_div)
register_div_mini_box.pack(padx=10,pady=10)
register_div_login_label = Label(register_div_mini_box, text="Login: ", bg=None, fg="black", font=("Arial", 12, "normal"))
register_div_login_label.pack(side=LEFT,padx=5)
register_div_login_entry = Entry(register_div_mini_box, width=30)
register_div_login_entry.pack(side=LEFT,padx=5)
register_div_mini_box2 = Frame(register_div)
register_div_mini_box2.pack(padx=10,pady=10)
register_div_password_label = Label(register_div_mini_box2, text="Hasło: ", bg=None, fg="black", font=("Arial", 12, "normal"))
register_div_password_label.pack(side=LEFT,padx=5)
register_div_password_entry = Entry(register_div_mini_box2, width=30, show="*")
register_div_password_entry.pack(side=LEFT,padx=5)
register_div_password_entry_button = Button(register_div_mini_box2,width=15, image=show_icon, command=lambda:toggle_password(register_div_password_entry))
register_div_password_entry_button.pack(side=LEFT,padx=5)
register_div_mini_box3 = Frame(register_div)
register_div_mini_box3.pack(padx=10,pady=10)
register_div_password2_label = Label(register_div_mini_box3, text="Powtórz hasło: ", bg=None, fg="black", font=("Arial", 12, "normal"))
register_div_password2_label.pack(side=LEFT,padx=5)
register_div_password2_entry = Entry(register_div_mini_box3, width=30, show="*")
register_div_password2_entry.pack(side=LEFT,padx=5)
register_div_password_entry_button2 = Button(register_div_mini_box3,width=15, image=show_icon, command=lambda:toggle_password(register_div_password2_entry))
register_div_password_entry_button2.pack(side=LEFT,padx=5)
register_div_mini_box4 = Frame(register_div)
register_div_mini_box4.pack(padx=10,pady=10)
register_div_login_button = Button(register_div_mini_box4, text="Powrót (Zaloguj się)", foreground="#252F48", background="#E0E7F7", command=
                      lambda: register_div_login_button_click())
register_div_login_button.pack(side=LEFT,padx=5)
register_div_register_button = Button(register_div_mini_box4, text="Utwórz konto", foreground="#252F48", background="#E0E7F7", command=
                      lambda: check_register(
                          register_div_login_entry.get(),
                          register_div_password_entry.get(),
                          register_div_password2_entry.get()
                      ))
register_div_register_button.pack(side=LEFT,padx=5)


# Okno Find - okno do pokazywania wszystkich haseł
find_div = Frame(root)
find_div_title_label = Label(find_div, text="Znajdź swoje hasło",bg=None, fg="black", font=("Arial", 14, "bold"))
find_div_title_label.pack(pady=10)
find_div_find_box = Frame(find_div)
find_div_find_box.pack(padx=10, pady=10)
find_div_name_find_entry = Entry(find_div_find_box, width=30)
find_div_name_find_entry.pack(side=LEFT, padx=5)
find_div_button_find = Button(find_div_find_box, text=" Znajdź", command=lambda:find(find_div_name_find_entry.get()), image=loop_icon, compound=LEFT, foreground="#252F48", background="#E0E7F7")
find_div_button_find.pack(side=LEFT, padx=5)


# Okno Generate - okno do generowania hasła
generate_password_div = Frame(root)
generate_password_div_title_label = Label(generate_password_div, text="Wygeneruj swoje hasło",bg=None, fg="black", font=("Arial", 14, "bold"))
generate_password_div_title_label.pack(pady=10)
label(generate_password_div,"Podaj ile znaków ma mieć hasło?")
generate_password_div_charamonut_entry = Entry(generate_password_div, width=30, validate='key', validatecommand=vcmd)
generate_password_div_charamonut_entry.pack(pady=5)
label(generate_password_div,"Zaznacz jakie elementy ma mieć hasło")
generate_password_div_upper_letters_value = IntVar()
generate_password_div_upper_letters = tk.Checkbutton(generate_password_div, text="Wielkie litery", variable=generate_password_div_upper_letters_value)
generate_password_div_upper_letters.pack(pady=5)
generate_password_div_numbers_value = IntVar()
generate_password_div_numbers = tk.Checkbutton(generate_password_div, text="Cyfry", variable=generate_password_div_numbers_value)
generate_password_div_numbers.pack(pady=5)
generate_password_div_special_letters_value = IntVar()
generate_password_div_special_letters = tk.Checkbutton(generate_password_div, text="Znaki specjalne", variable=generate_password_div_special_letters_value)
generate_password_div_special_letters.pack(pady=5)
generate_password_div_create_button = Button(
    generate_password_div,
    text=" Wygeneruj hasło",
    command=lambda: generate_button_click(
        generate_password_div_charamonut_entry.get(),
        generate_password_div_upper_letters_value.get(),
        generate_password_div_numbers_value.get(),
        generate_password_div_special_letters_value.get()
    ), image=refresh_icon, compound=LEFT, foreground="#252F48", background="#E0E7F7"
)
generate_password_div_create_button.pack(pady=5)


# Okno Save - okno do zapisywania haseł
save_password_div = Frame(root)
save_password_div_title_label = Label(save_password_div, text="Zapisz swoje hasło",bg=None, fg="black", font=("Arial", 14, "bold"))
save_password_div_title_label.pack(pady=10)
label(save_password_div,"Pod jaką nazwą ma być zapisane hasło?")
save_password_div_name_entry = Entry(save_password_div, width=30)
save_password_div_name_entry.pack(pady=5)
label(save_password_div,"Podaj hasło jakie chcesz zapisać:")
save_password_div_mini_box = Frame(save_password_div)
save_password_div_password_entry = Entry(save_password_div_mini_box, width=30, show="*")
save_password_div_password_entry.pack(side=LEFT,padx=5)
register_div_password_entry_button2 = Button(save_password_div_mini_box,width=15, image=show_icon, command=lambda:toggle_password(save_password_div_password_entry))
register_div_password_entry_button2.pack(side=LEFT,padx=5)
save_password_div_mini_box.pack(pady=5)
save_password_div_save_button = Button(
    save_password_div,
    text=" Zapisz",
    command=lambda: save_button_click(save_password_div_password_entry.get(),save_password_div_name_entry.get()), image=check_icon, compound=LEFT, foreground="white", background="green"
)
save_password_div_save_button.pack(pady=5)


# Menu - główne menu
def setMenu():
    menu_bar = Menu(root)
    empty = " "
    pass_menu = Menu(menu_bar, tearoff=0)
    pass_menu.add_command(label="Zapisz Hasło", command=lambda:new_pass(empty))
    pass_menu.add_command(label="Generuj Hasło", command=create_pass)
    pass_menu.add_command(label="Wyloguj się", command=register_div_login_button_click)
    menu_bar.add_cascade(label="Menu", menu=pass_menu)
    menu_bar.add_cascade(label="Znajdź Hasło", command=find_pass)
    root.config(menu=menu_bar)


# Odpalenie aplikacji
root.mainloop()