import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog

class Student:
    next_id = 1

    def __init__(self):
        self.id = Student.next_id
        Student.next_id += 1
        self.subjects = {}

class Subject:
    def __init__(self, name):
        self.name = name
        self.grades = []

student_dict = {}

def save_data(student_dict, filename="student_data.txt"):
    try:
        with open(filename, "w") as file:
            for student_id, student in student_dict.items():
                file.write(f"Student ID: {student_id}\n")
                for subject_name, grades in student.subjects.items():
                    file.write(f"  Subject: {subject_name}, Grades: {','.join(map(str, grades))}\n")
        print(f"Data saved successfully to {os.path.abspath(filename)}.")
    except Exception as e:
        print(f"Error saving data: {e}")

def load_data(filename="student_data.txt"):
    student_dict = {}
    try:
        with open(filename, "r") as file:
            current_student = None
            for line in file:
                if line.startswith("Student ID:"):
                    student_id = int(line.split(":")[1].strip())
                    current_student = Student()
                    current_student.id = student_id
                    student_dict[student_id] = current_student
                elif line.startswith("  Subject:"):
                    subject_name, grades_str = line.split(",")[0].split(":")[1].strip(), line.split(",")[1].split(":")[1].strip()
                    grades = [int(grade) for grade in grades_str.split(",")]
                    current_student.subjects[subject_name] = grades
        print(f"Data loaded successfully from {os.path.abspath(filename)}.")
    except FileNotFoundError:
        print(f"File not found: {filename}. Please ensure the file exists.")
    except Exception as e:
        print(f"Error loading data: {e}")
    return student_dict

def find_student(student_id):
    return student_dict.get(student_id)

def calculate_average_grades(student, text_widget):
    for subject_name, grades in student.subjects.items():
        if grades:
            average_grade = sum(grades) / len(grades)
            grades_str = ', '.join(map(str, grades))
            text_widget.insert(tk.END, f"Subject: {subject_name}\nGrades: {grades_str}\nAverage: {average_grade:.2f}\n\n")
        else:
            text_widget.insert(tk.END, f"Subject: {subject_name}\nNo grades available.\n\n")

