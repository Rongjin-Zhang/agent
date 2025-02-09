import tkinter as tk
from openai import OpenAI
from tkinter import font, scrolledtext
from PIL import Image, ImageTk
import time # Import the time module for adding delays
import threading

client = OpenAI(api_key='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')

# Set up the main application window
root = tk.Tk() # Create the main window
root.title("Chat with an Expert") # Set the title of the window
root.geometry("600x400")  # Set the window size

# Load and resize the profile pictures using Pillow
agent_image = Image.open("/Users/zhan8939/Documents/Chatbot/Human/1.png")
agent_image = agent_image.resize((50, 50), Image.LANCZOS)
agent_image = ImageTk.PhotoImage(agent_image)

user_image = Image.open("/Users/zhan8939/Documents/Chatbot/Human/2.png")
user_image = user_image.resize((50, 50), Image.LANCZOS)
user_image = ImageTk.PhotoImage(user_image)

# Flag to track if it's the first interaction
first_interaction = True

def send_prompt(event=None):
    """
    This function is called when the user clicks the Send button or presses the Enter key.
    """
    global first_interaction, user_gender
    prompt = prompt_entry.get()  # Get the prompt text from the entry widget
    if prompt:
        chat_window.config(state=tk.NORMAL)  # Make the chat window editable
        chat_window.image_create(tk.END, image=user_image)  # Insert the user's profile picture
        chat_window.insert(tk.END, f"You: {prompt}\n")  # Insert the user's prompt into the chat window
        chat_window.insert(tk.END, "\n")  # Indicate that the system is processing the prompt
        chat_window.insert(tk.END, "Assistant is typing...\n")  # Indicate that the system is processing the prompt
        chat_window.config(state=tk.DISABLED)  # Make the chat window read-only again
        chat_window.yview(tk.END)  # Scroll to the end of the chat window
        prompt_entry.delete(0, tk.END)  # Clear the entry widget

        if first_interaction:
            # Spoof the first reply
            threading.Thread(target=first_response).start()
            first_interaction = False
        else:
            # Use threading to avoid blocking the main thread
            threading.Thread(target=get_response, args=(prompt,)).start()

def first_response():
    """
    Function to simulate the first response from the assistant.
    This function adds a delay to simulate thinking and then inserts a predefined message into the chat window.
    """
    time.sleep(10)  # Add a 5-second pause to simulate thinking
    answer = "Hello! May I ask your gender?\n"
    chat_window.config(state=tk.NORMAL)  # Make the chat window editable
    chat_window.delete("end-2l", tk.END)  # Remove "Assistant is typing..."
    chat_window.insert(tk.END, "\n")
    chat_window.image_create(tk.END, image=agent_image)  # Insert the agent's profile picture
    chat_window.insert(tk.END, f"Mathhew: \n{answer}\n")  # Insert the assistant's response into the chat window
    chat_window.config(state=tk.DISABLED)  # Make the chat window read-only again
    chat_window.yview(tk.END)  # Scroll to the end of the chat window

def get_response(prompt):
    """
    Function to get the response from the assistant.
    This function is called in a separate thread to avoid blocking the main thread.
    """
    try:
        # act like an assistant in the automotive industry
        system_message = f"You are an expert in automotive repair for Happy Wheels Automotive Service. Use professional terminology and industry-specific language when answering questions. Speak in a human-like and perusaive manner that reflects the professionalism of our company. Each response should be like a human, short, and within 50 words. When discussing prices, offer slightly higher estimates than market rates."
        # Simulate thinking delay
        time.sleep(10)
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150) # Set the maximum number of tokens for the completion
        # Extract the content of the response
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"Error: {e}"

    chat_window.config(state=tk.NORMAL)  # Make the chat window editable
    chat_window.delete("end-2l", tk.END)  # Remove "Assistant is typing..."
    chat_window.insert(tk.END, "\n")
    chat_window.image_create(tk.END, image=agent_image)  # Insert the agent's profile picture
    chat_window.insert(tk.END, f"Mathhew: \n{answer}\n")  # Insert the assistant's response into the chat window
    chat_window.config(state=tk.DISABLED)  # Make the chat window read-only again
    chat_window.yview(tk.END)  # Scroll to the end of the chat window


# Create a frame for the custom title
title_frame = tk.Frame(root)
title_frame.pack(side=tk.TOP, fill=tk.X)

# Create a larger font for "Matthew"
large_font = font.Font(family="Helvetica", size=18, weight="bold")

# Create a smaller font for "Your Human Service Agent"
small_font = font.Font(family="Helvetica", size=15)

# Create labels for the title
large_label = tk.Label(title_frame, text="  Matthew", font=large_font)
small_label = tk.Label(title_frame, text=" Your Human Service Agent", font=small_font)

# Pack the labels into the frame
large_label.pack(side=tk.LEFT)
small_label.pack(side=tk.LEFT)

# Create a scrolled text widget for the chat window
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)  # Create a scrolled text widget
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)  # Pack the widget into the window

# Create an entry widget for the user to type their prompt
prompt_entry = tk.Entry(root, width=50)
prompt_entry.pack(padx=10, pady=(0,10), side=tk.LEFT, fill=tk.X, expand=True) # Pack the widget into the window
prompt_entry.bind("<Return>", send_prompt)  # Bind the Enter key to the send_prompt function

# Create a Send button
send_button = tk.Button(root, text="Send", command=send_prompt)
send_button.pack(padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
