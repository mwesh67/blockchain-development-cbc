import requests
from flask import Flask, request, jsonify
import sqlite3
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database setup
DB_FILE = "students.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nemis_no TEXT UNIQUE,
                    name TEXT,
                    institution TEXT,
                    competency TEXT,
                    grade TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# API Routes
@app.route('/api/students', methods=['GET'])
def get_students():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = [{"id": row[0], "nemis_no": row[1], "name": row[2], "institution": row[3], "competency": row[4], "grade": row[5]} for row in c.fetchall()]
    conn.close()
    return jsonify(students)

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO students (nemis_no, name, institution, competency, grade) VALUES (?, ?, ?, ?, ?)", 
                  (data['nemis_no'], data['name'], data['institution'], data['competency'], data['grade']))
        conn.commit()
        conn.close()
        return jsonify({"message": "Student added successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Student with this NEMIS number already exists!"}), 400

# Tkinter GUI
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CBC Blockchain")
        
        # Tabbed Interface
        self.tab_control = ttk.Notebook(root)
        self.add_tab = ttk.Frame(self.tab_control)
        self.view_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.add_tab, text="Add Student")
        self.tab_control.add(self.view_tab, text="View Students")
        self.tab_control.pack(expand=1, fill="both")

        # Form Fields
        self.create_form_fields()
        self.create_view_table()

    def create_form_fields(self):
        ttk.Label(self.add_tab, text="NEMIS No:").grid(row=0, column=0, padx=5, pady=5)
        self.nemis_entry = ttk.Entry(self.add_tab)
        self.nemis_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_tab, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.add_tab)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.add_tab, text="Institution:").grid(row=2, column=0, padx=5, pady=5)
        self.institution_entry = ttk.Entry(self.add_tab)
        self.institution_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.add_tab, text="Competency:").grid(row=3, column=0, padx=5, pady=5)
        self.competency_entry = ttk.Entry(self.add_tab)
        self.competency_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.add_tab, text="Grade:").grid(row=4, column=0, padx=5, pady=5)
        self.grade_entry = ttk.Entry(self.add_tab)
        self.grade_entry.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        add_button = tk.Button(self.add_tab, text="Add Student", bg="green", fg="white", command=self.add_student)
        add_button.grid(row=5, column=0, padx=5, pady=5)
        
        clear_button = tk.Button(self.add_tab, text="Clear Fields", bg="red", fg="white", command=self.clear_fields)
        clear_button.grid(row=5, column=1, padx=5, pady=5)

    def create_view_table(self):
        self.tree = ttk.Treeview(self.view_tab, columns=("ID", "NEMIS No", "Name", "Institution", "Competency", "Grade"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("NEMIS No", text="NEMIS No")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Institution", text="Institution")
        self.tree.heading("Competency", text="Competency")
        self.tree.heading("Grade", text="Grade")
        self.tree.pack(expand=True, fill="both")

        refresh_button = tk.Button(self.view_tab, text="Refresh", command=self.refresh_students)
        refresh_button.pack(pady=5)

    def add_student(self):
        student_data = {
            "nemis_no": self.nemis_entry.get(),
            "name": self.name_entry.get(),
            "institution": self.institution_entry.get(),
            "competency": self.competency_entry.get(),
            "grade": self.grade_entry.get(),
        }

        response = requests.post("http://127.0.0.1:5000/api/students", json=student_data)

        if response.status_code == 201:
            messagebox.showinfo("Success", "Student added successfully!")
            self.refresh_students()  # Refresh student list
        else:
            messagebox.showerror("Error", response.json().get("error", "Failed to add student!"))

    def clear_fields(self):
        self.nemis_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.institution_entry.delete(0, tk.END)
        self.competency_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)

    def refresh_students(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        response = requests.get("http://127.0.0.1:5000/api/students")
        if response.status_code == 200:
            for student in response.json():
                self.tree.insert("", "end", values=(student["id"], student["nemis_no"], student["name"], student["institution"], student["competency"], student["grade"]))
        else:
            messagebox.showerror("Error", "Failed to load students!")

def run_tkinter():
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()

# Run Flask and Tkinter together
if __name__ == '__main__':
    threading.Thread(target=run_tkinter, daemon=True).start()
    app.run(debug=True, port=5000)
