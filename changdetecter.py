import requests
from bs4 import BeautifulSoup
import difflib
import os
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

def fetch_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text()
    cleaned_text = " ".join(text.split())
    return cleaned_text

def overwrite_file_content(content, filename):
    with open(f'{filename}.txt', 'w') as f:  # 'w' for overwriting
        f.write(content.replace('', ''))


def save_content(content, filename):
    with open(f'{filename}.txt', 'a') as f:  # 'a' for appending instead of overwriting
        f.write(content.replace('', ''))

def load_content(filename):
    if os.path.isfile(f'{filename}.txt'):
        with open(f'{filename}.txt') as f:
            return f.read()
    return None

def has_content_changed(new_content, old_content):
    return new_content not in old_content

def get_differences(new_content, old_content):
    differ = difflib.Differ()
    new_sentences = new_content.split(". ")
    old_sentences = old_content.split(". ")
    differences = list(differ.compare(old_sentences, new_sentences))
    return '\n'.join(line for line in differences if line.startswith('- ') or line.startswith('+ '))



def check_for_changes(urls, filename):
    old_content = load_content(filename)
    all_new_content = ""  # Collect all new content to show and save later
    initial_save = False  # Track if it's the first time saving content

    for url in urls:
        new_content = fetch_webpage(url)
        all_new_content += new_content # Collect the new content for each URL

    if old_content is None:
        initial_save = True
    else:
        differences = get_differences(all_new_content, old_content)
        if differences:
            show_changed_content(all_new_content, differences, urls, filename)  # Display the changed content
        else:
            show_no_change_message()

    if initial_save:
        save_content(all_new_content, filename)  # Always save the new content at first
        messagebox.showinfo("Initial Save", "Initial content has been saved.")




def show_no_change_message():
    window = tk.Toplevel()
    window.title("Data Not Changed")

    message_label = tk.Label(window, text="Data has not changed.")
    message_label.pack()

    window.mainloop()


def show_changed_content(content, differences, urls, filename):
    window = tk.Toplevel()
    window.title("Changed Content")

    text_widget = ScrolledText(window, height=30, width=100)
    text_widget.insert(tk.END, content + "\n\nDifferences:\n" + differences)
    text_widget.pack()

    save_button = tk.Button(window, text="Save Changes", command=lambda: overwrite_file_content(content, filename))
    save_button.pack()

    window.mainloop()
    
    
def run_gui():
    window = tk.Tk()
    window.title("Webpage Monitor")
    
    url_entries = []
    for i in range(10):
        url_label = tk.Label(window, text=f"URL {i+1}:")
        url_label.pack()
        url_entry = tk.Entry(window)
        url_entry.pack()
        url_entries.append(url_entry)
    
    filename_label = tk.Label(window, text="Filename (without extension):")
    filename_label.pack()
    filename_entry = tk.Entry(window)
    filename_entry.pack()
    
    submit_button = tk.Button(window, text="Monitor Changes", command=lambda: check_for_changes([url_entry.get() for url_entry in url_entries if url_entry.get() != ''], filename_entry.get()))
    submit_button.pack()
    
    window.mainloop()

if __name__ == "__main__":
    run_gui()

