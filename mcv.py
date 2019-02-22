"""
    Parse the .MCV text files for TTB.
    They are in a compressed/obfuscated format, see notes.md for more info.
"""

import os
from rominfo import CTRL

def decompress(filename):
    # Flip all the bits first
    with open("TBS/SCN/%s" % filename, 'rb') as f:
        contents = f.read()
        with open("flipped/%s" % filename, 'wb') as g:
            for c in contents:
                g.write((c ^ 0xff).to_bytes(1, 'little'))

    with open("flipped/%s" % filename, 'rb') as f:
        contents = f.read()
        cursor = 0
        result = b''
        while cursor < len(contents):
            b = contents[cursor]
            # Weird control code type stuff
            if b == 0x0:
                result += b'[END]'
            elif b <= 0xf:
                if b in CTRL:
                    result += CTRL[b]
                else:
                    result += b'[%i]' % b
                #result += b'?'
            elif b <= 0x16:
                cursor += 1
                b2 = contents[cursor]
                #b2 = b2 ^ 0xff
                result += b.to_bytes(1, 'little')
                result += b2.to_bytes(1, 'little')

            # Aspirated hiragana
            elif b <= 0x1f:
                result += CTRL[b]

            # Punctuation 1
            elif b <= 0x2f:
                result += CTRL[b]

            # Numbers
            elif b <= 0x39:
                result += CTRL[b]

            # Punctuation 2
            elif b  <= 0x40:
                result += CTRL[b]

            # Fullwidth caps
            elif b <= 0x5f:
                result += CTRL[b]

            # other stuff
            elif b <= 0x7f:
                result += CTRL[b]

            # Normal SJIS, but flip 2nd byte again
            elif b <= 0x9f:
                cursor += 1
                b2 = contents[cursor]
                #b2 = b2 ^ 0xff
                result += b.to_bytes(1, 'little')
                result += b2.to_bytes(1, 'little')

            # More stuff
            elif b <= 0xe0:
                result += CTRL[b]

            elif b <= 0xef:
                cursor += 1
                #b2 = contents[cursor]
                b2 = b2 ^ 0xff
                result += b.to_bytes(1, 'little')
                result += b2.to_bytes(1, 'little')

            elif b <= 0xff:
                result += CTRL[b]
            cursor += 1
        with open("decompressed/%s" % filename, 'wb') as g:
            g.write(result)

if __name__ == "__main__":
    for filename in os.listdir("TBS/SCN"):
        if filename.endswith(".MCV"):
            print(filename)
            decompress(filename)
    #decompress("SEN000A.MCV")