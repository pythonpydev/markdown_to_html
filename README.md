# README.md

##  Purpose

The purpose of the application is to import one or more markdown files, collate them into a single text file, and then format and output the content as a HTML file.



Execute the following command in the terminal:

```script
python3 main.py . file.txt index.html
```

>**main.py** is the Python file name.

>**.** Represents the current directory where the markdown files are stored (although they could be stored in any path).

>**file.txt** is the name of the text file where the combined content of all of the markdown files is stored.

>**index.html** is the html page that the markdown content from the text file will be output to.

## To do

- Create a txt file automatically.  At the moment, the app reads in text from a pre-created text file.
- Bypass the text file completely and convert the collated md files into a single formatted string, which can then be output to HTML.
- Create a Joplin plugin that will allow users to use this functionality with their notebooks and todos.