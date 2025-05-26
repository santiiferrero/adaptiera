def sanitize_input(text):
    return text.strip().replace("<", "").replace(">", "")
