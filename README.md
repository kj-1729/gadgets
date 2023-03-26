# gadgets

This is a basic tool in applying a list of files to some task.
To do this, use list_files.py to list all the files under a directory,
then feed the list to another tools (ocr, etc).

Usage:
```
python list_files.py (dirname) > file_list.txt
cat file_list.txt | python (some task).py
```
