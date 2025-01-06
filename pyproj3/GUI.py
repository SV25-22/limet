import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import projekat as proj
import text_helper as th

index_helper = -1

def set_window_icon(window):
    try:
        icon_image = tk.PhotoImage(file="one piece icon.png")
        window.iconphoto(True, icon_image)
    except Exception as e:
        print(f"Failed to set window icon: {e}")

def add_title():
    add_title_window = tk.Toplevel(root)
    add_title_window.title("Add Title")
    add_title_window.geometry("350x200")

    title_label = tk.Label(add_title_window, text="Title:", font=("Roboto", 14))
    title_label.grid(row=0, column=0, padx=10, pady=20, sticky="w")

    title_input = tk.Entry(add_title_window, font=("Roboto", 14))
    title_input.grid(row=0, column=1, padx=10, pady=20, sticky="w")

    once_create = tk.IntVar()
    download_checkbox = tk.Checkbutton(add_title_window, text="Download only once", font=("Roboto", 14), variable=once_create)
    download_checkbox.grid(row=1, column=0, columnspan=2, padx=40, pady=10, sticky="w")

    def submit_title():
        title = title_input.get()
        download_once = once_create.get()
        th.add_title(title, download_once)
        add_title_window.destroy()

    submit_button = tk.Button(add_title_window, text="Submit", font=("Roboto", 14), command=submit_title)
    submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    add_title_window.columnconfigure(0, weight=1)

def delete_title():
    delete_title_window = tk.Toplevel(root)
    delete_title_window.title("Delete Title")
    delete_title_window.geometry("400x200")

    title_label = tk.Label(delete_title_window, text="Select a title:", font=("Roboto", 14))
    title_label.grid(row=0, column=0, padx=10, pady=20, sticky="w")

    titles = th.delete_titles(th.read_titles("naslovi.txt"))
    title_combobox = ttk.Combobox(delete_title_window, values=titles, font=("Roboto", 14), state="readonly")
    title_combobox.set(titles[0])
    title_combobox.grid(row=0, column=1, padx=10, pady=20, sticky="w")

    def delete_selected_title():
        selected_title = title_combobox.get()
        if("(movie)" in selected_title):
            selected_title = selected_title[:-8]
        th.delete_title("naslovi.txt",selected_title)
        delete_title_window.destroy()

    submit_button = tk.Button(delete_title_window, text="Delete", font=("Roboto", 14), command=delete_selected_title)
    submit_button.configure(bg="red", fg="white", activebackground="darkred", activeforeground="white")
    submit_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    delete_title_window.columnconfigure(0, weight=1)

def edit_title():
    edit_title_window = tk.Toplevel(root)
    edit_title_window.title("Edit Title")
    edit_title_window.geometry("450x250")

    title_label = tk.Label(edit_title_window, text="Titles:", font=("Roboto", 14))
    title_label.grid(row=0, column=0, padx=10, pady=20, sticky="w")

    titles = th.delete_titles(th.read_titles("naslovi.txt"))
    indexes = th.edit_title_indexing(titles)
    titles = th.edit_titles_show(titles)

    title_combobox = ttk.Combobox(edit_title_window, values=titles, font=("Roboto", 14))
    title_combobox.set(titles[0])
    title_combobox.grid(row=0, column=1, padx=10, pady=20, sticky="w")

    type_label = tk.Label(edit_title_window, text="Type:", font=("Roboto", 14))
    type_label.grid(row=1, column=0, padx=10, pady=20, sticky="w")


    def update_selected_type(event):
        selected_index = title_combobox.current()
        global index_helper
        index_helper = title_combobox.current()
        if indexes[selected_index] == 0:
            selected_type.set("series")
        else:
            selected_type.set("movie")

    initial_index = title_combobox.current()
    global index_helper
    index_helper = initial_index
    if indexes[initial_index] == 0:
        selected_type = tk.StringVar(value="series")
    else:
        selected_type = tk.StringVar(value="movie")

    movie_radio = tk.Radiobutton(edit_title_window, text="Movie", font=("Roboto", 14), variable=selected_type, value="movie")
    movie_radio.grid(row=1, column=1, padx=(10, 10), pady=20, sticky="w")

    series_radio = tk.Radiobutton(edit_title_window, text="Series", font=("Roboto", 14), variable=selected_type, value="series")
    series_radio.grid(row=1, column=2, padx=(10, 10), pady=20, sticky="w")

    title_combobox.bind("<<ComboboxSelected>>", update_selected_type)

    def submit_edit_title():
        global index_helper
        selected_title = title_combobox.get()
        selected_type_value = selected_type.get()
        old_titles = th.read_titles("naslovi.txt")
        th.delete_title("naslovi.txt",old_titles[index_helper])
        once = False
        if(selected_type_value == "movie"):
            once = True
        th.add_title(selected_title,once)
        edit_title_window.destroy()

    submit_button = tk.Button(edit_title_window, text="Submit", font=("Roboto", 14), command=submit_edit_title)
    submit_button.configure(bg="green", fg="white", activebackground="darkgreen", activeforeground="white")
    submit_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
    edit_title_window.columnconfigure(0, weight=1)

def one_piece_function():
    proj.main_lime()

root = tk.Tk()
root.title("ONE PIECE")
root.geometry("400x300")

set_window_icon(root)

style = Style(theme="superhero")

title_label = tk.Label(root, text="Welcome to ONE PIECE!", font=("Roboto", 24))
title_label.pack(pady=20)

one_piece_button = tk.Button(root, text="ONE PIECE", font=("Roboto", 18), command=one_piece_function)
one_piece_button.configure(bg="deepskyblue", fg="white", activebackground="royalblue", activeforeground="white", padx=20)
one_piece_button.pack(pady=20)

button_frame = tk.Frame(root)
button_frame.pack(pady=40)

add_title_button = tk.Button(button_frame, text="Add Title", font=("Roboto", 14), command=add_title)
add_title_button.configure(bg="green", fg="white", activebackground="darkgreen", activeforeground="white")
add_title_button.pack(side=tk.LEFT, padx=10)

edit_title_button = tk.Button(button_frame, text="Edit Title", font=("Roboto", 14), command=edit_title)
edit_title_button.configure(bg="orange", fg="white", activebackground="darkorange", activeforeground="white")
edit_title_button.pack(side=tk.LEFT, padx=10)

delete_title_button = tk.Button(button_frame, text="Delete Title", font=("Roboto", 14), command=delete_title)
delete_title_button.configure(bg="red", fg="white", activebackground="darkred", activeforeground="white")
delete_title_button.pack(side=tk.LEFT, padx=10)

root.mainloop()