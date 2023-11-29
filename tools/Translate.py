from googletrans import Translator
import httpcore
setattr(httpcore, 'SyncHTTPTransport', 'AsyncHTTPProxy')
def translate_text(text, target_language):
    translator = Translator()
    try:
        # Translate the text to the desired language
        translation = translator.translate(text, dest=target_language)

        # Print the original and translated text
        # print(f"Original text ({translation.src}): {text}")
        # print(f"Translated text ({target_language}): {translation.text}")

        return translation.text

    except Exception as e:
        print(f"Translation error: {e}")
        return None
    
def TranslatorTool(text: str, target_language: str) -> str:
    """Useful to translate text to a different language
    :param text: text to translate
    :param target_language: language to translate to
    :returns: translated text
    """
    ans = translate_text(text, target_language)
    return ans