from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load pre-trained T5 model and tokenizer
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Input sentence to rephrase
text = "Rephrase this sentence for clarity."

# Format for T5 rephrasing
input_text = "paraphrase: " + text + " </s>"
input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

# Generate rephrased text
outputs = model.generate(
    input_ids,
    max_length=128,
    num_beams=5,
    early_stopping=True
)

# Decode and print the result
rephrased = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Original: ", text)
print("Rephrased:", rephrased)

