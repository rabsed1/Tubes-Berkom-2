from backend.date import tanggal_tambah
from backend import config
from date import tanggal_tambah

def max_imp(a, b):
    # fungsi max() keknya juga nggak boleh bawaan
    if a <= b:
        return b
    
    return a

def clamp_imp(angka, min, maks):
    # FUNGSI CLAMP() KAGAK BOLEH!!!! sedih bet
    # diperluin buat ngebatasin nilai n
    angka = int(angka)
    
    if angka < min:
        angka = min
    if angka > maks:
        angka = maks
    
    return angka

def map_grade(q):
    # Mapping grade kita ke grade SM-2
    return {0: 1, 1: 2, 2: 3, 3: 4}[q]

def special_IF(q):
    # interval factor khusus untuk tiap2 grade
    return {0: 1, 1: 0.9, 2: 1, 3: 1.1}[q]

def jadwal_update(kartu, q, tanggal_str, IFg=1):
    # ALGORITMA SM-2
    # Modifikasi sedikit: q di [0,3]. q < 2 dianggap incorrect.
    # Versi original: q di [0,5]. q < 3 dianggap incorrect.
    # Alhasil formula EF juga berubah

    NRp = kartu[config.IDX_NR]
    EFp = kartu[config.IDX_EF]
    Ip = kartu[config.IDX_I_LAST] # Ini interval (dalam hari)

    # Klasifikasi grade
    if q >= 2:
        if NRp == 0:
            Ip = 1
        elif NRp == 1:
            Ip = 6
        else:
            Ip = round(Ip * EFp)
            # Optimisasi interval (mirip anki)
            # 1. Mengalikan dengan faktor interval global
            # 2. Mengalikan dengan faktor interval khusus
            # 3. Pastikan at least sehari setelah Ip
            # 4. Pastikan tidak lebih dari interval maks
            Ip = round(Ip * IFg)
            Ip = round(Ip * special_IF(q))
            Ip = max(kartu[config.IDX_I_LAST]+1, Ip)
            Ip = clamp_imp(Ip, 1, config.SM_MAX_INTERVAL)
        
        NRp += 1
    else:
        NRp = 0
        Ip = 0 # Alias ngulang

    # Update nilai EF. Harusnya sebelum klasifikasi grade q sih
    # Pertumbuhan EF juga dibatesin pake fungsi clamp() itu
    # Dan formulanya pake EF SM-2 yang ori, jadi q grade kita di map ke q grade yang ori
    # Pake fungsi map_grade
    Qm = map_grade(q)
    EFp = EFp + (0.1-(5-Qm)*(.08+(5-Qm)*.02))
    EFp = clamp_imp(EFp, 1.3, config.SM_MAX_EF)

    # Update informasi
    kartu[config.IDX_LAST] = tanggal_str
    kartu[config.IDX_NEXT] = tanggal_tambah(kartu[config.IDX_LAST], Ip)
    kartu[config.IDX_EF] = EFp
    kartu[config.IDX_NR] = NRp
    kartu[config.IDX_Q_LAST] = q
    kartu[config.IDX_I_LAST] = Ip
    kartu[config.IDX_R] = 1

    return kartu