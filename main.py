import emoji
import functions
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from info import TOKEN
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update


GAME = range(1)
field = [1, 2, 3, 4, 5, 6, 7, 8, 9]  


def markup_key():
    keyboard = [['1', '2', '3'],
                ['4', '5', '6'],
                ['7', '8', '9']]  # список кнопок
    markup_key = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    return markup_key

# Обрабатываем команду /start если пользователь отменил разговор
def start(update, _):  # Старт

    user = update.message.from_user
    update.message.reply_text(emoji.emojize(f'Привет {user.first_name}!\n'
                                            'Тебя привествует игра\n:cross_mark: крестики-нолики :hollow_red_circle:.\n\n'
                                            'Правила игры: Игроки по очереди ставят на свободные клетки поля 3×3 знаки '
                                            '(один всегда крестики, другой всегда нолики). Первый, выстроивший в ряд 3 своих фигуры по вертикали, '
                                            'горизонтали или диагонали, выигрывает. Первый ход определяется жеребьевкой.\n\n'
                                            'Давай сыграем!'))
    update.message.reply_text(functions.field_play(field))
    # ход игрока
    update.message.reply_text(f'{user.first_name}, твой ход {chr(10060)}',
                                  reply_markup=markup_key())  # вывод сообщения в чат
    return GAME


# основная чать
def game(update, _):
    global field
    user = update.message.from_user

    # ход игрока
    motion = int(update.message.text)  # принимаем данные от игрока
    # если по данным ввода поле занято, просим ввести новые данные, до тех пор пока не будет введены данные свободной позиции
    while field[int(motion) - 1] == chr(10060) or field[int(motion) - 1] == chr(11093):
        update.message.reply_text(f'Поле занято повторите ввод!', reply_markup=markup_key()) 
        motion = int(update.message.text)  # принимаем данные от игрока
        # return PLAYER
    else: field[int(motion) - 1] = chr(10060)
     
    update.message.reply_text(functions.field_play(field))  # вывод поля в чат
    
    # условия выйгрышей
    if functions.check_win(field) == chr(10060):
        update.message.reply_text(f'Ура!!! {chr(10060)} выйграли!!!!', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    elif functions.check_win(field) == 9:
        update.message.reply_text(f'Игра окончена! Ничья!', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    
    # ход бота
    motion = functions.bot_motion(field)  
    field[motion] = chr(11093)  # изменение списка в соответсвоо с ходом бота
    update.message.reply_text(f'Бот сделал ход {chr(11093)} на позицию {motion + 1}')  # оповещение в чат
    
    update.message.reply_text(functions.field_play(field))  
    
    # условия выйгрышей
    if functions.check_win(field) == chr(11093):
        update.message.reply_text(f'Ура!!! {chr(11093)} выйграли!!!!', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    update.message.reply_text(f'{user.first_name}, твой ход {chr(10060)}',
                                  reply_markup=markup_key())  # вывод сообщения в чат
    
    return GAME
  



# Обрабатываем команду /cancel если пользователь отменил разговор
def cancel(update, _):
    
    update.message.reply_text(emoji.emojize(f'Пока :waving_hand:\n'),
                              reply_markup=ReplyKeyboardRemove())  # Отвечаем на отказ поговорить

    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater(TOKEN)  # Создаем Updater и передаем ему токен бота, токен вставляем в папку config.py

    dispatcher = updater.dispatcher  # получаем диспетчера для регистрации обработчиков

    # Определяем обработчик разговоров `ConversationHandler` 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],  # точка входа в разговор

        states={  # этапы разговора, каждый со своим списком обработчиков сообщений
            GAME: [MessageHandler(Filters.text, game)],
            
        },
        
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    
    dispatcher.add_handler(conv_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()
