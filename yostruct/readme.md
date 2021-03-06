# Теория
## Концепция

Информация, которой становится всё больше и больше, требует упорядочивания.
Одной из форм такого упорядочивания является оформление - разметка. Стандарты
разметки, принятые в мире в качестве ключевых и основополагающих, отвечали
потребностям тех времён, когда они создавались, а именно, в 90-е годы XX века.

Но отвечают ли они потребностям сегодняшнего дня? Время требует неумолимого
ускорения, появляется желание сделать больше, лучше и быстрее. Стандарт 
web-разметки HTML хранит в себе излишнее количество разметки и недостаточное
количество полезного наполнения. Писать на нём долго и запутанно. Конечно,
существуют инструменты для полуавтоматической работы с этим форматом, но это
не решает концептуально проблемы громоздкой и нечитаемой разметки.

Мировые стандарты в один день не отменяются, но альтернативу предложить можно.

И такой альтернативой выступает *Yo Struct*. Эта часть проекта *Yo* заточена под 
описание всевозможных структур данных. Практической составляющей этой части
проекта является преобразование человекочитаемого и краткого yostruct-формата
в тяжелый для понимания людей, но не машин html.

> Программирование для людей, а не машин

## Реализация

*Yo Struct* реализован на *Python 3* и представляет из себя лексический анализатор
текста с его преобразованием в древовидную структуру и форматированием этой
структуры в формат html.

Файлы, созданные с помощью *Yo Struct* можно сразу же конвертировать в 
web-формат и открыть в браузере. Для интегрированной работы планируется 
использовать специальную среду разработки *Yo Structer* в интерфейсе PyQt5.

## Перспективы

После полноценной реализации html-конвертера планируется добавить *Yo Struct*
в синтаксис языка *Yo* со всеми возможностями пользования. Также ожидается 
наличие css-конвертера, потому что к читаемости и минималистичности css-формата
тоже есть вопросы.

> Задача - объять необъятное

> Всё программирование в одном интерфейсе

# Описание формата

## Терминология

*Дерево* - структура данных из соподчиняющихся друг другу элементов

*Узел* - элемент дерева, который может иметь родительский элемент и дочерние

*Свойство* - какой-либо признак, присущий узлу

*Корень* - узел, не имеющий родителя, основание дерева и предок всех
остальных элементов

*Лист* - узел, не имеющий дочерних узлов

*Родитель* - узел, являющийся для данного узла непосредственным предком

*Дочерний узел* - узел, являющийся для данного узла непосредственным 
потомком

*Предок* - узел, связанный с данным цепочкой дочерних узлов

*Потомок* - узел, связанный с данным цепочкой родительских узлов

*Тег* - термин html, обозначающий узел дерева документа

*Атрибут* - термин html, обозначающий свойство узла дерева документа

*Контент* - полезное наполнение структуры, структурируемая информация

Для улучшения понимания, будут приводиться примеры сравнения конструкций html 
и эквивалентных им конструкций yo-struct. Это будет выглядеть примерно вот так:

    HTML
    конструкция html
    
    Yo Struct
    эквивалент yo struct

## Узлы (теги)

Тег, он же узел, является основной единицей в языке разметки html. Теги делятся
на двойные и одинарные. Двойной тег объявляется следующим образом:
    
    HTML
    <p>Привет, мир!</p>
    
    Yo Struct
    p(): "Привет, мир!"
    
Одинарный не имеет внутреннего содержимого и объявляется так:

    HTML
    <br/>
    
    Yo Struct
    br

## Атрибуты

Атрибуты, они же свойства, тегов записываются внутри первого тега html. В 
yo struct атрибуты записываются внутри круглых скобок.

    HTML
    <html lang="ru">
        ...
    </html>
    
    Yo Struct
    html(lang="ru"): 
        ...

Атрибуты-флаги записываются без значения и знака "=". Если html-атрибут
сам принимает на вход значение true, то оно должно быть записано в кавычках. 

    HTML
    <script async> ... </script>
    <p hidden="true">"Скрыто"</p>
    
    Yo Struct
    script(async): 
        ...
    p(hidden="true"): "Скрыто"
    
