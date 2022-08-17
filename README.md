# vocabularyNoteBookCrawler
This is a crawler that crawls word analysis from Baidu translation to complete the word list
1. Python environment needs to be configured:

- Selenium package is needed.

  - You need to configure Google browser and Google browser driver.

- Lxml package is needed.

- Pycharm is recommended.

2. Use main_md.py generates. MD files (Markdown syntax). It is recommended to browse .md files by using Typora.

3. Precautions:

- The user needs to change the Google browser driver path in line 23 of main_md.py to the path in your computer.

- The program crawls the translated content from Baidu translation.

- Each time you run the program, it asks you to enter one word and add the content of the word in .md file.
