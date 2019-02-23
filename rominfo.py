"""
    Rom information for Tokyo Twilight Busters (PC-98).
"""

import os
from romtools.dump import DumpExcel
from romtools.disk import Disk, Gamefile

ORIGINAL_ROM_PATH = 'original/Tokyo Twilight Busters.hdi'
TARGET_ROM_PATH = 'patched/Tokyo Twilight Busters.hdi'
DUMP_XLS_PATH = 'bustin_dump.xlsx'

FILES_TO_REINSERT = [
    'TBS.EXE',
]

FILES = [
    'TBS.EXE',
    'AVM.BIN',
    'CLM.BIN',
    'EDM.BIN',
    'FTM.BIN',
    'MPM.BIN',
    'RTM.BIN',
    'STM.BIN',
    'RTD/MSGS.001',
    'RTD/MSGS.004',
    'RTD/MSGS.005',
    'RTD/MSGS.007',
    'RTD/MSGS.010',
    'RTD/MSGS.012',
    'RTD/MSGS.013',
    'RTD/RTMS.001',
    'RTD/RTMS.004',
    'RTD/RTMS.005',
    'RTD/RTMS.007',
    'RTD/RTMS.010',
    'RTD/RTMS.012',
    'RTD/RTMS.013',
    'ABG/TOKYO.DAT',
    'DAT/INIT.DAT',
]

FILE_BLOCKS = {
    'TBS.EXE': [
        (0x109b0, 0x10bc9), # dev/programming info
        (0x10c46, 0x10cd6),
        (0x10e74, 0x10e7c),
        (0x10e8e, 0x10ea3),
        (0x10f1c, 0x11014),
        (0x11030, 0x110de),
        (0x11060, 0x112c6),
        (0x112e6, 0x11311),
        (0x1131e, 0x11334),
        (0x1134b, 0x11370),
        (0x11430, 0x12260), # big table of stuff, probably need to edit carefully
        (0x12490, 0x13790), # another big unsafe table
        (0x15ad2, 0x15b64), # system stuff?
        (0x16778, 0x16792), # date stuff
        (0x16880, 0x15925), # stats?
        (0x1696f, 0x16a2d),
        (0x16a7b, 0x16a93),
        (0x16ac3, 0x16b39),
        (0x16b64, 0x16cf2),
    ],
    'STM.BIN': [
        (0x1586, 0x15ff),
        (0x1748, 0x177f),
        (0x180a, 0x19ed),
        (0x19ff, 0x2125),
        (0x213b, 0x2218),
    ],
    'RTD/MSGS.001': [
        (0xf4, 0x8c44),
    ],
}


# Auto-generate file blocks when they are not manually defined
Dump = DumpExcel(DUMP_XLS_PATH)
OriginalTBS = Disk(ORIGINAL_ROM_PATH, dump_excel=Dump)
TargetTBS = Disk(TARGET_ROM_PATH)
for file in FILES:
    print(file)
    if file not in FILE_BLOCKS and file in FILES:
        print(file, "not in FILE_BLOCKS")
        if file.endswith('MCV'):
            file_path = file
        else:
            file_path = os.path.join('TBS', file)
        gf = Gamefile(file_path, disk=OriginalTBS, dest_disk=TargetTBS, pointer_constant=0)

        blocks = []
        start = None
        last_string_end = None
        if file.endswith('MCV'):
            translations = Dump.get_translations(file, include_blank=True)
        else:
            if "/" in file:
                sheet_name = file.replace("/", "-")
            else:
                sheet_name = file
            print(sheet_name)
            translations = Dump.get_translations(sheet_name, include_blank=True)
        for t in translations:

            if not start:
                start = t.location
            else:
                distance = t.location - last_string_end
                # Just seems like a good number
                if distance > 17:
                    blocks.append((start, last_string_end))
                    start = t.location
            last_string_end = t.location + len(t.jp_bytestring)
        blocks.append((start, last_string_end))
        for b in blocks:
            print("(%s, %s)" % (hex(b[0]), hex(b[1])))
        FILE_BLOCKS[file] = blocks



for file in os.listdir('decompressed'):
    FILES.append(os.path.join('decompressed', file))

inline_CTRL = {
    b'[4]',
    b'[5]',
    b'[6]',
    b'[7]',
    b'[8]',
    b'[9]',
    b'[A]',
    b'[B]',
    b'[C]',
    b'[D]',
    b'[E]',
    b'[F]',
}

