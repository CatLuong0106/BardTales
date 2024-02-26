import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

torch.set_default_device("cuda")

model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype="auto", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)

input =  """
Use this template: 

Reflective Melody: Contemplative, introspective, melodic, soul-stirring
Narrative Journey: Evocative storytelling, lyrical narration, emotional depth
Diverging Paths: Choices, crossroads, uncertainty, branching possibilities
Nature's Embrace: Woodsy ambiance, rustling leaves, whispered breezes
Exploration: Curiosity, discovery, venturing into the unknown
Echoes of Decision: Regret, determination, acceptance, the weight of choices
The Road Less Traveled: Adventure, risk-taking, forging one's own path
Legacy of Choices: Impact, consequence, the ripple effect of decisions

Make a similar prompt for an audio that encapsulates the content of this text: 

Two roads diverged in a yellow wood,
And sorry I could not travel both
And be one traveler, long I stood
And looked down one as far as I could
To where it bent in the undergrowth;

Then took the other, as just as fair,
And having perhaps the better claim,
Because it was grassy and wanted wear;
Though as for that the passing there
Had worn them really about the same,

And both that morning equally lay
In leaves no step had trodden black.
Oh, I kept the first for another day!
Yet knowing how way leads on to way,
I doubted if I should ever come back.

I shall be telling this with a sigh
Somewhere ages and ages hence:
Two roads diverged in a wood, and I—
I took the one less traveled by,
And that has made all the difference.
"""

inputs = tokenizer(input, return_tensors="pt", return_attention_mask=False)

outputs = model.generate(**inputs, max_length=400)
text = tokenizer.batch_decode(outputs)[0]
print(text)

