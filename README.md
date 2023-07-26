# README

Tired of adding comments manually to your code line by line? Let the Code Comment Assistant help you! 

This Python script whips up comments for your long code.

- It resolves the input tokens limitations of ChatGPT.
- It supports almost all programming languages.
- It supports modifying the prompt to achieve more possibilities, such as adding comments in any language to the code, translating long articles, summarizing long articles, etc.

**Note**: To run this script, you'll need to make sure your network can connect to the OpenAI API.

This script is open source, you can [check the source code here]().

## User Guide

1. Click [this link]() to download the project zip file.
2. Unzip the project file. Open the unzipped folder and find auto_comment_GUI_github_v2.zip.
3. Unzip auto_comment_GUI_github_v2.zip.
4. Navigate to the unzipped file directory auto_comment_GUI_github_v2\dist\run.
5. Find run.exe and double-click to run it.
6. Enter your OpenAI API key. If you do not have an OpenAI API key, please refer to [How to get the OpenAI API key]().
7. Make sure there are no lines in your input code file that exceed 1000 characters. It is recommended to save the code in a .txt file.
8. Choose the paths for the input and output files, and the encoding method when opening the files.
9. Click 'Run Script' to start the commenting process.
10. Please wait patiently.
11. After the operation is complete, the output file will be saved as a .txt file and will open automatically.

## Features

- Graphical user interface for easy interaction.
- Splits large files into segments to avoid exceeding the token limit.
- Sends code to OpenAI's API to generate comments.
- Handles errors and exceptions.
- Task progress bar.
- Measures the time taken for each operation.

## How to get the OpenAI API key

1. If you do not have an API, you can get your API from [this link](https://platform.openai.com/account/api-keys).
2. After registration or login, click on View API keys on the right, then click Create new secret key, name the Key, and you can generate a new API Key.
3. Remember to copy and save this API Key immediately after it is generated. This Key will only be displayed once, and if you forget to save it, you will need to create it again.
4. Follow the [user guide]() to run the script, and enter the API Key in the "Enter your OpenAI API Key below." section. Or save the API Key in the api_key.txt file in the run folder.
