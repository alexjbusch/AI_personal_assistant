import wikipedia
def Text(query):
    try:
        wiki = wikipedia.page(query, auto_suggest=False)
        text = wiki.content
        return text.split(". ")[0]

    except wikipedia.DisambiguationError as e:
        return f"did you mean {e.options[0]} or {e.options[1]}?"
