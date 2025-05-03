import os
import pdfplumber
from huggingface_hub import InferenceClient
import re
import time

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using pdfplumber."""
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n\n"
        
        if not text.strip():
            return "Error: No text could be extracted from the PDF."
        
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

def generate_mcqs_from_pdf(pdf_path, num_questions=5):
    """Generate MCQs from a PDF using the llama2-pdf-to-quizz-13b model."""
    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    if pdf_text.startswith("Error"):
        return pdf_text
    
    # Truncate if too long (token limits)
    content_for_mcq = pdf_text[:15000]  # Truncate to avoid token limits
    
    print(f"Generating {num_questions} MCQs using llama2-pdf-to-quizz-13b...")
    
    try:
        # Initialize the Inference API client
        client = InferenceClient(
            model="fbellame/llama2-pdf-to-quizz-13b",
            token=os.getenv("HF_API_TOKEN")  # Get token from environment variable
        )
        
        # Prepare the prompt
        prompt = f"""
You are an expert educator who creates high-quality multiple-choice questions.

Create exactly {num_questions} multiple-choice questions based on the following content extracted from a PDF:

{content_for_mcq}

For each question:
1. Make sure it tests understanding of important concepts from the text
2. Provide 4 options (A, B, C, D)
3. Only one option should be correct
4. The other options should be plausible but clearly incorrect
5. Indicate the correct answer at the end

Format each question exactly like this:

Q1. [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Correct Answer: [A, B, C, or D]

Ensure each question is clear, accurate, directly based on the provided content, and follows the exact format above. Do not include extra text, introductions, or explanations outside the formatted questions.
"""
        
        # Handle potential rate limiting with retries
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.text_generation(
                    prompt,
                    max_new_tokens=2000,
                    temperature=0.7,
                    top_p=0.9,
                    repetition_penalty=1.1
                )
                break
            except Exception as e:
                if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5  # Exponential backoff
                    print(f"Rate limited. Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    raise e
        
        # Parse the output to extract properly formatted questions
        generated_text = response.strip()
        pattern = r"Q\d+\.\s.*?\nA\).*?\nB\).*?\nC\).*?\nD\).*?\nCorrect Answer: [A-D]"
        matches = re.findall(pattern, generated_text, re.DOTALL)
        
        questions = []
        for match in matches[:num_questions]:
            questions.append(match.strip())
        
        if not questions:
            return "No valid MCQs were produced. Please check the PDF content."
        
        return "\n\n".join(questions)
    
    except Exception as e:
        return f"Error generating MCQs: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Print a welcome message
    print("=" * 80)
    print("MCQ Generator from PDF using Llama2-PDF-to-Quizz-13B".center(80))
    print("=" * 80)
    
    # Check if HF_API_TOKEN is set
    if not os.getenv("HF_API_TOKEN"):
        print("Warning: HF_API_TOKEN environment variable is not set.")
        print("Please set it with your Hugging Face API token to use this script.")
        print("You can get a token at https://huggingface.co/settings/tokens")
        exit(1)
    
    # Get PDF path from user
    pdf_path = input("Enter the path to your PDF file: ")
    
    # Get number of questions
    try:
        num_questions = int(input("How many questions do you want to generate? [5]: ") or "5")
    except ValueError:
        num_questions = 5
        print("Invalid input. Using default value of 5 questions.")
    
    print(f"\nProcessing PDF and generating {num_questions} MCQs...")
    print("This may take a while depending on the PDF size...")
    
    # Generate MCQs from the PDF
    mcqs = generate_mcqs_from_pdf(pdf_path, num_questions)
    
    print("\n" + "=" * 80)
    print("Generated MCQs:".center(80))
    print("=" * 80 + "\n")
    print(mcqs)