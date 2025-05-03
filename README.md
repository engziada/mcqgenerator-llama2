# MCQ Generator using Llama2-PDF-to-Quizz-13B

This project provides a Python script to generate multiple-choice questions (MCQs) from PDF documents using the [fbellame/llama2-pdf-to-quizz-13b](https://huggingface.co/fbellame/llama2-pdf-to-quizz-13b) model from Hugging Face.

## Features

- Extract text from PDF documents
- Generate high-quality multiple-choice questions based on the PDF content
- Customizable number of questions
- Automatic formatting of questions with options and correct answers

## Requirements

- Python 3.11 or higher
- Hugging Face API token (get one at https://huggingface.co/settings/tokens)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/engziada/mcqgenerator-llama2.git
   cd mcqgenerator-llama2
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set your Hugging Face API token as an environment variable:
   ```
   # On Windows
   set HF_API_TOKEN=your_token_here
   
   # On macOS/Linux
   export HF_API_TOKEN=your_token_here
   ```

## Usage

Run the script:
```
python generate_mcqs_from_pdf_llama2.py
```

The script will prompt you for:
1. The path to your PDF file
2. The number of questions you want to generate (default: 5)

## Example Output

```
================================================================================
                MCQ Generator from PDF using Llama2-PDF-to-Quizz-13B                
================================================================================
Enter the path to your PDF file: sample.pdf
How many questions do you want to generate? [5]: 3

Processing PDF and generating 3 MCQs...
This may take a while depending on the PDF size...

================================================================================
                               Generated MCQs:                               
================================================================================

Q1. What is the main purpose of the document?
A) To provide a historical overview of the company
B) To outline the quarterly financial results
C) To announce a new product launch
D) To describe the company's strategic vision
Correct Answer: B

Q2. Which financial metric showed the most significant improvement?
A) Gross margin
B) Operating expenses
C) Revenue growth
D) Net profit
Correct Answer: C

Q3. What challenge was mentioned as affecting the company's performance?
A) Increased competition
B) Supply chain disruptions
C) Regulatory changes
D) Currency fluctuations
Correct Answer: B
```

## How It Works

1. The script extracts text from the provided PDF using `pdfplumber`
2. It sends the extracted text to the Hugging Face Inference API with the `fbellame/llama2-pdf-to-quizz-13b` model
3. The model generates multiple-choice questions based on the content
4. The script formats and returns the questions with options and correct answers

## Limitations

- The free tier of Hugging Face Inference API has usage limits
- Very large PDFs may need to be processed in chunks due to token limits
- The quality of generated questions depends on the clarity and structure of the PDF content

## License

MIT