import logging
from array import array

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery
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
CREATION_BEFORE_NAME, NAME, PAY, INFO_ABOUT_VACANCY, DEADLINE, CREATE, COST = range(7)
# Callback data
ZERO, ONE, TWO, FIND_JOB, THREE, CONTENT, COMPUTER_HELP, PROGRAMMING, HELP_HOMEWORK, VOLUNTEER, MARKETING, \
LANGUAGES, SERVING, F_CONTENT, F_COMPUTER_HELP, F_PROGRAMMING, F_HELP_HOMEWORK, F_VOLUNTEER, F_MARKETING, \
F_LANGUAGES, F_SERVING, VACANCIES, NAME, PAY_CARD_OR_CASH, UPLOADER, WITHOUT_MONEY, ACCEPT, INFO = \
    range(28)
NEEDED = {}
LASTID = {}
SEEN_VACANCY = []
ACTIVE_USERS = {}


def start(update: Update, context: CallbackContext) -> None:
    """Send message on `/start`."""
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    ACTIVE_USERS["{}".format(user.id)] = {}
    NEEDED["{}".format(user.id)] = []
    LASTID["{}".format(user.id)] = {}
    logger.info(ACTIVE_USERS)
    logger.info(LASTID)
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
            InlineKeyboardButton("Изменить существующую", callback_data=str(THREE)),
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
    NEEDED.clear()
    LASTID.clear()
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


def name(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    ACTIVE_USERS["{}".format(update.message.from_user.id)]["user_id"] = update.message.from_user.id
    ACTIVE_USERS["{}".format(update.message.from_user.id)]["name_of_vacancy"] = text
    logger.info(ACTIVE_USERS)
    update.message.reply_text(
        text="Введите описание вакансии"
    )
    return INFO_ABOUT_VACANCY


def info_about_vacancy(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    ACTIVE_USERS["{}".format(update.message.from_user.id)]["about_vacancy"] = text
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
    text = update.message.text
    ACTIVE_USERS["{}".format(update.message.from_user.id)]["cost"] = text
    logger.info(ACTIVE_USERS)
    update.message.reply_text(text="Укажите срок выполнения работы")
    return DEADLINE


def without_money(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    ACTIVE_USERS["{}".format(update.callback_query.from_user.id)]["payment"] = "Безвозмездная работа"
    logger.info(ACTIVE_USERS)
    query.message.reply_text(
        text="Укажите срок выполнения работы"
    )
    return DEADLINE


def deadline(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    print(update.message.from_user)
    ACTIVE_USERS["{}".format(update.message.from_user.id)]["deadline"] = text
    logger.info(ACTIVE_USERS)
    keyboard = [
        [
            InlineKeyboardButton("Создать", callback_data=str(CREATE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
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

    query.message.reply_text(
        text="Вакансия успешно создана."
    )
    ACTIVE_USERS["{}".format(update.callback_query.from_user.id)].clear()
    return ConversationHandler.END


def accept(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    logger.info(LASTID["{}".format(update.callback_query.from_user.id)])
    for i in range(0, LASTID["{}".format(update.callback_query.from_user.id)]):
        query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data=FIND_JOB)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    logger.info(LASTID)
    logger.info(query.message.message_id)
    query.message.reply_text(text="Ник: @{}".format(
        NEEDED[query.message.message_id - LASTID[0] - 1]["username"]
    ), reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def f_computer_help(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    LASTID["{}".format(update.callback_query.from_user.id)] = []
    NEEDED["{}".format(update.callback_query.from_user.id)] = list(jobdata.PCColl.find())
    LASTID["{}".format(update.callback_query.from_user.id)].append(query.message.message_id)
    logger.info(NEEDED["{}".format(update.callback_query.from_user.id)])
    for i in range(0,len(NEEDED["{}".format(update.callback_query.from_user.id)])):
        logger.info(LASTID)
        if i == len(NEEDED["{}".format(update.callback_query.from_user.id)]) - 1:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][i]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][i]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][i]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][i]["deadline"]),
                reply_markup=reply_markup2)
            LASTID["{}".format(update.callback_query.from_user.id)].append(query.message.message_id)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED["{}".format(update.callback_query.from_user.id)][i]["name_of_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][i]["about_vacancy"],
                NEEDED["{}".format(update.callback_query.from_user.id)][i]["payment"],
                NEEDED["{}".format(update.callback_query.from_user.id)][i]["deadline"]),
                reply_markup=reply_markup)
            LASTID["{}".format(update.callback_query.from_user.id)].append(query.message.message_id)

    return CREATION_BEFORE_NAME


def f_programming(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    vacancies = jobdata.ProgColl.find()
    LASTID.clear()
    NEEDED.clear()
    for i in vacancies:
        if i["type_of_work"] == "Программирование":
            NEEDED.append(i)
    for i in range(0, len(NEEDED)):
        if i == 0:
            LASTID.append(query.message.message_id)
        if i == len(NEEDED) - 1:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED[i]["name_of_vacancy"],
                NEEDED[i]["about_vacancy"],
                NEEDED[i]["payment"], NEEDED[i]["deadline"]), reply_markup=reply_markup2)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED[i]["name_of_vacancy"],
                NEEDED[i]["about_vacancy"],
                NEEDED[i]["payment"], NEEDED[i]["deadline"]), reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def f_help_homework(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    vacancies = jobdata.LessColl.find()
    LASTID.clear()
    NEEDED.clear()
    for i in vacancies:
        if i["type_of_work"] == "Уроки(помощь)":
            NEEDED.append(i)
    for i in range(0, len(NEEDED)):
        if i == 0:
            LASTID.append(query.message.message_id)
        if i == len(NEEDED) - 1:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED[i]["name_of_vacancy"],
                NEEDED[i]["about_vacancy"],
                NEEDED[i]["payment"], NEEDED[i]["deadline"]), reply_markup=reply_markup2)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED[i]["name_of_vacancy"],
                NEEDED[i]["about_vacancy"],
                NEEDED[i]["payment"], NEEDED[i]["deadline"]), reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def f_volunteer(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    vacancies = jobdata.VolColl.find()
    LASTID.clear()
    NEEDED.clear()
    for i in range(0, len(NEEDED)):
        if i == 0:
            LASTID.append(query.message.message_id)
        if i == len(NEEDED) - 1:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED[i]["name_of_vacancy"],
                NEEDED[i]["about_vacancy"],
                NEEDED[i]["payment"], NEEDED[i]["deadline"]), reply_markup=reply_markup2)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED[i]["name_of_vacancy"],
                NEEDED[i]["about_vacancy"],
                NEEDED[i]["payment"], NEEDED[i]["deadline"]), reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def f_marketing(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    vacancies = jobdata.MarkColl.find()
    LASTID.clear()
    NEEDED.clear()
    for i in vacancies:
        if i["type_of_work"] == "Маркетинг":
            NEEDED.append(i)
    for i in range(0, len(NEEDED)):
        if i == 0:
            LASTID.append(query.message.message_id)
        if i == len(NEEDED) - 1:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED[i]["name_of_vacancy"],
                NEEDED[i]["about_vacancy"],
                NEEDED[i]["payment"], NEEDED[i]["deadline"]), reply_markup=reply_markup2)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED[i]["name_of_vacancy"],
                NEEDED[i]["about_vacancy"],
                NEEDED[i]["payment"], NEEDED[i]["deadline"]), reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def f_languages(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    vacancies = jobdata.LangColl.find()
    LASTID.clear()
    NEEDED.clear()
    for i in vacancies:
        if i["type_of_work"] == "Языки":
            NEEDED.append(i)
    for i in range(0, len(NEEDED)):
        if i == 0:
            LASTID.append(query.message.message_id)
        if i == len(NEEDED) - 1:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED[i]["name_of_vacancy"],
                NEEDED[i]["about_vacancy"],
                NEEDED[i]["payment"], NEEDED[i]["deadline"]), reply_markup=reply_markup2)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED[i]["name_of_vacancy"],
                NEEDED[i]["about_vacancy"],
                NEEDED[i]["payment"], NEEDED[i]["deadline"]), reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def f_serving(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    vacancies = jobdata.ServColl.find()
    LASTID.clear()
    NEEDED.clear()
    for i in vacancies:
        if i["type_of_work"] == "Обслуживание":
            NEEDED.append(i)
    for i in range(0, len(NEEDED)):
        if i == 0:
            LASTID.append(query.message.message_id)
        if i == len(NEEDED) - 1:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED[i]["name_of_vacancy"],
                NEEDED[i]["about_vacancy"],
                NEEDED[i]["payment"], NEEDED[i]["deadline"]), reply_markup=reply_markup2)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED[i]["name_of_vacancy"],
                NEEDED[i]["about_vacancy"],
                NEEDED[i]["payment"], NEEDED[i]["deadline"]), reply_markup=reply_markup)
    return CREATION_BEFORE_NAME


