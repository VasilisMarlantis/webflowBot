from transformers import T5Tokenizer, T5ForConditionalGeneration

model_name = "google-t5/t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Input text to paraphrase
input_text = "paraphrase: The quick brown fox jumps over the lazy dog."

# Tokenize
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# Generate
outputs = model.generate(input_ids, max_length=64, num_return_sequences=1, do_sample=True, top_k=50, top_p=0.95)

# Decode
paraphrased = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Paraphrased:", paraphrased)
