from transformers import T5ForConditionalGeneration, T5Tokenizer

model_name = "t5-small"  # You can use t5-base or another local model

tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

text = "Rephrase this sentence for clarity."
input_text = "paraphrase: " + text + " </s>"

input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

outputs = model.generate(
    input_ids,
    max_length=128,
    num_beams=5,
    early_stopping=True
)

rephrased = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Rephrased:", rephrased)

