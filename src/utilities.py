def format_to_plain_text(info_dict):
    """
    Formatea el diccionario de información en un texto plano con saltos de línea adecuados.

    Args:
        info_dict (dict): Diccionario que contiene la información sobre la respuesta.

    Returns:
        str: Texto plano con la información formateada.
    """
    formatted_text = ""

    # Append the Title
    formatted_text += f"\n\nTitle: {info_dict['Title']}\n\n"

    # Append the Introduction
    formatted_text += f"Introduction:\n{info_dict['Introduction']}\n\n"

    # Append the Answer
    formatted_text += f"Answer:\n{info_dict['Answer']}\n\n"

    # Append the Conclusion
    formatted_text += f"Conclusion:\n{info_dict['Conclusion']}\n\n"

    # Append the Related Questions
    formatted_text += "Related Questions:\n"
    related_questions = info_dict['Related Questions'].strip().split('?')
    for question in related_questions:
        if question:
            formatted_text += f"- {question.strip()}?\n"

    return formatted_text