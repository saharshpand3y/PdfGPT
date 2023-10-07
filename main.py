import PyPDF2
import os
import requests
import re
import openai
import random
from colorama import Fore, Style, init
import sys
import colorama
colors = [Fore.YELLOW, Fore.BLUE, Fore.WHITE, Fore.RED, Fore.GREEN]
colorama.init(autoreset=True)

sys.stdout.write(
    f"""{colorama.Fore.YELLOW}
██████╗░██████╗░███████╗░██████╗░██████╗░████████╗
██╔══██╗██╔══██╗██╔════╝██╔════╝░██╔══██╗╚══██╔══╝
██████╔╝██║░░██║█████╗░░██║░░██╗░██████╔╝░░░██║░░░
██╔═══╝░██║░░██║██╔══╝░░██║░░╚██╗██╔═══╝░░░░██║░░░
██║░░░░░██████╔╝██║░░░░░╚██████╔╝██║░░░░░░░░██║░░░
╚═╝░░░░░╚═════╝░╚═╝░░░░░░╚═════╝░╚═╝░░░░░░░░╚═╝░░░
Welcome To PdfGPT.\n\n\n"""
)

def extract_questions(pdf_path):
    global colors
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        print(f'{colorama.Fore.YELLOW}-' * 70)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            question_pattern = re.compile(r'\b(\d+)\.\s*(.+?)\s*(?=\d+\.|\Z)', re.DOTALL)
            matches = question_pattern.findall(text)
            for match in matches:
                question_number, question_text = match
                color = random.choice(colors)
                openai.api_key = ""  #Add Your API Key
                completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                            {
                                'role': 'user',
                                'content': question_text
                            }
                        ]
                )
                response_content = completion.choices[0].message.content.strip()
                print('-' * 50)
                print(f"{colorama.Fore.GREEN}Ans {question_number}: {colorama.Fore.WHITE}{response_content}\n")
        print(f'{colorama.Fore.YELLOW}-' * 70)

def main():
    pdf_path = input(f"{colorama.Fore.BLUE}Enter the path of PDF: ")

    if not os.path.exists(pdf_path):
        print(f"{colorama.Fore.RED}Error: The file {pdf_path} does not exist.")
        return

    extract_questions(pdf_path)

if __name__ == "__main__":
    main()
