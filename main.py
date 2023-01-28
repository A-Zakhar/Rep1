def priv():
    print("--------------------------")
    print("   Игра крестики-нолики")
    print("--------------------------")
    print("           0  1  2")
    print("        0  -  -  -")
    print("        1  -  -  -")
    print("        2  -  -  -")
    print("--------------------------")
    print("Ведите два числа от 0 до 2")
    print(" (Номер строки и столбца)")

def viv_igr_pol():
    print("--------------------------")
    print("           0  1  2")
    for i in range(3):
        stroka = "  ".join(igr_pole[i])
        print(" " * 8 + f"{i}  {stroka}")

def vvod():
    otstup = " " * 6
    while True:
        vvod_str = input(otstup + "Ваш ход: ").split()

        if len(vvod_str) != 2:
            print(otstup+"Должно быть два числа!")
            continue

        N_str, N_stolb = vvod_str

        if not(N_str.isdigit()) or not(N_stolb.isdigit()):
            print(otstup + "Вводимые данные должны быть числами!")
            continue

        N_str, N_stolb = int(N_str), int(N_stolb)

        if 0 > N_str or N_str > 2 or 0 > N_stolb or N_stolb > 2:
            print(otstup + "Числа должны быть от 0 до 2!")
            continue

        if igr_pole[N_str][N_stolb] != "-":
            print(otstup + "Это поле занято!")
            continue

        return N_str, N_stolb

def proverka():
    pob_komb = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for komb in pob_komb:
        pob = []
        for c in komb:
            pob.append(igr_pole[c[0]][c[1]])
        if pob == ["X", "X", "X"]:
            print("\n Выиграл Крестик!!!")
            return True
        if pob == ["O", "O", "O"]:
            print("\n Выиграл Нолик!!!")
            return True
    return False
#
# Начало игры
#
igr_pole = [["-"] * 3 for i in range(3)]
N_Xoda = 0
priv()
while True:
    N_Xoda += 1
    if N_Xoda % 2 == 1:
        print(" Ходят крестики")
    else:
        print(" Ходят нолики")

    x, y = vvod()

    if N_Xoda % 2 == 1:
        igr_pole[x][y] = "X"
    else:
        igr_pole[x][y] = "O"

    viv_igr_pol()

    if proverka():
        break

    if N_Xoda == 9:
        print("\n Ничья!")
        break