def f_content(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.bot.delete_message(query.message.chat.id, query.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Выбрать", callback_data=str(ACCEPT))
        ],
        [
            InlineKeyboardButton("Выбрать другой тип", callback_data=str(FIND_JOB))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    vacancies = jobdata.ContColl.find()
    LASTID.clear()
    NEEDED.clear()
    for i in vacancies:
        if i["type_of_work"] == "Создание контента":
            NEEDED.append(i)
    for i in range(0, len(NEEDED)):
        if i == 0:
            LASTID.append(query.message.message_id)
        if i == len(NEEDED) - 1:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED[i]["name_of_vacancy"],
                NEEDED[i]["about_vacancy"],
                NEEDED[i]["payment"], NEEDED[i]["deadline"]), reply_markup=reply_markup2)
        else:
            query.message.reply_text(text="Название: {} \nОписание: {} \nОплата: {} \nСрок: {}".format(
                NEEDED[i]["name_of_vacancy"],
                NEEDED[i]["about_vacancy"],
                NEEDED[i]["payment"], NEEDED[i]["deadline"]), reply_markup=reply_markup)
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
                CommandHandler('start', start), MessageHandler(Filters.text, name),
                CallbackQueryHandler(accept, pattern='^' + str(ACCEPT) + '$'),
            ],

            PAY: [CallbackQueryHandler(pay_card_or_cash, pattern='^' + str(PAY_CARD_OR_CASH) + '$'),
                  CallbackQueryHandler(without_money, pattern='^' + str(WITHOUT_MONEY) + '$'),
                  CommandHandler('start', start), MessageHandler(Filters.text, name),
                  ],

            INFO_ABOUT_VACANCY: [CommandHandler('start', start), MessageHandler(Filters.text, info_about_vacancy),
                                 MessageHandler(Filters.text, name)],
            DEADLINE: [CommandHandler('start', start), MessageHandler(Filters.text, deadline)],
            CREATE: [CallbackQueryHandler(create, pattern='^' + str(CREATE) + '$'),
                     CommandHandler('start', start), MessageHandler(Filters.text, name)],
            COST: [CommandHandler('start', start), MessageHandler(Filters.text, cost)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()