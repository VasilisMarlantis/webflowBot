from transformers import T5Tokenizer, T5ForConditionalGeneration

model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

text = "Rephrase this sentence for clarity."

# Prefix with paraphrase task
input_text = f"paraphrase: {text}"
input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

# Generate output
outputs = model.generate(
    input_ids=input_ids,
    max_length=64,
    num_beams=5,
    early_stopping=True
)

# Decode result
rephrased = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Print correctly
print("Original:", text)
print("Rephrased:", rephrased)
print("DEBUG TYPE:", type(rephrased), "VALUE:", repr(rephrased))

