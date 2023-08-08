# README

Tired of adding comments manually to your code line by line? Let the Code Comment Assistant help you! 

This Python script whips up comments for your long code.

- Resolves ChatGPT's input token limitations.
- Supports nearly all programming languages.
- Facilitates prompt modification for expanded possibilities, including adding code comments in any language, translating lengthy articles, and summarizing extensive texts.

**Note**: To run this script, you'll need to make sure your network can connect to the OpenAI API.

This script is open-source, you can [check the source code here](https://github.com/RaycarlLei/Add-Comments-to-Your-Codes/blob/main/run.py).

## Getting Start

1. Click [this link](https://raw.githubusercontent.com/RaycarlLei/Add-Comments-to-Your-Codes/main/auto_comment_GUI_English_github.zip) to download the project zip file.
2. Unzip the project file. Open the unzipped folder and find __auto_comment_GUI_English_github.zip__.
3. Unzip __auto_comment_GUI_English_github.zip__.
4. Navigate to the unzipped file directory __auto_comment_GUI_English_github\dist\run__.
5. Find run.exe and double-click to run it.
6. Enter your OpenAI API key. If you do not have an OpenAI API key, please refer to [How to get the OpenAI API key](https://github.com/RaycarlLei/Add-Comments-to-Your-Codes#how-to-get-the-openai-api-key).
7. Make sure there are no lines in your input code file that exceed 1000 characters. It is recommended to save the code in a .txt file.
8. Select the file paths for input and output, along with the encoding method for file opening.
9. Click 'RUN' to start the commenting process.
10. Please wait patiently.
11. After the operation is complete, the output file will be saved as a .txt file and will open automatically.
![image](https://github.com/RaycarlLei/Add-Comments-to-Your-Codes/assets/38275852/a8262406-5472-44a9-ae57-da586681ef51)

## What`s New
1. You can now chuck in your prompt by reading a local txt file.This is ideal for lengthy prompts and a convenient way to save them for future use.

## Features

- Graphical user interface for easy interaction.
- Segments large files to avoid exceeding the tokens limit.
- Caches API keys and output addresses.
- Handles errors and exceptions.
- Progress bar for task tracking.
- Records the duration of each operation.

## How to get the OpenAI API key

1. If you do not have an API, you can get your API from [this link](https://platform.openai.com/account/api-keys).
2. After registration or login, click on View API keys on the right, then click Create new secret key, name the Key, and you can generate a new API Key.
3. Remember to copy and save this API Key immediately after it is generated. This Key will only be displayed once, and if you forget to save it, you will need to create it again.
4. Follow the [Getting Start](https://github.com/RaycarlLei/Add-Comments-to-Your-Codes#getting-start) to run the script, and enter the API Key in the "Enter your OpenAI API Key below." section. Or save the API Key in the api_key.txt file in the run folder.
