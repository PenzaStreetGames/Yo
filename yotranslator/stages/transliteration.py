def transliterate(yolp, word, lang_current, lang_need):
    if lang_current == lang_need:
        return word

    if lang_current == "en":
        return yolp[word][lang_need]

    for dict_word, dict_value in yolp.items():
        if dict_value[lang_current] == word:
            return dict_word if lang_need == "en" else dict_value[lang_need]

    return word
