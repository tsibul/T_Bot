from telebot import TeleBot, types

class Phone:
    def __init__(self, *args, **kwargs):
        if len(args) == 5:
            self.surname = args[1]
            self.name = args[2]
            self.phone = args[3]
            self.phone_type = args[4]
            self.id = args[0]
        #            xxx = kwargs["key"]

        elif len(args) == 1:
            self.__init__(args[0][0], args[0][1], args[0][2], args[0][3], args[0][3])
        else:
            raise TypeError("wrong number of args")

    def __repr__(self):
        return self.id + ' ' + self.name + ' ' + self.surname + ' ' + self.phone

    def __str__(self):
        return self.id + ' ' + self.name + ' ' + self.surname + ' ' + (self.phone).replace(' ', '') + ' ' +self.phone_type


def split_string(string):
    string = string.replace('+', ' + ')
    string = string.replace('-', ' - ')
    string = string.replace('*', ' * ')
    string = string.replace('/', ' / ')
    string = string.replace('(', ' ( ')
    string = string.replace(')', ' ) ')
    return string.split()


def calc_parse(digit_lst):
    new_list = []
    try:
        for i in range(len(digit_lst)):
            if digit_lst[i] != '+' and digit_lst[i] != '-' and digit_lst[i] != '*' and digit_lst[i] != '/' and \
                digit_lst[i] != ')' and digit_lst[i] != '(' and i > 0:
                digit_lst[i] = float(digit_lst[i])
                if digit_lst[i-1] == '+':
                    new_list.append(digit_lst[i])
                elif digit_lst[i-1] == '-':
                    new_list.append(digit_lst[i] * -1)
                elif digit_lst[i-1] == '*':
                    new_list[-1] = digit_lst[i] * new_list[-1]
                elif digit_lst[i-1] == '/':
                    new_list[-1] = new_list[-1] / digit_lst[i]
            elif digit_lst[i] != '+' and digit_lst[i] != '-' and digit_lst[i] != '*' and digit_lst[i] != '/' and \
                    digit_lst[i] != ')' and digit_lst[i] != '(' and i == 0:
                digit_lst[i] = float(digit_lst[i])
                new_list.append(digit_lst[i])
        return sum(new_list)
    except:
        return 'error'


def calc_result(string2):
    count = 0

    while '(' in string2:
        string3 = string2
        try:
            for i in range(len(string2)):
                if string2[i] == '(':
                    count += 1
                    begin = i
                elif string2[i] == ')':
                    count -= 1
                    end = i
                    digit_lst2 = split_string(string2[begin + 1:end])
                    string3 = string3.replace(string2[begin:end + 1], str(calc_parse(digit_lst2)))
            string2 = string3
        except:
            return 'error'
    digit_lst3 = split_string(string2)
    return calc_parse(digit_lst3)


def change_turn(turn):
    if turn == 'x':
        turn = 'o'
    else:
        turn = 'x'
    return turn

def print_help():
    return '/calc - Калькулятор \n' \
           ' /cross - Крестики/нолики  \n ' \
           '/log - Логирование \n ' \
           '/phonebook - Телефонная книга'


def print_menu():
    return ('Введите пункт меню:' +
    '\n 1: Редактирование' +
    '\n 2: Экспорт' +
    '\n 3: Вывод' +
    '\n 8: Выйти')

def print_edit():
    return ('Введите пункт меню:'+
    '\n 1: Ввод' +
    '\n 2: Редактирование' +
    '\n 3: Удаление' +
    '\n 8: Возврат в главное меню')


def print_outputs():
    return ('Введите пункт меню:'+
    '\n 1: Показать всех' +
    '\n 2: Поиск по id' +
    '\n 3: Поиск' +
    '\n 8: Возврат в главное меню')


def print_exports():
    return ('Введите пункт меню:'+
    '\n 1: Экспорт в csv' +
    '\n 2: Экспорт в xml' +
    '\n 3: Экспорт в html' +
    '\n 8: Возврат в главное меню')


def arr_from_phonebook(phonebook):
    arr = []
    for phone in phonebook:
        arr.append(str(phone).split())
    return arr

