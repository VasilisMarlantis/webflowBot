import os
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

# Configuration - Change these if needed
MODEL_REPO = "TheBloke/Meta-Llama-3-8B-GGUF"
MODEL_FILE = "llama-3-8b.Q4_K_M.gguf"
HF_TOKEN = "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"  # Replace with your token or use env var

def load_model():
    """Load the model with authentication handling"""
    try:
        model_path = hf_hub_download(
            repo_id=MODEL_REPO,
            filename=MODEL_FILE,
            token=HF_TOKEN if HF_TOKEN.startswith("hf_") else None,
            resume_download=True
        )
        return Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4,
            verbose=False
        )
    except Exception as e:
        print(f"Model loading failed: {str(e)}")
        print("Possible solutions:")
        print("1. Verify your Hugging Face token is correct")
        print("2. Accept the model terms at: https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct")
        raise

def paraphrase(text, llm):
    """Generate a paraphrase with error handling"""
    try:
        prompt = f"Paraphrase this text keeping the same meaning:\n{text}\nOutput:"
        output = llm.create_completion(
            prompt,
            max_tokens=200,
            temperature=0.7,
            top_p=0.9
        )
        return output['choices'][0]['text'].strip()
    except Exception as e:
        print(f"Generation failed: {str(e)}")
        return None

if __name__ == "__main__":
    # Initialize model (will download on first run)
    print("Loading model...")
    llm = load_model()
    
    # Test paraphrase
    test_text = "The quick brown fox jumps over the lazy dog."
    print("\nOriginal:", test_text)
    print("Paraphrased:", paraphrase(test_text, llm))
