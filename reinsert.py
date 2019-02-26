"""
    Possessioner reinserter.
    Based on the CRW reinserter base via TBS98-II.
"""

import os
from mcv import compress

from rominfo import ORIGINAL_ROM_PATH, TARGET_ROM_PATH, DUMP_XLS_PATH, FILES_TO_REINSERT, FILE_BLOCKS
from romtools.disk import Disk, Gamefile, Block
from romtools.dump import DumpExcel, PointerExcel

Dump = DumpExcel(DUMP_XLS_PATH)
OriginalTBS = Disk(ORIGINAL_ROM_PATH, dump_excel=Dump)
TargetTBS = Disk(TARGET_ROM_PATH)

for filename in FILES_TO_REINSERT:
    path_in_disk = "TBS\\"
    if filename.endswith(".MCV"):
        print(filename)
        gamefile_path = os.path.join('original/decompressed/', filename)
    else:
        gamefile_path = os.path.join('original', filename)
    print(filename)
    gamefile = Gamefile(gamefile_path, disk=OriginalTBS, dest_disk=TargetTBS)

    if filename == 'TBS.EXE':
        # Ascii text hack for the main menu, see notes.md
        gamefile.edit(0xe51d, b'\x08\xc0\x74\xf6\x3c\x20\x72\x19\x3c\x80\x72\x0b\x3c\x9f\x76\x19\x3c\xe0\x73\x0b\xe9\x81\xff\xb4\x82\x90\x90\xeb\x09\x90\x90')

        gamefile.edit(0xe4e1, b'\x85')  # font table change
        gamefile.edit(0xe41e, b'\x01')  # cursor change

        # Freeing up all of ascii space for "direct" display
        #gamefile.edit(0xe4c3, b'\x14')  # better jump
        #gamefile.edit(0xe4cb, b'\x0c')
        #gamefile.edit(0xe4d2, b'\x76\x04')
        #gamefile.edit(0xe4d4, b'\xfe\xc0\x90\x90\x90\x90\x90\x90\x90\x90')


    for block in FILE_BLOCKS[filename]:
        block = Block(gamefile, block)
        print(block)
        previous_text_offset = block.start
        diff = 0
        if filename.endswith(".MCV"):
            sheet_name = filename.split("/")[-1]
        else:
            sheet_name = filename
        for i, t in enumerate(Dump.get_translations(block, include_blank=True, sheet_name=sheet_name)):
            #print(t.english)
            loc_in_block = t.location - block.start + diff

            this_diff = len(t.en_bytestring) - len(t.jp_bytestring)

            if t.english == b'' or t.english == t.japanese:
                #print(hex(t.location), t.english, "Blank string")
                this_diff = 0
                #print("Diff is", diff)

                #gamefile.edit_pointers_in_range((previous_text_offset, t.location), diff)
                previous_text_offset = t.location
                continue

            try:
                i = block.blockstring.index(t.jp_bytestring)
            except ValueError:
                print(t, "wasn't found in the string. Skipping for now")
                continue
            j = block.blockstring.count(t.jp_bytestring)

            # Does this do anything????
            index = 0
            while index < len(block.blockstring):
                index = block.blockstring.find(t.jp_bytestring, index)
                #print("Found it at", hex(index))
                if index == -1:
                    break
                index += len(t.jp_bytestring) # +2 because len('ll') == 2

            assert loc_in_block == i, (t, hex(loc_in_block), hex(i))
            #while loc_in_block != i:

            block.blockstring = block.blockstring.replace(t.jp_bytestring, t.en_bytestring, 1)
            #print(block.blockstring)

            #gamefile.edit_pointers_in_range((previous_text_offset, t.location), diff)
            previous_text_offset = t.location

            diff += this_diff
            #print("Diff is", diff)

        #print("Looking for:", block.original_blockstring)
        block.incorporate()

    if filename.endswith(".MCV"):
        gamefile.write(path_in_disk=path_in_disk, skip_disk=True, dest_path=filename.replace("original/", ""))
        compress(filename)
        compressed_filename = 'patched/%s' % filename
        print(compressed_filename)
        cgf = Gamefile(compressed_filename, disk=OriginalTBS, dest_disk=TargetTBS)
        cgf.write(path_in_disk='TBS/SCN')
    else:
        gamefile.write(path_in_disk=path_in_disk)
