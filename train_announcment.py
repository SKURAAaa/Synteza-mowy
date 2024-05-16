from pydub import AudioSegment
from playsound import playsound
import os
import unidecode
import re

def normalize_phrase(phrase):
    """
    Normalizuje frazę do postaci bez polskich znaków, małymi literami i bez interpunkcji
    """
    phrase = re.sub(r'[^\w\s]', '', phrase)  # Usuń interpunkcję
    return unidecode.unidecode(phrase).lower()  # Usuń polskie znaki i zamień na małe litery

def find_audio_file(directory, phrase):
    """
    Znajduje plik audio odpowiadający danej frazie w określonym katalogu
    """
    normalized_phrase = normalize_phrase(phrase)
    print(f"Normalizowana fraza: {normalized_phrase}")  # Debugowanie
    for filename in os.listdir(directory):
        normalized_filename = normalize_phrase(filename)
        print(f"Sprawdzanie pliku: {filename} (znormalizowany: {normalized_filename})")  # Debugowanie
        if normalized_phrase in normalized_filename:
            print(f"Znaleziono plik: {filename}")  # Debugowanie
            return os.path.join(directory, filename)
    return None

def synthesize_speech(text):
    """
    Syntetyzuje mowę na podstawie wprowadzonego tekstu
    """
    base_dir = "C:\\Users\\Kacper\\PycharmProjects\\Synteza_mowy"
    stacje_dir = os.path.join(base_dir, "stacje")
    perony_i_tory_dir = os.path.join(base_dir, "perony_i_tory")
    do_z_stacji_dir = os.path.join(base_dir, "do_z_stacji")

    # Usuwamy przecinki i dzielimy tekst na frazy
    phrases = re.split(r',|\s', text)
    phrases = [phrase.strip() for phrase in phrases if phrase.strip()]  # Usuń puste frazy i zbędne spacje
    audio_segments = []

    i = 0
    while i < len(phrases):
        phrase = phrases[i]
        audio_file = None
        print(f"Przetwarzanie frazy: {phrase}")  # Debugowanie

        # Jeśli fraza zawiera "stacji" lub "przez", spróbuj znaleźć skomponowaną frazę
        if "stacji" in phrase or "przez" in phrase:
            if i + 1 < len(phrases):
                combined_phrase = f"{phrase} {phrases[i + 1]}"
                audio_file = find_audio_file(stacje_dir, combined_phrase)
                if audio_file:
                    audio_segments.append(AudioSegment.from_file(audio_file))
                    print(f"Dodano frazę: {combined_phrase}")  # Debugowanie
                    i += 2  # Pomiń następną frazę, ponieważ była użyta w kombinacji
                    continue

            # Jeśli nie znaleziono skomponowanej frazy, spróbuj znaleźć pojedynczą frazę
            audio_file = find_audio_file(stacje_dir, phrase)
        elif "peronie" in phrase or "toru" in phrase:
            audio_file = find_audio_file(perony_i_tory_dir, phrase)
        else:
            audio_file = find_audio_file(do_z_stacji_dir, phrase)

        if audio_file:
            audio_segments.append(AudioSegment.from_file(audio_file))
            print(f"Dodano frazę: {phrase}")  # Debugowanie
        else:
            print(f"Nie znaleziono pliku dla frazy: {phrase}")

        i += 1

    if audio_segments:
        # Połącz wszystkie segmenty audio w jeden plik
        combined = audio_segments[0]
        for segment in audio_segments[1:]:
            combined += segment

        # Zapisz wynikowy plik audio
        output_file = os.path.join(base_dir, "wynik.wav")
        combined.export(output_file, format="wav")
        print(f"Plik wynikowy zapisany jako: {output_file}")

        # Odtwórz plik za pomocą playsound
        playsound(output_file)
    else:
        print("Brak odpowiednich nagrań do syntezy.")

if __name__ == "__main__":
    text = input("Wpisz tekst: ")
    synthesize_speech(text)
