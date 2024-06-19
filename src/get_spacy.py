import spacy

def get_spacy_answer(text):
    """
    Функция для извлечения именованных сущностей из текста и возврата полного текста с отметками.

    :param text: строка, содержащая текст для анализа
    :return: кортеж из двух элементов: список именованных сущностей и текст с отметками
    """
    # загрузка обученной модели
    nlp_NER = spacy.load('models\spaCy')

    # получаем список ИС
    doc = nlp_NER(text)

    # создание текста с отметками и подчеркиванием
    marked_text = text
    offset = 0
    for ent in doc.ents:
        start = ent.start_char + offset
        end = ent.end_char + offset
        entity = f"_{ent.text}_ <{ent.label_}>"
        marked_text = marked_text[:start] + entity + marked_text[end:]
        offset += len(entity) - (end - start)

    return marked_text