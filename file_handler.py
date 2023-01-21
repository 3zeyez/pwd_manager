from pickle import dump, load
from pwd import *
# noinspection PyUnresolvedReferences
from prettytable import PrettyTable
from os import remove
from os.path import exists


# take the name the file that we work on from user
def get_file_name():
    while True:
        file_name = input("Name your file : ")
        if verify(file_name):
            if file_name[-4:] == ".pwd":
                return file_name[:-4]
            return file_name
        else:
            print("File name doesn't support the following characters: \\/:*?\"<>|")


# verify if the file's name is valid
def verify(chaine):
    return True if len([i for i in chaine if i in '\\/:*?"<>|']) == 0 else False


def get_domain(msg='Enter domain: '):
    domain = ""
    while domain == "":
        domain = input(msg)
    return domain.capitalize()


# this function helps you to check if the domain exist before or not
def domain_exists_in_file(domain, file_name):
    with open(file_name, 'rb') as f:
        while True:
            try:
                data = load(f)
                if data['domain'] == domain:
                    return True

            except EOFError:
                break


def create_file():
    file_name = get_file_name() + '.pwd'

    if exists(file_name):
        print('This file already exist!')
        create_file()
    else:
        with open(file_name, 'wb'):
            print("File is created successfully!")


# append in an existed file
def add_to_file():
    file_name = get_file_name() + '.pwd'
    if exists(file_name):
        with open(file_name, 'ab') as f:
            domain = get_domain()
            while domain_exists_in_file(domain, file_name):
                print('The domain name is used!\nTry another one!')
                domain = get_domain()

            pwd_is_random = pwd_random_or_not()
            if pwd_is_random:
                data = {'domain': domain, 'pwd': create_pwd_randomly()}
            else:
                data = {'domain': domain, 'pwd': create_pwd_manually()}

            dump(data, f)  # load data to the file

    else:
        print('Please enter a valid file name!')
        add_to_file()


# read the whole file
def read_file():
    file_name = get_file_name() + '.pwd'
    if exists(file_name):
        with open(file_name, 'rb') as f:
            file_data = []
            counter = 0
            while True:
                try:
                    file_data.append(load(f))
                    counter += 1

                except EOFError:
                    if counter == 0:
                        print('File is empty!')
                    else:
                        print_file(file_data)
                    break

    else:
        print('Please enter a valid file name!')
        read_file()


# choose : update the domain or the password
def update_domain_or_pwd():
    while True:
        rep = input('Do you want to update the domain or the password or both? domain or pwd or both?\n')
        rep = rep.lower()
        if rep in ['domain', 'pwd', 'both']:
            break
        else:
            print('If you wat nto update the domain, then type "domain".\n'
                  + 'If you want to update the password, then type "pwd".\n'
                  + 'If you want to update the domain and the password as well type "both".')
    return rep


def get_new_domain():
    domain = ""
    while domain == "":
        domain = input('Enter new domain : ')
    return domain


def get_search_box():
    rep = input("Search box: ")
    return rep


# search in file by letter function
def search():
    f_name = get_file_name()
    rep = get_search_box()

    try:
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
    except FileNotFoundError:
        print("Invalid file name!")
        search()


def print_file(tab):
    tab = [[e['domain'], e['pwd']] for e in tab]
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


# mettre le fichier a jour - update of the file
def update():
    try:
        file_name = get_file_name() + '.pwd'

        with open(file_name, 'rb') as f:
            tab = []
            rep = update_domain_or_pwd()

            # the user here choose to update just the domain
            if rep == 'domain':
                domain = get_domain()

                # check if the domain does not exist before
                while not domain_exists_in_file(domain, file_name):
                    print('The domain name does not exist!')
                    domain = get_domain()

                new_domain = get_domain('Enter new domain: ')

                while True:
                    try:
                        data = load(f)
                        if data['domain'] == domain:
                            new_data = {'domain': new_domain, 'pwd': data['pwd']}
                            tab.append(new_data)
                        else:
                            tab.append(data)

                    except EOFError:
                        break
                print("The domain is updated", end="")

            # here the user choose to update just the password
            elif rep == 'pwd':
                domain = get_domain()

                # check if the domain does not exist before
                while not domain_exists_in_file(domain, file_name):
                    print('The domain name does not exist!')
                    domain = get_domain()

                print('Choose how to create your new password!')
                pwd_rand = pwd_random_or_not()
                if pwd_rand:
                    newpwd = create_pwd_randomly()
                else:
                    newpwd = create_pwd_manually()

                while True:
                    try:
                        data = load(f)
                        if data['domain'] == domain:
                            new_data = {'domain': data['domain'], 'pwd': newpwd}
                            tab.append(new_data)
                        else:
                            tab.append(data)

                    except EOFError:
                        break
                print("Password is updated", end="")

            # here the user choose to update both the domain and the password
            else:
                domain = get_domain()

                # check if the domain does not exist before
                while not domain_exists_in_file(domain, file_name):
                    print('The domain name does not exist!')
                    domain = get_domain()

                new_domain = get_new_domain()

                print('Choose how to create your new password!')
                pwd_rand = pwd_random_or_not()
                if pwd_rand:
                    newpwd = create_pwd_randomly()
                else:
                    newpwd = create_pwd_manually()

                while True:
                    try:
                        data = load(f)
                        if data['domain'] == domain:
                            new_data = {'domain': new_domain, 'pwd': newpwd}
                            tab.append(new_data)
                        else:
                            tab.append(data)

                    except EOFError:
                        break
                print("Domain and password are updated", end="")

        # loading the data to the new file updated
        with open(file_name, 'wb') as f:
            for data in tab:
                dump(data, f)
        print(" successfully!")

    except FileNotFoundError:
        print('Please enter a valid file name!')
        update()


# supprimer un domaine - delete domain
# noinspection PyBroadException
def delete():
    file_name = get_file_name() + '.pwd'

    try:
        with open(file_name, 'rb') as f:
            counter = 0
            try:
                load(f)
                counter += 1
            except EOFError:
                if counter == 0:
                    raise Exception

            domain = get_domain()

            # check if the domain exist or not
            while not domain_exists_in_file(domain, file_name):
                print("This domain does not exist!")
                domain = get_domain()

            tab = []
            while True:
                try:
                    data = load(f)
                    if data['domain'] != domain:
                        tab.append(data)

                except EOFError:
                    break

        with open(file_name, 'wb') as f:
            for data in tab:
                dump(data, f)

        print('The domain is deleted successfully!')
    except FileNotFoundError:
        print('Please enter a valid file name!')
        delete()
    except Exception:
        print("File is empty! You can do this operation!")


# remove file - supprimer le fichier
def remove_file():
    _file_name = get_file_name() + ".pwd"
    if exists(_file_name):
        remove(_file_name)
        print("File deleted successfully!")
    else:
        print("Please enter a valid file name!")
        remove_file()
