# A simple python program demonstrating a student management system
# Using Python and the python libraries tkinter and sqlite3

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")

        # Code for the Database
        self.conn = sqlite3.connect("student_database.db")
        self.create_table()

        # Code for the Graphical User Interface GUI
        self.create_gui()


    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS students (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            age INTEGER,
                            grade TEXT
            )
        ''')
        self.conn.commit()
        
    def create_gui(self):
        # Entry variables go here
        self.name_var = tk.StringVar()
        self.age_var  = tk.StringVar()
        self.grade_var = tk.StringVar()

        # Labels
        ttk.Label(self.root, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(self.root, text="Age:").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        ttk.Label(self.root, text="Grade").grid(row=2, column=2, padx=10, pady=5, sticky="w")

        # The Entry Widgets go here
        ttk.Entry(self.root, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5)
        ttk.Entry(self.root, textvariable=self.age_var).grid(row=1, column=1, padx=10, pady=5)
        ttk.Entry(self.root, textvariable=self.grade_var).grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        ttk.Button(self.root, text="Add Student", command=self.add_student).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self.root, text="View Students", command=self.view_students).grid(row=4, column=0, columnspan=2, pady=10)

        # This is the add student function

    def add_student(self):
        name = self.name_var.get()
        age = self.age_var.get()
        grade = self.grade_var.get()

        if name and age and grade:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", (name, age, grade))
            self.conn.commit()
            tk.messagebox.showinfo("Success", "Student added successfully!")
            self.clear_entries()
        else:
            tk.messagebox.showwarning("Warning", "Please fill in all the fields")

            # This the view students function
    def view_students(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Students")

        tree = ttk.Treeview(view_window, columns=("ID", "Name", "Age", "Grade"), show="headings")

        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Age", text="Age")
        tree.heading("Grade", text="Grade")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", "end", values=row)

        tree.pack()

    def remove_student(self):
        selected_item = self.tree.selection()

        if not selected_item:
            tk.messagebox.showwarning("Warning", "Please select a student to remove.")
        return

        student_id = self.tree.item(selected_item)['values'][0]

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        self.conn.commit()

        tk.messagebox.showinfo("Success", "Student removed successfully!")
        self.view_students()

        # Clear entries function
    def clear_entries(self):
        self.name_var.set("")
        self.age_var.set("")
        self.grade_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()





        