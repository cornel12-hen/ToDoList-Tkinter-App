import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
from datetime import date
from PIL import Image, ImageTk

root = tk.Tk()
root.title("To-Do List & Note")
root.geometry("880x690")

tugas_asli = []
catatan_asli = []

def show_description(event):
    selection = tree.selection()
    if selection:
        selected_item = selection[0]
        index_tugas = tree.index(selected_item)
        tugas_detail = tugas_asli[index_tugas]
        deskripsi = tugas_detail.get("deskripsi", "Deskripsi tidak tersedia.")
        messagebox.showinfo("Deskripsi Tugas", deskripsi)
    else:
        messagebox.showwarning("Peringatan", "Anda harus memilih tugas.")
def tambah_tugas():
    tugas = entry.get()
    deskripsi = deskripsi_entry.get("1.0", tk.END).strip()
    prioritas = prioritas_var.get()
    jatuh_tempo = jatuh_tempo_var.get()
    kategori = kategori_var.get()

    if tugas != "":
        tugas_detail = {
            "tugas": tugas,
            "deskripsi": deskripsi,
            "prioritas": prioritas,
            "jatuh_tempo": jatuh_tempo,
            "kategori": kategori,
            "selesai": False
        }
        tree.insert("", tk.END, values=(tugas, jatuh_tempo, prioritas, kategori, "Belum Selesai"))
        tugas_asli.append(tugas_detail)
        entry.delete(0, tk.END)
        deskripsi_entry.delete("1.0", tk.END)
        update_counts()
    else:
        messagebox.showwarning("Peringatan", "Anda harus memasukkan tugas.")

def hapus_tugas():
    selected_items = tree.selection()
    if selected_items:
        for selected_item in selected_items:
            index_tugas = tree.index(selected_item)
            tree.delete(selected_item)
            del tugas_asli[index_tugas]
        update_counts()
    else:
        messagebox.showwarning("Peringatan", "Anda harus memilih tugas untuk dihapus.")

def tandai_selesai():
    selected_items = tree.selection()
    if selected_items:
        for selected_item in selected_items:
            index_tugas = tree.index(selected_item)
            tugas_detail = tugas_asli[index_tugas]
            if not tugas_detail["selesai"]:
                tugas_detail["selesai"] = True
                tree.item(selected_item, values=(tugas_detail["tugas"], tugas_detail["jatuh_tempo"], tugas_detail["prioritas"], tugas_detail["kategori"], "Selesai"))
                tugas_asli[index_tugas] = tugas_detail
        update_counts()
    else:
        messagebox.showwarning("Peringatan", "Anda harus memilih tugas untuk ditandai selesai.")

def hapus_semua():
    tree.delete(*tree.get_children())
    tugas_asli.clear()
    update_counts()

def simpan_tugas():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as file:
            json.dump(tugas_asli, file)
        messagebox.showinfo("Info", "Tugas berhasil disimpan.")

def simpan_catatan():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("TXT files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            json.dump(catatan_asli, file)
        messagebox.showinfo("Info", "Catatan berhasil disimpan.")

def muat_tugas():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'r') as file:
            global tugas_asli
            tugas_asli = json.load(file)
        tree.delete(*tree.get_children())
        for tugas_detail in tugas_asli:
            status = "Selesai" if tugas_detail["selesai"] else "Belum Selesai"
            tree.insert("", tk.END, values=(tugas_detail["tugas"], tugas_detail["jatuh_tempo"], tugas_detail["prioritas"], tugas_detail["kategori"], status))
        update_counts()



def edit_tugas():
    selected_item = tree.selection()
    if selected_item:
        selected_item = selected_item[0]
        index_tugas = tree.index(selected_item)
        tugas_detail = tugas_asli[index_tugas]
        entry.delete(0, tk.END)
        entry.insert(0, tugas_detail["tugas"])
        deskripsi_entry.delete("1.0", tk.END)
        deskripsi_entry.insert("1.0", tugas_detail["deskripsi"])
        prioritas_var.set(tugas_detail["prioritas"])
        jatuh_tempo_var.set(tugas_detail["jatuh_tempo"])
        kategori_var.set(tugas_detail["kategori"])
        tree.delete(selected_item)
        del tugas_asli[index_tugas]
        update_counts()
    else:
        messagebox.showwarning("Peringatan", "Anda harus memilih tugas untuk diedit.")

