#!/usr/bin/env python
# coding: utf-8

# In[103]:


import telebot
import requests
from telebot import types
import matplotlib.pyplot as plt
from PIL import Image
from datetime import date
bot = telebot.TeleBot("1799078640:AAFsJy-RhRDhZHNnXJiAObBqYIEj3xNnTr0")

@bot.message_handler(commands=['start'])
def send_keyboard(message, text="Привет! Поинвестируем?"):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Общая информация по тикеру') 
    itembtn2 = types.KeyboardButton('О компании')
    itembtn3 = types.KeyboardButton('Инвестиционная рекомендация')
    itembtn4 = types.KeyboardButton("Обменный курс валюты")
    itembtn5 = types.KeyboardButton('Последние новости')
    itembtn6 = types.KeyboardButton('Календарь IPO')
    itembtn7 = types.KeyboardButton('Последние дивиденды по акциям')
    keyboard.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
    msg = bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
    bot.register_next_step_handler(msg, get_info)      

def fn_way(msg):
    if msg.text.lower() == 'да' and function_name == 'fn6':
        send_keyboard(msg, 'Выберите другую функцию!')
    elif msg.text.lower() == 'да':
        msg = bot.send_message(msg.chat.id, 'Можете вводить!')
        if function_name == 'fn1':
            bot.register_next_step_handler(msg, fn1)
        elif function_name == 'fn2':
            bot.register_next_step_handler(msg, fn2)
        elif function_name == 'fn3':
            bot.register_next_step_handler(msg, fn3)
        elif function_name == 'fn4':
            bot.register_next_step_handler(msg, fn4)
        elif function_name == 'fn5':
            bot.register_next_step_handler(msg, fn5)    
        elif function_name == 'fn7':
            bot.register_next_step_handler(msg, fn7)  
    elif msg.text.lower() == 'нет':
        send_keyboard(msg, 'Выберите другую функцию!')
    else:
        msg = bot.send_message(msg.chat.id, 'Напишите по-человечески (Да/Нет)')
        bot.register_next_step_handler(msg, fn_way)

def fn1(msg):
    stock_ticker = msg.text.upper()
    if len(stock_ticker) <= 4 and len(stock_ticker) >= 0: 
        try:
            bot.reply_to(msg, f"Тикер: {stock_ticker}. Нейросеть обрабатывает информацию...")
            url = f'https://financialmodelingprep.com/api/v3/profile/{stock_ticker}?apikey=ad694b340c143f34b855df423c5056e8'
            result = requests.get(url)
            result_json = result.json()[0]
            beta = str(result_json["beta"])
            cur = str(result_json["currency"])
            response = str(result_json["symbol"]) + '. Цена сейчас: ' + str(result_json["price"]) + ' ' + cur + "\n" + 'Коэффициент Beta: ' + str(beta)
            bot.send_message(msg.chat.id, response)   
            
            url = f'https://financialmodelingprep.com/api/v3/quote/{stock_ticker}?apikey=ad694b340c143f34b855df423c5056e8'
            result = requests.get(url)
            result_json = result.json()[0]
            current_price = float(result_json["price"])
            open_price = float(result_json["open"])
            price_change = round(current_price/open_price*100-100, 2)
            response = 'Изменение цены за день: ' + str(price_change) + '%'
            bot.send_message(msg.chat.id, response)  

            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_ticker}&apikey=602BSAC2PVP683RH'
            result = requests.get(url)
            x = result.json()['Time Series (Daily)']
            c = []
            t = []
            for key in x.keys():
                t.append(key)
                c.append(float(x[key]['4. close']))
            c.reverse()
            t.reverse()
            plt.clf()
            plt.figure(figsize=(15, 6))
            plt.plot(t, c, label="Close Price - Day", color = 'blue');
            plt.xticks(size=7, rotation=90)
            plt.xlabel('Дата')
            plt.ylabel(f'{cur}')
            plt.title(f'Дневной график с начала 2021 года - {stock_ticker}', fontsize = 16, fontfamily = 'montserrat', fontweight = 'bold', alpha = 0.7, color = 'black')
            plt.grid(True);
            plt.savefig('saved_figure.png', dpi = 200)
            img = Image.open(r'saved_figure.png')
            bot.send_photo(msg.chat.id, img)

            global function_name
            function_name = 'fn1'
            msg = bot.send_message(msg.chat.id, 'Ещё по тикеру?) Да/Нет')
            bot.register_next_step_handler(msg, fn_way)

        except:
            bot.send_message(msg.chat.id, 'Только американские акции! Введите заново!') 
            bot.register_next_step_handler(msg, fn1)  
    else:
        msg = bot.send_message(msg.chat.id, 'Напишите по-человечески(')
        bot.register_next_step_handler(msg, fn1)
        
