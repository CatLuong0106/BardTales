import pydub
import os
import sys
import json
import google.generativeai as genai
import os
from audiocraft.models import MAGNeT
from audiocraft.utils.notebook import display_audio
from audiocraft.data.audio import audio_write
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing

def llm(prompt: str) -> str: 
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
    model = genai.GenerativeModel("gemini", generation_config=generation_config)
    response = model.generate_content([prompt])
    print(response.text)
    return response.text

def text_to_speech(input_path: str) -> None:
    # Assuming your JSON file is named 'data.json'
    file_path = 'credentials.json'

    # Open the JSON file and load its contents
    with open(file_path, 'r') as file:
        credentials = json.load(file)

    # Create a client using the credentials and region defined in the [adminuser]
    # section of the AWS credentials file (~/.aws/credentials).
    # session = Session(profile_name="adminuser")
    session = Session(
        aws_access_key_id=credentials['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=credentials['AWS_SECRET_ACCESS_KEY'],
        # aws_session_token=credentials['AWS_SESSION_TOKEN'],  # if using temporary credentials
        region_name=credentials['AWS_DEFAULT_REGION'],
    )
    polly = session.client("polly")

    with open(input_path, 'r', encoding='utf-8') as file: 
        content = file.read()

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(
            Text=str(content), OutputFormat="mp3", VoiceId="Salli"
        )
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            # output = os.path.join(gettempdir(), "speech.mp3")
            output = os.path.join(".", "speech.wav")

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)

def music_gen(prompt: str) -> None:
    model = MAGNeT.get_pretrained("facebook/magnet-small-10secs")

    model.set_generation_params(
        use_sampling=True,
        top_k=0,
        top_p=0.9,
        temperature=3.0,
        max_cfg_coef=10.0,
        min_cfg_coef=1.0,
        decoding_steps=[
            int(20 * model.lm.cfg.dataset.segment_duration // 10),
            10,
            10,
            10,
        ],
        span_arrangement="stride1",
    )

    ###### Text-to-music prompts - examples ######
    # text =  """
    #         Reflective Melody: Contemplative, introspective, melodic, soul-stirring
    #         Narrative Journey: Evocative storytelling, lyrical narration, emotional depth
    #         Diverging Paths: Choices, crossroads, uncertainty, branching possibilities
    #         Nature's Embrace: Woodsy ambiance, rustling leaves, whispered breezes
    #         Exploration: Curiosity, discovery, venturing into the unknown
    #         Echoes of Decision: Regret, determination, acceptance, the weight of choices
    #         The Road Less Traveled: Adventure, risk-taking, forging one's own path
    #         Legacy of Choices: Impact, consequence, the ripple effect of decisions
    #         """

    # text = "80s electronic track with melodic synthesizers, catchy beat and groovy bass. 170 bpm"
    # text = "Earthy tones, environmentally conscious, ukulele-infused, harmonic, breezy, easygoing, organic instrumentation, gentle grooves"
    # text = "Funky groove with electric piano playing blue chords rhythmically"
    # text = "Rock with saturated guitars, a heavy bass line and crazy drum break and fills."
    # text = "A grand orchestral arrangement with thunderous percussion, epic brass fanfares, and soaring strings, creating a cinematic atmosphere fit for a heroic battle"

    N_VARIATIONS = 1
    descriptions = [prompt for _ in range(N_VARIATIONS)]

    print(f"text prompt: {prompt}\n")
    output = model.generate(
        descriptions=descriptions, progress=True, return_tokens=True
    )
    # display_audio(output[0], sample_rate=model.compression_model.sample_rate)
    for idx, one_wav in enumerate(output[0]):
        # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
        audio_write(f'background', one_wav.cpu(), model.sample_rate, strategy="loudness")


def audio_gen() -> None: 
    model = MAGNeT.get_pretrained("facebook/audio-magnet-small")

    model.set_generation_params(
        use_sampling=True,
        top_k=0,
        top_p=0.8,
        temperature=3.5,
        max_cfg_coef=20.0,
        min_cfg_coef=1.0,
        decoding_steps=[
            int(20 * model.lm.cfg.dataset.segment_duration // 10),
            10,
            10,
            10,
        ],
        span_arrangement="stride1",
    )

    ###### Text-to-audio prompts - examples ######
    text = "Seagulls squawking as ocean waves crash while wind blows heavily into a microphone."
    # text = "A toilet flushing as music is playing and a man is singing in the distance."

    N_VARIATIONS = 3
    descriptions = [text for _ in range(N_VARIATIONS)]

    print(f"text prompt: {text}\n")
    output = model.generate(
        descriptions=descriptions, progress=True, return_tokens=True
    )
    display_audio(output[0], sample_rate=model.compression_model.sample_rate)

def combine() -> None: 
    # Load the audio files
    background_audio = pydub.AudioSegment.from_file("background.wav")
    narration_audio = pydub.AudioSegment.from_file("speech.wav")
    background_audio = background_audio - 6
    narration_audio = narration_audio + 4

    # Calculate the number of times to repeat the background audio to match the duration of the narration
    num_repeats = int(narration_audio.duration_seconds / background_audio.duration_seconds) + 1

    # Extend the background audio by concatenating it multiple times
    background_audio = background_audio * num_repeats

    # Mix the two audio files together
    mixed_audio = background_audio.overlay(narration_audio)

    # Export the mixed audio file
    mixed_audio.export("mixed.wav", format="wav")

def main():
    prompt = """
    Use this template: 

    Grandeur: Majestic, grand, monumental, heroic
    Orchestral: Symphonic, lush, rich, full-bodied
    Intensity: Powerful, dramatic, intense, thrilling
    Emotion: Emotional, poignant, moving, stirring
    Epic Scale: Massiv, expansive, vast, larger-than-life
    Dynamic Range: Dynamic, constrast, crescendos, swells
    Chorus: Choral, choir, vocal, harmonies 
    Percussion: Percussive, driving, rhythmic, thunderous
    Melodic Themes: Memorable, catchy, thematic, motifs
    Building Tension: Suspenseful, building, climactic, anticipation
    Cinematic Sound Design: Textured, atmospheric, immersive, soundscapes
    Instrumentation: Bass, strings, woodwinds, percussion, synthesizers
    Momentum: Energetic, propulsive, relentless, pulse sounding
    Imagery: Evocative, visual, picturesque, storytelling
    Heroic Journey: Triumph, resolve, determination, perserverance

    Make a similar prompt but not exactly for an audio that encapsulates the content of this text: 

    """
    text_file_path = "input.txt"
    with open(text_file_path, "r", encoding='utf-8') as f:
        text = f.read()
    prompt = prompt + text
    # prompt = """
    # A musical composition that captures the essence of making a choice at a crossroad in a yellow wood. 
    # The piece begins with a soft and reflective melody that represents the contemplation and introspection of the narrator. 
    # The melody then splits into two contrasting themes, each representing a different path. 
    # One theme is more upbeat and adventurous, while the other is more calm and familiar. 
    # The themes alternate and intertwine, creating a sense of curiosity and exploration. 
    # The piece then reaches a climax, where the narrator has to make a decision. 
    # The music becomes tense and dramatic, as the narrator weighs the pros and cons of each path.
    # The music then resolves into a single theme, the one that the narrator chose. 
    # The theme is played with confidence and determination, but also with a hint of regret and acceptance for the path not taken. 
    # The piece ends with a gentle echo of the other theme, suggesting the lasting impact of the choice and the possibility of what could have been. 
    # """
    text_to_speech(text_file_path)
    music_gen(llm(prompt))
    combine()

if __name__ == "__main__": 
    main()