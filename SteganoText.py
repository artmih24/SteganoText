import copy

def count_letters(textlist, alphalist):
    cnt = 0
    for i in range(len(textlist)):
        for j in range(len(alphalist)):
            if textlist[i] == alphalist[j]: 
                cnt += 1
    return cnt

def check_text_alpha(textlist, alphalist):
    if len(textlist) == count_letters(textlist, alphalist): 
        return True
    else: 
        return False

def embed_text(textlist, binary_code, rus_alpha_eng, eng_alpha_rus):
    textlist1 = textlist
    binary_code_list = list(binary_code)
    if textlist1[len(textlist1) - 1] != "." and textlist1[len(textlist1) - 1] != "?" and textlist1[len(textlist1) - 1] != "!":
        if count_letters(textlist1, rus_alpha_eng) < len(binary_code_list): 
            textlist1.append(".")
    while count_letters(textlist1, rus_alpha_eng) < len(binary_code_list): 
        textlist1 += list(" ") + textlist
    while len(binary_code_list) < count_letters(textlist1, rus_alpha_eng): 
        binary_code_list.append("0")
    k = 0
    for i in range(len(textlist1)):
        for j in range(len(rus_alpha_eng)):
            if textlist1[i] == rus_alpha_eng[j]:
                if binary_code_list[k] == "1": 
                    textlist1[i] = eng_alpha_rus[j]
                k += 1
    return ''.join(textlist1)

def stegano_cipher(plaintext, crypttext, plaintextrusflag, plaintextengflag):
    plaintextlist = list(plaintext)
    crypttextlist = list(crypttext)
    crypttextcharcodes = []
    for i in range(len(crypttextlist)): 
        crypttextcharcodes.append(ord(crypttextlist[i]))
    crypttextcharcodesbin = []
    for i in range(len(crypttextcharcodes)): 
        crypttextcharcodesbin.append(bin(crypttextcharcodes[i]))
    crypttextcharcodesbinstr = []
    for i in range(len(crypttextcharcodesbin)): 
        crypttextcharcodesbinstr.append(str(crypttextcharcodesbin[i])[2:])
    for i in range(len(crypttextcharcodesbinstr)):
        while len(list(crypttextcharcodesbinstr[i])) < lenbin: 
            crypttextcharcodesbinstr[i] = "0" + crypttextcharcodesbinstr[i]
    crypttextcharcodesbinstrall = ''.join(crypttextcharcodesbinstr)
    if plaintextrusflag and plaintextengflag: 
        steganotext = embed_text(plaintextlist, crypttextcharcodesbinstrall, rusalphaeng2, engalpharus2)
    else:
        if plaintextrusflag: 
            steganotext = embed_text(plaintextlist, crypttextcharcodesbinstrall, rusalphaeng2, engalpharus2)
        if plaintextengflag: 
            steganotext = embed_text(plaintextlist, crypttextcharcodesbinstrall, engalpharus3, rusalphaeng3)
    return steganotext

def try_stegano_decipher(text, rus_alpha_eng, eng_alpha_rus):
    textlist = list(text)
    binary_code_list = []
    for i in range(len(textlist)):
        for j in range(len(eng_alpha_rus)):
            if textlist[i] == eng_alpha_rus[j]: 
                binary_code_list.append("1")
            if textlist[i] == rus_alpha_eng[j]: 
                binary_code_list.append("0")
    length_decipher = int(len(binary_code_list) / lenbin)
    decipher_bin_codes = []
    for i in range(length_decipher):
        decipher_bin_code = list("0b")
        for j in range(lenbin): 
            decipher_bin_code.append(binary_code_list[j + i * lenbin])
        decipher_bin_codes.append(decipher_bin_code)
    char_codes = []
    for i in range(length_decipher): 
        char_codes.append(int(''.join(decipher_bin_codes[i]), 2))
    decipher_text_list = []
    for i in range(length_decipher): 
        decipher_text_list.append(chr(char_codes[i]))
    return ''.join(decipher_text_list)

