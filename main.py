# password generator - générateur de mot de passe
# Developed by ABBASSI Ahmed Aziz
# Dévlopée par ABBASSI Ahmed Aziz


# import libs - importer les bibliothèques
from pickle import dump, load
from random import choice
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from prettytable import PrettyTable
from os import remove
from os.path import exists
import time


# creer un mot de passe au hazard - generate a random password
def creer_pwd_rand():
    # generer le mot de passe - generate the password
    all_chars = ascii_lowercase + ascii_uppercase + digits + punctuation
    pwd = ''.join([choice(all_chars) for _ in range(16)])
    while not check_password(pwd):
        pwd = ''.join([choice(all_chars) for _ in range(16)])
    print(f'Password = {pwd}')
    return pwd


# verifier si le mot de passe contient des lettres, des numeros et des symboles
# verify that the password contain chars, digits and symbols
def check_password(pwd):
    alpha_lower = False
    alpha_upper = False
    num = False
    symb = False
    i = -1
    while True:
        i += 1
        if pwd[i] in ascii_lowercase:
            alpha_lower = True
        elif pwd[i] in ascii_uppercase:
            alpha_upper = True
        elif pwd[i] in digits:
            num = True
        elif pwd[i] in punctuation:
            symb = True
        else:
            print("White Spaces are prohibited!")
            return False
        if (alpha_lower and alpha_upper and num and symb) or i == len(pwd) - 1:
            break
    if alpha_lower and alpha_upper and num and symb:
        return True
    else:
        print('Password is very week. Try another one!')
        return False


# creer un mot de passe par l'utilisateur
# generate a password by the user himself
def creer_pwd():
    while True:
        strong_or_not = input("Wanna u follow strength polices? yes or no(Y/n)?")
        mene3milch_chek = True
        if strong_or_not.lower() in ["yes", "y"]:
            mene3milch_chek = False
        pwd = input('Password: ')
        if mene3milch_chek:
            break
        elif check_password(pwd):
            break
    return pwd


# nommer le ficher dont nous travaillons
# name the file that we work on
def file_name():
    while True:
        _file_name = input('Name your file : ')
        if verif(_file_name):
            if _file_name[-4:] == '.pwd':
                return _file_name[:-4]
            return _file_name
        else:
            print('File name doesn\'t support the following characters: \\/:*?"<>|')


# verifier si le nom du fichier est valid
# verify if the file's name is valid
def verif(chaine):
    return True if len([i for i in chaine if i in '\\/:*?"<>|']) == 0 else False


# creer un nouveau fichier
# create a new file
def creer_file():
    _file_name = file_name() + '.pwd'

    if exists(_file_name):
        print('This file already exist!')
        creer_file()
    else:
        file = open(_file_name, 'wb')
        file.close()
        print("File is created successfully!")


# ajouter dans un fichier existant
# append in an existed file
def ajout_in_file():
    _file_name = file_name()
    try:
        # just to check if the file exist before
        # file = open(_file_name + '.pwd', 'rb')
        # file.close()
        # end here

        with open(_file_name + '.pwd', 'ab') as f:
            domain = lire_domain()

            # check if the domain exist before
            while existed_domain(domain, _file_name):
                print('The domain name is used!')
                domain = lire_domain()

            # ask if the password will be random or not
            pwd_rand = pass_rand()
            if pwd_rand:
                data = {'domain': domain, 'pwd': creer_pwd_rand()}
            else:
                data = {'domain': domain, 'pwd': creer_pwd()}

            # load data to the file
            dump(data, f)

    except FileNotFoundError:
        print('Please enter a valid file name!')
        ajout_in_file()


# this function helps you to check
# if the domain exist before or not
def existed_domain(domain, _file_name):
    with open(_file_name + '.pwd', 'rb') as f:
        while True:
            try:
                data = load(f)
                if data['domain'] == domain:
                    return True

            except EOFError:
                break


