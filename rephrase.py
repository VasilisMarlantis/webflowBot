from transformers import T5ForConditionalGeneration, T5Tokenizer

model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# ✅ Text to rephrase
text = "Rephrase this sentence for clarity."

# ✅ Format input properly (no manual </s>)
input_text = f"paraphrase: {text}"
input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

# ✅ Generate output
outputs = model.generate(
    input_ids,
    max_length=128,
    num_beams=5,
    early_stopping=True,
    num_return_sequences=1,
)

# ✅ Decode properly
rephrased = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("Original: ", text)
print("Rephrased:", rephrased)

