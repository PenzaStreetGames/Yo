Возможные операции с сегментами:
* Системная область
    1. Инициализация
        1. Запись сегмента
* Стек памяти
    1. Инициализация
        1. Запись сегмента
        2. Передача ссылки в системную область
        3. Установка вершины стека
* Стек вызовов
    1. Инициализация
        1. Запись сегмента
        2. Передача ссылки в системную область
        3. Установка вершины стека
* Программа
    1. Иницализация
        1. Оценка размера сегмента
        2. Запись заголовка
        3. Запись набора команд
        4. Определение родителя импортации
        5. Инициализация пространства имён
        6. Передача ссылки в системную область, если программа 
        главная
* Сегмент данных
    1. Инициализация
        1. Запись сегмента
        2. Передача ссылки в системную область
    2. Расширение
        1. Оценка размера сегмента
        2. Передача ссылки в системную область
        3. Передача ссылки в предыдущий сегмент
        4. Закрытие предыдущего сегмента для записи
* Сегмент списка
    1. Инициализация
        1. Запись сегмента
    2. Расширение
        1. Оценка размера сегмента
        2. Передача ссылки в предыдущий сегмент
        3. Закрытие предыдущего сегмента для записи
* Сегмент словаря
    1. Инициализация
        1. Запись сегмента
    2. Расширение
        1. Оценка размера сегмента
        2. Передача ссылки в предыдущий сегмент
        3. Закрытие предыдущего сегмента для записи
* Пространство имён
    1. Инициализация
        1. Запись сегмента
    2. Расширение
        1. Оценка размера сегмента
        2. Передача ссылки в предыдущий сегмент
        3. Закрытие предыдущего сегмента для записи