import random as rn
import json
from collections import Counter
import re

def most_common_word(text):
    # Приводим текст к нижнему регистру и удаляем знаки препинания
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Считаем частоту каждого слова
    word_counts = Counter(words)
    
    # Находим самое частое слово
    most_common = word_counts.most_common(1)
    
    return most_common[0] if most_common else None

def load(file):
    try:
        with open("base/" + file, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"frases_of_ai1": [], "freses_of_ai2": {"words_to_words": {}}}
    except json.JSONDecodeError:
        print(f'Ошибка при загрузке файла {file}.')
        return {"frases_of_ai1": [], "freses_of_ai2": {"words_to_words": {}}}

def generator(word):
    data = load("frases_1.json")["freses_of_ai2"]["words_to_words"]
    if word not in data.keys():
        return False
    else:
        return rn.choice(
            data[word]
        )

def save(file, data):
    with open("base/" + file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def IBT1(prompt):
    frases = load("frases_1.json")["frases_of_ai1"]
    if len(frases) != 0:
        if len(prompt.split()) >= 3 or not len(frases) >= 15:
            out = rn.choice(frases)
            frases.append(prompt)
            save("frases_1.json", frases)
            return out
        else:
            return "Мой хозяин запрещает мне разговаривать с теми у которых словарный запас как минимум 6 слов"
    else:
        frases.append(prompt)
        save("frases_1.json", frases)
        return "Ошибка: мало фраз, надо больше"


def IBT2(prompt):
    data = load("frases_1.json")
    if len(data["freses_of_ai2"]["words_to_words"].keys()) != 0:
        words_user = prompt.lower().split()
        context_word = most_common_word(prompt.lower())[0]
        a = False
        if context_word or rn.choice(prompt.lower().split()) in data["freses_of_ai2"]["words_to_words"].keys():
            a = True
            new_word = context_word
            message = [new_word]
            while True:
                text = ""
                for word in message:
                    text += word + " "
                text = text[:-1]
                if (len(message) >= 120) or (len(text) >= 4096):
                    new_word = new_word + "."
                    del message[len(message) - 1]
                    message.append(new_word)
                    break
                else:
                    nnew_word = generator(new_word)
                    if not nnew_word:
                        new_word = new_word + "."
                        del message[len(message) - 1]
                        message.append(new_word)
                        break
                    else:
                        new_word = nnew_word
                        message.append(new_word)
            text = " ".join(message)
        
        ks = prompt.lower().split()[:-1]
        vs = prompt.lower().split()[1:]
        for k, v in zip(ks, vs):
            if k in data["freses_of_ai2"]["words_to_words"].keys():
                data["freses_of_ai2"]["words_to_words"][k].append(v)
            else:
                data["freses_of_ai2"]["words_to_words"][k] = [v]
        save("frases_1.json", data)
        
        if a:
            print(text)
            return text
        else:
            return "Я не знаю этого слова, простите"

    else:
        ks = prompt.lower().split()[:-1]
        vs = prompt.lower().split()[1:]
        for k, v in zip(ks, vs):
            if k in data["freses_of_ai2"]["words_to_words"].keys():
                data["freses_of_ai2"]["words_to_words"][k].append(v)
            else:
                data["freses_of_ai2"]["words_to_words"][k] = [v]
        save("frases_1.json", data)
        return "Ошибка: мало фраз, надо больше"


def IBT3(tokens, prompt):
    data = load("frases_1.json")
    if len(data["freses_of_ai2"]["words_to_words"].keys()) != 0:
        words_user = prompt.lower().split()
        context_word = most_common_word(prompt.lower())[0]
        a = False
        if context_word or rn.choice(prompt.lower().split()) in data["freses_of_ai2"]["words_to_words"].keys():
            a = True
            new_word = context_word
            message = [new_word]
            while True:
                if len(message) >= tokens:
                    new_word = new_word + "."
                    del message[len(message) - 1]
                    message.append(new_word)
                    break
                else:
                    nnew_word = generator(new_word)
                    if not nnew_word:
                        new_word = new_word + "."
                        del message[len(message) - 1]
                        message.append(new_word)
                        break
                    else:
                        new_word = nnew_word
                        message.append(new_word)
            text = " ".join(message)
        
        ks = prompt.lower().split()[:-1]
        vs = prompt.lower().split()[1:]
        for k, v in zip(ks, vs):
            if k in data["freses_of_ai2"]["words_to_words"].keys():
                data["freses_of_ai2"]["words_to_words"][k].append(v)
            else:
                data["freses_of_ai2"]["words_to_words"][k] = [v]
        save("frases_1.json", data)
        
        if a:
            return text
        else:
            return "Я не знаю этого слова, простите"

    else:
        ks = prompt.lower().split()[:-1]
        vs = prompt.lower().split()[1:]
        for k, v in zip(ks, vs):
            if k in data["freses_of_ai2"]["words_to_words"].keys():
                data["freses_of_ai2"]["words_to_words"][k].append(v)
            else:
                data["freses_of_ai2"]["words_to_words"][k] = [v]
        save("frases_1.json", data)
        return "Ошибка: мало фраз, надо больше"

"""

def IBT2(prompt):
    data = load("frases_1.json")
    banned_words = load("banned_words.json")
    if len(data["freses_of_ai2"]["words_to_words"].keys()) != 0:
        words_user = prompt.lower().split()
        context_word = most_common_word(prompt.lower())[0]
        a = False
        if context_word or rn.choice(prompt.lower().split()) in data["freses_of_ai2"]["words_to_words"].keys():
            a = True
            new_word = context_word
            message = [new_word]
            while True:
                if len(message) >= 120:
                    new_word = new_word + "."
                    del message[len(message) - 1]
                    message.append(new_word)
                    break
                else:
                    nnew_word = generator(new_word)
                    if not nnew_word:
                        new_word = new_word + "."
                        del message[len(message) - 1]
                        message.append(new_word)
                        break
                    else:
                        if nnew_word not in banned_words:
                            new_word = nnew_word
                            print(nnew_word)
                            message.append(new_word)
                        else:
                            while nnew_word in banned_words:
                                nnew_word = generator(new_word)
                                if nnew_word not in banned_words:
                                    new_word = nnew_word
                                    message.append(new_word)
                                    break
                                else:
                                    pass
                                
            text = " ".join(message)
        
        ks = prompt.lower().split()[:-1]
        vs = prompt.lower().split()[1:]
        for k, v in zip(ks, vs):
            if k in data["freses_of_ai2"]["words_to_words"].keys():
                data["freses_of_ai2"]["words_to_words"][k].append(v)
            else:
                data["freses_of_ai2"]["words_to_words"][k] = [v]
        save("frases_1.json", data)
        
        if a:
            print(text)
            return text
        else:
            return "Я не знаю этого слова, простите"

    else:
        ks = prompt.lower().split()[:-1]
        vs = prompt.lower().split()[1:]
        for k, v in zip(ks, vs):
            if k in data["freses_of_ai2"]["words_to_words"].keys():
                data["freses_of_ai2"]["words_to_words"][k].append(v)
            else:
                data["freses_of_ai2"]["words_to_words"][k] = [v]
        save("frases_1.json", data)
        return "Ошибка: мало фраз, надо больше"

"""
