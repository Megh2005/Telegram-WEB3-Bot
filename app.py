from telebot import TeleBot, types
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
model = genai.GenerativeModel("gemini-1.5-flash")

# Define the context for the bot
SYSTEM_PROMPT = """You are an expert in Web3 and blockchain technology. 
Your role is to educate users by providing clear, accurate, and concise information 
on topics such as blockchain basics, cryptocurrencies, smart contracts, DeFi, NFTs, 
and other Web3 concepts. Ensure your responses are informative and easy to understand.
When explaining concepts, consider the following:
1. Provide definitions and explanations for technical terms.
2. Use analogies and examples to make complex ideas more relatable.
3. Highlight the significance and potential impact of the technology.
4. Address common misconceptions and clarify any confusion.
5. Offer insights into current trends and future developments in the Web3 space.
6. Encourage curiosity and further exploration by suggesting additional resources.

Your goal is to make Web3 and blockchain technology accessible to everyone, regardless of their prior knowledge. 
Be patient, thorough, and supportive in your responses."""


@bot.message_handler(commands=["start"])
def handle_start(message):
    # Create a keyboard with a start button
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("Start Learning 🚀")
    keyboard.add(start_button)

    # Welcome message
    welcome_message = """Welcome to TJP's Web3 Education Bot! 👋

I'm here to help you learn about blockchain technology and Web3. You can ask me questions about:
• Blockchain basics
• Cryptocurrencies
• Smart contracts
• DeFi (Decentralized Finance)
• NFTs
• Web3 concepts
• And more!

Just type your question, and I'll do my best to help you understand! 🚀"""

    # Sending the image and welcome message
    with open("welcome.png", "rb") as image_file:
        bot.send_photo(
            message.chat.id, image_file, caption=welcome_message, reply_markup=keyboard
        )


@bot.message_handler(commands=["commands"])
def handle_commands(message):
    commands_message = """Here are the available commands:
1. /start - Start the bot and display the welcome message
2. /help - Get help and example questions
3. /commands - Display this command list

Feel free to type any Web3-related question!"""
    bot.send_message(message.chat.id, commands_message)


@bot.message_handler(commands=["help"])
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
    if message.text.lower() == "start learning 🚀":
        bot.send_message(
            message.chat.id,
            "Great! Type your question, and I'll help you learn about Web3! 🌟",
        )
        return

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
@bot.message_handler(content_types=["photo", "video", "document", "audio"])
def handle_non_text(message):
    bot.reply_to(
        message,
        "I can only process text messages. Please type your question about Web3 or blockchain.",
    )


# Starting
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
