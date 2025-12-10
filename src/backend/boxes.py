import os
import json
import config

# path-nya absolute, tapi relatif terhadap path berkas boxes.py
path = os.path.abspath(__file__)
path = os.path.dirname(path)
path = os.path.join(path, config.NAMA_BOXES)
BOXES_PATH = path

# buat folder boxes kalau belum ada
if not os.path.exists(BOXES_PATH):
    os.makedirs(BOXES_PATH)

# ===== FUNGSI-FUNGSINYA =======
def box_nama(nama = ""):
    # Mensanitasi nama untuk penamaan box
    # Hanya menerima karakter alfanumerik, _, -, dan spasi
    hasil = ""
    for char in nama:
        if char.isalnum() or char == "_" or char == "-" or char == " ":
            hasil += char

    return hasil.strip()

def box_path(nama_box):
    # Mengambil path dari box dengan nama
    # Asumsinya itu nama box sudah aman
    return os.path.join(BOXES_PATH, f"{nama_box}.json")

def box_buat(nama_box, daftar_kartu, tanggal_dibuat_str, label=""):
    # Membuat box baru
    nama_aman = box_nama(nama_box)
    path_box = box_path(nama_box)
    
    if nama_aman == "":
        return 0
    if type(daftar_kartu) != list:
        return 0

    data = {
        "tanggal_pembuatan": tanggal_dibuat_str,
        "label": label,
        "kartu": daftar_kartu
    }
    
    file = open(path_box, "w", encoding="utf-8")
    json.dump(data, file, ensure_ascii=False, indent=2)
    file.close()

def boxes_ambil(nama_box):
    # Mengambil konten box yang ada dalam suatu box
    nama_aman = box_nama(nama_box)
    path_box = box_path(nama_box)
    
    if nama_aman == "" or not os.path.exists(path_box):
        return 0
    
    file = open(path_box, "r", encoding="utf-8")
    data = json.load(file)
    file.close()

    return data

def boxes_daftar():
    # Mengambil path box2 yang ada di folder boxes
    # Dibuat sebagai fungsi karena sewaktu-waktu bisa berubah
    # ASUMSI KRITIS: FOLDER BOXES HANYA PUNYA FILE .JSON SAJA !!!!
    daftar_box_nama = os.listdir(BOXES_PATH)
    jumlah_box = len(daftar_box_nama)
    
    daftar_box_path = ["" for i in range(jumlah_box)]
    for i in range(jumlah_box):
        daftar_box_path[i] = box_path(daftar_box_nama[i][:-5])
    
    return daftar_box_path
