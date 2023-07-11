# TextbookTermExplorer

TextbookTermExplorer is a Python script that uses OpenAI's GPT-3.5 to automatically generate definitions of terms within a given PDF textbook. The user can ask for a definition of a technical term, and if the term is not found in a definitions file, the script will parse the PDF file to find the context of the term. The script then asks GPT-3.5 to generate a definition based on the context, which it saves in the definitions file for future reference.

This [website](https://tonyfu97.github.io/TextbookTermExplorer/) shows some example definitions generate from the book "Conscious Mind, Resonant Brain: How Each Brain Makes a Mind" by Stephen Grossberg (2021).

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have a working installation of Python 3.
* You have registered for an API key at [OpenAI](https://platform.openai.com/overview).
* You have installed the necessary Python libraries: PyPDF2, openai, python-dotenv, tqdm, and argparse. Install them using pip:

```bash
pip install PyPDF2 openai python-dotenv tqdm argparse
```

## Using TextbookTermExplorer

To use TextbookTermExplorer, follow these steps:

* Create a `.env` file in the same directory as the script, and set your OpenAI API key:

```
OPENAI_API_KEY=your-api-key
```

* Run the script in the terminal by specifying the paths to your PDF file and definitions file:

```bash
python3 main.py /path/to/your/book.pdf /docs/definitions.json
```

The script will then ask you to enter a term. If the term exists in the definitions file, it will display the definition. If the term doesn't exist, it will search the PDF file for the context, generate a definition, and save it in the definitions file.

You can terminate the script at any point by typing 'q', 'Q', 'quit', or 'Quit' when asked for a term.

## Configuration

You can adjust the following constants to modify the behavior of the script:

* `WINDOW_SIZE_BEFORE` (default: 50) - The number of words before the term to include in the context.
* `WINDOW_SIZE_AFTER` (default: 100) - The number of words after the term to include in the context.
* `MAX_NUM_CONTEXTS` (default: 10) - The maximum number of contexts to consider when generating a definition.

## Customizing the Chatbot Prompt

You can modify the `get_definition` function in the script to customize the prompt sent to the Chatbot. The current prompt asks for a succinct definition of the term and optionally highlights any differences between the term's usage in the provided context and its conventional meaning. You can change the wording of this prompt to better suit your needs.

## Warning

Please be aware of OpenAI's pricing structure. Generating definitions can consume a significant number of tokens depending on the size of the context and the number of terms for which you generate definitions.

## Contributing to TextbookTermExplorer

If you wish to contribute to this project, please fork the repository and submit a pull request.