from telebot import TeleBot
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve API keys from environment variables
TELEBOT_API_KEY = os.getenv("TELEBOT_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not TELEBOT_API_KEY or not GEMINI_API_KEY:
    raise ValueError("API keys are missing. Please set them in the .env file.")

# Initialize the bot and Gemini
bot = TeleBot(TELEBOT_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Define the context for the bot
SYSTEM_PROMPT = """You are a knowledgeable Web3 and blockchain education assistant. 
You provide clear, accurate, and helpful information about blockchain technology, 
cryptocurrencies, smart contracts, DeFi, NFTs, and other Web3-related topics. 
Keep responses concise yet informative."""

@bot.message_handler(commands=['start'])
def handle_start(message):
    welcome_message = """Welcome to the TJP's Web3 Education Bot! 👋

I'm here to help you learn about blockchain technology and Web3. You can ask me questions about:
• Blockchain basics
• Cryptocurrencies
• Smart contracts
• DeFi (Decentralized Finance)
• NFTs
• Web3 concepts
• And more!

Just type your question, and I'll do my best to help you understand! 🚀"""
    
    bot.send_message(message.chat.id, welcome_message)

@bot.message_handler(commands=['help'])
def handle_help(message):
    help_message = """Here are some example questions you can ask:

1. "What is blockchain technology?"
2. "How do smart contracts work?"
3. "Explain DeFi in simple terms"
4. "What are the use cases of NFTs?"
5. "What is the difference between Web2 and Web3?"

Feel free to ask any question about Web3 and blockchain! 🎓"""
    
    bot.send_message(message.chat.id, help_message)

@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    # Send a loading message
    loading_message = bot.send_message(message.chat.id, "Thinking... 🤔")
    
    try:
        # Prepare the prompt with context
        prompt = f"{SYSTEM_PROMPT}\n\nUser Question: {message.text}"
        
        # Generating response using Gemini
        response = model.generate_content(prompt)
        answer = response.text
        
        # Sending the answer
        bot.send_message(message.chat.id, answer)
        
    except Exception as e:
        # Handling any errors
        error_message = "Sorry, I encountered an error while processing your question. Please try again."
        bot.send_message(message.chat.id, f"{error_message}\nError: {str(e)}")
    
    finally:
        # Removing the loading message
        bot.delete_message(message.chat.id, loading_message.message_id)

# Error handler
@bot.message_handler(content_types=['photo', 'video', 'document', 'audio'])
def handle_non_text(message):
    bot.reply_to(message, "I can only process text messages. Please type your question about Web3 or blockchain.")

# Starting
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
