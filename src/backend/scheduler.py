from backend.date import tanggal_tambah
import config

def clamp(angka, maks):
    # FUNGSI CLAMP() KAGAK BOLEH!!!! sedih bet
    # diperluin buat ngebatasin nilai n
    angka = int(angka)
    
    if angka < 1:
        angka = 1
    if angka > config.MAX_NR_CLAMP:
        angka = config.MAX_NR_CLAMP
    
    return angka

def jadwal_update(kartu, q, tanggal_today_str):
    # ALGORITMA SM-2
    # Modifikasi sedikit: q di [0,3]. q < 2 dianggap incorrect.
    # Versi original: q di [0,5]. q < 3 dianggap incorrect.
    # Alhasil formula EF juga berubah

    NRp = kartu[config.IDX_NR]
    EFp = kartu[config.IDX_EF]
    Ip = 0 # Ini interval (dalam hari)

    # Klasifikasi grade
    if q >= 2:
        if NRp == 0:
            Ip = 1
        elif NRp == 1:
            Ip = 6
        else:
            Ip = round(Ip * EFp)
        
        NRp = clamp(NRp + 1)
    else:
        NRp = 0
        Ip = 0 # Alias ngulang
    
    # Update nilai EF. Harusnya sebelum klasifikasi grade q sih
    EFp = EFp + (0.1-(3-q)) * (.08+(3-q)*.02)
    if EFp < 1.3:
        EFp = 1.3
    
    kartu[config.IDX_LAST] = tanggal_today_str
    kartu[config.IDX_NEXT] = tanggal_tambah(tanggal_today_str, Ip)
    kartu[config.IDX_EF] = EFp
    kartu[config.IDX_NR] = NRp
    kartu[config.IDX_Q_LAST] = q

    return kartu
