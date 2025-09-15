# successfactors/__main__.py
from . import config  # ensures dotenv + logging setup

def main():
    print("✅ SuccessFactors container is running!")
    # You can call your real pipeline here:
    # from .data_transformers import run_pipeline
    # run_pipeline()

if __name__ == "__main__":
    main()
