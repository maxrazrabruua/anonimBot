import telebot
from t import t
import json
import random
from IBT_ai import IBT2
import time
import My_Algoritms as ma # локальная библиотека
import os

safe = ma.Safe({
    "pi": 3.1415,
    "i": 1.0,
    "e": 2.71828,
    "d": 180 / 3.1415,
    "r": 3.1415 / 100,
    "NaN": -1.0,
    "infinity": 1_000_000_000*1_000_000_000*1_000_000_000,
    "N": -1,
    "inf": 1_000_000_000
})

HOST_ID = "ТВОЙ_ИНДИФИКАТОР"
FILE = "main.json"
VERSION = "2.5.11(11 января)" # НЕ МЕНЯЙ
CANAL_ID = "-1002368289037" # НЕ МЕНЯЙ
CHAT_ID = "-1002168363601"# НЕ МЕНЯЙ
time.sleep(1.5)

bot = telebot.TeleBot(t())
def load(file):
    try:
        with open("base/" + file, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f'Ошибка при загрузке файла {file}.')
        return {}

def save(file, data):
    with open("base/" + file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def proverka(user):
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    """
    return (bot.get_chat_member(CANAL_ID, user).status in ['member', 'administrator', 'creator']) and (bot.get_chat_member(CHAT_ID, user).status in ['member', 'administrator', 'creator'])

@bot.message_handler(commands=["start"])
def startf(message):
    bot.reply_to(message, "Привет, это бот анонимного чата чтоб узнать все команды напиши это:\n/help\nА также напишите /politic и прочитайте его")
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    if proverka(str(message.from_user.id)):
        if str(message.from_user.id) not in j["users"].keys():
            j["stata"][str(message.from_user.id)] = {"отправлено": 0, "получено": 0, "диалогов": 0, "закончено": 0, "ии": 0, "слова": {}} # В словах будет типо 'слово': int
            j["modeAnon"][str(message.from_user.id)] = True
            j["users"][str(message.from_user.id)] = "свободный"
            bot.reply_to(message, "Вы в базе данных, поздравляю!")
        else:
            bot.reply_to(message, "Вы зарегистрировались")
        j["info"][str(message.from_user.id)] = message.from_user.username
    else:
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
    save(FILE, j)

@bot.message_handler(commands=["help"])
def helpf(message):
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    bot.reply_to(message, "Все команды:\n/help - для помощи\n/start - старт бота\n/chat - открытие чата для вас(поиск людей которые тоже ищут)\n/cancel - закрытие поиска\n/stop - закрытие текущего чата(если он открыт)\n/status - пишет ваш статус\n/stata - статистика\n/my_mode - пишет ваш режим анонимности\n/mode - переключает режим")
    bot.reply_to(message, "Административные команды:\n/addadmin <speaker/helper/operator/promoter> <id> - внимание, если туда ввести ид владельца то будет ошибка, а если в первый аргумент host написать будет ошибка, а если promoter - и вы не хост - будет ошибка, а выполнять команды эти могут только промоутеры и хост иначе никак\n/upadmin <id> - повышение админа если он ниже operator если вы прмоутер иначе ниже promoter, выполняют лишь промоутеры и хост\n/downadmin <id> - противположна к /upadmin, она делает админку ниже(если вы промоутер то можно понизить людей у который должность operator а если вы хост то тогда промоутеров)\n/deladmin <id> - удаляет человека с админки если вы промоутер то можете понизить начиная с operator-ов, а если вы хост то промоутеров\n/addhost - использует только хост бота\n/admins - список админов\n/speak <текст> - рассылка\n/madmin <текст> - обращение к ВСЕМ админам\n/tadmin <текст> - ответ пользователю\n/ban <id> - Бан пользователя по айди\n/unban <id> - разбан\n/banlist - список с забаныными пользователями(с ид и с юзернеймом(по возможности))")
    bot.reply_to(message, "Особые:\n/version - показывает версию нашего бота\n/dialogs - посмотреть все свои(если ты не админ) и чужие(если ты админ)\n/dialog <id диалога> - просмотреть свои и чужие диалоги(если ты админ)\n/deldialog <id> - для админов начиная с операторов\n/del - стереть себя из базы данных\n/politic - Политика нашей кондифициальности.\n/username <id> - получить юзернейм по индификатору телеграмм(доступно только админам)\n/server - информация про нашу базу данных\n/matimatic <выражение> - расчёты")

@bot.message_handler(commands=["matimatic"])
def matimaticf(message):
    """
    Создан в 02.01.2025
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if str(message.from_user.id) in j["users"].keys():
        try:
            r = safe.mati(message.text[10:])
        except ValueError:
            bot.reply_to(message, "Нельзя писать запрещённые символы или этой переменной не существует")
        except SyntaxError:
            bot.reply_to(message, "Ошибка в выражении")
        except ZeroDivisionError:
            bot.reply_to(message, f"Итог выражения: {safe.mati('inf')}")
        else:
            bot.reply_to(message, f"Итог выражения: {r}")
    else:
        bot.reply_to(message, "зарегистрируйтесь пожалуйста")

@bot.message_handler(commands=["server"])
def serverf(message):
    """
    Создан в 01.01.2025
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    if str(message.from_user.id) in j["users"].keys():
        suser = str(message.from_user.id)
        admins = []
        for rang in j['admins'].keys():
            for admin in j['admins'][rang]:
                admins.append(admin)
        bot.reply_to(message, f"Пользователей: {len(j['users'].keys())}\n"
                      f"Юзернеймов доступно: {len([u for u in j['info'].values() if u is not None])}\n"
                      f"Владельцев стастистики: {len(j['stata'].keys())}\n"
                      f"Анонимность(анонимны/не анонимны): {sum(1 for u in j['modeAnon'].values() if u)} / {sum(1 for u in j['modeAnon'].values() if not u)}\n"
                      f"Админов: {len(admins)}\n"
                      f"Забаненых: {len(j['banned'])}\n"
                      f"Вы забанены: {'да' if suser in j['banned'] else 'нет'}\n"
                      f"Диалогов: {len(j['dialogs'])}\n"
                      f"Слов: {len(j['words'])}\n"
                      f"Имеют ссылки к чатам: {len(j['tChat'].keys())}\n"
                      f"Ждут удаления: {len(j['tDel'])}\n")
        active, search, free = 0, 0, 0
        for status in j['users'].values():
            if isinstance(status, list) and status[1] == "активный":
                active += 1
            elif status == "ищет":
                search += 1
            else:
                free += 1
        t = time.time()
        obu = message.date
        obs = t
        for file in [FILE, "frases_1.json"]:
            i = load(file)
        it = time.time()
        bot.reply_to(message, f"Статусы пользователей:\n\nАктивные: {active}\nИщущие: {search}\nСвободные: {free}\nВаш пинг: {int((t - message.date) * 100)}\nОтклик баз данных(загрузок) формат (от пользователя/от сервера): ({int((it - obu) * 1000)}/{int((it - obs) * 1000)})\nПоследний раз было сообщений от пользователя до сервера: {int((time.time() - j['timeOfUserPing']) * 1000)}мс")
        j['timeOfUserPing'] = message.date
        save(FILE, j)
    else:
        bot.reply_to(message, "зарегистрируйтесь пожалуйста")

@bot.message_handler(commands=["username"])
def usernamef(message):
    """
    Создан в 29.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if str(message.from_user.id) in j["users"].keys():
        user = message.from_user.id
        suser = str(user)
        admins = []
        for rang in list(j["admins"].keys()):
            for u in j["admins"][rang]:
                admins.append(u)
        
        if suser in admins:
            if len(message.text.split()) == 2:
                args = message.text.split()[1]
                if args in j["users"].keys():
                    bot.reply_to(message, f"Его юзернейм: {'@' + j['info'][args] if not j['info'][args] is None else 'Нет юзернейма'}")
                else:
                    bot.reply_to(message, "Его нет в базе данных")
            else:
                bot.reply_to(message, "Маленькая или слишком большая ширина команды")
        else:
            bot.reply_to(message, "Вы не админ")
    else:
        bot.reply_to(message, "зарегистрируйтесь пожалуйста")

@bot.message_handler(commands=["politic"])
def politicsf(message):
    """
    Создан в 27.12.2024
    """
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    text = ""
    document = [ # ИЗМЕНИШЬ - ДЕБИЛ МОЖНО ЛИШЬ ТО ЧТО В СКОБКАХ
        "--------------------------------------------------------------------------------------------------------",
        "Политика нашей конфиденциальности(страна: Украина и (ТВОЯ СТРАНА), Днепр и (ТВОЙ ГОРОД)).",
        "Если вы написали /start вы автоматически согласились, чтобы отменить соглашение напишите /del",
        "Местоимения:",
        "   Мы, наш, наших, проект, бот, сервис - это одно и тоже в рамках доккумента и означает наш сервис",
        "   Вы, ваш, ваших - это вы",
        "   Другие, других т.д. вариации - это другие пользователи",
        "ЭТО НЕ ОРИГИНАЛЬНЫЙ БОТ, ОРИГИНАЛ: @tgardanonimchatg2_bot"
        "--------------------------------------------------------------------------------------------------------",
        "А ТАКЖЕ МЫ ИМЕЕМ ПРАВО ВАМ ПРЕДЛАГАТЬ НА НАС ПОДПИСАТЬСЯ ПО ПОНЯТНЫМ ПРИЧИНАМ ТАКИЗ ТАК ОБЩЕНИЕ С НАШИМ КОМЬЮНИТИ ИЛИ НОВОСТИ!",
        "Не смейте нарушать это:",
        "   1. рекламировать, оскорблять и т.д. пользователей",
        "   2. оскорблять админов и хоста",
        "Что будет если нарушить: БАН",
        "Все жалобы и т.д. в писать в madmin",
        "За что мы не отвечаем:",
        "   1. За ИИ",
        "   2. За генератор названий",
        "   3. За сбои в работе бота, могут быть другие причины к примеру отключение света",
        "За что мы отвечаем:",
        "   1. За качеством сервиса",
        "   2. За справедливость администрации",
        "   3. За общение",
        "   4. За вас и другими",
        "Что вы должны делать в этом проекте:",
        "   1. Не нарушать правила",
        "   2. Общаться и использовать наш сервис",
        "   3. ЖЕЛАТЕЛЬНО соблюдать законы Украины потому что наш сервис НЕ для криминальности",
        "Что мы от других вас скрываем и наоборот:",
        "   1. Юзернейм/Индификатор телеграмм через настройки анонимности(/mode, /mymode)",
        "   2. Сообщения диалога и их/ваши истории",
        "Что мы от вас собираем:",
        "   1. Юзернейм",
        "   2. Индификатор телеграмм(для регистрации)",
        "   3. Ваши слова(для генерации названий диалогов в будущем(не удаляется))",
        "   4. Диалоги ваши с другими людьми(для администрации и для улучшения нашего сервиса)",
        "   5. Анонимность(True, False)",
        "   6. Текущий диалог",
        "   7. Статистику взаимнодействий(для вас)",
        "   8. Текущий статус в базе данных(для работы сервиса)",
        "Будем вежливы(лично ЛС ТГ): @Ardija1 в проекте ХОСТ",
        "(p.s. Администрация имеет право изменять политику конфиденциальности повидомив пользователей заранее или после изменения, p.s. не изменяется)",
        "(Д.Д.(Дополнительная доккументация): Данный доккумент не является под юридической силы, она используется лишь в проекте и в боте не выходя за рамками сервиса)"
    ]
    for string in document:
        text += string + "\n"
    bot.reply_to(message, text)

@bot.message_handler(commands=["dialogs"])
def dialogsf(message):
    """
    Создан в 26.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if str(message.from_user.id) in j["users"].keys():
        user = message.from_user.id
        suser = str(user)
        if not (suser in j["banned"]):
            admins = []
            text = ""
            for rang in list(j["admins"].keys()):
                for u in j["admins"][rang]:
                    admins.append(u)
            if suser in admins:
                massive = range(1, len(j["dialogs"]) + 1)
                for dialog, i in zip(j["dialogs"][::-1], massive[::-1]):
                    text += f"[{'🟢' if suser in dialog['ids'] else '🔴'}]|[{i}]: {dialog["name"]}\n"
                
                if len(text) == 0:
                    text = "Нету диалогов"
            else:
                massive = range(1, len(j["dialogs"]) + 1)
                for dialog, i in zip(j["dialogs"][::-1], massive[::-1]):
                    if suser in dialog['ids']:
                        text += f"[🟢]|[{i}]: {dialog["name"]}\n"
                if len(text) == 0:
                    text = "Нету диалогов"
            bot.reply_to(message, text)
        else:
            bot.reply_to(message, "вы забанены")
    else:
        bot.reply_to(message, "зарегистрируйтесь пожалуйста")

@bot.message_handler(commands=["dialog"])
def dialogf(message):
    """
    Создан в 26.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if str(message.from_user.id) in j["users"].keys():
        user = message.from_user.id
        suser = str(user)
        if not (suser in j["banned"]):
            admins = []
            for rang in list(j["admins"].keys()):
                for u in j["admins"][rang]:
                    admins.append(u)
            if len(message.text.split()) == 2:
                try:
                    args = int(message.text.lower().split()[1])
                    j["dialogs"][args - 1]
                except IndexError:
                    bot.reply_to(message, "диалог не найден")
                except ValueError:
                    bot.reply_to(message, "должно быть числом")
                else:
                    if suser in j["dialogs"][args - 1]["ids"]:
                        for m in j["dialogs"][args - 1]["messages"]:
                            ui = m['iduser']
                            if suser == j["dialogs"][args - 1]["ids"][0]:
                                sob = j["dialogs"][args - 1]["ids"][1]
                            else:
                                sob = j["dialogs"][args - 1]["ids"][0]
                            bot.send_message(user, f"{'вы:' if m['iduser'] == suser else f'он({ui if suser in admins else (j['info'][sob] or sob if j['modeAnon'] else 'Секретно')}):'} {m['text']}")
                    else:
                        if suser in admins:
                            for m in j["dialogs"][args]["messages"]:
                                bot.send_message(user, f"{f'первый собеседник({j['dialogs'][args - 1]['ids'][0]})' if m['iduser'] == j['dialogs'][args - 1]['ids'][0]  else f'второй собеседник({j['dialogs'][args - 1]['ids'][1]}):'} {m['text']}")
                        else:
                            bot.reply_to(message, "а ну не смотреть!")
            else:
                bot.reply_to(message, "Слишком маленькая или большая ширина команды")
        else:
            bot.reply_to(message, "вы забанены")
    else:
        bot.reply_to(message, "зарегистрируйтесь пожалуйста")

@bot.message_handler(commands=["deldialog"])
def deldialogf(message):
    """
    Создан в 26.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if str(message.from_user.id) in j["users"].keys():
        user = message.from_user.id
        suser = str(user)
        if not (suser in j["banned"]):
            admins = []
            for rang in list(j["admins"].keys())[2:]:
                for u in j["admins"][rang]:
                    admins.append(u)
            if len(message.text.split()) == 2:
                try:
                    args = int(message.text.lower().split()[1])
                    j["dialogs"][args - 1]
                except IndexError:
                    bot.reply_to(message, "диалог не найден")
                except ValueError:
                    bot.reply_to(message, "должно быть числом")
                else:
                    for user_of_d in j["dialogs"][args - 1]["ids"]:
                        bot.send_message(user_of_d, f"Ваш чат {j['dialogs'][args - 1]['name']} удалён, не забывайте этого человека: {j['dialogs'][args - 1]['ids'][1] if j['dialogs'][args - 1]['ids'][0] == user_of_d else j['dialogs'][args - 1]['ids'][0]}")
                    del j["dialogs"][args - 1]
                    save(FILE, j)
            else:
                bot.reply_to(message, "Слишком маленькая или большая ширина команды")
        else:
            bot.reply_to(message, "вы забанены")
    else:
        bot.reply_to(message, "зарегистрируйтесь пожалуйста")
        

@bot.message_handler(commands=["banlist"])
def banlistf(message):
    """
    Создан в 25.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if str(message.from_user.id) in j["users"].keys():
        user = message.from_user.id
        suser = str(user)
        admins = []
        for rang in list(j["admins"].keys()):
            for u in j["admins"][rang]:
                admins.append(u)
        if suser in admins:
            banlist = []
            for user in j["banned"]:
                banlist.append(f"({user} / {'@' + j['info'][user] if not (j['info'][user] is None) else 'Без юзернейма'})")
            bot.reply_to(message, f"Банлист: {", ".join(banlist) if len(banlist) > 0 else 'Нет пользователей'}")
        else:
            bot.reply_to(message, "Вы не админ")
    else:
        bot.reply_to(message, "Зарегистрируйтесь!")


@bot.message_handler(commands=["ban"])
def banf(message):
    """
    Создан в 25.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if str(message.from_user.id) in j["users"].keys():
        if len(message.text.split()) == 2:
            args = message.text.lower().split()[1]
            user = message.from_user.id
            suser = str(user)
            admins = []
            absolutesadmin = []
            for rang in list(j["admins"].keys())[2:]:
                for u in j["admins"][rang]:
                    admins.append(u)
            
            for rang in j["admins"].keys():
                for u in j["admins"][rang]:
                    absolutesadmin.append(u)
            
            if suser in admins:
                if args in absolutesadmin:
                    bot.reply_to(message, "Это админ, не смей банить!")
                else:
                    if args in j["banned"]:
                        bot.reply_to(message, "Данный пользователь уже был забанен")
                    else:
                        j["banned"].append(args)
                        bot.reply_to(message, "Пользователь успешно забанен")
                        save(FILE, j)
            else:
                bot.reply_to(message, "Вы не админ, вы должны быть на уровне оператора")
        else:
            bot.reply_to(message, "Слишком маленькая или большая ширина команды")
    else:
        bot.reply_to(message, "Зарегистрируйтесь!")

@bot.message_handler(commands=["unban"])
def unbanf(message):
    """
    Создан в 25.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if str(message.from_user.id) in j["users"].keys():
        if len(message.text.split()) == 2:
            args = message.text.lower().split()[1]
            user = message.from_user.id
            suser = str(user)
            admins = []
            for rang in list(j["admins"].keys())[2:]:
                for u in j["admins"][rang]:
                    admins.append(u)
            if suser in admins:
                if not (args in j["banned"]):
                    bot.reply_to(message, "Данный пользователь не в бане")
                else:
                    j["banned"].remove(args)
                    bot.reply_to(message, "Пользователь успешно разбанен")
                    save(FILE, j)
            else:
                bot.reply_to(message, "Вы не админ, вы должны быть на уровне оператора")
        else:
            bot.reply_to(message, "Слишком маленькая или большая ширина команды")
    else:
        bot.reply_to(message, "Зарегистрируйтесь!")


@bot.message_handler(commands=["version"])
def versionf(message):
    """
    Создан в 25.12.2024
    """
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if str(message.from_user.id) in j["users"].keys():
        bot.reply_to(message, f"Версия: {VERSION}")
    else:
        bot.reply_to(message, "Зарегистрируйтесь!")

@bot.message_handler(commands=["tadmin"])
def tadminf(message):
    """
    Создан в 24.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if len(message.text.split()) >= 3:
        args = message.text.lower().split()[1:]
        user = message.from_user.id
        suser = str(user)
        ur = int(args[0])
        text = args[1:]
        admins = []
        for rang in list(j["admins"].keys())[1:]:
            for u in j["admins"][rang]:
                admins.append(u)
        if (suser in admins) and (suser in j["users"].keys()):
            try:
                bot.send_message(ur, " ".join(text))
            except Exception:
                bot.reply_to(message, "Кому обращаетесь?")
        elif not (suser in j["users"].keys()):
            bot.reply_to(message, "Зарегистрируйтесь!")
        else:
            bot.reply_to(message, "Вы не админ")
    else:
        bot.reply_to(message, "Слишком маленькая ширина команды")


@bot.message_handler(commands=["madmin"])
def madminf(message):
    """
    Создан в 24.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if not (str(message.from_user.id) in j["banned"]):
        user = message.from_user.id
        suser = str(user)
        if suser in j["users"].keys():
            if len(message.text.split()) >= 2:
                args = message.text.lower().split()[1:]
                admins = []
                for rang in list(j["admins"].keys())[1:]:
                    for u in j["admins"][rang]:
                        admins.append(u)
                
                for admin in admins:
                    bot.send_message(int(admin), f"От поддержки: ид человека: {suser}: {" ".join(args)}")
            else:
                bot.reply_to(message, "Слишком маленькая ширина команды")
        else:
            bot.reply_to(message, "Вы не зарегистрированы в системе")
    else:
        bot.reply_to(message, "вы забанены")
        

@bot.message_handler(commands=["speak"])
def speakf(message):
    """
    Создан в 24.12.2024
    """
    g = '0'
    if not proverka(str(message.from_user.id)) and (not (str(message.from_user.id) == "777000") and (message.chat.username == "botovykh")):
        if not str(message.from_user.id) == "777000":
            bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
            print('a')
            return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    g = '1'
    if len(message.text.split()) >= 2:
        args = message.text.lower().split()[1:]
        user = message.from_user.id
        suser = str(user)
        admins = []
        for rang in list(j["admins"].keys())[1:]:
            for u in j["admins"][rang]:
                admins.append(u)
        g = '2'
        if ((suser in admins) and (suser in j["users"].keys())) or ((str(message.from_user.id) == "777000") and (message.chat.username == "botovykh")):
            g = '3'
            for u in j["users"].keys():
                g = '4'
                try:
                    g = '5'
                    if str(message.from_user.id) == "777000":
                        if message.chat.type == "supergroup":
                            i = 'anonimuskanaliz'
                            emoji = "🗣"
                    else:
                        i = j["info"][suser]
                        emoji = "⭐" if suser in j["admins"]["speaker"] else \
                            "⭐⭐" if suser in j["admins"]["helper"] else \
                            "🟢" if suser in j["admins"]["operator"] else \
                            "🔴" if suser in j["admins"]["promoter"] else \
                            "🟣"
                    bot.send_message(int(u), f'Рассылка от администратора {emoji} @{i}: {" ".join(args)}')
                except Exception as e:
                    pass
            if not str(message.from_user.id) == "777000":
                bot.send_message(user, "отправлено всем")
            else:
                bot.send_message(HOST_ID, "отправлено всем")
        elif not (suser in j["users"].keys()):
            if not str(message.from_user.id) == "777000":
                bot.reply_to(message, "Зарегистрируйтесь!")
        else:
            if not str(message.from_user.id) == "777000":
                bot.reply_to(message, "Вы не админ")
    else:
        if not str(message.from_user.id) == "777000":
            bot.reply_to(message, "Слишком маленькая ширина команды")
        
        

@bot.message_handler(commands=["admins"])
def adminsf(message):
    """
    Создан в 24.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    bot.reply_to(message, f'⭐{(("speaker(громкоговоритель)" if len(j["admins"]["speaker"]) == 1 else "speakers(громкоговорители)") + ":\n" + ", @".join(j["info"][user] or user + "\n" for user in j["admins"]["speaker"]) if j["admins"]["speaker"] else "Нет пользователей")}\n⭐⭐{(("helper(помощник)" if len(j["admins"]["helper"]) == 1 else "helpers(помощники)") + ":\n" + ", @".join([j["info"][user] or user + "\n" for user in j["admins"]["helper"]]) if j["admins"]["helper"] else "Нет пользователей")}\n🟢{(("operator(оператор)" if len(j["admins"]["operator"]) == 1 else "operators(операторы)") + ":\n" + ", @".join([j["info"][user] or user + "\n" for user in j["admins"]["operator"]]) if j["admins"]["operator"] else "Нет пользователей")}\n🔴{(("promoter(промоутер)" if len(j["admins"]["promoter"]) == 1 else "promoters(промоутеры)") + ":\n" + ", @".join([j["info"][user] or user + "\n" for user in j["admins"]["promoter"]]) if j["admins"]["promoter"] else "Нет пользователей")}\n🟣{(("host(хост)" if len(j["admins"]["host"]) == 1 else "hosts(хосты)") + ":\n" + ", @".join([j["info"][user] + "\n" for user in j["admins"]["host"]]) if j["admins"]["host"] else "Нет пользователей")}')


@bot.message_handler(commands=["addhost"])
def addhost(message):
    """
    создан в 24.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if str(message.from_user.id) == HOST_ID:
        if len(j["admins"]["host"]) < 1:
            j["admins"]["host"].append(HOST_ID)
            save(FILE, j)
        else:
            bot.reply_to(message, "Хост наш любимый, ты не можешь себя добавить на роль если ты есть")
    else:
        bot.reply_to(message, "Вы не хост!")

@bot.message_handler(commands=["addadmin"])
def addadminf(message):
    """
    создан в 23.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if len(message.text.split()) == 3:
        args = message.text.lower().split()[1:]
        user = message.from_user.id
        suser = str(user)
        admins = []
        if ((suser in j["admins"]["promoter"]) or (suser in j["admins"]["host"])) and (suser in j["users"].keys()):
            for rang in list(j["admins"].keys()):
                for u in j["admins"][rang]:
                    admins.append(u)
            
            if args[1] in j["users"].keys():
                if not (args[1] in admins):
                    try:
                        if suser in j["admins"]["host"]:
                            if args[0] != "host":
                                j["admins"][args[0]].append(args[1])
                                save(FILE, j)
                            else:
                                bot.reply_to(message, "Пользователь не может быть хостом")
                        else:
                            if not (args[1] in ["host", "promoter"]):
                                j["admins"][args[0]].append(args[1])
                                save(FILE, j)
                            elif args[1] == "promoter":
                                bot.reply_to(message, "Вы не хост чтобы баловать других")
                            else:
                                bot.reply_to(message, "Пользователь не может быть хостом")
                    except KeyError:
                        bot.reply_to(message, "Напоминаю, единочисленный...")
                else:
                    bot.reply_to(message, "Пользователь уже админ")
            else:
                bot.reply_to(message, f"Пользователь с индификатором {suser} не зарегистрирован")
        elif not (suser in j["users"].keys()):
            bot.reply_to(message, "Зарегистрируйтесь!")
        else:
            bot.reply_to(message, "Вы не админ такого уровня как promoter или выше")
    else:
        bot.reply_to(message, "Слишком маленькая или большая ширина команды")

@bot.message_handler(commands=["deladmin"])
def deladminf(message):
    """
    создан в 23.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if len(message.text.split()) == 2:  # Чтобы ввести только одну цель для удаления
        args = message.text.lower().split()[1:]
        user = message.from_user.id
        suser = str(user)
        admins = []
        
        # Проверяем, является ли вызывающий команду промоутером или хостом
        if ((suser in j["admins"]["promoter"]) or (suser in j["admins"]["host"])) and (suser in j["users"].keys()):
            
            # Составляем список всех администраторов
            for rang in list(j["admins"].keys()):
                for u in j["admins"][rang]:
                    admins.append(u)
            
            # Проверяем, существует ли указанный пользователь и есть ли он в списке админов
            if args[0] in j["users"].keys():
                
                # Проверяем, является ли пользователь администратором
                if args[0] in admins:
                    rangUser = False
                    
                    # Ищем роль пользователя в списке админов
                    for rang in j["admins"].keys():
                        if args[0] in j["admins"][rang]:
                            rangUser = rang
                            break
                    
                    # Если роль найдена
                    if rangUser:
                        
                        # Если вызывающий промоутер, он может удалять тех, кто ниже его уровня
                        if suser in j["admins"]["promoter"]:
                            if rangUser not in ["promoter", "host"]:  # Промоутер не может удалить других промоутеров
                                j["admins"][rangUser].remove(args)  # Удаляем пользователя из его роли
                                bot.reply_to(message, f"Пользователь {args} удален из администраторов.")
                                save(FILE, j)
                            else:
                                bot.reply_to(message, "Вы не можете удалить промоутера или хоста.")
                        
                        # Если вызывающий хост, он может удалить кого угодно ниже его уровня (кроме хоста)
                        elif suser in j["admins"]["host"]:
                            if rangUser != "host":  # Хост не может удалить себя
                                for rang in j["admins"].keys():
                                    if args[0] in j["admins"][rang]:
                                        j["admins"][rang].remove(args)
                                        bot.reply_to(message, f"Пользователь {args} удален из администраторов.")
                                        save(FILE, j)
                                        break
                            else:
                                bot.reply_to(message, "Вы не можете удалить хоста.")
                    
                    else:
                        bot.reply_to(message, "Этот пользователь не является администратором.")
                else:
                    bot.reply_to(message, f"Пользователь {args} не найден среди администраторов.")
            else:
                bot.reply_to(message, f"Пользователь с ID {args} не зарегистрирован.")
        
        elif suser not in j["users"].keys():
            bot.reply_to(message, "Вы не зарегистрированы! Пожалуйста, зарегистрируйтесь.")
        else:
            bot.reply_to(message, "Вы не имеете прав на выполнение этой команды.")
    
    else:
        bot.reply_to(message, "Слишком мало или много аргументов в команде.")

@bot.message_handler(commands=["upadmin"])
def upadminf(message):
    """
    создан в 23.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if len(message.text.split()) == 2:
        args = message.text.lower().split()[1:]
        listadmin = []
        listrangs = list(j["admins"].keys())[:-2]
        for rang in j["admins"].keys():
            for u in j["admins"][rang]:
                listadmin.append([rang, u])
        
        user = message.from_user.id
        suser = str(user)

        if ((suser in j["admins"]["promoter"]) or (suser in j["admins"]["host"])) and (suser in j["users"].keys()):
            userAdmin = False
            for package in listadmin:
                _, u = package
                if args == u:
                    userAdmin = True
                    break
            
            if not userAdmin:
                if args in j["users"].keys():
                    j["admins"]["speacker"].append(args)
                    save(FILE, j)
                else:
                    bot.reply_to(message, "Ваш человек для повышения не зарегистрирован")
            else:
                rangUser = False
                for package in listadmin:
                    rang, u = package
                    if args == u:
                        rangUser = rang
                        break
                if rangUser:
                    if not (rangUser in ["operator", "promoter", "host"]):
                        j["admins"][listrangs[listrangs.index(rangUser)]].remove(args)
                        j["admins"][listrangs[listrangs.index(rangUser) + 1]].append(args)
                        save(FILE, j)
                        bot.reply_to(message, "Пользователь поднят!")
                    else:
                        bot.reply_to(message, "Вы не можете при помощи этой команды поднять оператора выше, это может только команда /addadmin если вы host, а вот промоутера нельзя потому что для этого нужна команда /addhost по такой же причине, а в любом случае нельзя поднять host ещё выше потому что это же host самый главный")
                else:
                    bot.reply_to(message, "Чё за ерунда случилась?!")
        elif not (args in j["users"].keys()):
            bot.reply_to(message, "Зарегистрируйтесь!")
        else:
            bot.reply_to(message, "Вы не админ такого уровня как promoter или выше")
    else:
        bot.reply_to(message, "Слишком маленькая или большая ширина команды")

def notIf(message, settings=True, result=True, say=True, notTrue='Не подошло по условию'):
    """
    Эта функция используется в улучшенной сложности условия if-else
    :param message: Сообщение от пользователя
    :param settings: Условие от которого завиит результат функции
    :param result: Результат функции если условие settings выполниться
    :param notTrue: Текст который надо отправить если не выполнено

    :return: Результат функции благодаря условии settings
    """
    if settings:
        return result
    else:
        if say:
            bot.reply_to(message, notTrue)
        return False

@bot.message_handler(commands=["autoUnPin"])
def autoUnPinf(message):
    """
    создан в 10.01.2025
    """
    if notIf(message, (message.chat.type == "supergroup") and (str(message.from_user.id) == HOST_ID) and (message.chat.username == "botovykh"), notTrue="Эту команду можно использовать только в группе нашей"):
        if notIf(message, not proverka(str(message.from_user.id)), "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh", False):
            return
        j = load(FILE)
        j["timeOfUserPing"] = message.date
        save(FILE, j)
        suser = str(message.from_user.id)

        if notIf(message, suser == HOST_ID, notTrue="Вы не администратор"):
            j["autoUnPinning"] = not j["autoUnPinning"]
            save(FILE, j)
            bot.reply_to(message, f'Автооткрпеление: {("Включено") if j["autoUnPinning"] else ("Выключено")}')

@bot.message_handler(commands=["downadmin"])
def downadminf(message):
    """
    создан в 23.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if len(message.text.split()) == 2:
        args = message.text.lower().split()[1:]
        listadmin = []
        listrangs = list(j["admins"].keys())[:-2]
        for rang in j["admins"].keys():
            for u in j["admins"][rang]:
                listadmin.append([rang, u])
        
        user = message.from_user.id
        suser = str(user)

        if ((suser in j["admins"]["promoter"]) or (suser in j["admins"]["host"])) and (suser in j["users"].keys()):
            userAdmin = False
            for package in listadmin:
                _, u = package
                if args == u:
                    userAdmin = True
                    break
            
            if not userAdmin:
                if args in j["users"].keys():
                    bot.reply_to(message, "Ваш человек не админ")
                else:
                    bot.reply_to(message, "Ваш человек для понижения не зарегистрирован")
            else:
                rangUser = False
                for package in listadmin:
                    rang, u = package
                    if args == u:
                        rangUser = rang
                        break
                if rangUser:
                    if not (rangUser in ["promoter", "host"]):
                        if (listrangs.index(rangUser) - 1) > 0:
                            j["admins"][listrangs[listrangs.index(rangUser)]].remove(args)
                            j["admins"][listrangs[listrangs.index(rangUser) - 1]].append(args)
                            bot.reply_to(message, "Пользователь понижен!")
                        else:
                            j["admins"][listrangs[listrangs.index(rangUser)]].remove(args)
                            bot.reply_to(message, "Пользователь удалён!")
                        save(FILE, j)
                    else:
                        bot.reply_to(message, "Нельзя понизить промоутера или хоста по понятным причинам")
                else:
                    bot.reply_to(message, "Чё за ерунда случилась?!")
        elif not (args in j["users"].keys()):
            bot.reply_to(message, "Зарегистрируйтесь!")
        else:
            bot.reply_to(message, "Вы не админ такого уровня как promoter или выше")
    else:
        bot.reply_to(message, "Слишком маленькая или большая ширина команды")

@bot.message_handler(commands=["chat"])
def chatf(message):
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if not (str(message.from_user.id) in j["banned"]):
        if str(message.from_user.id) in j["users"].keys():
            j["users"][str(message.from_user.id)] = "ищет"
            save(FILE, j)
            bot.reply_to(message, "Ищу собеседника...")
            if not isinstance(j["users"][str(message.from_user.id)], list):
                users = []
                for user in j["users"].keys():
                    if j["users"][user] == "ищет":
                        if user != str(message.from_user.id):
                            users.append(user)
                
                if not str(message.from_user.id) in j['stata'].keys():
                    j["stata"][str(message.from_user.id)] = {"отправлено": 0, "получено": 0, "диалогов": 0, "закончено": 0, "ии": 0, "слова": {}} # В словах будет типо 'слово': int
                
                if len(users) == 0:
                    bot.reply_to(message, "Собеседник не нашлся :(\nЯ жду другого")
                else:
                    user = random.choice(users)
                    j["users"][str(message.from_user.id)] = [user, "активный"]
                    j["users"][user] = [str(message.from_user.id), "активный"]
                    if not user in j['stata'].keys():
                        j["stata"][user] = {"отправлено": 0, "получено": 0, "диалогов": 0, "закончено": 0, "ии": 0, "слова": {}} # В словах будет типо 'слово': int
                    try:
                        bot.send_message(int(user), "Собеседник нашёлся")
                        bot.send_message(message.from_user.id, "Собеседник нашёлся")
                        j["stata"][str(message.from_user.id)]['диалогов'] += 1
                        j["stata"][user]['диалогов'] += 1
                        generWord = ""
                        for _ in range(random.randint(int(j["words"] / 10), int(j["words"] / 5))):
                            generWord += random.choice(j["words"])
                        j["dialogs"].append({"name": generWord, "ids": [str(message.from_user.id), user], "messages": []})
                        j["tChat"][str(message.from_user.id)] = len(j["dialogs"]) - 1
                        j["tChat"][user] = len(j["dialogs"]) - 1
                        save(FILE, j)
                    except Exception as e:
                        bot.reply_to(message, f"Произошла ошибка: {e}")
                        if witherror(e) != "Неизвестная ошибка.":
                            bot.reply_to(message, witherror(e))
                            bot.reply_to(message, "А ой, походу что-то не так... Удаляю пользователя.")
                            del j["users"][j["users"][str(message.from_user.id)][0]]
                            j["users"][str(message.from_user.id)] = "свободный"
                            save(FILE, j)
            else:
                bot.reply_to(message, "Прекратите общаться для начала")
        else:
            bot.reply_to(message, "Зарегистрируйся!")
    else:
        bot.reply_to(message, "вы забанены")

@bot.message_handler(commands=["cancel"])
def cancel(message):
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if not (str(message.from_user.id) in j["banned"]):
        if str(message.from_user.id) in j["users"].keys():
            if j["users"][str(message.from_user.id)] == "ищет":
                bot.reply_to(message, "Прекращаю поиск...")
                j["users"][str(message.from_user.id)] = "свободный"
                save(FILE, j)
            elif j["users"][str(message.from_user.id)] == "свободный":
                bot.reply_to(message, "Вы сейчас свободны")
            else:
                bot.reply_to(message, "Прекратите общаться для начала")
        else:
            bot.reply_to(message, "Зарегистрируйся!")
    else:
        bot.reply_to(message, "вы забанены")

@bot.message_handler(commands=["stop"])
def stop(message):
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if not (str(message.from_user.id) in j["banned"]):
        if str(message.from_user.id) in j["users"].keys():
            if j["users"][str(message.from_user.id)][1] == "активный":
                bot.reply_to(message, "Прекращаю общение...")
                if not str(message.from_user.id) in j['stata'].keys():
                    j["stata"][str(message.from_user.id)] = {"отправлено": 0, "получено": 0, "диалогов": 0, "закончено": 0, "ии": 0, "слова": {}} # В словах будет типо 'слово': int
                try:
                    bot.send_message(int(j["users"][str(message.from_user.id)][0]), "Собеседник решил перестать продолжать диалог")
                    if str(message.from_user.id) in j["modeAnon"].keys():
                        if not str(message.from_user.id) in j["info"].keys():
                            j["info"][str(message.from_user.id)] = message.from_user.username
                    else:
                        j["modeAnon"][str(message.from_user.id)] = True
                    
                    if not j["users"][str(message.from_user.id)][0] in j["modeAnon"].keys():
                        j["modeAnon"][j["users"][str(message.from_user.id)][0]] = True
                    
                    del j["tChat"][str(message.from_user.id)]
                    del j["tChat"][j['users'][str(message.from_user.id)][0]]
                    
                    save(FILE, j)

                    bot.send_message(int(j["users"][str(message.from_user.id)][0]), f"Собеседника зовут: {(message.from_user.username or message.from_user.id) if not j['modeAnon'][str(message.from_user.id)] or False else 'Секрет'}")

                    bot.send_message(message.from_user.id, f"Собеседника зовут: {(j['info'][j['users'][str(message.from_user.id)][0]] or j['users'][str(message.from_user.id)][0]) if not j['modeAnon'][j['users'][str(message.from_user.id)][0]] or False else 'Секрет'}")

                    j["stata"][str(message.from_user.id)]['закончено'] += 1
                except Exception as e:
                    bot.reply_to(message, f"Произошла ошибка: {e}")
                    if witherror(e) != "Неизвестная ошибка.":
                        bot.reply_to(message, witherror(e))
                        bot.reply_to(message, "А ой, походу что-то не так... Удаляю пользователя.")
                        del j["users"][j["users"][str(message.from_user.id)][0]]
                        j["users"][str(message.from_user.id)] = "свободный"
                        save(FILE, j)
                        return
                        
                j["users"][j["users"][str(message.from_user.id)][0]] = "свободный"
                j["users"][str(message.from_user.id)] = "свободный"
                save(FILE, j)
            elif j["users"][str(message.from_user.id)] == "свободный":
                bot.reply_to(message, "Вы сейчас свободны")
            else:
                bot.reply_to(message, "Вы ещё ищите людей")
        else:
            bot.reply_to(message, "Зарегистрируйся!")
    else:
        bot.reply_to(message, "вы забанены")

@bot.message_handler(commands=["status"])
def statusf(message):
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if not (str(message.from_user.id) in j["banned"]):
        bot.reply_to(message, f"Ваш статус: {j['users'][str(message.from_user.id)] if not isinstance(j['users'][str(message.from_user.id)], list) else j['users'][str(message.from_user.id)][1]}")
    else:
        bot.reply_to(message, "вы забанены")

def witherror(e):
    if "blocked" in str(e):
        return "Бот заблокирован пользователем."
    elif "user not found" in str(e):
        return "Пользователь отсутствует."
    else:
        return "Неизвестная ошибка."

@bot.message_handler(commands=["nas"])
def nasf(message):
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if str(message.from_user.id) in j["users"].keys():
        if len(message.text.lower().split()) == 4:
            args = message.text.lower().split()[1:]
            if args[2] == "PASSWORD":
                dect = j["statistik"]
                if args[0] in dect.keys():
                    try:
                        result = dect[args[0]][0] + int((dect[args[0]][1] * int(args[1])))
                        bot.reply_to(message, f"Населние страны {args[0]} через {args[1]} месяцев будет равно {result}")
                    except Exception:
                        bot.reply_to(message, "Ошибка в расчётах")
                else:
                    bot.reply_to(message, "Нет такой страны")
            else:
                bot.reply_to(message, "Неверный пароль")
        else:
            bot.reply_to(message, "Что такое длина текста?")
    else:
        bot.reply_to(message, "Зарегистрируйся!")

@bot.message_handler(commands=["nasa"])
def nasaf(message):
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if str(message.from_user.id) in j["users"].keys():
        if len(message.text.lower().split()) == 5:
            args = message.text.lower().split()[1:]
            contry, nass, prirost, password = args[0], (int(args[1]) if int(args[1]) >= 0 else int(int(args[1]) * -1)), int(args[2]), args[3]
            if args[3] == "PASSWORD":
                j["statistik"][contry] = [nass, prirost]
                save(FILE, j)
                bot.reply_to(message, "Страна добавлена или изменилась")
            else:
                bot.reply_to(message, "Неверный пароль")
        else:
            bot.reply_to(message, "Что такое длина текста?")
    else:
        bot.reply_to(message, "Зарегистрируйся!")

@bot.message_handler(commands=["nasd"])
def nadf(message):
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if str(message.from_user.id) in j["users"].keys():
        if len(message.text.lower().split()) == 3:
            args = message.text.lower().split()[1:]
            contry, password = args[0], args[1]
            if args[1] == "PASSWORD":
                if contry in j["statistik"].keys():
                    del j["statistik"][contry]
                    save(FILE, j)
                    bot.reply_to(message, "Страна удалена")
                else:
                    bot.reply_to(message, "Нет такой страны")
            else:
                bot.reply_to(message, "Неверный пароль")
        else:
            bot.reply_to(message, "Что такое длина текста?")
    else:
        bot.reply_to(message, "Зарегистрируйся!")

@bot.message_handler(commands=["stata"])
def stataf(message):
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if not (str(message.from_user.id) in j["banned"]):
        if str(message.from_user.id) in j["users"].keys():
            if str(message.from_user.id) in j['stata'].keys():
                try:
                    user = str(message.from_user.id)
                    if len(j["stata"][user]["слова"].keys()) > 0:
                        word = ma.maxKey(j["stata"][user]["слова"]) # функция из моей локальной библиотеки по названием мои алгоритмы
                    else:
                        word = "Ещё нет слов для анализа"
                    bot.reply_to(message, f"Ваша информация в базе данных:\n\n👤Вы - {str(j['info'].get(user, 'ноунейм'))}\n🪪Ваш ID TELEGRAM: {user}\n\nСтатистика:\n\n📥Было получено сообщений: {str(j['stata'].get(user, {}).get('получено', 0))}\n📤Было сообщений отправлено: {str(j['stata'].get(user, {}).get('отправлено', 0))}\n✉️Было диалогов: {str(j['stata'].get(user, {}).get('диалогов', 0))}\n🗄Вы закончили диалогов: {str(j['stata'].get(user, {}).get('закончено', 0))}\n🤖Было отправлено ИИ сообщений: {str(j['stata'].get(user, {}).get('ии', 0))}\n👅Сам(ы/о)е часто используем(ы/о)е слов(а/о): {word}\n✍️Вы написали слов: {len(j['stata'][user]['слова'].keys())}")
                except KeyError as e:
                    print(j['stata'][str(user)], j['stata'][str(user)]['ии'])
            else:
                j["stata"][str(message.from_user.id)] = {"отправлено": 0, "получено": 0, "диалогов": 0, "закончено": 0, "ии": 0, "слова": {}}
                save(FILE, j)
                bot.reply_to(message, "База обновлена, повторите попытку")
        else:
            bot.reply_to(message, "Зарегистрируйся!")
    else:
        bot.reply_to(message, "вы забанены")

@bot.message_handler(commands=["mode"])
def modef(message):
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if not (str(message.from_user.id) in j["banned"]):
        if str(message.from_user.id) in j["users"].keys():
            if str(message.from_user.id) in j['modeAnon'].keys():
                j["modeAnon"][str(message.from_user.id)] = not j["modeAnon"][str(message.from_user.id)]
                save(FILE, j)
                bot.reply_to(message, "Анонимность "  + ('включена' if j['modeAnon'][str(message.from_user.id)] else 'выключена'))
            else:
                j["modeAnon"][str(message.from_user.id)] = True
                save(FILE, j)
                bot.reply_to(message, "База обновлена, повторите попытку")
        else:
            bot.reply_to(message, "Зарегистрируйся!")
    else:
        bot.reply_to(message, "вы забанены")

@bot.message_handler(commands=["my_mode"])
def mymodef(message):
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if not (str(message.from_user.id) in j["banned"]):
        if str(message.from_user.id) in j["users"].keys():
            if str(message.from_user.id) in j['modeAnon'].keys():
                bot.reply_to(message, "Анонимность в данный момент " + ("включена" if j["modeAnon"][str(message.from_user.id)] else "выключена"))
            else:
                j["modeAnon"][str(message.from_user.id)] = True
                save(FILE, j)
                bot.reply_to(message, "База обновлена, повторите попытку")
        else:
            bot.reply_to(message, "Зарегистрируйся!")
    else:
        bot.reply_to(message, "вы забанены")

@bot.message_handler(commands=["del"])
def delsf(message):
    """
    Создан в 27.12.2024
    """
    if not proverka(str(message.from_user.id)):
        bot.reply_to(message, "Подпишись на эти каналы или чаты: t.me/anonimuskanaliz t.me/botovykh")
        return
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    if str(message.from_user.id) in j["users"].keys():
        user = message.from_user.id
        suser = str(user)
        if not (suser in j["banned"]):
            if suser in j["tDel"]:
                bot.reply_to(message, "Скажи 'да' в качестве подтверждения для удаления вашей учётной записи из базы данных")
            else:
                j["tDel"].append(suser)
                save(FILE, j)
                bot.reply_to(message, "чтобы удалить свою учётную запись скажите 'да' в любом регистре иначе удаление отмениться")
        else:
            bot.reply_to(message, "Хотели обхитрить правила проекта? Не получится! Вы ЗАБАНЕНЫ!")
    else:
        bot.reply_to(message, "зарегистрируйтесь пожалуйста")

def deleteBase(user):
    f = "Ошибка"
    try:
        j = load(FILE)
        suser = str(user)
        f = "Ошибка юзерс"
        del j["users"][suser]
        f = "инфо"
        del j["info"][suser]
        f = "стата"
        try:
            del j["stata"][suser]
            
        except Exception:
            pass
        f = "модеАнон"
        del j["modeAnon"][suser]
        yourDialogs = []
        i = 0
        f = "Диалоги 0"
        for d in j["dialogs"]:
            if suser in d["ids"]:
                yourDialogs.append(i)
            i += 1
        f = "Диалоги 1"
        for d in yourDialogs:
            del j["dialogs"][d]
        
        admins = []
        f = "админс 0"
        for rang in j["admins"].keys():
            for u in j["admins"][rang]:
                admins.append([rang, u])
        f = "Админс 1"
        for a in admins:
            rang, u = a
            if u == suser:
                j["admins"][rang].remove(u)
        f = "конец"
        del j["tDel"][j["tDel"].index(suser)]
        save(FILE, j)
        bot.send_message(user, "Поздравляю вы удалены")
    except Exception as e:
        print(e, f)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    j = load(FILE)
    j["timeOfUserPing"] = message.date
    save(FILE, j)
    print(not (str(message.from_user.id) == "777000") and (message.chat.username == "botovykh"), str(message.from_user.id) == "777000", str(message.from_user.id), message.chat.username == "botovykh", message.chat.username)
    if (str(message.from_user.id) == "777000") and (message.chat.username == "botovykh"):
        if j["autoUnPinning"]:
            bot.unpin_chat_message(chat_id=message.chat.id, message_id=message.id)
        message.text = f"/speak {message.text}"
        speakf(message)
    else:
        if proverka(str(message.from_user.id)):
                if str(message.from_user.id) in j["users"].keys():
                    if not str(message.from_user.id) in j['stata'].keys():
                        j["stata"][str(message.from_user.id)] = {"отправлено": 0, "получено": 0, "диалогов": 0, "закончено": 0, "ии": 0, "слова": {}} # В словах будет типо 'слово': int

                    if not (str(message.from_user.id) in j["tDel"]):
                        if isinstance(j["users"][str(message.from_user.id)], list) and j["users"][str(message.from_user.id)][1] == "активный":
                            try:
                                if not (str(message.from_user.id) in j["banned"]):
                                    bot.send_message(int(j["users"][str(message.from_user.id)][0]), message.text)
                                    j['stata'][j["users"][str(message.from_user.id)][0]]['получено'] += 1
                                    j['stata'][str(message.from_user.id)]['отправлено'] += 1
                                    j["dialogs"][j["tChat"][str(message.from_user.id)]]["messages"].append({"iduser": str(message.from_user.id), "text": message.text})
                                    j["words"] += ma.ds(message.text).split()
                                    for word in ma.ds(message.text).lower().split():
                                        if word in j["stata"][str(message.from_user.id)]["слова"].keys():
                                            j["stata"][str(message.from_user.id)]["слова"][word] += 1
                                        else:
                                            j["stata"][str(message.from_user.id)]["слова"][word] = 1
                                    save(FILE, j)
                                else:
                                    bot.reply_to(message, "вы забанены")
                                    stop(message)
                            except Exception as e:
                                bot.reply_to(message, f"Произошла ошибка: {e}")
                                if witherror(e) != "Неизвестная ошибка.":
                                    bot.reply_to(message, witherror(e))
                                    bot.reply_to(message, "А ой, походу что-то не так... Удаляю пользователя.")
                                    del j["users"][j["users"][str(message.from_user.id)][0]]
                                    j["users"][str(message.from_user.id)] = "свободный"
                        elif message.reply_to_message and (str(message.reply_to_message.from_user.id) == "7821675338"):
                            bot.reply_to(message, f"Bot ibt-2: {IBT2(message.text)}")
                            j['stata'][str(message.from_user.id)]['ии'] += 1
                
                    else:
                        if message.text.lower() == "да":
                            bot.reply_to(message, "Начинаю удаление")
                            deleteBase(message.from_user.id)
                        else:
                            j["tDel"].remove(str(message.from_user.id))
                            save(FILE, j)
                            bot.reply_to(message, "Удаление отменено")

while True:
    try:
        # Запуск бота
        bot.polling(non_stop=True)
    except Exception as e:
        os.system("cls")
        print(e)
        continue
