# gadgets

First, use list_files.py (dirname) to list files under the directory.
Then feed those files to each tools (ocr, etc) to get results.

```
ex)
python list_files.py (dirname) > file_list.txt
cat file_list.txt | python ocr_tesseract.py
```
