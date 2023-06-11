from passlib.context import CryptContext
from datetime import date

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password(password):
    return bcrypt_context.hash(password)


a = get_password('atda')

# print(a)


def correcter(cor):
    if int(cor) <= 9:
        cor = '0' + cor
        return cor
    else: 
        return cor


day = correcter(str(date.today().day))
month = correcter(str(date.today().month))
today = f'{day}.{month}.{date.today().year}'

# today = correcter(f'{date.today().month}')
print(today)
