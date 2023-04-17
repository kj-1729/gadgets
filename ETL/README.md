# xls_copy_and_paste
This copies cells from an Excel file to another.

Usage:
```
python xls_copy_and_paste.py (config_file name)
```

## Config file
This contains information about
- Excel files copied from/to
- Spreadsheet/cells copied from/to

<img width="422" alt="config" src="https://user-images.githubusercontent.com/87534698/232361877-fb15aba1-570c-4c83-a2a4-87d943f388b5.png">

## How it works...
"from" sheet of data_from.xlsx

<img width="329" alt="data_from" src="https://user-images.githubusercontent.com/87534698/232361961-ed3ea744-1d89-4f2c-a87c-cba1febe40e6.png">

"to" sheet of data_to.xlsx (before/after the python code is run)
<img width="539" alt="data_to" src="https://user-images.githubusercontent.com/87534698/232361982-7ed81d09-571c-4ff3-af18-57bf76efa99d.png">

# xls2db.py
This extracts data from an Excel file, output these data with cell index (row/column index).

Usage:
```
python xls2db.py (data filename(xlsx)) (output filename(xlsx))
```

## Output Data Layout

 | No. | item | content |
 | --- | --- | --- |
 | 0 | SEQNO | sequential number |
 | 1 | SHEETNAME | sheetname |
 | 2 | ROW | row index |
 | 3 | COLUMN | column index |
 | 4 | DATATYPE | datatype |
 | 5 | VALUE | value |
 
## Sample Input/Output

### Sample Input: 

sheet: "from"

<img width="329" alt="data_from" src="https://user-images.githubusercontent.com/87534698/232361961-ed3ea744-1d89-4f2c-a87c-cba1febe40e6.png">

sheet: "from2"

<img width="284" alt="data_from2" src="https://user-images.githubusercontent.com/87534698/232391814-e63cfcb5-bf81-46f2-a684-e14c7f45dc5f.png">

### Sample Output:

<img width="406" alt="xls2db_output" src="https://user-images.githubusercontent.com/87534698/232391826-e1ffc4d5-58f3-43dd-b5c7-04f961bd0e7a.png">

