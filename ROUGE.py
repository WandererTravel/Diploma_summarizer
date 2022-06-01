from rouge import Rouge  # Алгоритм для расчета параметров ROUGE-метрик для результатов систем-аналогов

menu_var = int(input("Варианты ввода результатов суммаризации:\n\n 1. Файл\n 2. Ручной ввод текста\n\n"))
if menu_var == 1:
    system_var = int(input("Какой инструментарий использовать?\n\n 1. TLDR this\n 2. paraphraser.io\n\n"))
    if system_var == 1:
        article_var = int(input("Какую статью использовать?\n\n 1. Интернет (стандартный, малый)\n "
                                "2. Интернет (рус.) (продвинутый, малый)\n 3. Интернет (продвинутый, малый)\n "
                                "4. Телевидение (продвинутый, объемный)\n\n"))
        if article_var == 1:
            print("Выбрана статья про Интернет. Метод суммаризации - стандартный, объем - малый")
            essay = open("F:\Diploma\TLDR_Internet_com_s.txt")
            summary = essay.read()
        elif article_var == 2:
            print("Выбрана статья про Интернет на русском языке. Метод суммаризации - стандартный, объем - малый")
            essay = open("F:\Diploma\TLDR_Internet_com_s_ru.txt", encoding='utf-8')
            summary = essay.read()
        elif article_var == 3:
            print("Выбрана статья про Интернет. Метод суммаризации - продвинутый, объем - малый")
            essay = open("F:\Diploma\TLDR_Internet_adv_s.txt")
            summary = essay.read()
        elif article_var == 4:
            print("Выбрана статья про Телевидение. Метод суммаризации - продвинутый, объем - большой")
            essay = open("F:\Diploma\TLDR_Television_adv_l.txt")
            summary = essay.read()
        else:
            exit()
    elif system_var == 2:
        article_var = int(input("Какую статью использовать?\n\n 1. ИИ\n 2. Интернет\n\n"))
        if article_var == 1:
            print("Выбрана статья про Искусственный Интеллект")
            essay = open("F:\Diploma\PARAPHRASER_AI.txt")
            summary = essay.read()
        elif article_var == 2:
            print("Выбрана статья про Интернет")
            essay = open("F:\Diploma\PARAPHRASER_Internet.txt")
            summary = essay.read()
        else:
            exit()
    else:
        exit()
elif menu_var == 2:
    summary = input("Введите исходный текст для реферирования: ")
else:
    exit()

select_article = int(input("\nЧеловеческий реферат:\n\n 1. ИИ (англ.)\n 2. Интернет (англ.)\n "
                           "3. Интернет (рус.)\n 4. Телевидение (англ.)\n\n"))
if select_article == 1:
    print("Выбран реферат по статье про ИИ на английском языке")
    human_essay = "F:\Diploma\my_human_ai.txt"
elif select_article == 2:
    print("Выбран реферат по статье про Интернет на английском языке")
    human_essay = "F:\Diploma\my_human_internet.txt"
elif select_article == 3:
    print("Выбран реферат по статье про Интернет на русском языке")
    human_essay = "F:\Diploma\my_human_internet_ru.txt"
elif select_article == 4:
    print("Выбран реферат по статье про Телевидение на английском языке")
    human_essay = "F:\Diploma\my_human_television.txt"
else:
    exit()

print("Вычисление параметров ROUGE-метрик")
human_sum_file = open(human_essay)
human_sum = human_sum_file.read()
human_sum_file.close()
rouge = Rouge()
scores = rouge.get_scores(summary, human_sum)
print("\nПараметры ROUGE-метрик:\n")
print(scores)
scores_file = open("F:\Diploma\my_scores.txt", "w")
for item in scores:
    scores_file.write("%s\n" % item)
scores_file.close()
