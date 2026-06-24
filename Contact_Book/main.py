from tkinter import *
root = Tk()
root.title("Contact Book")
root.geometry("800x500")
root.configure(bg="#0f172a")

def view_contacts():

    contact_list.delete(
        0,
        END
    )

    file = open(
        "contacts.txt",
        "r"
    )

    data = file.readlines()

    file.close()

    for contact in data:

        contact_list.insert(
            END,
            contact.strip()
        )

def reset_fields():

    name_entry.delete(
        0,
        END
    )

    phone_entry.delete(
        0,
        END
    )

    email_entry.delete(
        0,
        END
    )

def add_contact():

    name = name_entry.get()

    phone = phone_entry.get()

    email = email_entry.get()

    file = open(
        "contacts.txt",
        "a"
    )

    file.write(
        f"{name},{phone},{email}\n"
    )

    file.close()

    view_contacts()

    reset_fields()



title = Label(
    root,
    text="CONTACT BOOK",
    font=("Segoe UI", 20, "bold"),
    bg="#0f172a",
    fg="white"
)

title.pack(pady=20)

Label(
    root,
    text="Name",
    bg="#0f172a",
    fg="white",
    font=("Segoe UI", 12)
).pack()

name_entry = Entry(
    root,
    width=40,
    font=("Segoe UI", 12)
)

name_entry.pack(pady=5)

Label(
    root,
    text="Phone",
    bg="#0f172a",
    fg="white",
    font=("Segoe UI", 12)
).pack()

phone_entry = Entry(
    root,
    width=40,
    font=("Segoe UI", 12)
)

phone_entry.pack(pady=5)

Label(
    root,
    text="Email",
    bg="#0f172a",
    fg="white",
    font=("Segoe UI", 12)
).pack()

email_entry = Entry(
    root,
    width=40,
    font=("Segoe UI", 12)
)

email_entry.pack(pady=5)

contact_list = Listbox(
    root,
    width=70,
    height=10,
    font=("Segoe UI", 11)
)

contact_list.pack(pady=20)

button_frame = Frame(
    root,
    bg="#0f172a"
)

button_frame.pack()

Button(
    button_frame,
    text="Add",
    command=add_contact,
    width=12,
    bg="#2563eb",
    fg="white"
).grid(
    row=0,
    column=0,
    padx=5
)

Button(
    button_frame,
    text="View",
    command=view_contacts,
    width=12,
    bg="#16a34a",
    fg="white"
).grid(
    row=0,
    column=1,
    padx=5
)

Button(
    button_frame,
    text="Reset",
    command=reset_fields,
    width=12,
    bg="#ea580c",
    fg="white"
).grid(
    row=0,
    column=2,
    padx=5
)

def delete_contact():

    selected = contact_list.curselection()

    if not selected:
        return

    index = selected[0]

    file = open(
        "contacts.txt",
        "r"
    )

    contacts = file.readlines()

    file.close()

    del contacts[index]

    file = open(
        "contacts.txt",
        "w"
    )

    file.writelines(
        contacts
    )

    file.close()

    view_contacts()

Button(
    button_frame,
    text="Delete",
    command=delete_contact,
    width=12,
    bg="#dc2626",
    fg="white"
).grid(
    row=0,
    column=3,
    padx=5
)

def edit_contact():

    selected = contact_list.curselection()

    if not selected:
        return

    index = selected[0]

    file = open(
        "contacts.txt",
        "r"
    )

    contacts = file.readlines()

    file.close()

    contacts[index] = (
        f"{name_entry.get()},"
        f"{phone_entry.get()},"
        f"{email_entry.get()}\n"
    )

    file = open(
        "contacts.txt",
        "w"
    )

    file.writelines(
        contacts
    )

    file.close()

    view_contacts()

Button(
    button_frame,
    text="Edit",
    command=edit_contact,
    width=12,
    bg="#7c3aed",
    fg="white"
).grid(
    row=0,
    column=4,
    padx=5
)

def load_contact(event):

    selected = contact_list.curselection()

    if not selected:
        return

    value = contact_list.get(
        selected[0]
    )

    name, phone, email = value.split(",")

    reset_fields()

    name_entry.insert(
        0,
        name
    )

    phone_entry.insert(
        0,
        phone
    )

    email_entry.insert(
        0,
        email
    )

contact_list.bind(
    "<<ListboxSelect>>",
    load_contact
)


root.mainloop()

