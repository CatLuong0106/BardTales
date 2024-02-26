from audiocraft.models import MAGNeT
from audiocraft.utils.notebook import display_audio
from audiocraft.data.audio import audio_write
def music_gen():
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
    text = """
        A musical composition that captures the essence of making a choice at a crossroad in a yellow wood. The piece begins with a soft and reflective melody that represents the contemplation and introspection of the narrator. The melody then splits into two contrasting themes, each representing a different path. One theme is more upbeat and adventurous, while the other is more calm and familiar. The themes alternate and intertwine, creating a sense of curiosity and exploration. The piece then reaches a climax, where the narrator has to make a decision. The music becomes tense and dramatic, as the narrator weighs the pros and cons of each path. The music then resolves into a single theme, the one that the narrator chose. The theme is played with confidence and determination, but also with a hint of regret and acceptance for the path not taken. The piece ends with a gentle echo of the other theme, suggesting the lasting impact of the choice and the possibility of what could have been.
    """
    # text = "80s electronic track with melodic synthesizers, catchy beat and groovy bass. 170 bpm"
    # text = "Earthy tones, environmentally conscious, ukulele-infused, harmonic, breezy, easygoing, organic instrumentation, gentle grooves"
    # text = "Funky groove with electric piano playing blue chords rhythmically"
    # text = "Rock with saturated guitars, a heavy bass line and crazy drum break and fills."
    # text = "A grand orchestral arrangement with thunderous percussion, epic brass fanfares, and soaring strings, creating a cinematic atmosphere fit for a heroic battle"

    N_VARIATIONS = 1
    descriptions = [text for _ in range(N_VARIATIONS)]

    print(f"text prompt: {text}\n")
    output = model.generate(
        descriptions=descriptions, progress=True, return_tokens=True
    )
    display_audio(output[0], sample_rate=model.compression_model.sample_rate)
    for idx, one_wav in enumerate(output[0]):
        # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
        audio_write(f'{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness")


def audio_gen():
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


def main():
    # audio_gen()
    music_gen()


if __name__ == "__main__":
    main()
