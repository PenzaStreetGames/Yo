# -Yo-
Разработка языка программирования

В идеале, должно быть много наворотов:

* Функциональность
    * Общее назначение
        * Структурное программирование (if else, while)
        * Функциональное программирование (func, lambda, return)
        * Модульное программирование (import, from)
        * Объектно-ориентированное программирование (class, static, public)
    * Объединение инструментов программирования
        * Язык разметки (structure {})
        * Базы данных и запросы к ним (from, select, where, order_by)
        * Язык стилизации ( .class { color: #ff00ff } )
        * Инструменты http (get, post, delete, put, patch)
        * Обработка действий пользователя в браузере ( фронт энд )
    * Поддержка языковых пакетов
        * Пользователю даётся возможность писать код на родном языке, 
        используя языковые пакеты, которые заменяют слова
        разных языков на английские
    * Работа с другими языками программирования
        * Для удобства написания библиотек нужен программный интерфейс для 
        работы с программами на других языках программирования
    * Исполнение
        * Виртуальное исполнение
        * Компилированное исполнение
        * Доступ пользователя к памяти
    * Файлы
        * Расширение .yo
        * Архивное строение:
            * Текст программы
            * Скомпилированный код

Текущая разработка осуществляется по следующим направлениям:

* Разработка виртуальной машины
    * Стандарты бинарной записи
    * Инициализация ленты памяти
    * Операции с ячейками
* Увеличение работоспособности компилятора
    * Распутать код
    * Добавить живучести
    * Добавить комментарии
* Среда разработки
    * Подсветка синтаксиса
    * Добавить разные кнопочки
