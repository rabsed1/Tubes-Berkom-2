import config

def kartu_buat(depan, belakang, tanggal_str):
    # membuat kartu tapi pake pemeriksaan data
    if type(depan) != list or type(belakang) != list:
        return 0
    elif type(tanggal_str) != str:
        return 0
    
    # Buat kartu dengan nilai EF, Q, dan NR default
    return [
        depan, 
        belakang, 
        tanggal_str, 
        tanggal_str, # tanggal next dan last disamakan
        config.SM_DEFAULT_EF,
        config.SM_DEFAULT_NR,
        config.SM_DEFAULT_Q_LAST,
        0,
        0
    ]

def kartu_valid(kartu):
    # NOTE: KARENA DI DALAM IF ADA RETURN, JADI NGGA MAKE ELIF
    # 1: cek tipe data kartu dan jumlah atributnya
    if type(kartu) != list:
        return False
    if len(kartu) != config.ATTR_KARTU:
        return False
    
    # 2: cek tipe data untuk tiap atribut
    depan = kartu[config.IDX_DEPAN]
    belakang = kartu[config.IDX_BELAKANG]
    tanggal_next = kartu[config.IDX_NEXT]
    tanggal_last = kartu[config.IDX_LAST]
    EF = kartu[config.IDX_EF]
    NR = kartu[config.IDX_NR]
    Q = kartu[config.IDX_Q_LAST]
    I = kartu[config.IDX_I_LAST]
    R = kartu[config.IDX_R]
    
    if type(depan) != list or type(belakang) != list:
        return False
    if type(tanggal_next) != str or type(tanggal_last) != str:
        return False
    if type(EF) != float or type(I) != int or type(NR) != int or type(Q) != int or type(R) != int:
        return False
    
    # klo bisa pass itu semua, selamat, elu validd
    return True
