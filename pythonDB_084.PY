
import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_database():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_database()

def prediksi_fakultas(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak dapat ditentukan"

def submit_nilai():
    nama = entry_nama.get().strip()

    try:
        biologi = int(entry_biologi.get())
        fisika = int(entry_fisika.get())
        inggris = int(entry_inggris.get())
    except ValueError:
        messagebox.showerror(
            "Input Error", "Semua nilai harus berupa angka."
        )
        return

    if not nama:
        messagebox.showerror(
            "Input Error", "Nama siswa tidak boleh kosong."
        )
        return

    if any(nilai < 0 or nilai > 100
        for nilai in [biologi, fisika, inggris]):
        messagebox.showerror(
            "Input Error", "Nilai harus antara 0 sampai 100."
        )
        return

    hasil_prediksi = prediksi_fakultas(
        biologi, fisika, inggris
    )

    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa
        (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, hasil_prediksi))

    conn.commit()
    conn.close()

    label_hasil.config(
        text="Prediksi Fakultas: " + hasil_prediksi
    )

    messagebox.showinfo(
        "Hasil Prediksi",
        f"Nama Siswa: {nama}\n"
        f"Prediksi Fakultas: {hasil_prediksi}"
    )

    entry_nama.delete(0, tk.END)
    entry_biologi.delete(0, tk.END)
    entry_fisika.delete(0, tk.END)
    entry_inggris.delete(0, tk.END)

def on_enter(e):
    btn_submit.config(bg="#dbeafe", fg="#1e3a8a")

def on_leave(e):
    btn_submit.config(bg="#2563eb", fg="white")


top = tk.Tk()
top.title("Aplikasi Prediksi Fakultas")
top.geometry("400x570")
top.configure(bg="#25255c")
top.resizable(False, False)

judul = tk.Label(
    top,
    text="PREDIKSI FAKULTAS",
    font=("Arial", 18, "bold"),
    bg="#25255c",
    fg="white"
)
judul.pack(pady=(25, 5))

subjudul = tk.Label(
    top,
    text="Masukkan data dan nilai siswa",
    font=("Arial", 10),
    bg="#25255c",
    fg="#d1d5db"
)
subjudul.pack(pady=(0, 20))

frame = tk.Frame(top, bg="#ffffff", padx=25, pady=20)
frame.pack(padx=25, fill="x")

tk.Label(
    frame, text="Nama Siswa",
    font=("Arial", 10, "bold"),
    bg="white", fg="#25255c"
).pack(anchor="w")

entry_nama = tk.Entry(frame, font=("Arial", 11))
entry_nama.pack(fill="x", pady=(5, 15), ipady=5)

tk.Label(
    frame, text="Nilai Biologi",
    font=("Arial", 10, "bold"),
    bg="white", fg="#25255c"
).pack(anchor="w")

entry_biologi = tk.Entry(frame, font=("Arial", 11))
entry_biologi.pack(fill="x", pady=(5, 12), ipady=4)

tk.Label(
    frame, text="Nilai Fisika",
    font=("Arial", 10, "bold"),
    bg="white", fg="#25255c"
).pack(anchor="w")

entry_fisika = tk.Entry(frame, font=("Arial", 11))
entry_fisika.pack(fill="x", pady=(5, 12), ipady=4)

tk.Label(
    frame, text="Nilai Bahasa Inggris",
    font=("Arial", 10, "bold"),
    bg="white", fg="#25255c"
).pack(anchor="w")

entry_inggris = tk.Entry(frame, font=("Arial", 11))
entry_inggris.pack(fill="x", pady=(5, 12), ipady=4)

btn_submit = tk.Button(
    top,
    text="HASIL PREDIKSI",
    font=("Arial", 11, "bold"),
    bg="#2563eb",
    fg="white",
    activebackground="#dbeafe",
    cursor="hand2",
    command=submit_nilai,
    relief="flat",
    pady=10
)
btn_submit.pack(fill="x", padx=25, pady=(18, 10))

btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

label_hasil = tk.Label(
    top,
    text="Hasil prediksi akan muncul di sini",
    font=("Arial", 10, "bold"),
    bg="#25255c",
    fg="white",
    wraplength=350
)
label_hasil.pack(pady=8)

top.mainloop()
