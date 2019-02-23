"""
    Generic dumper of Shift-JIS text into an excel spreadsheet.
    Meant for quick estimations of how much text is in a game.
"""

import sys
import os
import xlsxwriter
from rominfo import FILES, FILE_BLOCKS, inline_CTRL

ASCII_MODE = 1
# 0 = none
# 1: punctuation and c format strings only (not implemented)
# 2: All ascii

THRESHOLD = 4


def dump(files):
    for filename in files:
        if filename.endswith(".MCV"):
            file_path = filename
        else:
            file_path = os.path.join('TBS', filename)
        #if "/" in filename:
        #    sheet_name = filename.split("/")[1]
        sheet_name = filename.replace("/", "-")
        sheet_name = sheet_name.replace("decompressed\\", "")

        row = 1
        worksheet = workbook.add_worksheet(sheet_name)
        worksheet.write(0, 0, 'Offset', header)
        worksheet.write(0, 1, 'Japanese', header)
        worksheet.write(0, 2, 'JP_Len', header)
        worksheet.write(0, 3, 'English', header)
        worksheet.write(0, 4, 'EN_Len', header)
        worksheet.write(0, 5, 'Comments', header)

        worksheet.set_column('A:A', 8)
        worksheet.set_column('B:B', 60)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 60)


        with open(file_path, 'rb') as f:
            contents = f.read()

            if filename not in FILE_BLOCKS:
                blocks = [(0, len(contents))]
            else:
                blocks = FILE_BLOCKS[filename]

            for block in blocks:
                block_contents = contents[block[0]:block[1]]
                cursor = 0
                sjis_buffer = b""
                sjis_buffer_start = 0
                sjis_strings = []

                while cursor < len(block_contents):

                    # First byte of SJIS text. Read the next one, too
                    if (0x80 <= block_contents[cursor] <= 0x9f or 0xe0 <= block_contents[cursor] <= 0xef) and cursor+1 < len(block_contents):
                        #print(bytes(block_contents[cursor]))
                        sjis_buffer += block_contents[cursor].to_bytes(1, byteorder='little')
                        cursor += 1
                        sjis_buffer += block_contents[cursor].to_bytes(1, byteorder='little')

                    # ASCII text
                    elif 0x20 <=block_contents[cursor] <= 0x7e and ASCII_MODE in (1, 2):
                        sjis_buffer += block_contents[cursor].to_bytes(1, byteorder='little')

                    # C string formatting with %
                    #elif block_contents[cursor] == 0x25:
                    #    #sjis_buffer += b'%'
                    #    cursor += 1
                    #    if block_contents[cursor]

                    # End of continuous SJIS string, so add the buffer to the strings and reset buffer
                    else:
                        sjis_strings.append((sjis_buffer_start, sjis_buffer))
                        sjis_buffer = b""
                        sjis_buffer_start = cursor+1
                    cursor += 1
                    #print(sjis_buffer)

                    if any([sjis_buffer.endswith(x) for x in (b'[END]', b'[WAIT]', b'[LN]', b'[CLR]')]):
                        sjis_buffer = sjis_buffer.rstrip(b'[END]').rstrip(b'[WAIT]').rstrip(b'[LN]').rstrip(b'[CLR]')
                        sjis_strings.append((sjis_buffer_start+block[0], sjis_buffer))
                        sjis_buffer = b''
                        sjis_buffer_start = cursor

                # Catch anything left after exiting the loop
                if sjis_buffer:
                    sjis_strings.append((sjis_buffer_start+block[0], sjis_buffer))


                if len(sjis_strings) == 0:
                    continue

                for s in sjis_strings:
                    if len(s[1]) < THRESHOLD:
                        continue

                    loc = '0x' + hex(s[0]).lstrip('0x').zfill(5)
                    try:
                        jp = s[1].decode('shift-jis')
                    except UnicodeDecodeError:
                        print("Couldn't decode that")
                        continue

                    if len(jp.strip()) == 0:
                        continue

                    if '=' in jp:
                        jp = jp.replace('=', '[=]')

                    print(loc, jp)

                    worksheet.write(row, 0, loc)
                    worksheet.write(row, 1, jp)
                    worksheet.write(row, 2, '=LEN(B%s)' % str(row+1))
                    #worksheet.write(row, 3, filename)
                    row += 1

    workbook.close()

if __name__ == '__main__':
    workbook = xlsxwriter.Workbook('bustin_dump.xlsx')
    header = workbook.add_format({'bold': True, 'align': 'center', 'bottom': True, 'bg_color': 'gray'})
    dump(FILES)


# TODO: It'd be even better if it just took a disk, or a bunch of disks, and used ndc to get files.
# TODO: Column for disks

# TODO: Export the dump to a google doc as well?

# TODO: Detect blocks and export that to a skeleton rominfo.py file.
    # (That could help with detecting some of the one-string-only "blocks" in code sections.)
