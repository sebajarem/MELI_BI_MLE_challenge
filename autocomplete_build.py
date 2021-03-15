import autocompleter
import sys


def build():
    """
    compilacion del Autocompletado
    """
    my_autocompleter = autocompleter.Autocompleter()
    my_autocompleter.import_json("sample_conversations.json")
    my_autocompleter.prepros_text() # preprocesamiento de texto
    my_autocompleter.sentence_similarity() # modelo de similaridad entre oraciones
    my_autocompleter.save()

if __name__ == "__main__":
    sys.exit(build())