def filter_tugas():
    status = filter_var.get()
    tree.delete(*tree.get_children())

    if status == "Semua":
        for tugas_detail in tugas_asli:
            status_str = "Selesai" if tugas_detail["selesai"] else "Belum Selesai"
            tree.insert("", tk.END, values=(tugas_detail["tugas"], tugas_detail["jatuh_tempo"], tugas_detail["prioritas"], tugas_detail["kategori"], status_str))
    elif status == "Belum Selesai":
        for tugas_detail in tugas_asli:
            if not tugas_detail["selesai"]:
                tree.insert("", tk.END, values=(tugas_detail["tugas"], tugas_detail["jatuh_tempo"], tugas_detail["prioritas"], tugas_detail["kategori"], "Belum Selesai"))
    elif status == "Selesai":
        for tugas_detail in tugas_asli:
            if tugas_detail["selesai"]:
                tree.insert("", tk.END, values=(tugas_detail["tugas"], tugas_detail["jatuh_tempo"], tugas_detail["prioritas"], tugas_detail["kategori"], "Selesai"))

def cari_tugas():
    query = search_var.get().lower()
    tree.delete(*tree.get_children())
    for tugas_detail in tugas_asli:
        if query in tugas_detail["tugas"].lower():
            status = "Selesai" if tugas_detail["selesai"] else "Belum Selesai"
            tree.insert("", tk.END, values=(tugas_detail["tugas"], tugas_detail["jatuh_tempo"], tugas_detail["prioritas"], tugas_detail["kategori"], status))

def sort_tugas(col, reverse):
    tugas_asli.sort(key=lambda x: x[col.lower()], reverse=reverse)
    tree.delete(*tree.get_children())
    for tugas_detail in tugas_asli:
        status = "Selesai" if tugas_detail["selesai"] else "Belum Selesai"
        tree.insert("", tk.END, values=(tugas_detail["tugas"], tugas_detail["jatuh_tempo"], tugas_detail["prioritas"], tugas_detail["kategori"], status))
    tree.heading(col, command=lambda _col=col: sort_tugas(_col, not reverse))

def update_counts():
    total_tugas = len(tugas_asli)
    selesai_tugas = len([tugas for tugas in tugas_asli if tugas["selesai"]])
    belum_selesai_tugas = total_tugas - selesai_tugas
    count_label.config(text=f"Total: {total_tugas} | Belum Selesai: {belum_selesai_tugas} | Selesai: {selesai_tugas}")

def tambah_catatan():
    judul = judul_catatan_entry.get()
    isi = isi_catatan_entry.get("1.0", tk.END).strip()
    tanggal = str(date.today())

    if judul != "":
        catatan_detail = {
            "judul": judul,
            "isi": isi,
            "tanggal": tanggal
        }
        catatan_listbox.insert(tk.END, f"{judul} - {tanggal}")
        catatan_asli.append(catatan_detail)
        judul_catatan_entry.delete(0, tk.END)
        isi_catatan_entry.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Peringatan", "Anda harus memasukkan judul catatan.")

def hapus_catatan():
    selected_index = catatan_listbox.curselection()
    if selected_index:
        index_catatan = selected_index[0]
        catatan_listbox.delete(selected_index)
        del catatan_asli[index_catatan]
    else:
        messagebox.showwarning("Peringatan", "Anda harus memilih catatan untuk dihapus.")

def lihat_detail_catatan(event):
    selected_index = catatan_listbox.curselection()
    if selected_index:
        index_catatan = selected_index[0]
        catatan_detail = catatan_asli[index_catatan]
        messagebox.showinfo(catatan_detail["judul"], f"{catatan_detail['isi']}\n\nDibuat pada: {catatan_detail['tanggal']}")