Тег может и не иметь атрибутов. Тогда написание круглых скобок необязательно,
но оно лишний раз подчёркивает, что написан тег.

    HTML
    <p>Текст</p>
    <p class="important">Важный текст</p>
    
    Yo Struct
    # Круглые скобки при отсутствии атрибутов не обязательны 
    p: "Text"
    
    # Но обязательны при их наличии
    p(class="important"): "Важный текст"

## Контент

Типы контента соответствуют соответствующим типам данных json, но из них в
работе с html поддерживаются только строки, и специальные слова: *true*, *pass*

    HTML
    <i>Текст, выделенный курсивом</i>
    
    Yo Struct
    i: "Текст, выделенный курсивом"


Строки заключаются в кавычки: 'одинарные' или "двойные". Комбинации знаков
\\" и \\' позволяют писать кавычки внутри кавычек.

## Необрабатываемая область

Пока не поддерживается обработка синтаксиса *CSS* и *JavaScript* а также из-за
желания вставить готовый кусок html-кода, можно обернуть кусок 
неперерабатываемого текста в \`наклонные кавычки\`.

    HTML
    <script>
        function hello() {}
        function goodbye() {}
    </script>
    
    <p>Не продам html!</p>
    
    Yo Struct
    script:
        `function hello() {}
        function goodbye() {}`
        
    `<p>Не продам html!</p>`

Область внутри наклонных кавычек не обрабатывается и вставляется целиком в
итоговый html-файл.

## Комментарии

Пояснительные записи заключаются внутри комментария. Знак комментария в 
*Yo Struct* - решётка #

> В перспективе возможна поддержка многострочных комментариев, как в C++ 
/\*...\*/

    HTML
    <!--Комментарий-->
    
    Yo Struct
    # Комментарий

Однострочный комментарий действует до конца строки

## Содержимое тегов

Двойные теги могут содержать внутри себя другие теги, либо какой-нибудь 
контент. Существует несколько способов записать содержимое тегов:
1. Отступной (выделение отступом)
2. Скобочный (выделение фигурными скобками)
3. Однострочный (запись в одну строку)

Каждый из способов имеет свои особенности синтаксиса

## Отступной способ группировки

Чтобы показать, что содержимое лежит внутри нужного тега, нужно выделить его
лишним отступом. После заголовка тега (названия и круглых скобок) необходимо
поставить двоеточие ":" и перейти на новую строку. Все последующие строки, 
с уровнем отступа большим, чем у заголовка, будут отнесены к содержимому тега.

> Желательно оформлять строки одного уровня вложенности одинаковым количеством 
отступов. Но неодинаковое тоже будет обрабатываться корректно.

    HTML
    <p>
        <i>Курсивный текст</i>
        <b>Жирный текст</b>
        Обычный текст и всего-то
    </p>
    
    Yo Struct
    p:
        i: "Курсивный текст"
        b: "Жирный текст"
        "Обычный текст", " и всего-то"

Элементы, стоящие на одной строчке, необходимо отделять запятыми. Элементы,
стоящие на разных строках отделять запятыми необязательно, так как о разделении
говорит перенос строки (подобно формату *CSV*).

При сборке html-файла элементы перечисления просто "склеиваются" как строки без
дополнительных пробелов.

## Скобочный метод группировки

Также можно выделить содержимое тега с помощью {фигурных скобок}. Все элементы,
записанные внутри скобок, будут отнесены к содержимому тега.

    HTML
    <p>
        <i>Курсивный текст</i>
        <b>Жирный текст</b>
        Обычный текст и всего-то
    </p>
    
    Yo Struct
    p {
        i: "Курсивный текст",
        b: "Жирный текст",
        "Обычный текст", " и всего-то"
    }

Внутри скобок не учитываются отступы (вообще) и переносы строк. Все элементы
в перечислениях должны отделяться запятыми.

> Преимущество этого способа над отступным в том, что можно записать любую
струткуру вообще без переносов строки, то есть, в одну строчку. Однако, запись
в одну строку не приветствуется.


    HTML
    <p><i>Так любит делать <br> javascript. Всё в одну строчку.</i></p>
    
    Yo Struct
    p { i { "Так любит делать", br, "javascript. всё в одну строчку"} }



## Однострочный метод группировки

Если внутри тега лежит всего один элемент, то два вышеописанных метода могут
быть избыточными. Для этого метода тег и содержимое должны быть написаны в 
одной строке и разделены знаком двоеточия ":".

    HTML
    <i>Курсивный текст</i>
    
    Yo Struct
    # Отступ избыточен
    i:
        "Курсивный текст"
        
    # Скобки избыточны
    i { "Курсивный текст" }
    
    # Более короткий вариант
    i: "Курсивный текст"

Данный метод накладывает ограничение на количество вложенных элементов: он
должен быть всего один.

> Зато этот метод позволяет создавать неразрастающуюся вширь цепочку вложенных
друг в друга тегов, записанных довольно компактно и читаемо

    HTML
    <p><a href="vzlom.com"><u><i>Нажми на меня!<i></a></u></p>
    
    Yo Struct
    p: a(href="vzlom.com"): u: i: "Нажми на меня!"
    
## Пустой тег

Если у тега пусто внутри, но он двойной, то стоит обозначить это пустоту.
Для скобочного метода это пустые фигурные скобки {}. Для отступного и 
однострочного метода нужно написать служебное слово *pass*

    HTML
    <i></i>
    
    Yo Struct
    # Отступной способ
    i:
        pass
    
    # Скобочный способ
    i {}
    
    # Однострочный способ
    i: pass
    
> Использование "заглушек" для пустых тегов подразумевает их последующее 
заполнение а также позволяет отличать транслятору пустые теги от одинарных.

## Корень

После всех особенностей формата нельзя не сказать о корне. Корнем является сам 
файл *.yostruct*. Он является предком всех остальных тегов, описанных в файле.

Корень - это открытое перечисление тегов, строящееся на отступном способе, но
не зависящее от них, которое закрывается в конце файла.

    Yo Struct
    # Отступы в корне файла не имеют значения
    i: "Курсивный текст"
        i: "Курсивный текст"
    i: "Курсивный текст"
    
> Необоснованное выделение отступами не приветствуется

## Пример кода

Ниже приведён пример html документа и его yo struct эквивалент.

    HTML
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Название</title>
    </head>
    <body>
    <h1>Заголовок 1</h1>
    <p>Параграф</p>
    <p>Вставка <i>курсивного текста</i> в параграф</p>
    <table>
        <thead>Какая-то таблица</thead>
        <tr>
            <td>1</td>
            <td>2</td>
            <td>3</td>
        </tr>
        <tr>
            <td>4</td>
            <td>5</td>
            <td>6</td>
        </tr>
    </table>
    <p hidden="true">Скрыто</p>
    <q>Маленькая идея</q>
    <blockquote>Большая идея</blockquote>
    </body>
    </html>
    
    Yo Struct
    html(lang="ru"):
        head:
            meta(charset="UTF-8")
            title: "Название"
        body:
            h1: "Заголовок 1"
            p: "Параграф"
            p:
                "Вставка ", i:"курсивного текста", "в параграф"
            table:
                thead: "Какая-то таблица"
                tr:
                    td: "1"
                    td: "2"
                    td: "3"
                tr:
                    td: "4"
                    td: "5"
                    td: "6"
            q: "Маленькая идея"
            blockquote: "Большая идея"
            
Как видно, разница очевидна.

## Ограничения

### Теги в атрибутах

Наиболее существенным ограничением является невозможность записывать новые теги
в качестве атрибутов тега.

    Yo Struct
    # Так нельзя!
    a(href=i():"vzlom.com"): "Ссылка"
    
    # Так можно
    a(href="vzlom.com"): "Ссылка"
    
Теги должны объявляться строго в разделе содержимого.

### Однострочные теги

Нельзя записывать отступные и скобочные теги внутри однострочных. Необходимо
преобразовать однострочный тег в отступной или скобочный.

    Yo Struct
    # Так нельзя!
    p: i:
        "Курсивный текст"
    
    p: i {"Курсивный текст"}
    
    # Так можно
    p: i: "Курсивный текст"
    
    p:
        i:
            "Курсивный текст"
    
    p { i {"Курсивный текст"} }
            
Внутри однострочных тегов могут быть записаны только однострочные теги или 
контент.

### Вложенные теги

Внутри скобочных тегов не могут храниться отступные теги. Отступные теги
следует преобразовать в скобочные теги, либо скобочный тег следует преобразовать
в отступной.

    Yo Struct
    # Так нельзя!
    p {
        i:
            "Курсивный текст"
    }
    
    # Так можно
    p {
        i { "Курсивный текст" }
    }
    
    p:
        i:
            "Курсивный текст"
    

Внутри отступных тегов не могут храниться скобочные теги. Скобочные теги
следует преобразовать в отступные, либо отступной тег следует преобразовать 
в скобочный.

    Yo Struct
    # Так нельзя!
    p:
        i {
            "Курсивный текст"
        }
    
    # Так можно
    p {
        i { "Курсивный текст" }
    }
    
    p:
        i:
            "Курсивный текст"
            
> Отступы и фигурные скобки - смешать, но взбалтывать. 

Корень может хранить и отступные и скобочные теги сразу.

### Комментарии

Комментарий с точки зрения html - тоже тег. Поэтому его применение ограничено
такими же правилами, как и для тегов.

Комментарий не может лежать внутри однострочного тега (серьёзно, вы создавали 
тег из одного элемента, чтобы положить туда... комментарий?)

    Yo Struct
    # Так нельзя!
    p: # Комментарий
    
    # Так можно
    p:
        # Комментарий
        
Применение комментариев в скобочных тегах ограничено. После элемента-комментария
не нужно ставить запятую - она всё равно не обработается. Достаточно просто
перейти на новую строку.

    Yo Struct
    p {
        # Пушкин
        "Я памятник себе воздвиг нерукотворный,",
        "К нему не зарастёт народная тропа."
    }

### Особые значения

*Yo Struct* резервирует за собой пока только одно имя для тегов. Теги с таким
именем могут обрабатываться неправильно:

    pass
    
### Суть та же

Также стоит заметить, что *Yo Struct* не предлагает никаких новых тегов и
атрибутов, а только предоставляет возможность более удобной, короткой и читаемой
записи тех же самых тегов и атрибутов *HTML*. Все вопросы по работоспособности
написанного кода автоматически переадресовываются к стандартам *HTML*. 

# Потенциальные возможности

## Поддержка разных типов

Помимо строк и true значения, *Yo Struct* должен поддерживать основные типы 
данных json:
1. Логические величины (true, false)
2. Числа: целые и вещественные (10, 3.14)
3. Пустое значение (none)

Это приближает *Yo Struct* по возможностям к *XML*, *JSON* и прочим языкам 
разметки

## Поддержка словарей

Данная проблема неприменима к html, но актуальна для структуры в целом.
Поддержка словарей позволяет хранить и искать значения по ключу.

    Yo Struct v2
    dictionary:
        "key1": "value1"
        "key2": "value2"
        "key3": "value3"
        "key4":
            "key1": "value4"
            "key2": "value5"
        "value6"
        "value7"

Словари могут быть вложены друг в друга, а также хранить смешанные значения,
то есть как нумерованные (элементы списка), так и именованые (элементы словаря)

## Вычисления на ходу

После возможного встраивания *Yo Struct* в синтаксис языка *Yo* будет добавлена
возможность вычислять какие-то величины и объекты прямо в коде структуры. Для
этого кусок кода надо будет заключить в дополнительные (круглые скобки)

    Yo Struct in Yo
    struct square_roots:
        1: 1
        2: (sqrt(2))
        3: (sqrt(3))
        4: 2

Внутри круглых скобок можно будет использовать выражения с названиями переменных
и вызовами функций.

# Короче говоря

> Не интрумент, а сказка

>(Павел Соломатин)

Penza Street Company © Все права защищены.