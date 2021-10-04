"""
    Rom information for Tokyo Twilight Busters (PC-98).
"""

import os
from collections import OrderedDict
from romtools.dump import DumpExcel
from romtools.disk import Disk, Gamefile

ORIGINAL_ROM_PATH = 'original/Tokyo Twilight Busters.hdi'
TARGET_ROM_PATH = 'patched/Tokyo Twilight Busters.hdi'
DUMP_XLS_PATH = 'bustin_dump.xlsx'
POINTER_XLS_PATH = 'bustin_pointer_dump.xlsx'

# Backup sheet, to avoid overwriting a dump that has a bucn hof text in it
BACKUP_XLS_PATH = 'bustin_dump_backup.xlsx'

FILES_TO_REINSERT = [
    'TBS.EXE',
    'AVM.BIN',
    'RTM.BIN',
    #'CLM.BIN',
    'STM.BIN',
    'SEN013R.MCV',
    'SEN013R1.MCV',
    'RTD/MSGS.013',
    'RTD/RTMS.013',
]

FILES_WITH_POINTERS = [
    'TBS.EXE',
    'AVM.BIN',
    'RTM.BIN',
    'STM.BIN',
    'SEN013R.MCV',
    'SEN013R1.MCV',
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
        (0x11030, 0x110af),
        (0x110c9, 0x110df),
        (0x11160, 0x112c6),
        (0x112e6, 0x11311),
        (0x1131e, 0x11334),
        (0x1134b, 0x11370),
        (0x11433, 0x11445),
        (0x11473, 0x11485),
        (0x114b3, 0x114c5),
        (0x114f3, 0x11505),
        (0x11533, 0x11545),
        (0x11573, 0x11585),
        (0x115b3, 0x115c5),
        (0x115f3, 0x11603),
        (0x11633, 0x11642),
        (0x1164f, 0x1165f),  # Annoying table
        (0x1166c, 0x1167c),
        (0x11689, 0x11699),
        (0x116a6, 0x116b6),
        (0x116c3, 0x116d3),
        (0x116e0, 0x116f0),
        (0x116fd, 0x1170d),
        (0x1171a, 0x1172a),
        (0x11737, 0x11747),
        (0x11754, 0x11764),
        (0x11771, 0x11781),
        (0x1178e, 0x1179e),
        (0x117ab, 0x117bb),
        (0x117c8, 0x117d8),
        (0x117e5, 0x117f5),
        (0x11802, 0x11812),
        (0x1181f, 0x1182f),
        (0x1183c, 0x1184c),
        (0x11859, 0x11869),
        (0x11876, 0x11886),
        (0x11893, 0x118a3),
        (0x118b0, 0x118c0),
        (0x118cd, 0x118dd),
        (0x118ea, 0x118fa),
        (0x11907, 0x11917),
        (0x11924, 0x11934),
        (0x11941, 0x11951),
        (0x1195e, 0x1196e),
        (0x1197b, 0x1198b),
        (0x11998, 0x119a8),
        (0x119b5, 0x119c5),
        (0x119d2, 0x119e2),
        (0x119ef, 0x119ff),
        (0x11a0c, 0x11a1c),
        (0x11a29, 0x11a39),
        (0x11a46, 0x11a56),
        (0x11a63, 0x11a73),
        (0x11a80, 0x11a90),
        (0x11a9d, 0x11aad),
        (0x11aba, 0x11aca),
        (0x11ad7, 0x11ae7),
        (0x11af4, 0x11b04),
        (0x11b11, 0x11b21),
        (0x11b2e, 0x11b3e),
        (0x11b4b, 0x11b5b),
        (0x11b68, 0x11b78),
        (0x11b85, 0x11b95),
        (0x11ba2, 0x11bb2),
        (0x11bbf, 0x11bcf),
        (0x11bdc, 0x11bec),
        (0x11bf9, 0x11c09),
        (0x11c16, 0x11c26),
        (0x11c33, 0x11c43),
        (0x11c50, 0x11c60),
        (0x11c6d, 0x11c7d),
        (0x11c8a, 0x11c9a),
        (0x11ca7, 0x11cb7),
        (0x11cc4, 0x11cd4),
        (0x11ce1, 0x11cf1),
        (0x11cfe, 0x11d0e),
        (0x11d1b, 0x11d2b),
        (0x11d38, 0x11d48),
        (0x11d55, 0x11d65),
        (0x11d72, 0x11d82),
        (0x11d8f, 0x11d9f),
        (0x11dac, 0x11dbc),
        (0x11dc9, 0x11dd9),
        (0x11de6, 0x11df6),
        (0x11e03, 0x11e13),
        (0x11e20, 0x11e30),
        (0x11e3d, 0x11e4d),
        (0x11e5a, 0x11e6a),
        (0x11e77, 0x11e87),
        (0x11e94, 0x11ea4),
        (0x11eb1, 0x11ec1),
        (0x11ece, 0x11ede),
        (0x11eeb, 0x11efb),
        (0x11f08, 0x11f18),
        (0x11f25, 0x11f35),
        (0x11f42, 0x11f52),
        (0x11f5f, 0x11f6f),
        (0x11f7c, 0x11f8c),
        (0x11f99, 0x11fa9),
        (0x11fb6, 0x11fc6),
        (0x11fd3, 0x11fe3),
        (0x11ff0, 0x12000),
        (0x1200d, 0x1201d),
        (0x1202a, 0x1203a),
        (0x12047, 0x12057),
        (0x12064, 0x12074),
        (0x12081, 0x12091),
        (0x1209e, 0x120ae),
        (0x120bb, 0x120cb),
        (0x120d8, 0x120e8),
        (0x120f5, 0x12105),
        (0x12112, 0x12122),
        (0x1212f, 0x1213f),
        (0x1214c, 0x1215c),

        (0x1216a, 0x1225f),

        (0x12490, 0x13790), # another big unsafe table
        (0x15ad2, 0x15b64), # system stuff?
        (0x16778, 0x16792), # date stuff
        (0x16880, 0x15925), # stats?
        (0x1696f, 0x16a2d),
        (0x16a7b, 0x16a93),
        (0x16ac3, 0x16b39),
        (0x16b64, 0x16cf2),
    ],
    'AVM.BIN': [
        (0x5ed6, 0x60b6),
        (0x616e, 0x621c),
        (0x6f38, 0x6fe3),
        (0x7087, 0x719a),
        (0x7355, 0x7390),
        (0x741f, 0x7dd6),
        (0x7e44, 0x7e61),
        (0x7f9a, 0x805d),
        (0x8095, 0x8102),
        (0x8222, 0x824c),
        (0x82d0, 0x83c5),
        (0x83d5, 0x84b4),
        (0x84c5, 0x8bdf),
        (0x8bef, 0x8cd2),
    ],
    'CLM.BIN': [
        (0x2698, 0x4f1e),
        (0x4f4e, 0x4f90),
        (0x4fd0, 0x5039),
        (0x5040, 0x505e),
        (0x50a5, 0x5110),
        (0x5217, 0x53f6),
    ],
    'FTM.BIN': [
        (0x3c9f, 0x3d0c),
        (0x3e2c, 0x3e36),
        (0x3e41, 0x3e55),
        (0x3eaa, 0x3f5e),
        (0x3fbb, 0x401f),
        (0x424b, 0x47fb),
        (0x4833, 0x4c06),
        (0x4c36, 0x4f4a),
        (0x4f7a, 0x5101),
        (0x5131, 0x53a5),
        (0x53dd, 0x5564),
        (0x5634, 0x58bb),
        (0x58cb, 0x593a),
        (0x5973, 0x5b85),
        (0x5bc1, 0x5c40),
        (0x5c52, 0x5d38),
        (0x5d5c, 0x5f46),
        (0x5f64, 0x60ae),
        (0x60d1, 0x630d),
        (0x6392, 0x6577),
        (0x6587, 0x6ed7),
        (0x6eed, 0x6efd), # Hell table
        (0x6f0a, 0x6f1a),
        (0x6f27, 0x6f37),
        (0x6f44, 0x6f54),
        (0x6f61, 0x6f71),
        (0x6f7e, 0x6f8e),
        (0x6f9b, 0x6fab),
        (0x6fb8, 0x6fc8),
        (0x6fd5, 0x6fe5),
        (0x6ff2, 0x7002),
        (0x700f, 0x701f),
        (0x702c, 0x703c),
        (0x7049, 0x7059),
        (0x7066, 0x7076),
        (0x7083, 0x7093),
        (0x70a0, 0x70b0),
        (0x70bd, 0x70cd),
        (0x70da, 0x70ea),
        (0x70f7, 0x7107),
        (0x7114, 0x7124),
        (0x7131, 0x7141),
        (0x714e, 0x715e),
        (0x716b, 0x717b),
        (0x7188, 0x7198),
        (0x71a5, 0x71b5),
        (0x71c2, 0x71de), # End
    ],
    'RTM.BIN': [
        (0xeb72, 0xece0),
        (0xf2ae, 0xf2d2),
        (0xf2dc, 0x12a3c),
        (0x12a46, 0x12a9c),
        (0x12aa8,  0x12ab8),
        (0x12ac6, 0x12ad5),
        (0x12ae3, 0x12af2),
        (0x12b02, 0x12b11),
        (0x12b1b, 0x12b70),
        (0x12b7e, 0x12b8d),
        (0x12b9b, 0x12baa),
        (0x12bb8, 0x12bc7),
        (0x12bd7, 0x12c27),
        (0x16984, 0x169c1),
        (0x169f6, 0x16b0b),
        (0x16b3b, 0x16b84),
        (0x16baa, 0x16bfc),
    ],
    'STM.BIN': [
        (0x1586, 0x15ff),
        (0x1748, 0x177f),
        (0x180a, 0x18ff),
        (0x190f, 0x19ed),
        (0x19ff, 0x20c5),
        (0x20c5, 0x2126),
        (0x2136, 0x2218),
    ],
    'MPM.BIN': [
        (0x4040, 0x4bdf),
        (0x8ca3, 0x8cae),
    ],
    'EDM.BIN': [
        (0x5009, 0x5e13),
        (0x606d, 0x6729),
    ],
    'RTD/MSGS.001': [
        (0xf4, 0x8c44),
    ],

    'RTD/MSGS.013': [
        (0xf0, 0x2d2a),
    ],

    'RTD/RTMS.013': [
        (0x15a0, 0x3670),
    ],

    'SEN013R.MCV': [
        (0x0, 0x1250),
    ],

    'SEN013R1.MCV': [
        (0x0, 0x1250),
    ],
}

