from deep_translator import GoogleTranslator,exceptions

languages = {
    "Bengali": "bn",
    "Chinese": "zh-CN",
    "Dutch": "nl",
    "English": "en",
    "Finnish": "fi",
    "French": "fr",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Hindi": "hi",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Latin": "la",
    "Malay": "ms",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Nepali": "ne",
    "Punjabi": "pa",
    "Russian": "ru",
    "Spanish": "es",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
}  
def translate(text, target_lang, source_lang="English"):
    try:
        if not text or target_lang.lower() == source_lang.lower():
            return text
            
        source_code = languages.get(source_lang, "en")
        target_code = languages.get(target_lang, "en")
        
        if not source_code or not target_code:
            return text
            
        return GoogleTranslator(source=source_code, target=target_code).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text