CTRL = {
    0x01: b'[LN]',
    0x02: b'[WAIT]',
    0x03: b'[CLR]',
    0x04: b'[4]',
    0x05: b'[5]',
    0x06: b'[6]',
    0x07: b'[7]',
    0x08: b'[8]',
    0x09: b'[9]',
    0x0a: b'[A]',
    0x0b: b'[B]',
    0x0c: b'[C]',
    0x0d: b'[D]',
    0x0e: b'[E]',
    0x0f: b'[F]',

    0x16: b'\x82\xce',  # ば び  ぶ べ  ぼ ぱ ぴ  ぷ  ぺ ぽ
    0x17: b'\x82\xd1',
    0x18: b'\x82\xd4',
    0x19: b'\x82\xd7',
    0x1a: b'\x82\xda',
    0x1b: b'\x82\xcf',
    0x1c: b'\x82\xd2',
    0x1d: b'\x82\xd5',
    0x1e: b'\x82\xd8',
    0x1f: b'\x82\xdb',

    0x20: b'\x81\x40',  # sp !  ”  #  $  %  &  ’  (  )  *  +  、  -  .  /
    0x21: b'\x81\x49',
    0x22: b'\x81\x68',
    0x23: b'\x81\x94',
    0x24: b'\x81\x90',
    0x25: b'\x81\x93',
    0x26: b'\x81\x95',
    0x27: b'\x81\x66',
    0x28: b'\x81\x69',
    0x29: b'\x81\x6a',
    0x2a: b'\x81\x96',
    0x2b: b'\x81\x7b',
    0x2c: b'\x81\x41',
    0x2d: b'\x81\x7c',
    0x2e: b'\x81\x44',
    0x2f: b'\x81\x5e',

    0x30: b'\x82\x4f',  # Numbers
    0x31: b'\x82\x50',
    0x32: b'\x82\x51',
    0x33: b'\x82\x52',
    0x34: b'\x82\x53',
    0x35: b'\x82\x54',
    0x36: b'\x82\x55',
    0x37: b'\x82\x56',
    0x38: b'\x82\x57',
    0x39: b'\x82\x58',

    0x3a: b'\x81\x46',  # :  ;  <  =  >  ?  @
    0x3b: b'\x81\x47',
    0x3c: b'\x81\x83',
    0x3d: b'\x81\x81',
    0x3e: b'\x81\x84',
    0x3f: b'\x81\x48',
    0x40: b'\x81\x97',

    # 41-5a defined programmatically

    0x5b: b'\x81\x6d',  # [ ￥  ]  ^  _  ‘
    0x5c: b'\x81\x8f',
    0x5d: b'\x81\x6e',
    0x5e: b'\x81\x4f',
    0x5f: b'\x81\x51',
    0x60: b'\x81\x65',

    # 61-7a programmatically

    0x7b: b'\x81\x6f',  # {  ‖  }  ~  sp
    0x7c: b'\x81\x62',
    0x7d: b'\x81\x70',
    0x7e: b'\x81\x60',
    0x7f: b'\x81\x40',

    # 80-9f are SJIS

    0xa0: b'\x81\x40',  # sp 。   「 」  、  ・
    0xa1: b'\x81\x42',
    0xa2: b'\x81\x75',
    0xa3: b'\x81\x76',
    0xa4: b'\x81\x41',
    0xa5: b'\x81\x45',

    # a6-e0 programmatically
    # e1-ef are SJIS aa ac ae b0 b2 b4 b6 b8 ba bc be c0 c3 c5 c7

    0xf0: b'\x82\xaa',  # が  ぎ ぐ げ  ご  ざ  じ ず  ぜ  ぞ だ  ぢ づ  で ど...
    0xf1: b'\x82\xac',
    0xf2: b'\x82\xae',
    0xf3: b'\x82\xb0',
    0xf4: b'\x82\xb2',
    0xf5: b'\x82\xb4',
    0xf6: b'\x82\xb6',
    0xf7: b'\x82\xb8',
    0xf8: b'\x82\xba',
    0xf9: b'\x82\xbc',
    0xfa: b'\x82\xbe',
    0xfb: b'\x82\xc0',
    0xfc: b'\x82\xc3',
    0xfd: b'\x82\xc5',
    0xfe: b'\x82\xc7',
    0xff: b'\x82\xce',
}

for n in range(0x41, 0x5b):
    CTRL[n] = b'\x82' + (0x1f + n).to_bytes(1, 'little')

for n in range(0x61, 0x7b):
    CTRL[n] = b'\x82' + (0x1f + n).to_bytes(1, 'little')

# There's one (wo) at the end, and the rest are one too low. Shift and see what happens
ls = [ b'\xf0', b'\x9f', b'\xa1', b'\xa3', b'\xa5', b'\xa7', b'\xe1', b'\xe3', b'\xe5', 
       b'\xc1', b'\x00', b'\xa0', b'\xa2', b'\xa4', b'\xa6', b'\xa8', b'\xa9', b'\xab', 
       b'\xad', b'\xaf', b'\xb1', b'\xb3', b'\xb5', b'\xb7', b'\xb9', b'\xbb', b'\xbd', 
       b'\xbf', b'\xc2', b'\xc4', b'\xc6', b'\xc8', b'\xc9', b'\xca', b'\xcb', b'\xcc', 
       b'\xcd', b'\xd0', b'\xd3', b'\xd6', b'\xd9', b'\xdc', b'\xdd', b'\xde', b'\xdf', 
       b'\xe0', b'\xe2', b'\xe4', b'\xe6', b'\xe7', b'\xe8', b'\xe9', b'\xea', b'\xeb', 
       b'\xed', b'\xf1', b'\xaa', b'\xac', b'\xae', b'\xb0']

for n in range(0xa6, 0xe1):
    #print(ls[n - 0xa6])
    CTRL[n] = b'\x82' + ls[n - 0xa6]

CTRL[0xb1] = b'\x81\x5b'   # long dash; no idea why this overrides the list entry
