import os
from dotenv import load_dotenv
from google import genai
import tkinter as tk
from tkinter import scrolledtext, messagebox

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Please set GOOGLE_API_KEY in your .env file")

def generate_notes_from_url(url):
    client = genai.Client(api_key=api_key)

    chat = client.chats.create(model="gemini-2.5-flash")  

    prompt = f"""
You are an expert assistant. Here is a YouTube video URL:
{url}

Based on the URL, assume this is a video relevant to programming/tech content. 
Write detailed, structured notes (main points, sub‑points, key takeaways) about what such a video would likely cover. Use general reasoning — because transcript isn't available, you're inferring based on typical content of such videos.
"""

    response = chat.send_message(prompt)
    return response.text

def generate_notes_button_click():
    video_url = url_entry.get().strip()
    if not video_url:
        messagebox.showwarning("Input Required", "Please enter a YouTube video URL!")
        return

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Generating notes... Please wait...\n")
    root.update()

    try:
        notes = generate_notes_from_url(video_url)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, notes)
    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Error generating notes:\n{str(e)}")

root = tk.Tk()
root.title("YouTube Video Notes Generator (GenAI)")
root.geometry("800x600")

tk.Label(root, text="Paste YouTube Video URL here:").pack(pady=5)
url_entry = tk.Entry(root, width=80)
url_entry.pack(pady=5)

generate_btn = tk.Button(root, text="Generate Notes", command=generate_notes_button_click)
generate_btn.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=30)
output_text.pack(padx=10, pady=10)

root.mainloop()
