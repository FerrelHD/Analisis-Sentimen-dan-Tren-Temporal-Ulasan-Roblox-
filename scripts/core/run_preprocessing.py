import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.preprocessor import preprocess_data

if __name__ == "__main__":
    preprocess_data()
