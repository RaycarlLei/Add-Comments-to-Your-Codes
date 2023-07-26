import os
import time
import ctypes
import threading
import shutil
import datetime
import requests
import tkinter as tk
from tkinter import filedialog
import tkinter.scrolledtext as tkst
from tkinter import ttk
from tkinter import messagebox
import webbrowser
from tkinter import *
import subprocess

install_package = lambda package: subprocess.check_call(["python", "-m", "pip", "install", "--user", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL)

def show_popup(message):
    popup = tk.Tk()
    popup.geometry("350x150")
    popup.title("Error")
    label = tk.Label(popup, text=message, font=("Verdana", 12))
    label.grid(row=0, column=0, sticky=tk.N, padx=25)
    
    button_frame = tk.Frame(popup)
    button_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.S)
    
    def retry():
        popup.destroy()
        try:
            import openai
        except ImportError:
            show_popup("\nFailed to download openai package\n")
            popup.destroy()
            return
        
        try:
            install_package("openai")
        except subprocess.CalledProcessError:
            show_popup("\nFailed to install openai package\n")
            popup.destroy()
            return
        
        popup.destroy()
    
    retry_button = tk.Button(button_frame, text="Retry", command=retry)
    retry_button.pack(side=tk.LEFT, padx=5)
    
    exit_button = tk.Button(button_frame, text="Exit", command=exit)
    exit_button.pack(side=tk.RIGHT, padx=5)
    
    popup.mainloop()

try:
    import openai
except ImportError:
    show_popup("\nFailed to download openai package\n")
    exit()

try:
    install_package("openai")
except subprocess.CalledProcessError:
    show_popup("\nFailed to install openai package\n")
    exit()

def switch_state():
    if run_button['state'] == tk.NORMAL:
        run_button['state'] = tk.DISABLED
        stop_button['state'] = tk.NORMAL
    else:
        run_button['state'] = tk.NORMAL
        stop_button['state'] = tk.DISABLED

def open_link(event, link):
    webbrowser.open(link) 

def update_time():
    global update
    if update:
        total_time = time.time() - start_time
        minutes = (int)(total_time // 60)
        seconds = (int)(total_time % 60)
        time_label.config(text=f"This task has token {minutes} mins {seconds} seconds")
        total_time += 1
        time_label.after(1000, update_time)
    else:
        total_time = 0
        time_label.config(text=" ")
        run_button['state'] = tk.NORMAL
        

def read_file(file_path, encoding):
    global code, output_text
    try:
        if not os.path.exists(file_path):
            output_text.insert(tk.END, f'Failed to read file at "{file_path}". Please make sure the address is correct\n')
            raise Exception("File does not exists")
        with open(file_path, 'r', encoding=encoding) as input_file:
            lines = input_file.readlines()
            for line in lines:
                if len(line) > 1000:
                    raise Exception("Line exceeds 1000 characters")
            code = ''.join(lines)
        output_text.insert(tk.END, f'File opened with {encoding} successfully\n')
    except UnicodeDecodeError:
        output_text.insert(tk.END, f'File can`t open with {encoding}\n')
        code = ''
    except Exception as e:
        output_text.insert(tk.END, f'Error: {str(e)}\n')
        code = ''
    return code

def split_file(code):
    global parts, part
    parts = []
    part = ''

    if len(code) > 0:
        lines = code.split('\n')
        for line in lines:
            if len(part) + len(line) > 1000:
                parts.append(part)
                part = line + '\n'
            else:
                part += line + '\n'
        if part:
            parts.append(part)

    count = len(parts)
    output_text.insert(tk.END, f'File splitted into {count} parts successfully\n')
    return parts, count

def write_api_key(event=None):
    api_key = api_key_entry.get()
    with open(api_file_path, "w") as file:
        file.write(api_key)

def write_address_out(event=None):
    address_out_value = address_out.get()
    with open(address_out_path, "w") as file:
        file.write(address_out_value)

def write_file(formatted_now, annotated_code):
    global output_filename
    file_name = os.path.basename(file_path)

    
    file_name_no_ext = os.path.splitext(file_name)[0]

    output_filename = f'{file_name_no_ext}_{formatted_now}.txt'
    
    
    output_path = os.path.join(address_out.get(), output_filename)
    
    
    if annotated_code:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(annotated_code)
        output_text.insert(tk.END, f'File written successfully to {output_path}\n')
        return output_path
    else:
        output_text.insert(tk.END, 'There is no output\n')
        return None

def save_text():
    custom_prompt_entry = entry.get()
    window.destroy()

def stop_annotation_code():
    stop_button['state'] = tk.DISABLED

    global stop_thread
    stop_thread = True
    update_time()
    output_text.insert(tk.END, f'**Thread will stop after the last web request completed\n**Please wait patiently\n')
    

def browse_file(file_path_entry):
    global filename
    filename = filedialog.askopenfilename()
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, filename)

