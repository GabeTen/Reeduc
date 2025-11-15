FIELD_TRANSLATIONS = {
    "students": "estudantes",
    "publications": "publicacoes",
    "title": "titulo",
    "description": "descricao",
    "status": "status",
    "link": "link",
    "email": "e-mail",
    "username": "nome de usuário",
    # adicione outros conforme necessário
}

def translate_form_errors(errors_dict):
    translated = {}

    for field, messages in errors_dict.items():
        new_field = FIELD_TRANSLATIONS.get(field, field)
        translated[new_field] = messages

    return translated