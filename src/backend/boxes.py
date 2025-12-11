import os
import json
from backend import config
from backend.cards import kartu_valid

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

def box_buat(nama_box, tanggal_dibuat_str, label=""):
    # Membuat box baru
    nama_aman = box_nama(nama_box)
    path_box = box_path(nama_box)
    
    # nama nggak valid ato box ternyata udah ada
    if nama_aman == "" or os.path.exists(path_box):
        return 0

    data = {
        "tanggal_pembuatan": tanggal_dibuat_str,
        "label": label,
        "interval_factor": 1,
        "kartu": []
    }
    
    file = open(path_box, "w", encoding="utf-8")
    json.dump(data, file, ensure_ascii=False, indent=config.JSON_INDENT)
    file.close()

    return 1

def box_simpan(nama_box, box_data):
    # Mengambil konten box yang ada dalam suatu box
    nama_aman = box_nama(nama_box)
    path_box = box_path(nama_box)
    
    if nama_aman == "" or not os.path.exists(path_box):
        return 0

    # cek apakah kartu valid atau tidak
    daftar_kartu = box_data["kartu"]
    for kartu in daftar_kartu:
        if not kartu_valid(kartu):
            return 0

    file = open(path_box, "w", encoding="utf-8")
    json.dump(box_data, file, ensure_ascii=False, indent=config.JSON_INDENT)
    file.close()

    return 1

def box_hapus(nama_box):
    # Menghapus box (obviously, duhh)
    nama_aman = box_nama(nama_box)
    path_box = box_path(nama_box)
    
    if nama_aman == "" or not os.path.exists(path_box):
        return 0
    
    os.remove(path_box)
    return 1

def box_ambil(nama_box):
    # Mengambil konten box yang ada dalam suatu box
    nama_aman = box_nama(nama_box)
    path_box = box_path(nama_box)
    
    if nama_aman == "" or not os.path.exists(path_box):
        return 0
    
    file = open(path_box, "r", encoding="utf-8")
    data = json.load(file)
    file.close()

    return data

def box_ambil_stat(nama_box):
    # Mengambil statistik suatu box
    nama_aman = box_nama(nama_box)
    path_box = box_path(nama_box)
    
    if nama_aman == "" or not os.path.exists(path_box):
        return 0
    
    file = open(path_box, "r", encoding="utf-8")
    data_kartu = json.load(file)["kartu"]
    jumlah_kartu = len(data_kartu)
    file.close()

    if jumlah_kartu == 0:
        return 0

    # Proses pengambilan stat yang agak ribet dimulai di sini
    # Yang mau kita ambil: nilai q terakhir dan due date
    jumlah_q = [0,0,0,0]
    jumlah_q_p = [0,0,0,0] # p: primitive
    jumlah_yet_r = 0

    for kartu in data_kartu:
        q_kartu = kartu[config.IDX_Q_LAST]

        # Tambah jumlah kartu by grade
        if kartu[config.IDX_R] != 0:
            jumlah_q[q_kartu] += 1
        else:
            jumlah_yet_r += 1

        jumlah_q_p[q_kartu] += 1
    
    # kategorisasi kartu
    jumlah_kartu_by_due = {}
    kartu_by_q = {
        0: [None for i in range(jumlah_q_p[0])],
        1: [None for i in range(jumlah_q_p[1])],
        2: [None for i in range(jumlah_q_p[2])],
        3: [None for i in range(jumlah_q_p[3])]
    }

    # helpers
    index_by_q = [0,0,0,0]
    
    # kali ini pakai index
    for i in range(jumlah_kartu):
        # Tambah indeks kartu by berdasarkan due date
        q_kartu = data_kartu[i][config.IDX_Q_LAST]
        due_kartu = data_kartu[i][config.IDX_NEXT]

        if not hasattr(kartu_by_q, due_kartu):
            jumlah_kartu_by_due[due_kartu] = [0,0,0,0]
        
        jumlah_kartu_by_due[due_kartu][q_kartu] += 1
        
        # Masukin kartu ke daftar kartu based on grade
        idx = index_by_q[q_kartu]
        kartu_by_q[q_kartu][idx] = kartu
        index_by_q [q_kartu] += 1

    # Tambah stats mastery, yakni 
    # jumlah kartu dengan q=2 dibagi jumlah total kartu
    mastery_rate = 0
    if jumlah_q[2]+jumlah_q[3] != 0:
        mastery_rate = (jumlah_q[2]+jumlah_q[3])
        mastery_rate /= jumlah_q[0]+jumlah_q[1]+jumlah_q[2]+jumlah_q[3]
    
    return {
        "mastery_rate": f"{mastery_rate:.1f}",
        "kartu_by_q": kartu_by_q,
        "jumlah_kartu_by_q": jumlah_q,
        "jumlah_kartu_by_due": jumlah_kartu_by_due,
        "jumlah_kartu_belum_direview": jumlah_yet_r
    }

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

def boxes_daftar_nama():
    daftar_box = os.listdir(BOXES_PATH)
    jumlah_box = len(daftar_box)

    daftar_box_nama = ["" for i in range(jumlah_box)]
    for i in range(jumlah_box):
        daftar_box_nama[i] = daftar_box[i][:-5]
    return daftar_box_nama
