from secrets import choice
from telebot.types import ReplyKeyboardMarkup


# ход бота
def bot_motion(field):  
    motion_bot = choice(range(9))
    while field[motion_bot] == chr(10060) or field[motion_bot] == chr(11093):
        motion_bot = choice(range(9))
    return motion_bot

# проверка на выйгрыш или ничью
def check_win(field):  
    win_pos = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for i in win_pos:
        if field[i[0]] == field[i[1]] == field[i[2]] == chr(10060):
            return chr(10060)
        if field[i[0]] == field[i[1]] == field[i[2]] == chr(11093):
            return chr(11093)
    count = 0
    for i in range(9):
        if field[i] == chr(10060) or field[i] == chr(11093):
            count += 1
    if count == 9:
        return 9
    

# сoздание игрового поля
def field_play(field):

    return f'-----------------\n' \
           f'  {field[0]}     {field[1]}     {field[2]}\n' \
           '-----------------\n' \
           f'  {field[3]}     {field[4]}     {field[5]}\n' \
           '-----------------\n' \
           f'  {field[6]}     {field[7]}     {field[8]}\n'

