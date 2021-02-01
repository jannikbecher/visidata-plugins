'''
# Requirements
This plugin needs [fzf](https://github.com/junegunn/fzf) installed.

## Commands
- `select-col-fzf` fuzzy match the current column and select matching rows.
'''

__version__ = '0.1.0'
__author__ = 'Jannik Becher <becher.jannik@gmail.com>'

from visidata import Sheet, BaseSheet, asyncthread, copy, warning, Progress, vd
import subprocess

@Sheet.api
def select_col_fzf(sheet):
    command = ['fzf',  '--multi', '--bind', 'enter:select-all+accept']
    proc = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    rows_to_filter = list(sheet.cursorCol.getValues(sheet.rows))
    filtered_rows = proc.communicate(input='\n'.join(rows_to_filter))[0].splitlines()

    BaseSheet.refresh(sheet)

    rowIdxs = []
    for row in filtered_rows:
        rowIdxs += [i for i, x in enumerate(rows_to_filter) if x == row]

    sheet.select((sheet.rows[i] for i in rowIdxs), progress=False)

# Add longname-commands to VisiData to execute these methods
BaseSheet.addCommand(None, 'select-col-fzf', 'sheet.select_col_fzf()', 'select rows matching fzf in current column')
