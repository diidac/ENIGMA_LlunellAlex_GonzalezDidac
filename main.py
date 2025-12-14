import os
import random
import unicodedata
import re




ABECEDARI = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
rotor1 = random.sample(ABECEDARI, len(ABECEDARI))
n1 = random.choice(ABECEDARI)
rotor2 = random.sample(ABECEDARI, len(ABECEDARI))
n2 = random.choice(ABECEDARI)
rotor3 = random.sample(ABECEDARI, len(ABECEDARI))
n3 = random.choice(ABECEDARI)

with open("rotor1.txt", "w", encoding="utf-8") as f:
    f.write("".join(rotor1) + "\n")
    f.write(n1)
with open("rotor2.txt", "w", encoding="utf-8") as f:
    f.write("".join(rotor2) + "\n")
    f.write(n2)
with open("rotor3.txt", "w", encoding="utf-8") as f:
    f.write("".join(rotor3) + "\n")
    f.write(n3)


def normalitzar_text(text):
    text = text.upper()
    text = unicodedata.normalize("NFD", text)
    text = re.sub(r"[^A-Z]", "", text)
    return text


def separar_en_5(text):
    text_agrupat = ""
    for i in range(len(text)):
        text_agrupat += text[i]
        if (i + 1) % 5 == 0 and i + 1 != len(text):
            text_agrupat += " "
    return text_agrupat


def llegir_rotor(nom_fitxer):
    if not os.path.exists(nom_fitxer):
        raise FileNotFoundError(f"[ERROR] No s'ha trobat {nom_fitxer}")

    with open(nom_fitxer, "r", encoding="utf-8") as f:
        wiring = f.readline().strip()
        notch = f.readline().strip()

    if len(wiring) != 26 or not set(wiring) == set(ABECEDARI):
        raise ValueError(
            f"[ERROR] {nom_fitxer}: permutació incorrecta. Calen 26 lletres úniques A–Z"
        )
    return wiring, notch   # Guardem el Wiring i el Notch al fitxer de Rotor

def wiring_invers(wiring):
    inv = [""] * 26
    for i in range(26):
        lletra_entrada = ABECEDARI[i]
        lletra_sortida = wiring[i]
        j = ABECEDARI.index(lletra_sortida)
        inv[j] = lletra_entrada
    return "".join(inv)

def crear_rotor(wiring, notch, pos_ini):
    return {
        "wiring": wiring,
        "notch": notch,
        "pos": ABECEDARI.index(pos_ini),
        "wiring_invers": wiring_invers(wiring),
    }


def rotar_rotor(rotor):
    rotor["pos"] = (rotor["pos"] + 1) % 26
    return ABECEDARI[rotor["pos"]] == rotor["notch"]


def avançar_rotors(r1, r2, r3):
    if rotar_rotor(r1):
        if rotar_rotor(r2):
            rotar_rotor(r3)


def rotor_anada(rotor, lletra):
    pos = rotor["pos"]
    wiring = rotor["wiring"]
    idx = (ABECEDARI.index(lletra) + pos) % 26
    lletra_sortida = wiring[idx]
    idx2 = (ABECEDARI.index(lletra_sortida) - pos) % 26
    return ABECEDARI[idx2]





def rotor_tornada(rotor, lletra):
    pos = rotor["pos"]
    wiring_invers = rotor["wiring_invers"]
    idx = (ABECEDARI.index(lletra) + pos) % 26
    lletra_sortida = wiring_invers[idx]
    idx2 = (ABECEDARI.index(lletra_sortida) - pos) % 26
    return ABECEDARI[idx2]


def demanar_finestra():
    abc = input("Introdueix posició inicial (3 lletres, ex: A C B): ").strip().upper().replace(" ", "")
    if len(abc) != 3 or any(c not in ABECEDARI for c in abc):
        raise ValueError("[ERROR] Finestra inicial invàlida. Calen 3 lletres A–Z.")
    return abc