def export_grades(student_dict, file_type="txt"):
    if file_type == "txt":
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not filename:
            return  
        try:
            with open(filename, "w") as file:
                for student_id, student in student_dict.items():
                    file.write(f"Student ID: {student_id}\n")
                    for subject_name, grades in student.subjects.items():
                        file.write(f"  Subject: {subject_name}, Grades: {grades}\n")
                        if grades:
                            average_grade = sum(grades) / len(grades)
                            file.write(f"    Average Grade: {average_grade:.2f}\n")
                        else:
                            file.write(f"    No grades available.\n")
            print(f"Student grade report exported to {os.path.abspath(filename)} successfully.")
        except Exception as e:
            print(f"Error exporting grades to text file: {e}")

    elif file_type == "csv":
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not filename:
            return  
        try:
            with open(filename, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Student ID", "Subject", "Grades", "Average Grade"])
                for student_id, student in student_dict.items():
                    for subject_name, grades in student.subjects.items():
                        if grades:
                            average_grade = sum(grades) / len(grades)
                        else:
                            average_grade = "N/A"
                        writer.writerow([student_id, subject_name, grades, average_grade])
            print(f"Student grade report exported to {os.path.abspath(filename)} successfully.")
        except Exception as e:
            print(f"Error exporting grades to CSV file: {e}")

    else:
        print("Invalid file type. Please choose 'txt' or 'csv'.")

def style_gui():
    style = ttk.Style()
    style.theme_use("clam")

    
    style.configure("TButton",
                    background="#4B0082",  
                    foreground="white",    
                    font=("Arial", 12, "bold"),  
                    padding=10,            
                    borderwidth=3,
                    )         
    
    style.map("TButton",
              background=[("active", "#666666"),  
                          ("pressed", "#222222")], 
              foreground=[("disabled", "#777777")])  

    
    style.configure("TLabel",
                    font=("Arial", 12),
                    padding=5,
                    background="#4B0082", 
                    foreground="white")  

    
    style.configure("TEntry",
                    font=("Arial", 12),
                    padding=5,
                    background="#4B0082",  
                    foreground="black",  
                    fieldbackground="white",  
                    insertcolor="black",   
                    borderwidth=0)         
   
    root.configure(bg="white")



def add_student_gui():
    def add_student_to_dict():
        name = name_entry.get()
        if name:
            student = Student()
            student_dict[student.id] = student
            messagebox.showinfo("Success", f"Student '{name}' added with ID: {student.id}")
            name_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter a student name.")

    add_student_window = tk.Toplevel(root)
    add_student_window.title("Add Student")
    add_student_window.configure(bg="#F0F0F0")

    name_label = ttk.Label(add_student_window, text="Student Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5)

    name_entry = ttk.Entry(add_student_window)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    add_button = ttk.Button(add_student_window, text="Add Student", command=add_student_to_dict)
    add_button.grid(row=1, column=0, columnspan=2, pady=10)

def add_subject_and_grade_gui():
    def add_subject_to_student():
        try:
            student_id = int(student_id_entry.get())
            student = find_student(student_id)
            if student:
                subject_name = subject_name_entry.get()
                if subject_name:
                    if subject_name in student.subjects:
                        messagebox.showerror("Error", "Subject already exists for this student.")
                    else:
                        student.subjects[subject_name] = []
                        try:
                            num_grades = int(num_grades_entry.get())
                            grade_window = tk.Toplevel(add_subject_window)
                            grade_window.title("Enter Grades")
                            grade_window.configure(bg="#F0F0F0")

                            grade_entries = []
                            for i in range(num_grades):
                                grade_label = ttk.Label(grade_window, text=f"Grade {i+1}:")
                                grade_label.grid(row=i, column=0, padx=5, pady=5)

                                grade_entry = ttk.Entry(grade_window)
                                grade_entry.grid(row=i, column=1, padx=5, pady=5)
                                grade_entries.append(grade_entry)

                            def submit_grades():
                                try:
                                    for i, grade_entry in enumerate(grade_entries):
                                        grade = int(grade_entry.get())
                                        if 0 <= grade <= 100:
                                            student.subjects[subject_name].append(grade)
                                        else:
                                            messagebox.showerror("Error", f"Invalid grade for Grade {i+1}. Grade must be between 0 and 100.")
                                            return
                                    messagebox.showinfo("Success", "Subject and grades added successfully.")
                                    grade_window.destroy()
                                    student_id_entry.delete(0, tk.END)
                                    subject_name_entry.delete(0, tk.END)
                                    num_grades_entry.delete(0, tk.END)
                                except ValueError:
                                    messagebox.showerror("Error", "Invalid input. Please enter a valid number for grades.")

                            submit_button = ttk.Button(grade_window, text="Submit Grades", command=submit_grades)
                            submit_button.grid(row=num_grades, column=0, columnspan=2, pady=10)

                        except ValueError:
                            messagebox.showerror("Error", "Invalid number of grades.")
                else:
                    messagebox.showerror("Error", "Please enter a subject name.")
            else:
                messagebox.showerror("Error", "Student not found.")
        except ValueError:
            messagebox.showerror("Error", "Invalid student ID.")

    add_subject_window = tk.Toplevel(root)
    add_subject_window.title("Add Subject and Grade")
    add_subject_window.configure(bg="#F0F0F0")

    student_id_label = ttk.Label(add_subject_window, text="Student ID:")
    student_id_label.grid(row=0, column=0, padx=5, pady=5)

    student_id_entry = ttk.Entry(add_subject_window)
    student_id_entry.grid(row=0, column=1, padx=5, pady=5)

    subject_name_label = ttk.Label(add_subject_window, text="Subject Name:")
    subject_name_label.grid(row=1, column=0, padx=5, pady=5)

    subject_name_entry = ttk.Entry(add_subject_window)
    subject_name_entry.grid(row=1, column=1, padx=5, pady=5)

    num_grades_label = ttk.Label(add_subject_window, text="Number of Grades:")
    num_grades_label.grid(row=2, column=0, padx=5, pady=5)

    num_grades_entry = ttk.Entry(add_subject_window)
    num_grades_entry.grid(row=2, column=1, padx=5, pady=5)

    add_button = ttk.Button(add_subject_window, text="Add Subject and Grades", command=add_subject_to_student)
    add_button.grid(row=3, column=0, columnspan=2, pady=10)

def view_student_grades_gui():
    def display_grades():
        grades_text.delete("1.0", tk.END)
        try:
            student_id = int(student_id_entry.get())
            student = find_student(student_id)
            if student:
                if student.subjects:
                    calculate_average_grades(student, grades_text)
                else:
                    grades_text.insert(tk.END, "No subjects found for this student.")
            else:
                grades_text.insert(tk.END, "Student not found.")
        except ValueError:
            messagebox.showerror("Error", "Invalid student ID.")

    view_grades_window = tk.Toplevel(root)
    view_grades_window.title("View Student Grades")
    view_grades_window.configure(bg="#F0F0F0")

    student_id_label = ttk.Label(view_grades_window, text="Student ID:")
    student_id_label.grid(row=0, column=0, padx=5, pady=5)

    student_id_entry = ttk.Entry(view_grades_window)
    student_id_entry.grid(row=0, column=1, padx=5, pady=5)

    view_button = ttk.Button(view_grades_window, text="View Grades", command=display_grades)
    view_button.grid(row=1, column=0, columnspan=2, pady=10)

    grades_text = tk.Text(view_grades_window, wrap=tk.WORD, width=40, height=10)
    grades_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

def update_student_gui():
    def update_student_details():
        try:
            student_id = int(student_id_entry.get())
            student = find_student(student_id)
            if student:
                def update_subject():
                    subject_name = subject_name_entry.get()
                    if subject_name in student.subjects:
                        def update_subject_name():
                            new_subject_name = new_subject_name_entry.get()
                            if new_subject_name:
                                student.subjects[new_subject_name] = student.subjects.pop(subject_name)
                                messagebox.showinfo("Success", "Subject name updated successfully.")
                                update_subject_window.destroy()
                            else:
                                messagebox.showerror("Error", "Please enter a new subject name.")

                        def update_grades():
                            try:
                                num_grades = int(num_new_grades_entry.get())
                                new_grades = []
                                for i in range(num_grades):
                                    grade = simpledialog.askinteger("Input", f"Enter new grade {i+1} (0-100):")
                                    if grade is None:
                                        messagebox.showerror("Error", "Grade input cancelled.")
                                        return
                                    if 0 <= grade <= 100:
                                        new_grades.append(grade)
                                    else:
                                        messagebox.showerror("Error", "Grade must be between 0 and 100.")
                                        return
                                student.subjects[subject_name] = new_grades
                                messagebox.showinfo("Success", "Grades updated successfully.")
                                update_subject_window.destroy()
                            except ValueError:
                                messagebox.showerror("Error", "Invalid number of grades.")

                        def delete_subject():
                            del student.subjects[subject_name]
                            messagebox.showinfo("Success", "Subject deleted successfully.")
                            update_subject_window.destroy()

                        update_subject_window = tk.Toplevel(update_student_window)
                        update_subject_window.title("Update Subject")
                        update_subject_window.configure(bg="#F0F0F0")

                        update_choice_label = ttk.Label(update_subject_window, text="Choose an action:")
                        update_choice_label.grid(row=0, column=0, padx=5, pady=5)

                        update_name_button = ttk.Button(update_subject_window, text="Update Subject Name", command=update_subject_name)
                        update_name_button.grid(row=1, column=0, padx=5, pady=5)

                        update_grades_button = ttk.Button(update_subject_window, text="Update Grades", command=update_grades)
                        update_grades_button.grid(row=2, column=0, padx=5, pady=5)

                        delete_subject_button = ttk.Button(update_subject_window, text="Delete Subject", command=delete_subject)
                        delete_subject_button.grid(row=3, column=0, padx=5, pady=5)

                        new_subject_name_label = ttk.Label(update_subject_window, text="New Subject Name:")
                        new_subject_name_label.grid(row=4, column=0, padx=5, pady=5)

                        new_subject_name_entry = ttk.Entry(update_subject_window)
                        new_subject_name_entry.grid(row=4, column=1, padx=5, pady=5)

                        num_new_grades_label = ttk.Label(update_subject_window, text="Number of New Grades:")
                        num_new_grades_label.grid(row=5, column=0, padx=5, pady=5)

                        num_new_grades_entry = ttk.Entry(update_subject_window)
                        num_new_grades_entry.grid(row=5, column=1, padx=5, pady=5)
                    else:
                        messagebox.showerror("Error", "Subject not found for this student.")
                update_subject()
            else:
                messagebox.showerror("Error", "Student not found.")
        except ValueError:
            messagebox.showerror("Error", "Invalid student ID.")

    update_student_window = tk.Toplevel(root)
    update_student_window.title("Update Student")
    update_student_window.configure(bg="#F0F0F0")

    student_id_label = ttk.Label(update_student_window, text="Student ID:")
    student_id_label.grid(row=0, column=0, padx=5, pady=5)

    student_id_entry = ttk.Entry(update_student_window)
    student_id_entry.grid(row=0, column=1, padx=5, pady=5)

    subject_name_label = ttk.Label(update_student_window, text="Subject Name:")
    subject_name_label.grid(row=1, column=0, padx=5, pady=5)

    subject_name_entry = ttk.Entry(update_student_window)
    subject_name_entry.grid(row=1, column=1, padx=5, pady=5)

    update_button = ttk.Button(update_student_window, text="Update Student", command=update_student_details)
    update_button.grid(row=2, column=0, columnspan=2, pady=10)

def delete_student_gui():
    def delete_student_from_dict():
        try:
            student_id = int(student_id_entry.get())
            if student_id in student_dict:
                del student_dict[student_id]
                messagebox.showinfo("Success", "Student deleted successfully.")
                student_id_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Student not found.")
        except ValueError:
            messagebox.showerror("Error", "Invalid student ID.")

    delete_student_window = tk.Toplevel(root)
    delete_student_window.title("Delete Student")
    delete_student_window.configure(bg="#F0F0F0")

    student_id_label = ttk.Label(delete_student_window, text="Student ID:")
    student_id_label.grid(row=0, column=0, padx=5, pady=5)

    student_id_entry = ttk.Entry(delete_student_window)
    student_id_entry.grid(row=0, column=1, padx=5, pady=5)

    delete_button = ttk.Button(delete_student_window, text="Delete Student", command=delete_student_from_dict)
    delete_button.grid(row=1, column=0, columnspan=2, pady=10)

def save_data_gui():
    filename = tk.filedialog.asksaveasfilename(defaultextension=".txt")
    if filename:
        save_data(student_dict, filename)
        messagebox.showinfo("Success", "Data saved successfully.")

def load_data_gui():
    filename = tk.filedialog.askopenfilename(defaultextension=".txt")
    if filename:
        student_dict.clear()
        student_dict.update(load_data(filename))
        messagebox.showinfo("Success", "Data loaded successfully.")

def export_grades_gui():
    def export_to_file():
        file_type = file_type_var.get()
        if file_type == "txt":
            filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if filename:
                try:
                    with open(filename, "w") as file:
                        for student_id, student in student_dict.items():
                            file.write(f"Student ID: {student_id}\n")
                            for subject_name, grades in student.subjects.items():
                                file.write(f"  Subject: {subject_name}, Grades: {grades}\n")
                                if grades:
                                    average_grade = sum(grades) / len(grades)
                                    file.write(f"    Average Grade: {average_grade:.2f}\n")
                                else:
                                    file.write(f"    No grades available.\n")
                    messagebox.showinfo("Success", f"Student grade report exported to {filename} successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error exporting grades to text file: {e}")
        elif file_type == "csv":
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                try:
                    with open(filename, "w", newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(["Student ID", "Subject", "Grades", "Average Grade"])
                        for student_id, student in student_dict.items():
                            for subject_name, grades in student.subjects.items():
                                if grades:
                                    average_grade = sum(grades) / len(grades)
                                else:
                                    average_grade = "N/A"
                                writer.writerow([student_id, subject_name, grades, average_grade])
                    messagebox.showinfo("Success", f"Student grade report exported to {filename} successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error exporting grades to CSV file: {e}")
        else:
            messagebox.showerror("Error", "Invalid file type. Please choose 'txt' or 'csv'.")

        export_window.destroy()  

    export_window = tk.Toplevel(root)
    export_window.title("Export Grades")
    export_window.configure(bg="#F0F0F0")

    file_type_var = tk.StringVar(value="txt")  

    txt_radio = ttk.Radiobutton(export_window, text="Text (.txt)", variable=file_type_var, value="txt")
    txt_radio.grid(row=1, column=0, sticky="w")

    csv_radio = ttk.Radiobutton(export_window, text="CSV (.csv)", variable=file_type_var, value="csv")
    csv_radio.grid(row=2, column=0, sticky="w")

    export_button = ttk.Button(export_window, text="Export", command=export_to_file)
    export_button.grid(row=3, column=0, pady=10)


root = tk.Tk()
root.title("Student Grade Tracker")
root.configure(bg="black")  

style_gui()


add_student_button = ttk.Button(root, text="Add Student", command=add_student_gui)
add_student_button.pack(pady=10)

add_subject_button = ttk.Button(root, text="Add Subject and Grade", command=add_subject_and_grade_gui)
add_subject_button.pack(pady=10)

view_grades_button = ttk.Button(root, text="View Student Grades", command=view_student_grades_gui)
view_grades_button.pack(pady=10)

update_student_button = ttk.Button(root, text="Update Student", command=update_student_gui)
update_student_button.pack(pady=10)

delete_student_button = ttk.Button(root, text="Delete Student", command=delete_student_gui)
delete_student_button.pack(pady=10)

save_data_button = ttk.Button(root, text="Save Data", command=save_data_gui)
save_data_button.pack(pady=10)

load_data_button = ttk.Button(root, text="Load Data", command=load_data_gui)
load_data_button.pack(pady=10)

export_grades_button = ttk.Button(root, text="Export Grades", command=export_grades_gui)
export_grades_button.pack(pady=10)

root.mainloop()
