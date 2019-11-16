#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import vk_api
import random
import secret
vk = vk_api.VkApi(token=secret.TOKEN)

def get_random_id():
    return random.getrandbits(31) * random.choice([-1, 1])
def send(text, id):
    """
    отправить сообщение
    """
    vk.method('messages.send',  {'peer_id' : id,'message' : text, 'random_id' : get_random_id()})
def end_of_word(tp):
    if tp % 10 == 1 and tp % 100 != 11: # Формула 1
        return str(tp) + ' ошибка'
    elif tp % 10 >= 2 and tp % 10 <= 4 and (tp % 100 < 10 or tp % 100 > 20): # Формула 2
        return str(tp) + ' ошибки'
    else:
        return str(tp) + ' ошибок'

data = {}
questions = {}
answers = {}
f = open('questions.txt')
count = 1
for line in f.readlines():
    questions[count] = line
    count += 1
f.close()
f = open('answers.txt')
count = 1
for line in f.readlines():
    answers[count] = line
    count += 1
f.close()
print(questions, len(questions))
print(answers)
count = 1
while True:
    messages = vk.method('messages.getConversations', {'offset': 0, 'count': 20, 'filter': 'unread'})
    if messages['count'] > 0:
        id = messages['items'][0]['last_message']['from_id']  # айди отправителя
        body = messages['items'][0]['last_message']['text'].lower()  # текст сообщения
        if id in data:
            if body == 'заново':
                count = 1
                data[id] = -1
                send(questions[count], id)
            if count <= len(questions):
                print(body, answers[count], '\n', answers)
                if body + '\n' == answers[count]:
                    count += 1
                    send('Ответ верный! Следующий вопрос: ' + questions[count], id)
                else:
                    data[id] += 1
                    if data[id] > 0:
                        send('Ответ неверный, вами допущено ' + end_of_word(data[id]), id)
            else:
                send('Вы правильно ответили на все вопросы \n ошибок допущено: ' + end_of_word(data[id]) +  ' \n \n чтобы попробовать еще пишите "заново"', id)
        else:
            data[id] = 0
            send('Из какого слова из семи букв можно убрать одну "букву", чтобы осталось две буквы?  \n \n имейте в виду что ответом является строго определенный ответ', id)