def browse_folder(folder_path_entry):
    global foldername
    foldername = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, foldername)

def handle_selection(event):
    if prompt_combobox.get() == '**customized prompt**':
        global entry, window
        window = tk.Toplevel(root)
        window.title('Please enter your own prompt below:')
        window.geometry('410x90')

        window.attributes("-topmost", True)

        entry = tk.Entry(window, width=40)
        entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.N)
        
        save_button = tk.Button(window, text='  Save  ', command=save_text)
        save_button.grid(row=1, column=0, sticky=tk.E, pady=10,padx=80)
        
        close_button = tk.Button(window, text='Exit', command=lambda: window.destroy())
        close_button.grid(row=1, column=1, sticky=tk.W, pady=10,padx=80)

def update_temperature(temp):
    global temperature_value
    temperature_value = temperature_scale.get()
    
    return temperature_value

def handler(signum, frame):
    raise TimeoutError("Request timed out")

 

def annotate_code(parts):
    
    global annotated_code, total_time, part_time, minutes, seconds, model_engine, stop_thread, start_time
    minutes = 0
    seconds = 0
    annotated_code = ''
    model_engine = 'text-davinci-003'
    output_text.insert(tk.END, f'Model engine has been selected as {model_engine} successfully\n')
    
    start_time = time.time()
    global update
    update = True
    update_time()

    
    progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=600, mode='determinate', maximum=100.0, value=1) 
    progress_bar.grid(row=14, column=0, columnspan=2, padx=10, pady=10, sticky=tk.N)

    for i, part in enumerate(parts):
        if stop_thread:
            total_time = time.time() - start_time
            output_text.insert(tk.END, f'Thread stopped\nTotal time taken: {total_time:.2f} seconds\n')
            stop_thread = False
            break
    
        if prompt_combobox_value == 'Add code comments line by line':
            prompt = f'"Add code comments for the input line by line. The input is delimited by triple quotes. If no comments are necessary, respond with the original input. You can only add comments to the input. You must not delete or alter any existing characters, spaces, tabs, line breaks, or special symbols. Adjusting indentation and line breaks are prohibited. You must maintain the origin formating. Your response should not include any explanations. Here is the input:""""\n{part}\n"""'
        elif prompt_combobox_value == 'Add code comments at code block level':
            prompt = f'Add one English code comments for each code block in the input. The input is delimited by triple quotes. If no comments are necessary, respond with the original input. You can only add comments and must not delete or alter any existing characters, spaces, tabs, line breaks, or special symbols. Adjusting indentation and line breaks are prohibited. You must maintain the origin formating. Your response should not include any explanations. Here is the input:""""\n{part}\n"""'
        elif prompt_combobox_value == '**customized prompt**':
            prompt = custom_prompt_entry+f'""\n{part}\n""'
        part_time = time.time()
        output_text.insert(tk.END, f'Part {i+1}/{len(parts)} started at {time.strftime("%H:%M:%S", time.localtime())}\n')

        completions = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=temperature_value,
        )

        output_text.insert(tk.END, f'Part {i+1}/{len(parts)} has already processed\n')
        
        output_text.insert(tk.END, f'This part took {time.time() - part_time:.2f}s\n\n\n')
        
        
        
        progress = (i+1) / len(parts) * 100.0 
        progress_bar['value'] = progress

        annotated_code += completions.choices[0].text 

    total_time = time.time() - start_time
    minutes = total_time // 60
    seconds = total_time % 60
    update = False
    progress_bar.destroy()
    switch_state()

    return 

