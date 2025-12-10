def media_nama(nama = ""):
    # Mensanitasi nama untuk penamaan box
    # Hanya menerima karakter alfanumerik, _, -, dan spasi
    hasil = ""
    for char in nama:
        if char.isalnum() or char == "_" or char == "-" or char == " ":
            hasil += char

    return hasil.strip()
