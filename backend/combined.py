import pydub

def combine(): 
    # Load the audio files
    background_audio = pydub.AudioSegment.from_file("background.wav")
    narration_audio = pydub.AudioSegment.from_file("speech.wav")
    background_audio = background_audio - 4
    narration_audio = narration_audio + 2

    # Calculate the number of times to repeat the background audio to match the duration of the narration
    num_repeats = int(narration_audio.duration_seconds / background_audio.duration_seconds) + 1

    # Extend the background audio by concatenating it multiple times
    background_audio = background_audio * num_repeats

    # Adjust the length of the narration audio to match the length of the background audio
    # if narration_audio.duration_seconds < background_audio.duration_seconds:
    #     narration_audio = narration_audio.append(pydub.AudioSegment.silent(duration=background_audio.duration_seconds - narration_audio.duration_seconds))

    # Mix the two audio files together
    mixed_audio = background_audio.overlay(narration_audio)

    # Export the mixed audio file
    mixed_audio.export("mixed.wav", format="wav")

if __name__ == "__main__": 
    combine()