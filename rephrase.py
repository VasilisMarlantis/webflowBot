from transformers import T5Tokenizer, T5ForConditionalGeneration

model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

text = "Rephrase this sentence for clarity."
input_text = f"paraphrase: {text} </s>"

input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

outputs = model.generate(
    input_ids=input_ids,
    max_length=64,
    do_sample=True,
    top_k=50,
    top_p=0.95,
    temperature=0.9,
    num_return_sequences=1
)

rephrased = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("Original:", text)
print("Rephrased:", rephrased)
print("DEBUG TYPE:", type(rephrased), "VALUE:", repr(rephrased))