def fn2(msg):
    stock_ticker = msg.text
    if len(stock_ticker) <= 4 and len(stock_ticker) >= 0: 
        try:            
            bot.reply_to(msg, f"Тикер: {stock_ticker}. Ищем информацию...")
            url = f'https://financialmodelingprep.com/api/v3/profile/{stock_ticker}?apikey=ad694b340c143f34b855df423c5056e8'
            result = requests.get(url)
            result_json = result.json()[0]
            response = str(result_json["description"])
            bot.send_message(msg.chat.id, response)

            global function_name
            function_name = 'fn2'
            msg = bot.send_message(msg.chat.id, 'Ещё одну компанию?) Да/Нет')
            bot.register_next_step_handler(msg, fn_way)
        except:
            bot.send_message(msg.chat.id, 'Только американские акции! Введите заново!') 
            bot.register_next_step_handler(msg, fn2)             
    else:
        msg = bot.send_message(msg.chat.id, 'Напишите по-человечески(')
        bot.register_next_step_handler(msg, fn2)

def fn3(msg):
    stock_ticker = msg.text.upper()
    if len(stock_ticker) <= 4 and len(stock_ticker) >= 0: 
        try:            
            bot.reply_to(msg, f"Тикер: {stock_ticker}. Ищем информацию...")
            url = f'https://financialmodelingprep.com/api/v3/rating/{stock_ticker}?apikey=b59a97db01de231d304f7c4c20a0670d'
            result = requests.get(url)
            result_json = result.json()[0]
            response = 'Общий сравнительный рейтинг: ' + str(result_json["ratingScore"]) + ' out of 5. ' + "\n" + 'Сравнительный рейтинг P/E: ' + str(result_json["ratingDetailsPEScore"]) + ' out of 5. '+ "\n" +'Рекомендация: ' + f'*{str(result_json["ratingRecommendation"])}*' + '!'
            bot.send_message(msg.chat.id, response, parse_mode="Markdown")

            global function_name
            function_name = 'fn3'
            msg = bot.send_message(msg.chat.id, 'Ещё рекомендация?) Да/Нет')
            bot.register_next_step_handler(msg, fn_way)
        except:
            bot.send_message(msg.chat.id, 'Только американские акции! Введите заново!') 
            bot.register_next_step_handler(msg, fn3)  
    else:
        msg = bot.send_message(msg.chat.id, 'Напишите по-человечески(')
        bot.register_next_step_handler(msg, fn3)

def fn4(msg):
    currency = msg.text.upper()
    cur = currency.split('/')
    if len(cur[0]) == 3 and len(cur[1]) == 3: 
        try:            
            bot.reply_to(msg, f"Так, посмотрим обменный курс {currency}.")
            url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={cur[0]}&to_currency={cur[1]}&apikey=602BSAC2PVP683RH'
            r = requests.get(url)
            result_json = r.json()['Realtime Currency Exchange Rate']
            response = 'Обменный курс: ' + str(result_json['5. Exchange Rate'])
            bot.send_message(msg.chat.id, response)
            
            global function_name
            function_name = 'fn4'
            msg = bot.send_message(msg.chat.id, 'Хотите проверить другой курс?) Да/Нет')
            bot.register_next_step_handler(msg, fn_way)
        except:
            bot.send_message(msg.chat.id, 'Может быть вы ошиблись? Попробуем еще раз.') 
            bot.register_next_step_handler(msg, fn4)  
    else:
        msg = bot.send_message(msg.chat.id, 'Напишите по-человечески(')
        bot.register_next_step_handler(msg, fn4)

def fn5(msg):
    ticker = msg.text.upper()
    if len(ticker) <= 4 and len(ticker) >= 0: 
        try:
            bot.reply_to(msg, 'Так, что новенького...?')
            url = f'https://financialmodelingprep.com/api/v3/stock_news?tickers={ticker}&limit=50&apikey=b59a97db01de231d304f7c4c20a0670d'
            result = requests.get(url)
            res1 = result.json()[0]['title']
            res2 = result.json()[0]['image']
            res3 = result.json()[0]['url']
            response = f'Последние новости про {ticker}: ' + '\n' + res1 + '\n' + res3
            bot.send_message(msg.chat.id, response)

            global function_name
            function_name = 'fn5'
            msg = bot.send_message(msg.chat.id, 'Еще новости?) Да/Нет')
            bot.register_next_step_handler(msg, fn_way)
        except:
            bot.send_message(msg.chat.id, 'Может быть вы ошиблись? Попробуем еще раз.') 
            bot.register_next_step_handler(msg, fn5)  
    else:
        msg = bot.send_message(msg.chat.id, 'Напишите по-человечески(')
        bot.register_next_step_handler(msg, fn5)

