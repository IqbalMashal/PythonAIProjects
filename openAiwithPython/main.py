import openai
import os
from dotenv import load_dotenv
from colorama import init, Fore, Style
import json
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
import time

init()

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# File to store question-answer history
HISTORY_FILE = "chat_history.json"

def load_history():
    """Load chat history from JSON file."""
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_history(question, answer):
    """Save question and answer to history file."""
    history = load_history()
    history.append({"question": question, "answer": answer, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")})
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def show_history():
    """Display chat history."""
    history = load_history()
    if not history:
        print(f"{Fore.YELLOW}No history available.{Style.RESET_ALL}")
        return
    print(f"{Fore.CYAN}=== Chat History ==={Style.RESET_ALL}")
    for i, entry in enumerate(history, 1):
        print(f"{Fore.GREEN}Q{i}: {entry['question']}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}A{i}: {entry['answer']}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Time: {entry['timestamp']}{Style.RESET_ALL}\n")

def get_llm_response(prompt, retries=3, backoff_factor=0.5):
    """Get response from OpenAI API with retry mechanism."""
    for attempt in range(retries):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful but terse AI assistant who gets straight to the point."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0
            )
            return completion.choices[0].message["content"]
        except Exception as e:
            if attempt < retries - 1:
                sleep_time = backoff_factor * (2 ** attempt)
                print(f"{Fore.RED}API error: {e}. Retrying in {sleep_time}s...{Style.RESET_ALL}")
                time.sleep(sleep_time)
            else:
                return f"{Fore.RED}Error: Failed to get response after {retries} attempts.{Style.RESET_ALL}"

def get_user_question():
    """Prompt user for a question with auto-suggestions, with fallback to standard input."""
    try:
        # Initialize the prompt session outside the loop
        session = PromptSession(
            history=FileHistory("prompt_history.txt"),
            auto_suggest=AutoSuggestFromHistory(),
            multiline=False
        )

        userQuestion = f"Ask AI a question (type 'history' to see past questions, 'exit' to quit): "
        
        while True:
            try:
                # Move the prompt text to the session.prompt() call
                question = session.prompt(
                    userQuestion
                ).strip()
                
                if question.lower() == 'exit':
                    print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
                    return None
                elif question.lower() == 'history':
                    show_history()
                    continue
                elif question:
                    response = get_llm_response(question)
                    save_history(question, response)
                    return response
                else:
                    print(f"{Fore.YELLOW}Please enter a valid question.{Style.RESET_ALL}")
                    
            except (KeyboardInterrupt, EOFError):
                print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
                return None
            except Exception as e:
                print(f"{Fore.RED}Prompt error: {e}. Falling back to standard input.{Style.RESET_ALL}")
                question = input(f"{Fore.CYAN}Ask AI a question (type 'history' to see past questions, 'exit' to quit): {Style.RESET_ALL}").strip()
                
                if question.lower() == 'exit':
                    print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
                    return None
                elif question.lower() == 'history':
                    show_history()
                    continue
                elif question:
                    response = get_llm_response(question)
                    save_history(question, response)
                    return response
                else:
                    print(f"{Fore.YELLOW}Please enter a valid question.{Style.RESET_ALL}")
                    
    except Exception as e:
        print(f"{Fore.RED}Failed to initialize prompt session: {e}. Using standard input.{Style.RESET_ALL}")
        # Fallback to standard input
        while True:
            try:
                question = input(f"{Fore.CYAN}Ask AI a question (type 'history' to see past questions, 'exit' to quit): {Style.RESET_ALL}").strip()
                
                if question.lower() == 'exit':
                    print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
                    return None
                elif question.lower() == 'history':
                    show_history()
                    continue
                elif question:
                    response = get_llm_response(question)
                    save_history(question, response)
                    return response
                else:
                    print(f"{Fore.YELLOW}Please enter a valid question.{Style.RESET_ALL}")
            except (KeyboardInterrupt, EOFError):
                print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
                return None

def main():
    print(f"{Fore.CYAN}=== Welcome to Enhanced AI Chat ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Ask anything, view history with 'history', or type 'exit' to quit.{Style.RESET_ALL}\n")
    
    while True:
        response = get_user_question()
        if response is None:
            break
        print(f"{Fore.GREEN}Answer: {response}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()