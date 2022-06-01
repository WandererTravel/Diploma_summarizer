import bs4 as bs
import urllib.request
import re
import nltk
import heapq
from rouge import Rouge

# Исходные параметры
print('\nИсходные параметры:\n\n - Источник: Статья Википедии про ИИ\n - Язык: Английский\n '
      '- Максимальное кол-во слов в предложении: 30\n - Кол-во предложений в реферате: 10\n')
data_link = 'https://en.wikipedia.org/wiki/Artificial_intelligence'  # Ссылка на источник
language = 'english'  # Определение языка обработки
characters = '[^a-zA-Z]'  # Определение символов в зависимости от языка
max_w_in_sent = 30  # Максимальное кол-во слов в предложении
sentences = 10  # Кол-во предложений в реферате

change_params = int(input("Изменить параметры?\n\n 1. Да\n 2. Нет\n\n"))
if change_params == 1:
    data_link = input("Введите ссылку на источник: ")  # Ввод ссылки на источник
    select_lang = int(input("\nВыберите язык текста:\n\n 1. Английский\n 2. Русский\n\n"))  # Выбор языка обработки
    # Настройка языковых параметров, в зависимости от выбранного языка
    if select_lang == 1:
        print("Выбран английский язык")
        language = 'english'
        characters = '[^a-zA-Z]'
    elif select_lang == 2:
        print("Выбран русский язык")
        language = 'russian'
        characters = '[^а-яА-Я]'
    else:
        print("Введен некорректный символ, попробуйте еще раз.")
        exit()
    max_w_in_sent = int(input("\nМаксимальное кол-во слов в предложении: "))  # Ввод макс. кол-ва слов в предложении
    sentences = int(input("\nИтоговое кол-во предложений в реферате: "))  # Ввод кол-ва предложений в реферате
elif change_params == 2:
    print("\nВыбраны исходные параметры")
else:
    print("Введен некорректный символ, попробуйте еще раз.")
    exit()

scraped_data = urllib.request.urlopen(data_link)  # Открытие ссылки
article = scraped_data.read()  # Чтение полученных данных

parsed_article = bs.BeautifulSoup(article, 'lxml')  # Парсинг статьи
# параметры: очищенный объект данных (article) и парсер (lxml)
paragraphs = parsed_article.find_all('p')  # Возвращение всех абзацев статьи в виде списка

article_text = ""  # Создание пустой переменной для статьи

for p in paragraphs:  # Объединение абзацев, для воссоздания статьи
    article_text += p.text

# Удаление квадратных скобок и лишних пробелов для объекта article_text
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)
# article_text теперь содержит исходную статью

# Удаление специальных символов и цифр для объекта formatted_article_text
formatted_article_text = re.sub(characters, ' ', article_text)
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
# formatted_article_text теперь содержит отформатированную статью

sentence_list = nltk.sent_tokenize(article_text)  # Токенизация предложений
# Используется объект article_text, т.к. он содержит в себе знаки препинания, в отличие от formatted_article_text

stopwords = nltk.corpus.stopwords.words(language)  # Сохранение стоп-слов выбранного языка в переменную stopwords

word_frequencies = {}  # Создание пустого словаря word_frequencies
# Вычисление частоты встречаемости каждого слова
# Используется объект formatted_article_text, т.к. он не содержит в себе знаков препинания, цифр и других спец. символов
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:  # Является ли слово стоп-словом?
        if word not in word_frequencies.keys():  # Существует ли слово в словаре word_frequencies?
            word_frequencies[word] = 1  # Если слово встречается впервые,
        else:  # то оно добавляется в словарь в качестве ключа, а его значение становится равным 1
            word_frequencies[word] += 1  # Иначе, если слово уже есть в словаре, то его значение увеличивается на 1

maximum_frequency = max(word_frequencies.values())  # Нахождение максимальной частоты вхождения

# Нахождение взвешенной частоты путём деления числа всех вхождений всех слов на частоту наиболее встречающегося слова
for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

sentence_scores = {}  # Создание пустого словаря sentence_scores
# Вычисление баллов предложений
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():  # Если слово в списке слов
            if len(sent.split(' ')) <= max_w_in_sent:  # Если длина предложения <= заданного макс. значения
                if sent not in sentence_scores.keys():  # Если предложение не в словаре предложений
                    sentence_scores[sent] = word_frequencies[word]  # Добавление предложения в словарь в качестве ключа
                else:  # и присваивание ему взвешенной частоты первого слова в предложении в качестве значения
                    sentence_scores[sent] += word_frequencies[word]  # Иначе, добавление взвешенной частоты слова
                    # к существующему значению
# Теперь в словаре sentence_scores находится список предложений с соответствующей оценкой

# Вызов определенного количества предложений с самыми высокими баллами
summary_sentences = heapq.nlargest(sentences, sentence_scores, key=sentence_scores.get)

# Получение реферата, путем соединения предложений
summary = ' '.join(summary_sentences)

# Вывод реферата на экран
print("\nГотовый текст:\n" + summary)

# Запись результатов в файл
final_file = open("F:\Diploma\my_final.txt", "w")
final_file.write(summary)
final_file.close()

select_rouge = int(input("\nВычислить параметры ROUGE-метрик?\n\n 1. Да\n 2. Нет\n\n"))
# Инициализация расчетов ROUGE-метрик оценки автоматического реферирования
if select_rouge == 1:
    human_sum_file = open("F:\Diploma\my_human_internet.txt", encoding='utf-8')
    # my_human_ai, my_human_internet, my_human_television_ru
    human_sum = human_sum_file.read()
    human_sum_file.close()
    print("\nПараметры ROUGE-метрик:\n")
    rouge = Rouge()
    scores = rouge.get_scores(summary, human_sum)
    print(scores)
    # Запись результатов оценки реферирования в файл
    scores_file = open("F:\Diploma\my_scores.txt", "w")
    for item in scores:
        scores_file.write("%s\n" % item)
    scores_file.close()
elif select_rouge == 2:
    exit()
else:
    print("\nВведен некорректный символ, попробуйте еще раз.\n")
    exit()
