import random
from confmanager import Config
try:
    import pyperclip
except ModuleNotFoundError:
    print("> Вами не был установлен модуль необходимый для работы программы модуль «pyperclip»!")
    print("> Продолжение работы программы невозможно.")
    quit()
BOOL_DICT: dict = {
    "да": True,
    "нет": False
}
CONFIG_PATH: str = 'passwords.json'
PASSWORD_CHARS: str = "+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
storage_file: Config = Config(CONFIG_PATH, {}) 


def requestInt(message: str, ErrorMessage: str = '> Введено нечисловое значение!') -> int:
    print(message, sep='')
    while True:
        try:
            val: int = int(input('> Ваш ввод: '))
            return val
        except ValueError:
            print(ErrorMessage)
def generatePass(length: int) -> str:
    return ''.join([random.choice(PASSWORD_CHARS) for i in range(length)]) 
def boolFromWord(word: str) -> bool:
    return BOOL_DICT[word.casefold()]
def getAgreement(message: str, errorMessage: str = '> Введённое слово невозможно интерпретировать как согласие/несогласие!') -> bool:
    print(message, sep='')
    while True:
        try:
            agreement: bool = boolFromWord(input('> Ваш ввод: '))
            return agreement
        except KeyError:
            print(errorMessage)

def requestPass() -> str:
    passwordLen: int = requestInt('> Введите необходимую длину пароля.')
    while True:
        password: str = generatePass(passwordLen)
        agree: bool = getAgreement(f'> Сгенерированный пароль: «{password}». Хотели бы Вы сгенерировать его заново?')
        if not agree:
            return password


# Базовые функции команд

def add(useGenerator: bool = None,
        errorMessage: str = '> Данный ключ уже используется! Пожалуйста, используйте команду «перезапись», если вы хотите изменить уже существующее значение!',
        passwordRequest: str = '> Введите желаемый пароль: ',
        keyRequest: str = '> Введите желаемый ключ пароля: ',
        successMessage: str = '> Пароль успешно записан в файл и скопирован в буфер обмена!',
        isAdding: bool = True) -> None:
    if useGenerator is None:
        useGenerator = getAgreement('> Хотели бы Вы использовать генератор пароля?')
    password: str = requestPass() if useGenerator else input(passwordRequest)
    key: str = input(keyRequest)
    try:
        storage_file.write((key, password), isAdding)
        pyperclip.copy(password)
        print(successMessage)
    except KeyError:
        print(errorMessage)

def deleteKey():
    key: str = input('> Введите ключ, который хотите удалить из файла: ')
    try:
        storage_file.delete(key)
        print(f'> Запись под ключом «{key}» успешно удалена!')
    except KeyError:
        print('> Записи под данным ключом не существует!')


def getVal() -> None:
    key: str = input('> Введите ключ пароля: ')
    try:
        pyperclip.copy(storage_file.contents[key])
        print('> Пароль скопирован!')
    except KeyError:
        print('> Пароля под таким ключом не существует!')

def getKeys() -> None:
    keys: set[str] = set(storage_file.contents.keys())
    keysLen: int = len(keys)
    if not keysLen:
        print('> Файл пуст!')
        return
    print('> Ключи:')
    for key in keys:
        print(f'- «{key}»')
    print(f'> Всего ключей: {len(keys)}')

# Класс команд

class Command:
    description: str = ''
    name: str = ''
    def run(self) -> None:
        pass

# Классы команд

class AddCommand(Command):
    description = 'добавляет в файл новый пароль.'
    name = 'добавить'
    def run(self) -> None:
        add()

class DeleteCommand(Command):
    description = 'удаляет из файла запись под определённым ключом.'
    name = 'удалить'
    def run(self) -> None:
        deleteKey()

class RewriteCommand(Command):
    description = 'перезаписывает пароль под определённым ключом.'
    name = 'перезапись'
    def run(self) -> None:
        add(isAdding=False, errorMessage='> Записи под этим ключом не существует! Пожалуйста, используйте команду «добавить» для создания новых записей.',
            passwordRequest='> Введите новый пароль: ',
            keyRequest='> Введите ключ, который хотите изменить: ',
            successMessage='> Пароль успешно изменён и скопирован в буфер обмена!')

class AddGeneratedCommand(Command):
    description = 'добавляет в файл новый сгенерированный пароль.'
    name = 'добавитьГен'
    def run(self) -> None:
        add(True)

class GetValueCommand(Command):
    description = 'копирует пароль под определённым ключом в Ваш буфер обмена.'
    name = 'получить'
    def run(self) -> None:
        getVal()

class GetKeysCommand(Command):
    description = 'выводит все использованные ключи в консоль.'
    name = 'получитьКлючи'
    def run(self) -> None:
        getKeys()

class AddWrotenCommand(Command):
    description = 'добавляет в файл новый написанный Вами пароль.'
    name = 'добавитьРуч'
    def run(self) -> None:
        add(False)
        
class QuitCommand(Command):
    description = 'завершает работу программы.'
    name = 'выход'
    def run(self) -> None:
        print('> Закрываем программу...')
        quit()


# TODO: Реализовать это более адекватным образом ,_,

IMPLEMENTED_COMMANDS: tuple[Command] = (AddCommand(), AddGeneratedCommand(), AddWrotenCommand(), RewriteCommand(), DeleteCommand(), GetValueCommand(), GetKeysCommand(), QuitCommand())

def executeHelpCommand():
    print('> Доступные команды:')
    for command in IMPLEMENTED_COMMANDS:
        print(f'- «{command.name}» - {command.description}')
    print('- «помощь» - выводит полный список команд с их описанием.')

def main():
    print('> Добро пожаловать в программу «MyPassManager»')
    print('> Напишите «помощь» для получения списка доступных команд, если вы тут впервые.')
    while True:
        cmd: str = input('> Введите команду: ')
        if cmd == 'помощь':
            executeHelpCommand()
            continue
        for command in IMPLEMENTED_COMMANDS:
            if command.name == cmd:
                command.run()
                break
        else:
            print('> Такой команды не существует! Напишите «помощь» для получения списка доступных команд.')
if __name__ == '__main__':
    main()