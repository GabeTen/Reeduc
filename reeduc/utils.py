def get_form_errors_as_json(form):
    """Converte os erros do Django form em um dicionário JSON amigável."""
    errors = {}
    for field, error_list in form.errors.items():
        # "__all__" representa erros gerais do formulário (não ligados a um campo específico)
        if field == "__all__":
            errors["geral"] = error_list.as_text().replace("* ", "").split("\n")
        else:
            errors[field] = error_list.as_text().replace("* ", "").split("\n")
    return errors