tab_control = ttk.Notebook(root)

tab_tugas = ttk.Frame(tab_control)
tab_control.add(tab_tugas, text=" To-Do List ")
tab_control.pack(expand=1, fill="both")

tab_catatan = ttk.Frame(tab_control)
tab_control.add(tab_catatan, text=" Note ")
tab_control.pack(expand=1, fill="both")

input_frame = ttk.Frame(tab_tugas)
input_frame.pack(pady=10)

applogo = ImageTk.PhotoImage(Image.open("NoteLogo.png"))
label_logo = tk.Label(input_frame, image=applogo)
label_logo.grid(row=0, column=2, padx=(50, 0), pady=30, sticky=tk.W)

label_tugas = tk.Label(input_frame, text="Tugas:")
label_tugas.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entry = tk.Entry(input_frame, width=40)
entry.grid(row=1, column=1, padx=(5, 20), pady=5, sticky=tk.W)

label_deskripsi = tk.Label(input_frame, text="Deskripsi:")
label_deskripsi.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
deskripsi_entry = tk.Text(input_frame, width=30, height=3)
deskripsi_entry.grid(row=3, column=1, padx=(5, 20), pady=5, sticky=tk.W)

prioritas_var = tk.StringVar()
label_prioritas = tk.Label(input_frame, text="Prioritas:")
label_prioritas.grid(row=1, column=2, padx=10, pady=0, sticky=tk.W)
prioritas_dropdown = ttk.Combobox(input_frame, textvariable=prioritas_var, values=("Tinggi", "Sedang", "Rendah"))
prioritas_dropdown.grid(row=2, column=2, padx=10, pady=0)
prioritas_dropdown.current(0)

jatuh_tempo_var = tk.StringVar()
label_jatuh_tempo = tk.Label(input_frame, text="Deadline:")
label_jatuh_tempo.grid(row=1, column=3, padx=(25, 10), pady=0, sticky=tk.W)
jatuh_tempo_dropdown = ttk.Combobox(input_frame, textvariable=jatuh_tempo_var, values=(str(date.today())))
jatuh_tempo_dropdown.grid(row=2, column=3, padx=10, pady=0)
jatuh_tempo_dropdown.current(0)

kategori_var = tk.StringVar()
label_kategori = tk.Label(input_frame, text="Kategori:")
label_kategori.grid(row=1, column=4, padx=10, pady=0, sticky=tk.W)
kategori_dropdown = ttk.Combobox(input_frame, textvariable=kategori_var, values=("Pekerjaan", "Pribadi", "Sekolah", "Lainnya"))
kategori_dropdown.grid(row=2, column=4, padx=10, pady=0)
kategori_dropdown.current(0)

btn_tambah = tk.Button(input_frame, text="Tambah Tugas", command=tambah_tugas)
btn_tambah.grid(row=3, column=2, padx=10, pady=10)

count_label = tk.Label(input_frame, text="Total: 0 | Belum Selesai: 0 | Selesai: 0")
count_label.grid(row=3, column=3, padx=0, pady=10)

columns = "Tugas", "Jatuh Tempo", "Prioritas", "Kategori", "Status"
tree = ttk.Treeview(tab_tugas, height=6 ,columns=(columns), show="headings")
for col in columns:
    tree.heading(col, text=col, command=lambda _col=col: sort_tugas(_col, False))
    tree.column(col, width=150)
tree.heading("Tugas", text="Tugas", command=lambda: sort_tugas("Tugas", False))
tree.heading("Jatuh Tempo", text="Jatuh Tempo", command=lambda: sort_tugas("Jatuh Tempo", False))
tree.heading("Prioritas", text="Prioritas", command=lambda: sort_tugas("Prioritas", False))
tree.heading("Kategori", text="Kategori", command=lambda: sort_tugas("Kategori", False))
tree.heading("Status", text="Status", command=lambda: sort_tugas("Status", False))
tree.bind("<Double-1>", show_description)
tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(tab_tugas, orient="vertical", command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscroll=scrollbar.set)

