# gadgets

These are basic tools in applying a list of files to the some tasks.
To do this, use list_files.py to list all the files under a directory,
then feed the list to the other tool.

Usage:
```
python list_files.py (dirname) > file_list.txt
cat file_list.txt | python (some task).py
```
