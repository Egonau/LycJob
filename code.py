import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery, MessageId
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler, Filters)

import jobdata

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
CREATION_BEFORE_NAME, NAME, PAY, INFO_ABOUT_VACANCY, DEADLINE, CREATE, COST, CONNECT, EDITOR, ACCEPTOR = range(10)
# Callback data
ZERO, ONE, TWO, FIND_JOB, THREE, CONTENT, COMPUTER_HELP, PROGRAMMING, HELP_HOMEWORK, VOLUNTEER, MARKETING, \
LANGUAGES, SERVING, F_CONTENT, F_COMPUTER_HELP, F_PROGRAMMING, F_HELP_HOMEWORK, F_VOLUNTEER, F_MARKETING, \
F_LANGUAGES, F_SERVING, VACANCIES, NAME, PAY_CARD_OR_CASH, UPLOADER, WITHOUT_MONEY, ACCEPT, INFO, EDIT, VARIABLE_CHOOSE, E_ACCEPTED, E_ACCEPT, E_COMPUTER_HELP, E_CONTENT, E_PROGRAMMING, E_HELP_HOMEWORK, E_VOLUNTEER, E_MARKETING, \
E_LANGUAGES, E_SERVING, E_NAME, E_DESCRIPTION, E_DEADLINE, E_CONNECTION, E_COST, E_TYPE = \
    range(46)
NEEDED = {}
SEEN_VACANCY = []
ACTIVE_USERS = {}
NUMBER = {}
CHOSEN_VAR = {}
TEXT = {}