def try_plaintext_fix(text, rus_alpha_eng, eng_alpha_rus):
    textlist = list(text)
    plaintextfixlist = textlist
    for i in range(len(plaintextfixlist)):
        for j in range(len(eng_alpha_rus)):
            if plaintextfixlist[i] == eng_alpha_rus[j]: 
                plaintextfixlist[i] = rus_alpha_eng[j]
    return ''.join(plaintextfixlist)

def stegano_decipher(text):
    text1 = copy.deepcopy(text)
    decrypttext1 = try_stegano_decipher(text, rusalphaeng2, engalpharus2)
    plaintextfix1 = try_plaintext_fix(text, rusalphaeng2, engalpharus2)
    plaintextfixrusflag = check_text_alpha(list(plaintextfix1), rusalphaall)
    if check_text_alpha(list(plaintextfix1), rusalphaall) == check_text_alpha(list(plaintextfix1), engalphaall):
        return decrypttext1
    else:
        if not plaintextfixrusflag:
            decrypttext1 = try_stegano_decipher(text1, engalpharus3, rusalphaeng3)
            plaintextfix1 = try_plaintext_fix(text, engalpharus3, rusalphaeng3)
            plaintextfixengflag = check_text_alpha(list(plaintextfix1), engalphaall)
        if plaintextfixrusflag or plaintextfixengflag: 
            return decrypttext1

def plaintext_fix(text):
    textlist = list(text)
    plaintextfix1 = try_plaintext_fix(textlist, rusalphaeng2, engalpharus2)
    plaintextfixrusflag = check_text_alpha(list(plaintextfix1), rusalphaall)
    if plaintextfixrusflag == 0:
        plaintextfix1 = try_plaintext_fix(textlist, engalpharus3, rusalphaeng3)
        plaintextfixengflag = check_text_alpha(list(plaintextfix1), engalphaall)
    if check_text_alpha(list(plaintextfix1), rusalphaall) == check_text_alpha(list(plaintextfix1), engalphaall):
        plaintextfix1 = try_plaintext_fix(textlist, rusalphaeng2, engalpharus2)
    if plaintextfixrusflag or plaintextfixengflag: 
        return plaintextfix1

print("SteganoText\tv0.4.1 beta\t\tАвтор: @artmih24\n")
lenbin = 14
numbers10 = list("0123456789")
chars = list('''., :;-!?'"/\|()[]{}#№'$&%«»—<>*^~`_''')
rusalpha = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
rusalphacaps = list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
rusalphaall = rusalpha + rusalphacaps + chars + numbers10
engalpha = list("abcdefghijklmnopqrstuvwxyz")
engalphacaps = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
engalphaall = engalpha + engalphacaps + chars + numbers10
rusalphaeng = list("аеорсухАВЕКМНОРСТХ")
engalpharus = list("aeopcyxABEKMHOPCTX")
rusalphaadd = list("ёзиклмнтБГЁП!")
addalpharus = list("ëɜᴎĸᴫᴍʜᴛƂΓËΠǃ")
engalphaadd = list("dijqsuwzIJLNQSUWYZ!")
addalphaeng = list("ԁіјԛѕսԝᴢІЈԼΝԚЅՍԜҮΖǃ")
rusalphaeng2 = rusalphaeng + rusalphaadd
engalpharus2 = engalpharus + addalpharus
engalpharus3 = engalpharus + engalphaadd
rusalphaeng3 = rusalphaeng + addalphaeng
while True:
    plaintext = input("Введите текст\n")
    plaintextrusflag = check_text_alpha(plaintext, rusalphaall)
    plaintextengflag = check_text_alpha(plaintext, engalphaall)
    if not plaintextrusflag and not plaintextengflag:
        decrypttext = stegano_decipher(plaintext)
        plaintextfix = plaintext_fix(plaintext)
        print("\nИсходный текст без зашифрованного текста:\n", plaintextfix, sep = '')
        print("\nЗашифрованный текст:\n", decrypttext, '\n', sep = '')
    else:
        crypttext = input("\nВведите текст, который нужно зашифровать\n")
        steganotext = stegano_cipher(plaintext, crypttext, plaintextrusflag, plaintextengflag)
        print("\nТекст с зашифрованным текстом:\n", steganotext, '\n', sep = '')
    plaintextrusflag = 0
    plaintextengflag = 0