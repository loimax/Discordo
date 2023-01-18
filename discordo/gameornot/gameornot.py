import random
import sys
cas = int(input("""\n\nType du BO :
1. Solo/Duo - Dormir - Flex
2. Solo/Duo - Dormir
3. SoloDuo - Flex
4. Dormir - Flex
5. Finalement giga flemme? (pétasse)\n"""))
def input_manches():
    while True:
        manches = int(input("Combien de manches pour le BO ? "))
        if manches%2 == 0:
            print("Un BO se réalise avec un nombre de manches impair frère")
        else:
            return manches
    """
    manches = int(input("Combien de manches pour le BO ? "))
    assert manches%2 != 0, "Un BO se réalise avec un nombre de manches impaire frère"
    return manches
    """ 
    
match cas:
    case 1:
        manches = input_manches()
        match manches:
            case 1:
                e = random.randint(0, 2)
                if e == 0:
                    print(f"\n\n---------------------------------------------------\n\t Solo/Duo : 1 - Dormir : 0 - Flex : 0 \n\t   On Solo/Duo bande de pétasses\n---------------------------------------------------\n")
                elif e == 1:
                    print(f"\n\n---------------------------------------------------\n\t Dormir : 1 - Solo/Duo : 0 - Flex : 0\n\t   Go dormir bande de pétasses\n---------------------------------------------------\n")
                else:
                    print(f"\n\n---------------------------------------------------\n\t Flex : 1 -Solo/Duo : 0 - Dormir : 0 \n\t   Go flex bande de pétasses\n---------------------------------------------------\n")
            case _:
                dormir = 0
                jouer = 0
                flex = 0
                for i in range(manches):
                    essai = random.randint(0, 2)
                    if jouer >= (manches / 2) or dormir >= (manches / 2) or flex >= (manches / 2):
                        break
                    if essai == 0:
                        jouer += 1
                    elif essai == 1:
                        dormir += 1
                    else:
                        flex += 1
                if jouer == flex == dormir:
                    e = random.randint(0, 2)
                    if e == 0:
                        print(f"\n\n---------------------------------------------------\n\t Solo/Duo : {jouer} - Dormir : {dormir} - Flex : {flex}\n\t   On Solo/Duo bande de pétasses\n---------------------------------------------------\n")
                    elif max(jouer, dormir, flex) == dormir:
                        print(f"\n\n---------------------------------------------------\n\t Dormir : {dormir} - Solo/Duo : {jouer} - Flex : {flex}\n\t   Go dormir bande de pétasses\n---------------------------------------------------\n")
                    elif e == 2:
                        print(f"\n\n---------------------------------------------------\n\t Flex : {flex} - Solo/Duo : {jouer} - Dormir : {dormir}\n\t   Go flex bande de pétasses\n---------------------------------------------------\n")
                elif jouer == dormir and (flex < jouer and flex < dormir): #tg cédric
                    print("Egalité entre Solo/Duo et dormir avec une valeur de", dormir)
                    e = random.randint(0, 1)
                    if e == 0:
                        print(f"\n\n---------------------------------------------------\n\t Solo/Duo : 1 - Dormir : 0 - Flex : 0 \n\t   On Solo/Duo bande de pétasses\n---------------------------------------------------\n")
                    else:
                        print(f"\n\n---------------------------------------------------\n\t Dormir : 1 - Solo/Duo : 0 - Flex : 0\n\t   Go dormir bande de pétasses\n---------------------------------------------------\n")
                elif flex == dormir and (jouer < flex and jouer < dormir):
                    print("Egalité entre flex et dormir avec une valeur de", dormir)
                    e = random.randint(0, 1)
                    if e == 0:
                        print(f"\n\n---------------------------------------------------\n\t Flex : 1 - Solo/Duo : 0 - Dormir : 0\n\t   Go flex bande de pétasses\n---------------------------------------------------\n")
                    else:
                        print(f"\n\n---------------------------------------------------\n\t Dormir : 1 - Solo/Duo : 0 - Flex : 0\n\t   Go dormir bande de pétasses\n---------------------------------------------------\n")
                elif flex == jouer and (dormir < flex and dormir < jouer):
                    print("Egalité entre flex et Solo/Duo avec une valeur de", jouer)
                    e = random.randint(0, 1)
                    if e == 0:
                        print(f"\n\n---------------------------------------------------\n\t Solo/Duo : 1 - Dormir : 0 - Flex : 0 \n\t   On Solo/Duo bande de pétasses\n---------------------------------------------------\n")
                    else:
                        print(f"\n\n---------------------------------------------------\n\t Flex : 1 - Solo/Duo : 0 - Dormir : 0 \n\t   Go flex bande de pétasses\n---------------------------------------------------\n")
                else:
                    if max(jouer, dormir, flex) == jouer:
                        print(f"\n\n---------------------------------------------------\n\t Solo/Duo : {jouer} - Dormir : {dormir} - Flex : {flex}\n\t   On Solo/Duo bande de pétasses\n---------------------------------------------------\n")
                    elif max(jouer, dormir, flex) == dormir:
                        print(f"\n\n---------------------------------------------------\n\t Dormir : {dormir} - Solo/Duo : {jouer} - Flex : {flex}\n\t   Go dormir bande de pétasses\n---------------------------------------------------\n")
                    else:
                        print(f"\n\n---------------------------------------------------\n\t Flex : {flex} - Solo/Duo : {jouer} - Dormir : {dormir}\n\t   Go flex bande de pétasses\n---------------------------------------------------\n")
    case 2:
        manches = input_manches()
        e = random.randint(0, 1)
        match manches:
            case 1:
                if e == 0:
                    print(f"\n\n-------------------------------------------\n\t Solo/Duo : 1 - Dormir : 0 \n\tOn Solo/Duo bande de pétasses\n-------------------------------------------\n")
                else:
                    print(f"\n\n-------------------------------------------\n\t Dormir : 1 - Solo/Duo : 0 \n\tGo dormir bande de pétasses\n-------------------------------------------\n")
            case _:
                dormir = 0
                jouer = 0
                for i in range(manches):
                    essai = random.randint(0, 1)
                    if jouer >= (manches / 2) or dormir >= manches / 2:
                        break
                    if essai == 0:
                        jouer += 1
                    else:
                        dormir += 1
                if jouer > dormir:
                    print(f"\n\n-------------------------------------------\n\t Solo/Duo : {jouer} - Dormir : {dormir} \n\tOn Solo/Duo bande de pétasses\n-------------------------------------------\n")
                else:
                    print(f"\n\n-------------------------------------------\n\t Dormir : {dormir} - Solo/Duo : {jouer} \n\tGo dormir bande de pétasses\n-------------------------------------------\n")
    case 3:
        manches = input_manches()
        e = random.randint(0, 1)
        match manches:
            case 1:
                if e == 0:
                    print(f"\n\n-------------------------------------------\n\t Solo/Duo : 1 - Flex : 0 \n\tOn joue bande de pétasses\n------------------------------------------\n")
                else:
                    print(f"\n\n-------------------------------------------\n\t Flex : 1 - Solo/Duo : 0 \n\tGo flex bande de pétasses\n-------------------------------------------\n")
            case _:
                jouer = 0
                flex = 0
                for i in range(manches):
                    essai = random.randint(0, 1)
                    if jouer >= (manches / 2) or flex >= manches / 2:
                        break
                    if essai == 0:
                        jouer += 1
                    else:
                        flex += 1
                if jouer > flex:
                    print(f"\n\n-------------------------------------------\n\t Solo/Duo : {jouer} - Flex : {flex} \n\tOn Solo/Duo bande de pétasses\n-------------------------------------------\n")
                else:
                    print(f"\n\n-------------------------------------------\n\t Flex : {flex} - Solo/Duo : {jouer} \n\tGo flex bande de pétasses\n-------------------------------------------\n")
    case 4:
        manches = input_manches()
        e = random.randint(0, 1)
        match manches:
            case 1:
                if e == 0:
                    print(f"\n\n-------------------------------------------\n\t Dormir : 1 - Flex : 0 \n\tGo dormir bande de pétasses\n------------------------------------------\n")
                else:
                    print(f"\n\n-------------------------------------------\n\t Flex : 1 - Dormir : 0 \n\tGo flex bande de pétasses\n-------------------------------------------\n")
            case _:
                dormir = 0
                flex = 0
                for i in range(manches):
                    essai = random.randint(0, 1)
                    if dormir >= (manches / 2) or flex >= manches / 2:
                        break
                    if essai == 0:
                        dormir += 1
                    else:
                        flex += 1
                if dormir > flex:
                    print(f"\n\n-------------------------------------------\n\t Dormir : {dormir} - Flex : {flex} \n\tGo dormir bande de pétasses\n-------------------------------------------\n")
                else:
                    print(f"\n\n-------------------------------------------\n\t Flex : {flex} - Dormir : {dormir} \n\tGo flex bande de pétasses\n-------------------------------------------\n")
    case 5:
        print("\n\tBisous les pétasses :)\n")
        raise SystemExit