btn_hapus = tk.Button(tab_tugas, text="Hapus Tugas", command=hapus_tugas)
btn_hapus.pack(side=tk.LEFT, padx=10, pady=10)

btn_selesai = tk.Button(tab_tugas, text="Tandai Selesai", command=tandai_selesai)
btn_selesai.pack(side=tk.LEFT, padx=10, pady=10)

btn_hapus_semua = tk.Button(tab_tugas, text="Hapus Semua", command=hapus_semua)
btn_hapus_semua.pack(side=tk.LEFT, padx=10, pady=10)

btn_simpan = tk.Button(tab_tugas, text="Simpan Tugas", command=simpan_tugas)
btn_simpan.pack(side=tk.LEFT, padx=10, pady=10)

btn_muat = tk.Button(tab_tugas, text="Muat Tugas", command=muat_tugas)
btn_muat.pack(side=tk.LEFT, padx=10, pady=10)

btn_edit = tk.Button(tab_tugas, text="Edit Tugas", command=edit_tugas)
btn_edit.pack(side=tk.LEFT, padx=10, pady=10)

filter_var = tk.StringVar(value="Semua")
filter_frame = ttk.Frame(tab_tugas)
filter_frame.pack(padx=10, pady=10)

tk.Radiobutton(filter_frame, text="Semua", variable=filter_var, value="Semua", command=filter_tugas).pack(side=tk.LEFT)
tk.Radiobutton(filter_frame, text="Belum Selesai", variable=filter_var, value="Belum Selesai", command=filter_tugas).pack(side=tk.LEFT)
tk.Radiobutton(filter_frame, text="Selesai", variable=filter_var, value="Selesai", command=filter_tugas).pack(side=tk.LEFT)

search_var = tk.StringVar()
search_entry = tk.Entry(tab_tugas, textvariable=search_var, width=25)
search_entry.pack(side=tk.LEFT, padx=10, pady=10)

btn_cari = tk.Button(tab_tugas, text="Cari Tugas", command=cari_tugas)
btn_cari.pack(side=tk.LEFT, padx=10, pady=10)

style = ttk.Style()
style.configure("Treeview", font=("Arial", 12), rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
style.map('Treeview', background=[('selected', '#347083')])

input_catatan_frame = ttk.Frame(tab_catatan)
input_catatan_frame.pack(pady=10)

label_judul_catatan = tk.Label(input_catatan_frame, text="Judul:")
label_judul_catatan.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
judul_catatan_entry = tk.Entry(input_catatan_frame, width=40)
judul_catatan_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
judul_catatan_info = tk.Label(input_catatan_frame, text="Masukkan judul catatan.")
judul_catatan_info.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

label_isi_catatan = tk.Label(input_catatan_frame, text="Isi:")
label_isi_catatan.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
isi_catatan_entry = tk.Text(input_catatan_frame, width=30, height=5)
isi_catatan_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
isi_catatan_info = tk.Label(input_catatan_frame, text="Masukkan isi atau detail catatan.")
isi_catatan_info.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

btn_tambah_catatan = tk.Button(input_catatan_frame, text="Tambah Catatan", command=tambah_catatan)
btn_tambah_catatan.grid(row=2, column=1, padx=10, pady=10)

catatan_listbox = tk.Listbox(tab_catatan, height=15)
catatan_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

catatan_scrollbar = ttk.Scrollbar(tab_catatan, orient="vertical", command=catatan_listbox.yview)
catatan_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
catatan_listbox.configure(yscroll=catatan_scrollbar.set)

catatan_listbox.bind("<Double-Button-1>", lihat_detail_catatan)

btn_hapus_catatan = tk.Button(tab_catatan, text="Hapus Catatan", command=hapus_catatan)
btn_hapus_catatan.pack(side=tk.LEFT, padx=10, pady=10)

btn_hapus_catatan = tk.Button(tab_catatan, text="Simpan Catatan", command=simpan_catatan)
btn_hapus_catatan.pack(side=tk.LEFT, padx=10, pady=10)

root.mainloop()
