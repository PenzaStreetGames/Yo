
def transliterate(word, lang_current, lang_need):

    languages = ["en", "ru"]

    if languages.count(lang_current) + languages.count(lang_need) < 2:
        return word

    with open("../yotransliteration/translations.txt", "r", encoding="utf8") as file:
        data = list(map(lambda el: el.split(), file.readlines()))

    selection = list(list(zip(*data))[languages.index(lang_current)])
    if not word in selection:
        return word
    word_index = selection.index(word)

    return data[word_index][languages.index(lang_need)]


