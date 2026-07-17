import sys
import nltk
import spacy

def main():
    print("=== Downloading NLTK Resources ===")
    nltk_resources = ["stopwords", "punkt", "punkt_tab"]
    for resource in nltk_resources:
        try:
            print(f"Downloading {resource}...")
            nltk.download(resource, quiet=True)
            print(f"Successfully downloaded {resource}")
        except Exception as e:
            print(f"Failed to download {resource}: {e}")

    print("\n=== Downloading spaCy Model ===")
    model_name = "en_core_web_sm"
    try:
        print(f"Checking if spaCy model '{model_name}' is installed...")
        spacy.load(model_name)
        print(f"Model '{model_name}' is already installed.")
    except OSError:
        print(f"Model '{model_name}' not found. Downloading...")
        try:
            from spacy.cli import download
            download(model_name)
            print(f"Successfully downloaded spaCy model '{model_name}'")
        except Exception as e:
            print(f"Failed to download spaCy model: {e}")
            sys.exit(1)

    print("\n=== Resource Download Script Finished ===")

if __name__ == "__main__":
    main()
