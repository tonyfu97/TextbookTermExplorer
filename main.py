import os
import re
import json
import openai
import argparse
from PyPDF2 import PdfReader
from tqdm import tqdm
from dotenv import load_dotenv

WINDOW_SIZE_BEFORE = 50
WINDOW_SIZE_AFTER = 100
MAX_NUM_CONTEXTS = 10

def load_pdf(pdf_path):
    print("Loading PDF...")
    with open(pdf_path, "rb") as file:
        pdf = PdfReader(file)
        text = ""
        for page in tqdm(pdf.pages):
            text += page.extract_text()
    return text

def get_contexts(text, term):
    words = text.split()
    contexts = []
    for i in range(len(words)):
        if term in " ".join(words[i:i+len(term.split())]):
            context = " ".join(words[max(0, i-WINDOW_SIZE_BEFORE):min(len(words), i+len(term.split())+WINDOW_SIZE_AFTER)])
            highlighted_context = re.sub(f'({term})', r'\033[91m\1\033[0m', context, flags=re.IGNORECASE)
            print(highlighted_context)
            contexts.append(context)
            if len(contexts) == MAX_NUM_CONTEXTS:
                break
    return "\n".join(contexts)

def extract_contexts(book_text, term):
    # split the book text into individual words
    book_words = book_text.split()
    
    contexts = []
    term_pattern = re.compile(f'\\b{term}\\b', re.IGNORECASE)
    for match in term_pattern.finditer(book_text):
        # Find the index of the word that contains the start of the match
        start_index = len(book_text[:match.start()].split())
        start = max(0, start_index - WINDOW_SIZE_BEFORE)
        end = min(len(book_words), start_index + WINDOW_SIZE_AFTER)
        context = " ".join(book_words[start:end])
        contexts.append(context)

    contexts = contexts[:MAX_NUM_CONTEXTS]
    return "\n".join(contexts)

def get_definition(term, context):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"The term '{term}' is used in the following context: '{context}'. Please provide a succinct definition. If the usage of the term in this book diverges from its conventional meaning, highlight the differences.\n\nDefinition:",
        temperature=0.3,
        max_tokens=200
    )

    return response.choices[0].text.strip()

def main(pdf_path, definitions_path):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    text = load_pdf(pdf_path)
    
    definitions = {}
    if os.path.exists(definitions_path):
        with open(definitions_path, "r") as file:
            definitions = json.load(file)

    while True:
        term = input("Please enter a term to define, 'd term' to delete a term, or 'q' to quit: ").strip()
        if term.lower() in ['q', 'quit']:
            return

        # Check if user wants to delete a term
        if term.lower().startswith('d '):
            term_to_delete = term[2:]
            if term_to_delete in definitions:
                del definitions[term_to_delete]
                print(f"Deleted definition for '{term_to_delete}'.\n")
                # Save definitions to file
                with open(definitions_path, "w") as file:
                    json.dump(definitions, file)
            else:
                print(f"No definition found for '{term_to_delete}'.\n")
            continue
            
        # Check if term is in definitions file
        if term in definitions:
            print("Definition already exists in file:")
            print(definitions[term])
            print("Do you want to overwrite the definition above with a new defintion? (y/n)")   
            if input().lower() != 'y':
                continue
    
        # If term is not in definitions file, search in PDF
        contexts = get_contexts(text, term)
        if not contexts:
            print("Term not found in the book.")
            continue
            
        # Generate definition with ChatGPT for each context
        definition = get_definition(term, contexts)
        definitions[term] = definition
        print(f"\n\033[92mDefinition: {definition}\033[0m\n")

        # Save definitions to file
        with open(definitions_path, "w") as file:
            json.dump(definitions, file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file')
    parser.add_argument('definitions_path', type=str, help='Path to the definitions file')

    args = parser.parse_args()
    main(args.pdf_path, args.definitions_path)
