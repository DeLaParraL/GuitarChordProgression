import random
from typing import List, Tuple, Dict


# We use sharps only to keep the note spelling simple for v1.
NOTES: List[str] = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Scale patterns as semitone offsets from the root note.
MAJOR_OFFSETS: List[int] = [0, 2, 4, 5, 7, 9, 11]
MINOR_OFFSETS: List[int] = [0, 2, 3, 5, 7, 8, 10]  # natural minor

# Chord qualities for each scale degree 1 to 7.
# "maj" means plain major chord, "min" means minor chord, "dim" means diminished.
MAJOR_QUALITIES: List[str] = ["maj", "min", "min", "maj", "maj", "min", "dim"]
MINOR_QUALITIES: List[str] = ["min", "dim", "maj", "min", "min", "maj", "maj"]

# Progression templates:
# Each entry is (roman_numerals, degree_numbers)
# Degree numbers are 1 to 7 where 1 means the tonic chord of the key.
MAJOR_PROGRESSIONS: List[Tuple[List[str], List[int]]] = [
    (["I", "V", "vi", "IV"], [1, 5, 6, 4]),
    (["I", "vi", "IV", "V"], [1, 6, 4, 5]),
    (["vi", "IV", "I", "V"], [6, 4, 1, 5]),
    (["I", "IV", "V", "I"], [1, 4, 5, 1]),
]

MINOR_PROGRESSIONS: List[Tuple[List[str], List[int]]] = [
    (["i", "VI", "III", "VII"], [1, 6, 3, 7]),
    (["i", "iv", "v", "i"], [1, 4, 5, 1]),
    (["i", "VII", "VI", "VII"], [1, 7, 6, 7]),
    (["i", "VI", "VII", "i"], [1, 6, 7, 1]),
]


def pick_key_and_mode() -> Tuple[str, str]:
    """
    Randomly pick a root note and a mode.
    Returns (root_note, mode) where mode is "major" or "minor".
    """
    root = random.choice(NOTES)
    mode = random.choice(["major", "minor"])
    return root, mode


def build_scale(root: str, mode: str) -> List[str]:
    """
    Build the 7 note scale for the given root and mode.
    We do this by:
      1) finding the index of the root note in NOTES
      2) adding each offset and wrapping around with modulo 12
    """
    root_index = NOTES.index(root)

    offsets = MAJOR_OFFSETS if mode == "major" else MINOR_OFFSETS
    scale: List[str] = []

    for semitone_offset in offsets:
        note_index = (root_index + semitone_offset) % len(NOTES)
        scale.append(NOTES[note_index])

    return scale


def chord_name(root_note: str, quality: str) -> str:
    """
    Convert a root note and quality into a printable chord name.
    "maj" becomes just the note name (C)
    "min" becomes note + m (Am)
    "dim" becomes note + dim (Bdim)
    """
    if quality == "maj":
        return root_note
    if quality == "min":
        return f"{root_note}m"
    if quality == "dim":
        return f"{root_note}dim"

    # Fallback in case something unexpected happens.
    return root_note


def degree_to_chord(scale: List[str], degree: int, mode: str) -> str:
    """
    Convert a scale degree (1 to 7) into the correct chord name for the mode.
    Example in C major:
      degree 2 is Dm because major key degree 2 quality is "min".
    """
    if degree < 1 or degree > 7:
        raise ValueError("Degree must be between 1 and 7")

    qualities = MAJOR_QUALITIES if mode == "major" else MINOR_QUALITIES

    scale_index = degree - 1
    root_note = scale[scale_index]
    quality = qualities[scale_index]

    return chord_name(root_note, quality)


def pick_progression(mode: str) -> Tuple[List[str], List[int]]:
    """
    Choose a progression template based on mode.
    Returns (roman_numerals, degree_numbers).
    """
    if mode == "major":
        return random.choice(MAJOR_PROGRESSIONS)
    return random.choice(MINOR_PROGRESSIONS)


def generate_progression() -> None:
    """
    Orchestrates the full flow:
      pick key and mode
      build scale
      pick a progression template
      translate degrees into chord names
      print output
    """
    root, mode = pick_key_and_mode()
    scale = build_scale(root, mode)

    roman, degrees = pick_progression(mode)
    chords: List[str] = [degree_to_chord(scale, d, mode) for d in degrees]

    print("Random Chord Progression Generator")
    print(f"Key: {root} {mode}")
    print(f"Progression: {' '.join(roman)}")
    print(f"Chords: {' '.join(chords)}")
    print("Tip: Try 4 beats per chord.")


def main() -> None:
    generate_progression()


if __name__ == "__main__":
    main()