def run_script():
    global file_path_entry, encoding_combobox, prompt_combobox_value, address_out, minutes, seconds, output_text, debug_mode, prompt_combobox, file_path

    prompt_combobox_value = prompt_combobox.get()
    file_path = file_path_entry.get()

    encoding = encoding_combobox.get()

    now = datetime.datetime.now()
    formatted_now = now.strftime("%Y-%m-%d_%H-%M-%S")

    if debug_mode.get() == 1:
        folder_name = f"splitted_code_{formatted_now}"
        os.makedirs(folder_name, exist_ok=True) 

    code = read_file(file_path=file_path, encoding=encoding)
    parts, count = split_file(code=code)

    try:
        thread = threading.Thread(target=annotate_code, args=(parts,))
        thread.start()
        thread.join()
    except Exception as e:
        update = False
        output_text.insert(tk.END, f'Error: {e}\n')
        switch_state()
        return
    

    
    if annotate_code == None:
        update = False
        switch_state()
        stop_button.config(state=tk.DISABLED)
        return

    output_path = write_file(formatted_now, annotated_code)

    if output_path:  
        destination_path = os.path.join(address_out.get(), os.path.basename(output_path))
        if os.path.abspath(output_path) != os.path.abspath(destination_path):  
            shutil.copy(output_path, destination_path)
        os.startfile(destination_path)
        output_text.insert(tk.END, f'Total Time token: {minutes:.0f} minutes and {seconds:.2f} seconds\nInput has been splitted to {count} parts. Average process time for each task is {(total_time/count):.2f} seconds\n\n\n')
    else:
        output_text.insert(tk.END, 'No file generated\n')
    update = False
    switch_state()
    return

