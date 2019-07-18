# Запись объекта в сегмент данных
Оказалось, записать объект в сегмент данных, учитывая все переносы, очень 
сложно. А всё что сложно, надо записывать в вот такие файлы.
## Алгоритм
Мы записываем объект сначала?
* Да
    * Объект входит полностью?
        * Да
            * Записать объект с начала и до конца
        * Нет
            * Записать объект с начала и не до конца
            * Повторить алгоритм в новом сегменте для оставшейся части объекта
* Нет
    * Оставшаяся часть объекта входит полностью?
        * Да
            * Записать объект не с начала и до конца
        * Нет 
            * Записать объект не с начала и не до конца
            * Повторить алгоритм в новом сегменте для оставшейся части объекта