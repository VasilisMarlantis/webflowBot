import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def rephrase_text(text):
    # Load model and tokenizer
    model_name = "t5-base"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Tokenize input text
    input_ids = tokenizer.encode("Rephrase: " + text, return_tensors="pt")

    # Generate rephrased text
    output = model.generate(input_ids, max_length=200)

    # Decode rephrased text
    rephrased_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return rephrased_text

# Test the function
text = "Children’s Day is just around the corner on 1 June. For the special occasion, fast-food chains are, as usual, levelling up their toy game. However, in recent years, toys have increasingly been designed not so much for children but more for young adults, combining playability with practicality, putting the fun back in functionality, so to speak. The KFC x Sanrio collaboration is a prime example of this Children’s Day."
rephrased_text = rephrase_text(text)

print("Rephrased Text:")
print(rephrased_text)
