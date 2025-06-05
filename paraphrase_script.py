import sys
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Define the model name
MODEL_NAME = "prithivida/parrot_paraphraser_on_T5"

def paraphrase_text(input_text):
    """
    Loads the Parrot Paraphraser model based on T5 and paraphrases the input text.

    Args:
        input_text (str): The text to be paraphrased.

    Returns:
        str: The paraphrased text.
    """
    try:
        # Load tokenizer and model
        print(f"Loading tokenizer from {MODEL_NAME}...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        print(f"Loading model from {MODEL_NAME}...")
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

        # Check for GPU and move model if available
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        print(f"Using device: {device}")

        # Encode the input text
        # The T5 model expects a specific format, often prepended with a task prefix.
        # For general paraphrasing, simply encoding the text should work, but
        # for specific T5 fine-tunes, a prefix like "paraphrase: " might be needed.
        # Let's try without a specific prefix first.
        input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)

        # Generate paraphrased output
        # max_length: maximum length of the generated output
        # num_beams: number of beams for beam search (higher means better quality but slower)
        # early_stopping: stop beam search when all beams are finished
        # Temperature and top_k/top_p can be tuned for creativity vs. coherence
        outputs = model.generate(
            input_ids,
            max_length=60, # Adjust as needed for desired output length
            num_beams=5,
            early_stopping=True,
            temperature=1.0, # Controls randomness
            top_k=50,       # Limits vocabulary to top k
            top_p=0.95      # Nucleus sampling
        )

        # Decode the generated output back to text
        paraphrased_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return paraphrased_output

    except Exception as e:
        print(f"An error occurred during paraphrasing: {e}")
        return "Error: Could not paraphrase text."

if __name__ == "__main__":
    # Get input text from command line arguments
    # Expects the text as the first argument after the script name
    if len(sys.argv) > 1:
        text_to_paraphrase = sys.argv[1]
        print(f"Input text: '{text_to_paraphrase}'")
        result = paraphrase_text(text_to_paraphrase)
        print(f"Paraphrased text: '{result}'")
    else:
        print("Usage: python paraphrase_script.py 'Your text to paraphrase'")
        print("Example: python paraphrase_script.py 'The quick brown fox jumps over the lazy dog.'")

