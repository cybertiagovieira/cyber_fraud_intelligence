import argostranslate.package
import argostranslate.translate
import os

def setup_language_packs():
    """Downloads language packs locally on first run. Requires internet for this step only."""
    print("Updating offline translation package index...")
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    
    # We need Russian -> English and Portuguese -> English
    target_pairs = [("ru", "en"), ("pt", "en")]
    
    for from_lang, to_lang in target_pairs:
        package = next(
            filter(lambda x: x.from_code == from_lang and x.to_code == to_lang, available_packages), 
            None
        )
        if package:
            print(f"Installing offline pack: {from_lang} -> {to_lang}...")
            argostranslate.package.install_from_path(package.download())
    print("Translation engine ready.")

def translate_local(text, from_lang="ru"):
    """Translates text entirely offline."""
    if not text:
        return ""
    try:
        return argostranslate.translate.translate(text, from_lang, "en")
    except Exception as e:
        print(f"Translation failed: {e}")
        return text

if __name__ == "__main__":
    # Run this file directly once to download the language packs
    setup_language_packs()
    print(translate_local("Привет, это тест системы.", "ru"))