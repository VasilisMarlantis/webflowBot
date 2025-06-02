from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("google-t5/t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google-t5/t5-base")

input_text = "Rihanna’s Fenty Beauty opens first Mainland China concept store."
inputs = tokenizer(input_text, return_tensors="pt")

output_ids = model.generate(**inputs, max_length=256)
paraphrased_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print(paraphrased_text)

