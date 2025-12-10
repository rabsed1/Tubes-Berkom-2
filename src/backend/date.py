from datetime import date, timedelta

def tanggal_format(tanggal_obj):
    # metode rjust kayaknya dibolehin sih
    y = str(tanggal_obj.year).rjust(4, "0")
    m = str(tanggal_obj.month).rjust(2, "0")
    d = str(tanggal_obj.day).rjust(2, "0")

    return f"{d}/{m}/{y}"

def tanggal_parse(tanggal_str=""):
    teks = tanggal_str.strip()
    bagian = teks.split("/")
    
    # tanggal_str nya nggak valid
    if len(bagian) != 3:
        return []
    
    y = int(bagian[2])
    m = int(bagian[1])
    d = int(bagian[0])
    
    # harusnya pake keyword try, cuma keknya belom dibolehin
    return date(y, m, d)
    
def tanggal_tambah(tanggal_str, jumlah_hari=0):
    # Basically ngeparse, nambahin, lalu ngeformat balik
    dasar = tanggal_parse(tanggal_str)
    
    # tanggal_str nya nggak valid
    if dasar == []:
        return ""
    
    n = int(jumlah_hari)
    hasil = dasar + timedelta(days=n)

    return tanggal_format(hasil)

def tanggal_due(tanggal_next_str, tanggal_today_str):
    # kalau tanggal next atau last kosong, kartu dianggap due yeah
    if (tanggal_next_str or "").strip() == "":
        return 1
    
    a = tanggal_parse(tanggal_next_str)
    b = tanggal_parse(tanggal_today_str) # mending ambil dari luar aja
    
    if a == [] or b == []:
        return 1
    if a <= b:
        return 1
    return 0
