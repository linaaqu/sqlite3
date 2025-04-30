import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

conn = sqlite3.connect('notes.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS notes
                (id INTEGER PRIMARY KEY, note TEXT, priority INTEGER)''')

PRIORITY = {0: "Нет", 1: "Низкий", 2: "Средний", 3: "Высокий"}

def show_notes():
    tree.delete(*tree.get_children())
    cursor.execute("SELECT * FROM notes ORDER BY priority DESC")
    for row in cursor.fetchall():
        tree.insert("", END, values=(row[0], row[1], PRIORITY[row[2]]))

def add_note():
    if note_entry.get():
        cursor.execute("INSERT INTO notes (note, priority) VALUES (?, ?)",
                      (note_entry.get(), priority.get()))
        conn.commit()
        show_notes()
        note_entry.delete(0, END)

def update_note():
    if tree.selection():
        item = tree.item(tree.selection()[0])
        cursor.execute("UPDATE notes SET note=?, priority=? WHERE id=?",
                      (note_entry.get(), priority.get(), item['values'][0]))
        conn.commit()
        show_notes()

def delete_note():
    if tree.selection():
        cursor.execute("DELETE FROM notes WHERE id=?", 
                      (tree.item(tree.selection()[0])['values'][0],))
        conn.commit()
        show_notes()

def refresh_notes():
    show_notes()
    note_entry.delete(0, END)
    messagebox.showinfo("Обновлено", "Список заметок обновлен")

def on_select(event):
    if tree.selection():
        item = tree.item(tree.selection()[0])
        note_entry.delete(0, END)
        note_entry.insert(0, item['values'][1])
        priority.set([k for k,v in PRIORITY.items() if v == item['values'][2]][0])

root = Tk()
root.title("Заметки с приоритетами")

frame = Frame(root)
frame.pack(pady=10)

Label(frame, text="Текст:").grid(row=0, column=0)
note_entry = Entry(frame, width=30)
note_entry.grid(row=0, column=1)

Label(frame, text="Приоритет:").grid(row=1, column=0)
priority = IntVar(value=1)
for i, (k, v) in enumerate(PRIORITY.items()):
    Radiobutton(frame, text=v, variable=priority, value=k).grid(row=1, column=i+1)

btn_frame = Frame(root)
btn_frame.pack(pady=5)

Button(btn_frame, text="Добавить", command=add_note).pack(side=LEFT, padx=5)
Button(btn_frame, text="Изменить", command=update_note).pack(side=LEFT, padx=5)
Button(btn_frame, text="Удалить", command=delete_note).pack(side=LEFT, padx=5)
Button(btn_frame, text="Обновить", command=refresh_notes).pack(side=LEFT, padx=5)

tree = ttk.Treeview(root, columns=("ID", "Note", "Priority"), show="headings", height=10)
tree.pack(fill=BOTH, expand=1, padx=10, pady=5)
tree.heading("ID", text="ID")
tree.heading("Note", text="Заметка")
tree.heading("Priority", text="Приоритет")
tree.column("ID", width=50, anchor=CENTER)
tree.column("Note", width=200)
tree.column("Priority", width=100, anchor=CENTER)
tree.bind('<<TreeviewSelect>>', on_select)

show_notes()
root.mainloop()
conn.close()