def run_script_thread():
    switch_state()
    api_key = api_key_entry.get()
    try:
        timer = threading.Timer(5, handler)
        timer.start()
        openai.api_key = api_key
        openai.Engine.list()
        timer.cancel()
    except requests.exceptions.Timeout:
        output_text.insert(tk.END, "Can not connect to OpenAI.\n")
    except openai.error.AuthenticationError:
        output_text.insert(tk.END, "Wrong OpenAI API key!\n")
    except requests.exceptions.RequestException as e:
        output_text.insert(tk.END, f"Request ERROR: {str(e)}\n")
    finally:
        timer.cancel()
        switch_state()

        
    

    global stop_thread
    stop_thread = False
    

    file_path = os.path.join(folder_path, 'api_key.txt')
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(api_key_entry.get())

    file_path = os.path.join(folder_path, 'address_out_cache.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(address_out.get())

    thread = threading.Thread(target=run_script)
    thread.start()
    
    

def run_main():
    global root
    global file_path_entry, api_key_entry, encoding_combobox, output_text, address_out, debug_mode, folder_path, prompt_combobox, custom_prompt_entry, parts, stop_thread, address_out_path
    
    
    folder_path = os.getcwd()

    global api_file_path
    
    if not os.path.isfile("api_key.txt"):
        with open("api_key.txt", "w") as file:
            file.write("")
    api_file_path = os.path.join(folder_path, "api_key.txt")

    
    if os.path.exists(api_file_path):
        with open(api_file_path, "r") as file:
            api_key = file.read().strip()
    else:
        api_key = ""
        with open(api_file_path, "w") as file:
            file.write(api_key)

    
    if not os.path.isfile("address_out_cache.txt"):
        with open("address_out_cache.txt", "w") as file:
            file.write("")
            
    address_out_path = os.path.join(folder_path, "address_out_cache.txt")

    
    if os.path.exists(address_out_path):
        with open(address_out_path, "r") as file:
            address_out_value = file.read().strip()
    else:
        address_out_value = f"{folder_path}"
        with open(api_file_path, "w") as file:
            file.write(address_out_value)

    root = tk.Tk()
    root.title("Code Commentator")
    root.geometry("660x1050")
    root.resizable(width=1, height=1)

    stop_thread = False
    custom_prompt_entry = 'You msut response with the original input. Here is the original input:'
    

    
    

    github_label = tk.Label(root, text="Help", fg="blue", cursor="hand2")
    github_label.bind("<Button-1>", lambda event: open_link(event, "https://github.com/RaycarlLei"))
    github_label.grid(row=0, column=0, sticky="E")

    
    

    link_label = tk.Label(root, text="Get OpenAI API Key", fg="blue", cursor="hand2")
    link_label.bind("<Button-1>", lambda event: open_link(event, "https://beta.openai.com/"))
    link_label.grid(row=0, column=0, sticky="W")

    api_key_label = tk.Label(root, text="Enter your OpenAI API Key below. Click the link above to get your API Key.")
    api_key_label.grid(row=1, column=0, sticky="N")

    api_key_entry = tk.Entry(root, width=55)
    api_key_entry.grid(row=2, column=0, sticky="N")

    api_key_entry.insert(0, api_key)
    api_key_entry.bind("<KeyRelease>", write_api_key)

    address_out_label = tk.Label(root, text="\n\n\nOutput Path")
    address_out_label.grid(row=3, column=0, sticky=tk.W, padx=27)

    address_out = tk.Entry(root, width=77)
    address_out.grid(row=3, column=0, sticky=tk.W, padx=30)

    address_out.insert(0, address_out_value)
    address_out.bind("<KeyRelease>", write_address_out)

    
    

    browse_button_out = tk.Button(root, text="Browse", command=lambda: browse_folder(address_out))
    browse_button_out.grid(row=3, column=0, sticky=tk.E, pady=60)

    file_path_label = tk.Label(root, text="\n\n\nInput File Path")
    file_path_label.grid(row=4, column=0, sticky=tk.W, padx=27)
    file_path_entry = tk.Entry(root, width=77)
    file_path_entry.grid(row=4, column=0, sticky=tk.W, padx=30)

    browse_button_in = tk.Button(root, text="Browse", command=lambda: browse_file(file_path_entry))
    browse_button_in.grid(row=4, column=0, sticky=tk.E, pady=60)

    encoding_label = tk.Label(root, text="Encoding format used for reading the file:")
    encoding_label.grid(row=9, column=0, sticky=tk.W, padx=20)

    encoding_combobox = ttk.Combobox(root, values=['utf-8', 'latin-1', 'cp1252'], width=7)
    encoding_combobox.set('utf-8')
    encoding_combobox.grid(row=10, column=0, sticky=tk.W, padx=28)

    prompt_combobox = ttk.Combobox(root, values=['Add code comments line by line', 'Add code comments at code block level','**customized prompt**'], width=34)
    prompt_combobox.set('Add code comments line by line')
    prompt_combobox.bind('<<ComboboxSelected>>', handle_selection)
    prompt_combobox.grid(row=9, column=0, sticky=tk.E, padx=10)

    global temperature_label
    temperature_label = tk.Label(root, text="Temperature:")
    temperature_label.grid(row=7, column=0, sticky=tk.W, padx=10)
    temperature_label.bind("<Enter>", lambda event: temperature_label.config(text="Higher temperature leads to more creative\n but less controlled responses.                    \nRecommended value is 0.5~0.7."))

    temperature_label.bind("<Leave>", lambda event: temperature_label.config(text="Temperature:"))

    global temperature_scale
    temperature_scale = tk.Scale(root, from_=0.1, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=220, command=update_temperature)
    temperature_scale.set(0.5)
    temperature_scale.grid(row=8, column=0, sticky=tk.W, padx=20)

    debug_mode = tk.IntVar(value=0)
    debug_checkbox = tk.Checkbutton(root, text="Save splitted results to a folder", variable=debug_mode)
    debug_checkbox.grid(row=7, column=0, sticky=tk.E)

    global run_button
    run_button = tk.Button(root, text="      RUN      ", command=run_script_thread)
    run_button.grid(row=12, column=0, sticky=tk.N)

    global time_label
    time_label = tk.Label(root, text=" ")
    time_label.grid(row=13, column=0, sticky=tk.N)

    global stop_button
    stop_button = tk.Button(root, text="Stop next task", command=stop_annotation_code)
    stop_button.grid(row=15, column=0, sticky=tk.N)
    stop_button['state'] = tk.DISABLED

    output_text = tk.Text(root, name="auto commentor", height=20, width=80)
    output_text.grid(row=16, column=0, sticky=tk.W, padx=5)

    root.mainloop()

run_main()