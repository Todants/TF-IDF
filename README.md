# TF-IDF
Web-сервис, который позволяет загрузить до 5 файлов формата .txt и получить таблицу со значениями tf (сколько раз это слово встречается в тексте) и idf (обратная частота документа).
Чтобы запустить приложение необходимо скачать библиотеки django, nltk, pymorphy2, а затем запустить сервис командой "python manage.py runserver"

Сервис позволяет загрузить до 5 txt файлов с вашего устройства.

Из загруженных файлов выбирается один главный. Выбрать главный файл можно после загрузки файлов, нажимая на кнопки с названиями файлов над таблицей.

Колонка Word выводит все слова, содержащиеся в выбранном файле.
Колонка TF содержит число, являющееся отношением количества слов в выбранном тексте к общему количеству слов в этом файле.
Колонка IDF содержит число, являющееся отношением общего количества загруженных файлов к количеству файлов, в которых встречается данное слово.
Таблица упорядочена по столбцу IDF.

Таблица содержит до 50 строк. Если в выбранном тексте встречается более 50 уникальных слов - есть возможность перейти на следующую страницу таблицы, тогда выведутся следующие 50 слов. Также есть возможность и перехода на предыдущую страницу таблицы.

Есть возможность проводить подсчет TF и IDF по инфинитивам слов. Эту возможность можно переключать над таблицей. Если на кнопке написано "OFF", значит таблица содержит все слова в том виде, в котором они находятся в выбранном тексте. Если на кнопке написано "ON", значит таблица содержит записи со словами, сгруппированными по начальной форме этих слов. Эта функция позволяет проводить поиск и подсчёт слов, независимо от того, в какой именно форме встречается слово.