POINTER_CONSTANT = {
    'TBS.EXE': 0x10950, 
    'RTM.BIN': 0xea50,
    'STM.BIN': 0x1580,
    'AVM.BIN': 0x5c90,
    'SEN013R.MCV': 0x0,
    'SEN013R1.MCV': 0x0,
}

"""
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
        #FILE_BLOCKS[file] = blocks

"""

for file in os.listdir('original/decompressed'):
    FILES.append(os.path.join('decompressed', file))

FILE_CATEGORIES = OrderedDict({
    "System": ["TBS.EXE", "RTM.BIN", "STM.BIN", "AVM.BIN", "MPM.BIN", "FTM.BIN", "CLM.BIN", "EDM.BIN", "TOKYO.DAT", "INIT.DAT", "NEWS.MCV"],
    "Prologue": ["SEN013R.MCV", "SEN013R1.MCV", "RTMS.013"],
    "Chapter 1": ["SEN000A.MCV", "SEN000A1.MCV", "SEN000A6.MCV", "SEN000A7.MCV", "SEN000A8.MCV", "SEN000A9.MCV"],
});


inline_CTRL = {
    0x04: b'[4]',
    0x05: b'[5]',
    0x06: b'[6]',
    0x07: b'[7]',
    0x08: b'[8]',
    0x09: b'[9]',
    #0x0a: b'[A]',
    0x0b: b'[B]',
    0x0c: b'[C]',
    #0x0d: b'[D]',
    0x0e: b'[E]',
    0x0f: b'[F]',
}