def start(update: Update, context: CallbackContext) -> None:
    """Send message on `/start`."""
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    ACTIVE_USERS["{}".format(user.id)] = {}
    NEEDED["{}".format(user.id)] = []
    NUMBER["{}".format(user.id)] = []
    logger.info(ACTIVE_USERS)
    keyboard = [
        [
            InlineKeyboardButton("Создать/изменить вакансию", callback_data=str(ONE)),
        ],
        [
            InlineKeyboardButton("Найти вакансию", callback_data=str(FIND_JOB)),
        ],
        [
            InlineKeyboardButton("Информация", callback_data=str(INFO)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Что вы хотите сделать?", reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def zero(update: Update, context: CallbackContext) -> None:
    """Prompt same text & keyboard as `start` does but not as new message"""
    query = update.callback_query
    query.answer()
    NEEDED["{}".format(update.callback_query.from_user.id)] = {}
    NUMBER["{}".format(update.callback_query.from_user.id)] = -1
    TEXT["{}".format((update.callback_query.from_user.id))] = None
    keyboard = [
        [
            InlineKeyboardButton("Создать/изменить/удалить вакансию", callback_data=str(ONE)),
        ],
        [
            InlineKeyboardButton("Найти вакансию", callback_data=str(FIND_JOB)),
        ],
        [
            InlineKeyboardButton("Информация", callback_data=str(INFO)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Что вы хотите сделать?", reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def info(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data=str(ZERO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="ВАЖНЫЙ ТЕКСТ", reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def one(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Создать новую", callback_data=str(TWO)),
        ],
        [
            InlineKeyboardButton("Изменить существующую", callback_data=str(EDIT)),
        ],
        [
            InlineKeyboardButton("Назад", callback_data=str(ZERO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Что именно вы хотите сделать?", reply_markup=reply_markup
    )
    return CREATION_BEFORE_NAME


def find_job(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NEEDED["{}".format(update.callback_query.from_user.id)] = {}
    NUMBER["{}".format(update.callback_query.from_user.id)] = -1
    keyboard = [
        [
            InlineKeyboardButton("Создание контента", callback_data=str(F_CONTENT)),
            InlineKeyboardButton("Компьютерная помощь", callback_data=str(F_COMPUTER_HELP)),
        ], [
            InlineKeyboardButton("Программирование", callback_data=str(F_PROGRAMMING)),
            InlineKeyboardButton("Уроки(помощь)", callback_data=str(F_HELP_HOMEWORK))], [
            InlineKeyboardButton("Волонтерская помощь", callback_data=str(F_VOLUNTEER)),
            InlineKeyboardButton("Маркетинг", callback_data=str(F_MARKETING))], [
            InlineKeyboardButton("Языки", callback_data=str(F_LANGUAGES)),
            InlineKeyboardButton("Обслуживание", callback_data=str(F_SERVING))], [
            InlineKeyboardButton("Назад", callback_data=str(ZERO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Выберите тип вакансии", reply_markup=reply_markup
    )


def two(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Создание контента", callback_data=str(CONTENT)),
            InlineKeyboardButton("Компьютерная помощь", callback_data=str(COMPUTER_HELP)),
        ], [
            InlineKeyboardButton("Программирование", callback_data=str(PROGRAMMING)),
            InlineKeyboardButton("Уроки(помощь)", callback_data=str(HELP_HOMEWORK))], [
            InlineKeyboardButton("Волонтерская помощь", callback_data=str(VOLUNTEER)),
            InlineKeyboardButton("Маркетинг", callback_data=str(MARKETING))], [
            InlineKeyboardButton("Языки", callback_data=str(LANGUAGES)),
            InlineKeyboardButton("Обслуживание", callback_data=str(SERVING))], [
            InlineKeyboardButton("Назад", callback_data=str(ONE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Выберите тип вакансии", reply_markup=reply_markup
    )
    return CREATION_BEFORE_NAME


def content(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] = "Создание контента"
    logger.info(ACTIVE_USERS)
    keyboard = [[InlineKeyboardButton("Назад", callback_data=str(TWO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Введите название вакансии", reply_markup=reply_markup
    )
    return CREATION_BEFORE_NAME


def computer_help(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] = "Компьютерная помощь"
    logger.info(ACTIVE_USERS)
    keyboard = [[InlineKeyboardButton("Назад", callback_data=str(TWO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Введите название вакансии", reply_markup=reply_markup
    )
    return CREATION_BEFORE_NAME


def programming(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] = "Программирование"
    logger.info(ACTIVE_USERS)
    keyboard = [[InlineKeyboardButton("Назад", callback_data=str(TWO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Введите название вакансии", reply_markup=reply_markup
    )
    return CREATION_BEFORE_NAME


def help_homework(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] = "Уроки(помощь)"
    logger.info(ACTIVE_USERS)
    keyboard = [[InlineKeyboardButton("Назад", callback_data=str(TWO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Введите название вакансии", reply_markup=reply_markup
    )
    return CREATION_BEFORE_NAME


def volunteer(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] = "Волонтерская помощь"
    logger.info(ACTIVE_USERS)
    keyboard = [[InlineKeyboardButton("Назад", callback_data=str(TWO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Введите название вакансии", reply_markup=reply_markup
    )
    return CREATION_BEFORE_NAME


def marketing(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] = "Маркетинг"
    logger.info(ACTIVE_USERS)
    keyboard = [[InlineKeyboardButton("Назад", callback_data=str(TWO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Введите название вакансии", reply_markup=reply_markup
    )
    return CREATION_BEFORE_NAME


def languages(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] = "Языки"
    logger.info(ACTIVE_USERS)
    keyboard = [[InlineKeyboardButton("Назад", callback_data=str(TWO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Введите название вакансии", reply_markup=reply_markup
    )
    return CREATION_BEFORE_NAME


def serving(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] = "Обслуживание"
    logger.info(ACTIVE_USERS)
    keyboard = [[InlineKeyboardButton("Назад", callback_data=str(TWO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Введите название вакансии", reply_markup=reply_markup
    )
    return CREATION_BEFORE_NAME


def delete(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NEEDED["{}".format(update.callback_query.from_user.id)] = {}
    NUMBER["{}".format(update.callback_query.from_user.id)] = -1

    keyboard = [
        [
            InlineKeyboardButton("Создание контента", callback_data=str(E_CONTENT)),
            InlineKeyboardButton("Компьютерная помощь", callback_data=str(E_COMPUTER_HELP)),
        ], [
            InlineKeyboardButton("Программирование", callback_data=str(E_PROGRAMMING)),
            InlineKeyboardButton("Уроки(помощь)", callback_data=str(E_HELP_HOMEWORK))], [
            InlineKeyboardButton("Волонтерская помощь", callback_data=str(E_VOLUNTEER)),
            InlineKeyboardButton("Маркетинг", callback_data=str(E_MARKETING))], [
            InlineKeyboardButton("Языки", callback_data=str(E_LANGUAGES)),
            InlineKeyboardButton("Обслуживание", callback_data=str(E_SERVING))], [
            InlineKeyboardButton("Назад", callback_data=str(ONE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Выберите тип вакансии", reply_markup=reply_markup
    )
    return CREATION_BEFORE_NAME




def edit(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NEEDED["{}".format(update.callback_query.from_user.id)] = {}
    NUMBER["{}".format(update.callback_query.from_user.id)] = -1

    keyboard = [
        [
            InlineKeyboardButton("Создание контента", callback_data=str(E_CONTENT)),
            InlineKeyboardButton("Компьютерная помощь", callback_data=str(E_COMPUTER_HELP)),
        ], [
            InlineKeyboardButton("Программирование", callback_data=str(E_PROGRAMMING)),
            InlineKeyboardButton("Уроки(помощь)", callback_data=str(E_HELP_HOMEWORK))], [
            InlineKeyboardButton("Волонтерская помощь", callback_data=str(E_VOLUNTEER)),
            InlineKeyboardButton("Маркетинг", callback_data=str(E_MARKETING))], [
            InlineKeyboardButton("Языки", callback_data=str(E_LANGUAGES)),
            InlineKeyboardButton("Обслуживание", callback_data=str(E_SERVING))], [
            InlineKeyboardButton("Назад", callback_data=str(ONE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Выберите тип вакансии", reply_markup=reply_markup
    )
    return CREATION_BEFORE_NAME


def e_name(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    CHOSEN_VAR["{}".format(update.callback_query.from_user.id)] = 'name_of_vacancy'
    query.edit_message_text(
        text="Введите название вакансии"
    )
    return ACCEPTOR


def e_description(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    CHOSEN_VAR["{}".format(update.callback_query.from_user.id)] = "about_vacancy"
    query.edit_message_text(
        text="Введите описание вакансии"
    )
    return ACCEPTOR


def e_deadline(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    CHOSEN_VAR["{}".format(update.callback_query.from_user.id)] = 'deadline'
    query.edit_message_text(
        text="Введите дедлайн вакансии"
    )
    return ACCEPTOR


def e_cost(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    CHOSEN_VAR["{}".format(update.callback_query.from_user.id)] = 'cost'
    query.edit_message_text(
        text="Введите стоимость"
    )
    return ACCEPTOR


def e_connection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    CHOSEN_VAR["{}".format(update.callback_query.from_user.id)] = 'connection'
    query.edit_message_text(
        text="Введите средство связи"
    )
    return ACCEPTOR


def e_accept(update: Update, context: CallbackContext) -> None:
    TEXT["{}".format(update.message.from_user.id)] = update.message.text
    logger.info(TEXT)
    keyboard = [[InlineKeyboardButton("Подтверждаю", callback_data=str(E_ACCEPTED))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        text="Подтвердите изменение", reply_markup=reply_markup
    )
    return ACCEPTOR


def e_accepted(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NEEDED["{}".format(update.callback_query.from_user.id)][
        NUMBER["{}".format(update.callback_query.from_user.id)] % len(
            NEEDED["{}".format(update.callback_query.from_user.id)])][
        CHOSEN_VAR["{}".format(update.callback_query.from_user.id)]] = TEXT[
        "{}".format(update.callback_query.from_user.id)]
    ACTIVE_USERS["{}".format(update.callback_query.from_user.id)] = \
        NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Компьютерная помощь":
        jobdata.PCColl.update_one({"_id": ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["_id"]}, {
            "$set": {CHOSEN_VAR["{}".format(update.callback_query.from_user.id)]: TEXT[
                "{}".format(update.callback_query.from_user.id)]}})
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Программирование":
        jobdata.ProgColl.update_one({"_id": ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["_id"]}, {
            "$set": {CHOSEN_VAR["{}".format(update.callback_query.from_user.id)]: TEXT[
                "{}".format(update.callback_query.from_user.id)]}})
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Уроки(помощь)":
        jobdata.LessColl.update_one({"_id": ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["_id"]}, {
            "$set": {CHOSEN_VAR["{}".format(update.callback_query.from_user.id)]: TEXT[
                "{}".format(update.callback_query.from_user.id)]}})
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Волонтерская помощь":
        jobdata.VolColl.update_one({"_id": ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["_id"]}, {
            "$set": {CHOSEN_VAR["{}".format(update.callback_query.from_user.id)]: TEXT[
                "{}".format(update.callback_query.from_user.id)]}})
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Маркетинг":
        jobdata.MarkColl.update_one({"_id": ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["_id"]}, {
            "$set": {CHOSEN_VAR["{}".format(update.callback_query.from_user.id)]: TEXT[
                "{}".format(update.callback_query.from_user.id)]}})
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Языки":
        jobdata.LangColl.update_one({"_id": ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["_id"]}, {
            "$set": {CHOSEN_VAR["{}".format(update.callback_query.from_user.id)]: TEXT[
                "{}".format(update.callback_query.from_user.id)]}})
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Обслуживание":
        jobdata.ServColl.update_one({"_id": ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["_id"]}, {
            "$set": {CHOSEN_VAR["{}".format(update.callback_query.from_user.id)]: TEXT[
                "{}".format(update.callback_query.from_user.id)]}})
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Создание контента":
        jobdata.ContColl.update_one({"_id": ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["_id"]}, {
            "$set": {CHOSEN_VAR["{}".format(update.callback_query.from_user.id)]: TEXT[
                "{}".format(update.callback_query.from_user.id)]}})
    keyboard = [[InlineKeyboardButton("Назад", callback_data=str(EDIT))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Успешно изменено", reply_markup=reply_markup
    )
    return CREATION_BEFORE_NAME


def variable_choose(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    CHOSEN_VAR["{}".format(update.callback_query.from_user.id)] = None
    keyboard = [
        [
            InlineKeyboardButton("Название вакансии", callback_data=str(E_NAME)),
            InlineKeyboardButton("Описание вакансии", callback_data=str(E_DESCRIPTION)),
        ], [
            InlineKeyboardButton("Стоимость", callback_data=str(E_COST)),
            InlineKeyboardButton("Дедлайн", callback_data=str(E_DEADLINE))],
            [InlineKeyboardButton("Средство связи", callback_data=str(E_CONNECTION)),
            InlineKeyboardButton("Назад", callback_data=str(EDIT)),

        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Название вакансии", callback_data=str(E_NAME)),
            InlineKeyboardButton("Описание вакансии", callback_data=str(E_DESCRIPTION)),
        ], [
            InlineKeyboardButton("Дедлайн", callback_data=str(E_DEADLINE)),
            InlineKeyboardButton("Средство связи", callback_data=str(E_CONNECTION))], [
            InlineKeyboardButton("Назад", callback_data=str(EDIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    if (NEEDED["{}".format(update.callback_query.from_user.id)][
        NUMBER["{}".format(update.callback_query.from_user.id)] % len(
            NEEDED["{}".format(update.callback_query.from_user.id)])]['cost'] is None):
        query.edit_message_text(
            text="Выберите параметр для изменения", reply_markup=reply_markup2
        )
    else:
        query.edit_message_text(
            text="Выберите параметр для изменения", reply_markup=reply_markup
        )

    return CREATION_BEFORE_NAME


def e_computer_help(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(
        jobdata.PCColl.find({'user_id': update.callback_query.from_user.id}))
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Изменить", callback_data=str(VARIABLE_CHOOSE))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(E_COMPUTER_HELP))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def e_programming(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(
        jobdata.ProgColl.find({'user_id': update.callback_query.from_user.id}))
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Изменить", callback_data=str(VARIABLE_CHOOSE))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(E_PROGRAMMING))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def e_volunteer(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(
        jobdata.VolColl.find({'user_id': update.callback_query.from_user.id}))
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Изменить", callback_data=str(VARIABLE_CHOOSE))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(E_VOLUNTEER))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def e_content(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(
        jobdata.ContColl.find({'user_id': update.callback_query.from_user.id}))
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Изменить", callback_data=str(VARIABLE_CHOOSE))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(E_CONTENT))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def e_languages(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(
        jobdata.LangColl.find({'user_id': update.callback_query.from_user.id}))
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Изменить", callback_data=str(VARIABLE_CHOOSE))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(E_LANGUAGES))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def e_serving(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(
        jobdata.ServColl.find({'user_id': update.callback_query.from_user.id}))
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Изменить", callback_data=str(VARIABLE_CHOOSE))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(E_SERVING))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def e_marketing(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(
        jobdata.MarkColl.find({'user_id': update.callback_query.from_user.id}))
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Изменить", callback_data=str(VARIABLE_CHOOSE))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(E_MARKETING))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def e_help_homework(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(
        jobdata.LessColl.find({'user_id': update.callback_query.from_user.id}))
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Изменить", callback_data=str(VARIABLE_CHOOSE))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(E_HELP_HOMEWORK))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(EDIT))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def name(update: Update, context: CallbackContext) -> None:
    TEXT["{}".format(update.message.from_user.id)] = update.message.text
    ACTIVE_USERS["{}".format(update.message.from_user.id)]["user_id"] = update.message.from_user.id
    ACTIVE_USERS["{}".format(update.message.from_user.id)]["username"] = update.message.from_user.username
    ACTIVE_USERS["{}".format(update.message.from_user.id)]["connection"] = None
    ACTIVE_USERS["{}".format(update.message.from_user.id)]["name_of_vacancy"] = TEXT[
        "{}".format(update.message.from_user.id)]
    logger.info(ACTIVE_USERS)
    update.message.reply_text(
        text="Введите описание вакансии"
    )
    return INFO_ABOUT_VACANCY


def info_about_vacancy(update: Update, context: CallbackContext) -> None:
    TEXT["{}".format(update.message.from_user.id)] = update.message.text
    ACTIVE_USERS["{}".format(update.message.from_user.id)]["about_vacancy"] = TEXT[
        "{}".format(update.message.from_user.id)]
    logger.info(ACTIVE_USERS)
    keyboard = [
        [
            InlineKeyboardButton("Сдельная", callback_data=str(PAY_CARD_OR_CASH))], [
            InlineKeyboardButton("Безвозмездная работа", callback_data=str(WITHOUT_MONEY))]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        text="Введите тип оплаты", reply_markup=reply_markup
    )
    return PAY


def pay_card_or_cash(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["payment"] = "Сдельная"
    logger.info(ACTIVE_USERS)
    query.message.reply_text(
        text="Введите стоимость"
    )
    return COST


def cost(update: Update, context: CallbackContext) -> None:
    TEXT["{}".format(update.message.from_user.id)] = update.message.text
    ACTIVE_USERS["{}".format(update.message.from_user.id)]["cost"] = TEXT["{}".format(update.message.from_user.id)]
    logger.info(ACTIVE_USERS)
    update.message.reply_text(text="Укажите срок выполнения работы")
    return DEADLINE


def without_money(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["payment"] = "Безвозмездная работа"
    ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["cost"] = None
    logger.info(ACTIVE_USERS)
    query.message.reply_text(
        text="Укажите срок выполнения работы"
    )
    return DEADLINE


def deadline(update: Update, context: CallbackContext) -> None:
    TEXT["{}".format(update.message.from_user.id)] = update.message.text
    print(update.message.from_user)
    ACTIVE_USERS["{}".format(update.message.from_user.id)]["deadline"] = TEXT["{}".format(update.message.from_user.id)]
    logger.info(ACTIVE_USERS)
    update.message.reply_text(
        text="Введите данные для связи"
    )
    return CONNECT


def connection(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Создать", callback_data=str(CREATE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    TEXT["{}".format(update.message.from_user.id)] = update.message.text
    ACTIVE_USERS["{}".format(update.message.from_user.id)]["connection"] = TEXT[
        "{}".format(update.message.from_user.id)]
    update.message.reply_text(
        text="Создать вакансию?", reply_markup=reply_markup)
    return CREATE


def create(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Компьютерная помощь":
        jobdata.PCColl.insert_one(ACTIVE_USERS["{}".format(update.callback_query.from_user.id)])
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Программирование":
        jobdata.ProgColl.insert_one(ACTIVE_USERS["{}".format(update.callback_query.from_user.id)])
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Уроки(помощь)":
        jobdata.LessColl.insert_one(ACTIVE_USERS["{}".format(update.callback_query.from_user.id)])
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Волонтерская помощь":
        jobdata.VolColl.insert_one(ACTIVE_USERS["{}".format(update.callback_query.from_user.id)])
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Маркетинг":
        jobdata.MarkColl.insert_one(ACTIVE_USERS["{}".format(update.callback_query.from_user.id)])
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Языки":
        jobdata.LangColl.insert_one(ACTIVE_USERS["{}".format(update.callback_query.from_user.id)])
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Обслуживание":
        jobdata.ServColl.insert_one(ACTIVE_USERS["{}".format(update.callback_query.from_user.id)])
    if ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["type_of_work"] == "Создание контента":
        jobdata.ContColl.insert_one(ACTIVE_USERS["{}".format(update.callback_query.from_user.id)])
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data=str(ZERO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text(
        text="Вакансия успешно создана", reply_markup=reply_markup)
    ACTIVE_USERS["{}".format(update.callback_query.from_user.id)].clear()
    return CREATION_BEFORE_NAME


def accept(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data=FIND_JOB)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if (NEEDED["{}".format(update.callback_query.from_user.id)][
        NUMBER["{}".format(update.callback_query.from_user.id)] % len(
            NEEDED["{}".format(update.callback_query.from_user.id)])]["username"] is None):
        query.message.edit_text(text="Данные для связи: {}".format(
            NEEDED["{}".format(update.callback_query.from_user.id)][
                NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                    NEEDED["{}".format(update.callback_query.from_user.id)])]["connection"]
        ), reply_markup=reply_markup)
    else:
        query.message.edit_text(text="Ник: @{} \n"
                                     "Дополнительные данные для связи: {}".format(
            NEEDED["{}".format(update.callback_query.from_user.id)][
                NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                    NEEDED["{}".format(update.callback_query.from_user.id)])]["username"],
            NEEDED["{}".format(update.callback_query.from_user.id)][
                NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                    NEEDED["{}".format(update.callback_query.from_user.id)])]["connection"]
        ), reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def f_computer_help(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(jobdata.PCColl.find())
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(F_COMPUTER_HELP))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def f_programming(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(jobdata.ProgColl.find())
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(F_PROGRAMMING))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def f_help_homework(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(jobdata.LessColl.find())
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(F_HELP_HOMEWORK))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def f_volunteer(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(jobdata.VolColl.find())
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(F_VOLUNTEER))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def f_marketing(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(jobdata.MarkColl.find())
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(F_MARKETING))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def f_languages(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(jobdata.LangColl.find())
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(F_LANGUAGES))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def f_serving(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(jobdata.ServColl.find())
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(F_SERVING))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def f_content(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    NUMBER["{}".format(update.callback_query.from_user.id)] += 1
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(jobdata.ContColl.find())
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Следующий", callback_data=str(F_CONTENT))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    if (len(NEEDED["{}".format(update.callback_query.from_user.id)]) == 0):
        query.message.reply_text(text="Нет вакансий выбранного типа", reply_markup=reply_markup2)
    else:
        if (NEEDED["{}".format(update.callback_query.from_user.id)][
            NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"] != "Сдельная"):
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСтоимость: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["cost"],
                NEEDED["{}".format(update.callback_query.from_user.id)][
                    NUMBER["{}".format(update.callback_query.from_user.id)] % len(
                        NEEDED["{}".format(update.callback_query.from_user.id)])]["deadline"]),
                reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def main():
    updater = Updater("1617510398:AAG4zbRLKarnb9tvW_0clME-n97riE7-Y_g")

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CREATION_BEFORE_NAME: [
                CallbackQueryHandler(zero, pattern='^' + str(ZERO) + '$'),
                CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(info, pattern='^' + str(INFO) + '$'),
                CallbackQueryHandler(find_job, pattern='^' + str(FIND_JOB) + '$'),
                CallbackQueryHandler(content, pattern='^' + str(CONTENT) + '$'),
                CallbackQueryHandler(computer_help, pattern='^' + str(COMPUTER_HELP) + '$'),
                CallbackQueryHandler(programming, pattern='^' + str(PROGRAMMING) + '$'),
                CallbackQueryHandler(help_homework, pattern='^' + str(HELP_HOMEWORK) + '$'),
                CallbackQueryHandler(volunteer, pattern='^' + str(VOLUNTEER) + '$'),
                CallbackQueryHandler(languages, pattern='^' + str(LANGUAGES) + '$'),
                CallbackQueryHandler(serving, pattern='^' + str(SERVING) + '$'),
                CallbackQueryHandler(marketing, pattern='^' + str(MARKETING) + '$'),
                CallbackQueryHandler(f_content, pattern='^' + str(F_CONTENT) + '$'),
                CallbackQueryHandler(f_computer_help, pattern='^' + str(F_COMPUTER_HELP) + '$'),
                CallbackQueryHandler(f_programming, pattern='^' + str(F_PROGRAMMING) + '$'),
                CallbackQueryHandler(f_help_homework, pattern='^' + str(F_HELP_HOMEWORK) + '$'),
                CallbackQueryHandler(f_volunteer, pattern='^' + str(F_VOLUNTEER) + '$'),
                CallbackQueryHandler(f_languages, pattern='^' + str(F_LANGUAGES) + '$'),
                CallbackQueryHandler(f_serving, pattern='^' + str(F_SERVING) + '$'),
                CallbackQueryHandler(f_marketing, pattern='^' + str(F_MARKETING) + '$'),
                CallbackQueryHandler(e_content, pattern='^' + str(E_CONTENT) + '$'),
                CallbackQueryHandler(e_programming, pattern='^' + str(E_PROGRAMMING) + '$'),
                CallbackQueryHandler(e_help_homework, pattern='^' + str(E_HELP_HOMEWORK) + '$'),
                CallbackQueryHandler(e_volunteer, pattern='^' + str(E_VOLUNTEER) + '$'),
                CallbackQueryHandler(e_languages, pattern='^' + str(E_LANGUAGES) + '$'),
                CallbackQueryHandler(e_serving, pattern='^' + str(E_SERVING) + '$'),
                CallbackQueryHandler(e_marketing, pattern='^' + str(E_MARKETING) + '$'),
                CallbackQueryHandler(e_computer_help, pattern='^' + str(E_COMPUTER_HELP) + '$'),
                CallbackQueryHandler(accept, pattern='^' + str(ACCEPT) + '$'),
                CallbackQueryHandler(edit, pattern='^' + str(EDIT) + '$'),
                CallbackQueryHandler(variable_choose, pattern='^' + str(VARIABLE_CHOOSE) + '$'),
                CallbackQueryHandler(e_name, pattern='^' + str(E_NAME) + '$'),
                CallbackQueryHandler(e_description, pattern='^' + str(E_DESCRIPTION) + '$'),
                CallbackQueryHandler(e_deadline, pattern='^' + str(E_DEADLINE) + '$'),
                CallbackQueryHandler(e_connection, pattern='^' + str(E_CONNECTION) + '$'),
                CallbackQueryHandler(e_cost, pattern='^' + str(E_COST) + '$'),
                CommandHandler('start', start), MessageHandler(Filters.text, name),
            ],
            PAY: [CallbackQueryHandler(pay_card_or_cash, pattern='^' + str(PAY_CARD_OR_CASH) + '$'),
                  CallbackQueryHandler(without_money, pattern='^' + str(WITHOUT_MONEY) + '$'),
                  CommandHandler('start', start), MessageHandler(Filters.text, name),
                  ],

            ACCEPTOR: [
                CallbackQueryHandler(e_accept, pattern='^' + str(E_ACCEPT) + '$'),
                CallbackQueryHandler(e_accepted, pattern='^' + str(E_ACCEPTED) + '$'),
                CommandHandler('start', start), MessageHandler(Filters.text, e_accept),
            ],
            INFO_ABOUT_VACANCY: [CommandHandler('start', start), MessageHandler(Filters.text, info_about_vacancy),
                                 MessageHandler(Filters.text, name)],
            DEADLINE: [CommandHandler('start', start), MessageHandler(Filters.text, deadline)],
            CREATE: [CallbackQueryHandler(create, pattern='^' + str(CREATE) + '$'),
                     CommandHandler('start', start), MessageHandler(Filters.text, name)],
            COST: [CommandHandler('start', start), MessageHandler(Filters.text, cost)],
            CONNECT: [CommandHandler('start', start), MessageHandler(Filters.text, connection)]
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
