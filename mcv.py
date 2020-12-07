"""
    Parse the .MCV text files for TTB.
    They are in a compressed/obfuscated format, see notes.md for more info.
"""

import os
from rominfo import CTRL, inverse_CTRL

def decompress_file(filename):
    # Flip all the bits first
    with open("original/SCN/%s" % filename, 'rb') as f:
        flipped_contents = f.read()
        contents = b''
        for c in flipped_contents:
            contents += (c ^ 0xff).to_bytes(1, 'little')

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
            elif b <= 0x15:
                b2 = contents[cursor+1]
                #print(b, b2, b.to_bytes(1, 'little') + b2.to_bytes(1, 'little'))
                if b.to_bytes(1, 'little') + b2.to_bytes(1, 'little') in CTRL:
                    result += CTRL[b.to_bytes(1, 'little') + b2.to_bytes(1, 'little')]
                    cursor += 1
                else:
                    result += CTRL[b]

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
            elif b <= 0x40:
                result += CTRL[b]

            # Fullwidth caps
            elif b <= 0x5f:
                result += CTRL[b]

            # other stuff
            elif b <= 0x7f:
                result += CTRL[b]

            elif b == 0x86:
                cursor += 1
                b2 = contents[cursor]
                if b2 == 0xa2:
                    result += b'\x81\x5c'
                elif b2 == 0x91:
                    result += b'[8691]'
                elif b2 == 0x9c:
                    result += b'[869c]'
                elif b2 == 0x9d:
                    result += b'[869d]'
                else:
                    input()

            # Normal SJIS, but flip 2nd byte again
            # TODO: Or not?? The flip is disabled
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
        with open("original/decompressed/%s" % filename, 'wb') as g:
            #if b'\x86\xa2' in result:
            #    print("It has a line control code in it")
            g.write(result)

def compress(s):
    result = b''
    cursor = 0
    #print(len(s))
    while cursor < len(s):
        b = s[cursor]

        # two-byte commands, two-byte Japanese text
        if b <= 0x16 or 0x80 <= b <= 0x9f or 0xe0 <= b <= 0xea:
            cursor += 1
            b2 = s[cursor]

            code = b'' + b.to_bytes(1, 'little') + b2.to_bytes(1, 'little')
            #print(code)
            if code in inverse_CTRL:
                #print(code, "is a ctrl code for", hex(inverse_CTRL[code]))
                try:
                    result += inverse_CTRL[code].to_bytes(1, 'little')
                except AttributeError:
                    result += inverse_CTRL[code]
            else:
                #print(code, "is not a control code")
                result += b.to_bytes(1, 'little')
                result += b2.to_bytes(1, 'little')

        # Defined control codes within brackets
        elif s[cursor] == 0x5b: # '['
            code = b''
            while s[cursor] != 0x5d:
                code += s[cursor].to_bytes(1, 'little')
                cursor += 1
            code += s[cursor].to_bytes(1, 'little')
            assert code in inverse_CTRL, code

            try:
                result += inverse_CTRL[code].to_bytes(1, 'little')
            except AttributeError:
                # [LINE] and a few others are defined with two codes
                result += inverse_CTRL[code]

        # Ascii text
        else:
            result += s[cursor].to_bytes(1, 'little')

        cursor += 1

    flipped_result = b''
    for ch in result:
        flipped_result += (ch ^ 0xff).to_bytes(1, 'little')

    return flipped_result

def compress_file(filename):
    with open("patched/decompressed/%s" % filename, 'rb') as f:
        contents = f.read()

    result = compress(contents)

    # Switching g and h to double-flip the human-readable one
    with open("patched/%s" % filename, 'wb') as h:
        with open("patched/%s" % filename.replace(".MCV", "_readable.MCV"), 'wb') as g:
            # Flip all the bytes again
            for r in result:
                h.write(r.to_bytes(1, 'little')) # FOr a sanity check first
                g.write((r ^ 0xff).to_bytes(1, 'little'))

if __name__ == "__main__":
    for filename in os.listdir("TBS/SCN"):
        if filename.endswith(".MCV"):
            print(filename)
            decompress_file(filename)

    compress_file("SEN013R.MCV")