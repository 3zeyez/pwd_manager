from random import choice
from string import ascii_lowercase, ascii_uppercase, digits, punctuation


def create_pwd_randomly():
    all_chars = ascii_lowercase + ascii_uppercase + digits + punctuation
    pwd = ''.join([choice(all_chars) for _ in range(16)])
    while not is_pwd_strong(pwd):
        pwd = ''.join([choice(all_chars) for _ in range(16)])
    print(f'Password = {pwd}')
    return pwd


# verifier si le mot de passe contient des lettres, des numeros et des symboles
# verify that the password contain chars, digits and symbols
def is_pwd_strong(pwd):
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
def create_pwd():
    while True:
        strong_or_not = input("Wanna u follow strength polices? yes or no(Y/n)?")
        mene3milch_chek = True
        if strong_or_not.lower() in ["yes", "y"]:
            mene3milch_chek = False
        pwd = input('Password: ')
        if mene3milch_chek:
            break
        elif is_pwd_strong(pwd):
            break
    return pwd


# choisir si le mot de passe est au hazard ou non
# choose if the password is random or not
def pwd_random_or_not():
    while True:
        rand = input('Random password? yes or no? ')
        if rand.lower() in ['yes', 'no']:
            break
    return rand.lower() == 'yes'
