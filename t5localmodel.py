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
    output = model.generate(input_ids, max_length=100)

    # Decode rephrased text
    rephrased_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return rephrased_text

# Test the function
text = "This is a sample text that needs to be rephrased."
rephrased_text = rephrase_text(text)

print("Rephrased text:", rephrased_text)