def op_xifrar():
    wiring1, notch1 = llegir_rotor("rotor1.txt")
    wiring2, notch2 = llegir_rotor("rotor2.txt")
    wiring3, notch3 = llegir_rotor("rotor3.txt")

    finestra = demanar_finestra()
    pos_ini1, pos_ini2, pos_ini3 = finestra[0], finestra[1], finestra[2]

    rotor1 = crear_rotor(wiring1, notch1, pos_ini1)
    rotor2 = crear_rotor(wiring2, notch2, pos_ini2)
    rotor3 = crear_rotor(wiring3, notch3, pos_ini3)

    missatge = input("Introdueix el missatge a xifrar: ")
    missatge_normalitzat = normalitzar_text(missatge)

    missatge_xifrat = ""
    for lletra in missatge_normalitzat:
        avançar_rotors(rotor1, rotor2, rotor3)
        lletra_xifrada = rotor_anada(rotor3, rotor_anada(rotor2, rotor_anada(rotor1, lletra)))
        missatge_xifrat += lletra_xifrada

    missatge_agrupat = separar_en_5(missatge_xifrat)
    print(f"Missatge xifrat a \"xifrat.txt\"")
    with open("xifrat.txt", "w", encoding="utf-8") as f:
        f.write(missatge_agrupat + "\n")
    return


def op_desxifrar():
    wiring1, notch1 = llegir_rotor("rotor1.txt")
    wiring2, notch2 = llegir_rotor("rotor2.txt")
    wiring3, notch3 = llegir_rotor("rotor3.txt")

    finestra = demanar_finestra()
    pos_ini1, pos_ini2, pos_ini3 = finestra[0], finestra[1], finestra[2]

    rotor1 = crear_rotor(wiring1, notch1, pos_ini1)
    rotor2 = crear_rotor(wiring2, notch2, pos_ini2)
    rotor3 = crear_rotor(wiring3, notch3, pos_ini3)

    missatge = input("Introdueix el missatge a desxifrar: ")
    missatge_normalitzat = normalitzar_text(missatge)

    missatge_desxifrat = ""
    for lletra in missatge_normalitzat:
        avançar_rotors(rotor1, rotor2, rotor3)
        lletra_desxifrada = rotor_tornada(rotor1, rotor_tornada(rotor2, rotor_tornada(rotor3, lletra)))
        missatge_desxifrat += lletra_desxifrada

    print(f"Missatge desxifrat a \"desxifrat.txt\"")
    with open("desxifrat.txt", "w", encoding="utf-8") as f:
        f.write(missatge_desxifrat + "\n")
    return

def editar_rotor(nom_fitxer):
    op = input("Quin rotor vols editar? (1, 2 o 3): ").strip()
    if op == "1":
        nom_fitxer = "rotor1.txt"
    elif op == "2":
        nom_fitxer = "rotor2.txt"
    elif op == "3":
        nom_fitxer = "rotor3.txt"
    else:
        print("[ERROR] Opció invàlida.")
        return
   
    while True:
        perm = input("Introdueix la permutació del rotor (26 lletres A-Z sense repetir): ").strip().upper().replace(" ", "")

        if len(perm) != 26:
            print("[ERROR] Han de ser exactament 26 lletres.")
            continue
        
        if set(perm) != set(ABECEDARI):
            print("[ERROR] Han d'aparèixer totes les lletres A-Z una sola vegada.")
            continue

        break

    notch = input("Introdueix la lletra de notch (A-Z): ").strip().upper()
    if len(notch) != 1 or notch not in ABECEDARI:
        raise ValueError("[ERROR] Notch invàlid, ha de ser una lletra A-Z.")

    with open(nom_fitxer, "w", encoding="utf-8") as f:
        f.write(perm + "\n")
        f.write(notch)

    print(f"Rotor guardat a {nom_fitxer}")


def menu_principal():
    while True:
        print("ENIGMA:")
        print("-------------------------------")
        print("1. Xifrar missatge")
        print("2. Desxifrar missatge")
        print("3. Editar rotor")
        print("4. Sortir")

        op = input("> ").strip()
        if op == "1":
            op_xifrar()
        elif op == "2":
            op_desxifrar()
        elif op == "3":
            editar_rotor("")
        elif op == "4": 
            print("Sortint...")
            break
        else:
            print("[ERROR] Opció invàlida")


if __name__ == "__main__":
    menu_principal()