# lire tout le fichier existant
# read the whole file
def read_file():
    _file_name = file_name() + '.pwd'
    if exists(_file_name):
        with open(_file_name, 'rb') as f:
            tab = []
            counter = 0
            print("Reading file...")
            # time.sleep(3)
            while True:
                try:
                    data = load(f)
                    tab.append(data)
                    counter += 1

                except EOFError:
                    if counter == 0:
                        print('File is empty!')
                    else:
                        print_file(tab)
                    break

    else:
        print('Please enter a valid file name!')
        read_file()


def print_file(tab):
    tab = [[e['domain'].capitalize(), e['pwd']] for e in tab]
    tab.sort()
    pretty_tab = PrettyTable(["Domain", "Password"])
    final_tab = []
    ex_char = tab[0][0][0]
    while tab:
        final_tab.append(["------------------------", "------------------------"])
        final_tab.append([f"{ex_char}", f"{ex_char}"])

        while tab and tab[0][0][0] == ex_char:
            final_tab.append(tab[0])
            tab.pop(0)

        if tab:
            ex_char = tab[0][0][0]

    pretty_tab.add_rows(final_tab)
    print(pretty_tab)
    print('End of file!')


# choisir le mode de fonctionnement du programme
# choose the running mode
def lire_mode():
    modes = ['1', '2', '3', '4', '5', '6', '7', 'q', 'Q', 'quit']
    while True:
        mode = input(f'What mode you want? ({", ".join(modes)}): ')
        if mode in modes:
            break
        else:
            print("Please choose a valid mode!")
    return mode


# donner le nom du domaine
# name the domain
def lire_domain():
    while True:
        domain = input('Enter domain : ')
        if domain != '':
            break
    return domain


# choisir si le mot de passe est au hazard ou non
# choose if the password is random or not
def pass_rand():
    while True:
        rand = input('Random password? yes or no? ')
        if rand.lower() in ['yes', 'no']:
            break
    return rand.lower() == 'yes'


# mettre le domaine ou le mot de passe a jour
# update the domain or the password
def dom_or_pwd():
    while True:
        rep = input('Do you want to update the domain or the password or both? domain or pwd or both?\n')
        if rep.lower() in ['domain', 'pwd', 'both']:
            break
        else:
            print('If you want to update the domain type "domain".\n'
                  + 'If you want to update the password type "pwd".\n'
                  + 'If you want to update the domain and the password as well type "both".')
    return rep.lower()


# lire le nouveau domaine
# read the new domain
def lire_n_domain():
    while True:
        domain = input('Enter new domain : ')
        if domain != '':
            break
    return domain


def get_search_box():
    rep = input("Search box: ")
    return rep


# search in file by letter function
def search():
    f_name = file_name()
    rep = get_search_box()

    if exists(f_name):
        with open(f_name + '.pwd', 'rb') as f:
            tab = []
            while True:
                try:
                    data = load(f)
                    if rep.lower() in data['domain'].lower():
                        tab.append(data)
                except EOFError:
                    if len(tab) == 0:
                        print("No result found")
                    else:
                        print_file(tab)
                        break