def fn6():
    try:
        dt = date.today()
        url = f'https://finnhub.io/api/v1/calendar/ipo?from={str(dt)}&to=2021-09-17&token=c328vi2ad3ieculvdrc0'
        r = requests.get(url)
        datr = reversed(r.json()['ipoCalendar'])
        t = f''
        for i in datr:
            t += '.'.join(reversed(i['date'].split('-')))+' '+i['name']+' '+ f'({i["exchange"]})'+'\n'
        if len(t)>0:
            response = t[:-1]
        else:
            response = 'В ближайшее время IPO не запланированы'
        bot.send_message(msg2.chat.id, response)
        global function_name
        function_name = 'fn6'
        msg = bot.send_message(msg2.chat.id, 'Перейти на другую функцию? (Введите да, если хотите перейти)')
        bot.register_next_step_handler(msg, fn_way)
    except:
        bot.send_message(msg2.chat.id, 'В ближайшее время IPO не запланированы')
        msg = bot.send_message(msg2.chat.id, 'Перейти на другую функцию? (Введите да, если хотите перейти)')
        bot.register_next_step_handler(msg, fn_way)
def fn7(msg):
    stock_ticker = msg.text.upper()
    if len(stock_ticker) <= 4 and len(stock_ticker) >= 0: 
        try:            
            bot.reply_to(msg, f"Тикер: {stock_ticker}. Ищем информацию...")
            url = f'https://api.polygon.io/v2/reference/dividends/{stock_ticker}?&apiKey=8pTWyafW0p8wpmOGCtFgdqp2BnKCKphb'
            result = requests.get(url)
            if result.json()['count'] != 0:
                result_json = result.json()['results'][0]
                pdate = 'Дата последней выплаты: '+'.'.join(reversed(result_json['paymentDate'].split('-')))
                amm = 'Размер дивидендов: '+str(result_json['amount'])+'$'
                response = pdate + "\n" + amm
            else:
                response = 'Данной компанией дивиденды не выплачивались ( '
            bot.send_message(msg.chat.id, response)

            global function_name
            function_name = 'fn7'
            msg = bot.send_message(msg.chat.id, 'Ещё одну компанию?) Да/Нет')
            bot.register_next_step_handler(msg, fn_way)
        except:
            bot.send_message(msg.chat.id, 'Только американские акции! Введите заново!') 
            bot.register_next_step_handler(msg, fn7)             
    else:
        msg = bot.send_message(msg.chat.id, 'Напишите по-человечески(')
        bot.register_next_step_handler(msg, fn7)
        
def get_info(message):
    if  message.text == "Общая информация по тикеру":
        msg = bot.send_message(message.chat.id, 'Введите тикер акции! (пример AAPL)')
        bot.register_next_step_handler(msg, fn1)
    elif message.text == "О компании":
        msg = bot.send_message(message.chat.id, 'Введите тикер акции компании! (пример AAPL)')
        bot.register_next_step_handler(msg, fn2)    
    elif message.text == "Инвестиционная рекомендация":
        msg = bot.send_message(message.chat.id, 'Введите тикер акции! (пример AAPL)')
        bot.register_next_step_handler(msg, fn3) 
    elif message.text == "Обменный курс валюты":
        msg = bot.send_message(message.chat.id, 'Введите  интересующий вас курс! (пример USD/RUB)')
        bot.register_next_step_handler(msg, fn4) 
    elif message.text == "Последние новости":
        msg = bot.send_message(message.chat.id, 'Введите  тикер акции компании, новости про которую желаете узнать! (пример AAPL)')
        bot.register_next_step_handler(msg, fn5)
    elif message.text == "Календарь IPO":
        global msg2
        msg2 = bot.send_message(message.chat.id, 'Так, посмотрим ближайшие IPO...')
        fn6()
    elif message.text == "Последние дивиденды по акциям":
        msg = bot.send_message(message.chat.id, 'Введите тикер акции компании! (пример AAPL)')
        bot.register_next_step_handler(msg, fn7)
        
bot.polling(none_stop = True)