CTRL = {
    0x00: b'[END]',
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
    0x10: b'[10]',  # Used for coloring text in pink/orange for a nametag within text. 100e = start, 100f = end. Defined below
    0x11: b'[11]',  # Unknown, seems similar to [12] below, usually by itself after nametags or with 4/5/6 afterwards.
    0x12: b'[12]', # Unknown. Usually [12][4], 5, or 6. Sometimes right before an END. Maybe a speed/pause thing?
    0x13: b'[13]',
    0x14: b'[14]',
    0x15: b'[15]',

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
    0xa4: b'\x81\x41',     # The game prefers to use 0x2c for 8141
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

    # TODO: Disabling this for now
    #b'\x86\xad': b'\x81\x5c', # formerly [LINE]
    b'\x86\x91': b'[8691]',
    b'\x86\x9c': b'[869c]',
    b'\x86\x9d': b'[869d]',

    b'\x10\x0e': b'[Nametag]',
    b'\x10\x0f': b'[/Nametag]',
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
    #print(hex(n), CTRL[n])

CTRL[0xb0] = b'\x81\x5b' # Long dash
# b1 should code for little ぁ
#CTRL[0xb1] = b'\x81\x5b'   # long dash; no idea why this overrides the list entry

inverse_CTRL = {v: k for k, v in CTRL.items() if k != 0xa4}
#inverse_CTRL.remove(0xa4)