# mettre le fichier a jour - update of the file
def update():
    try:
        f_name = file_name()

        with open(f_name + '.pwd', 'rb') as f:
            tab = []
            rep = dom_or_pwd()

            # the user here choose to update just the domain
            if rep == 'domain':
                domain = lire_domain()

                # check if the domain does not exist before
                while not existed_domain(domain, f_name):
                    print('The domain name does not exist!')
                    domain = lire_domain()

                new_domain = lire_n_domain()

                while True:
                    try:
                        data = load(f)
                        if data['domain'] == domain:
                            newdata = {'domain': new_domain, 'pwd': data['pwd']}
                            tab.append(newdata)
                        else:
                            tab.append(data)

                    except EOFError:
                        break
                print("The domain is updated", end="")

            # here the user choose to update just the password
            elif rep == 'pwd':
                domain = lire_domain()

                # check if the domain does not exist before
                while not existed_domain(domain, f_name):
                    print('The domain name does not exist!')
                    domain = lire_domain()

                print('Choose how to create your new password!')
                pwd_rand = pass_rand()
                if pwd_rand:
                    newpwd = creer_pwd_rand()
                else:
                    newpwd = creer_pwd()

                while True:
                    try:
                        data = load(f)
                        if data['domain'] == domain:
                            newdata = {'domain': data['domain'], 'pwd': newpwd}
                            tab.append(newdata)
                        else:
                            tab.append(data)

                    except EOFError:
                        break
                print("Password is updated", end="")

            # here the user choose to update both the domain and the password
            else:
                domain = lire_domain()

                # check if the domain does not exist before
                while not existed_domain(domain, f_name):
                    print('The domain name does not exist!')
                    domain = lire_domain()

                new_domain = lire_n_domain()

                print('Choose how to create your new password!')
                pwd_rand = pass_rand()
                if pwd_rand:
                    newpwd = creer_pwd_rand()
                else:
                    newpwd = creer_pwd()

                while True:
                    try:
                        data = load(f)
                        if data['domain'] == domain:
                            newdata = {'domain': new_domain, 'pwd': newpwd}
                            tab.append(newdata)
                        else:
                            tab.append(data)

                    except EOFError:
                        break
                print("Domain and password are updated", end="")

        # loading the data to the new file updated
        with open(f_name + '.pwd', 'wb') as f:
            for data in tab:
                dump(data, f)
        print(" successfully!")

    except FileNotFoundError:
        print('Please enter a valid file name!')
        update()


# supprimer un domaine - delete domain
# noinspection PyBroadException
def delete():
    _file_name = file_name()

    try:
        with open(_file_name + '.pwd', 'rb') as f:
            counter = 0
            while True:
                try:
                    load(f)
                    # del data
                    counter += 1
                    if counter == 1:
                        break
                except EOFError:
                    break

            if counter == 0:
                print("File is empty!")
                raise Exception

            domain = lire_domain()

            # check if the domain exist or not
            while not existed_domain(domain, _file_name):
                print("This domain does not exist!")
                domain = lire_domain()

            tab = []
            while True:
                try:
                    data = load(f)
                    if data['domain'] != domain:
                        tab.append(data)

                except EOFError:
                    break

        with open(_file_name + '.pwd', 'wb') as f:
            for data in tab:
                dump(data, f)

        print('The domain is deleted successfully!')
    except FileNotFoundError:
        print('Please enter a valid file name!')
        delete()
    except Exception:
        delete()


# remove file - supprimer le fichier
def remove_file():
    _file_name = file_name() + ".pwd"
    if exists(_file_name):
        remove(_file_name)
        print("File deleted successfully!")
    else:
        print("Please enter a valid file name!")
        remove_file()


# le programme principal - the main program
def main():
    modes = [
        'Create a new file',
        'Add to file',
        'Read file',
        'Search in file',
        'Update file',
        'Delete domain from file',
        'Delete file',
        'Enter (q or Q or quit) to quit!'
    ]

    lens = []
    for mode in modes:
        lens.append(((len(modes[5]) - len(mode)) // 2) * ' ')

    space = ((len(modes[-1]) - len("Password Handler")) // 2) * "*"
    print(f'{space}Password Handler{space}')

    for _ in range(len(modes) - 1):
        print(f'{_ + 1}. {lens[_]}{modes[_]}{lens[_]}')

    print('Enter (q or Q or quit) to quit!')

    while True:
        mode = lire_mode()
        if mode == '1':
            creer_file()
            # ce mode n' est pas complete
            # this mode in not completed

        if mode == '2':
            ajout_in_file()

        if mode == '3':
            read_file()

        if mode == '4':
            search()

        if mode == '5':
            update()

        if mode == '6':
            delete()

        if mode == '7':
            remove_file()

        if mode in ['q', 'Q', 'quit']:
            time.sleep(0.5)
            print('Program closed successfully!')
            break


# exécuter le programme - run the program
if __name__ == '__main__':
    main()
