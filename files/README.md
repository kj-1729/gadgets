# files_dirs.py
This will list all directories/files under a given directory.

Usage:
```
python files_dirs.py (dirname)
```

Output file layout
 |　No.　|　column name　|　content　|
 | --- | --- | --- |
 | 0 | SEQNO | sequential number |
 | 1 | PARENT_SEQNO | parent sequential number |
 | 2 | DIR/FILE | 'DIR'/'File' |
 | 3 | DEPTH | depth (starting from ROOT) |
 | 4 | FILE_TYPE | file extention (xlsx, txt, etc) |
 | 5 | FILE_NAME | filename |
 | 6 | DIRNAME | directory name |
 | 7 | FULL_PATH | file path |
 | 8 | SIZE | file size |
 | 9 | LAST_MODIFIED | last modified date |
 | 10 | Path1 | path1 (starting from ROOT) |
 | 11 | Path2 | path2 (starting from ROOT) |
 | 12 | Path3 | path3 (starting from ROOT) |
 | ... | ... | ... | 

# sh_wrapper.py
This is a wrapper function of shell commands (copy/move/mkdir).

Usage:
```
cat data.txt | python sh_wrapper [copy/move/mkdir]
```

Input file layout:
 |　No.　|　column name　|　content　|
 | --- | --- | --- |
 | 0 | SEQNO | sequential number |
 | 1 | FILENAME_FROM | 'copy'/'move': directory/file name copied/moved from <br> 'mkdir': directory name to be creaated|
 | 2 | FILENAME_TO | 'copy'/'move': directory/file name copied/moved to <br> 'mkdir': not used |
 
