import os
import sys
from dotenv import load_dotenv

def run_diagnostics():
    print("--- Backend Diagnostics ---")
    
    # 1. Check Python Version
    print(f"Python Version: {sys.version}")
    
    # 2. Check current directory
    print(f"CWD: {os.getcwd()}")
    
    # 3. Check .env file
    env_path = os.path.join(os.getcwd(), '.env')
    print(f".env path: {env_path}")
    print(f".env exists: {os.path.exists(env_path)}")
    
    # 4. Load env
    load_dotenv()
    key = os.getenv('GEMINI_API_KEY')
    if key:
        print(f"GEMINI_API_KEY: Found (starts with {key[:4]}...)")
    else:
        print("GEMINI_API_KEY: NOT FOUND")
    
    # 5. Check dependencies
    try:
        import google.generativeai as genai
        print(f"google-generativeai: Installed (version {genai.__version__})")
        
        if key:
            try:
                genai.configure(api_key=key)
                model = genai.GenerativeModel('gemini-2.0-flash')
                print("Gemini Config: OK")
                
                # Test a very small generation
                print("Testing Gemini generation...")
                response = model.generate_content("Hello, respond with 'OK'")
                print(f"Gemini Test Response: {response.text.strip()}")
            except Exception as e:
                print(f"Gemini Test Failed: {e}")
    except ImportError:
        print("google-generativeai: NOT INSTALLED")

    try:
        import spacy
        print(f"spacy: Installed (version {spacy.__version__})")
        model_path = os.path.join(os.getcwd(), 'model')
        print(f"Model path: {model_path}")
        print(f"Model exists: {os.path.exists(model_path)}")
        if os.path.exists(model_path):
            try:
                nlp = spacy.load(model_path)
                print("Spacy Model Load: OK")
            except Exception as e:
                print(f"Spacy Model Load Failed: {e}")
    except ImportError:
        print("spacy: NOT INSTALLED")

    try:
        import sentence_transformers
        print(f"sentence-transformers: Installed")
    except ImportError:
        print("sentence-transformers: NOT INSTALLED")

if __name__ == "__main__":
    run_diagnostics()
