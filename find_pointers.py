import os
from collections import OrderedDict
# Need the third-party regex library, which supports overlapping matches
import regex as re
from romtools.dump import BorlandPointer, DumpExcel, PointerExcel
from romtools.disk import Gamefile

from rominfo import POINTER_CONSTANT
from rominfo import FILE_BLOCKS, DUMP_XLS_PATH, FILES_WITH_POINTERS

Dump = DumpExcel(DUMP_XLS_PATH)

# Removing the 9a at the end of this one. Didn't show up in some pointers.
pointer_regex = r'\\xa0\\x16\\x([0-f][0-f])\\x([0-f][0-f])'


def capture_pointers_from_function(hx, regex): 
    return re.compile(regex).finditer(hx, overlapped=True)


def location_from_pointer(pointer, constant):
    return '0x' + str(format((unpack(pointer[0], pointer[1]) + constant), '05x'))


def unpack(s, t=None):
    if t is None:
        t = str(s)[2:]
        s = str(s)[0:2]
    #print(s, t)
    s = int(s, 16)
    t = int(t, 16)
    value = (t * 0x100) + s
    return value


pointer_count = 0

try:
    os.remove('bustin_pointer_dump.xlsx')
except FileNotFoundError:
    pass

PtrXl = PointerExcel('bustin_pointer_dump.xlsx')

for gamefile in FILES_WITH_POINTERS:
    print("Getting pointers for", gamefile)
    pointer_locations = OrderedDict()
    gamefile_path = os.path.join('original', gamefile)

    if gamefile.endswith('.MCV'):
        gamefile_path = os.path.join('original', 'SCN', gamefile)
        GF2 = Gamefile(gamefile_path, pointer_constant=POINTER_CONSTANT[gamefile])
        GF = Gamefile(gamefile_path.replace(".MCV", ".SCV"), pointer_constant=POINTER_CONSTANT[gamefile])
        gamefile_path = gamefile_path.replace(".MCV", ".SCV")

    else:
        GF2 = Gamefile(gamefile_path, pointer_constant=POINTER_CONSTANT[gamefile])
        GF = Gamefile(gamefile_path, pointer_constant=POINTER_CONSTANT[gamefile])


    with open(gamefile_path, 'rb') as f:
        print(gamefile_path)
        bs = f.read()

        # target_area = (GF.pointer_constant, len(bs))
        #print(hex(target_area[0]), hex(target_area[1]))

        only_hex = u""
        for c in bs:
            only_hex += u'\\x%02x' % c


        #print(pointer_regex)
        for regex in (pointer_regex, ):
            if regex is None:
                continue
            print(regex)
            pointers = capture_pointers_from_function(only_hex, regex)

            for p in pointers:
                #print(p)
                # Different offsets for each regex?

                if regex == pointer_regex:
                    pointer_location = p.start()//4 + 2
                else:
                    raise Exception

                text_location = int(location_from_pointer((p.group(1), p.group(2)), GF.pointer_constant), 16)

                pointer_location = '0x%05x' % pointer_location

                all_locations = [int(pointer_location, 16),]

                print(hex(text_location), pointer_location)

                #print(pointer_locations)

                if (GF2, text_location) in pointer_locations.keys():
                    all_locations = pointer_locations[(GF2, text_location)]
                    all_locations.append(int(pointer_location, 16))

                pointer_locations[(GF2, text_location)] = all_locations


    # Setup the worksheet for this file
    worksheet = PtrXl.add_worksheet(GF2.filename)

    row = 1

    try:
        itemlist = sorted((pointer_locations.items()))
    except:
        itemlist = pointer_locations.items()

    for (gamefile, text_location), pointer_locations in itemlist:
        obj = BorlandPointer(gamefile, pointer_locations, text_location)
        #print(hex(text_location))
        #print(pointer_locations)

        # Restrict pointer locations to a particular area when there are dupes
        if text_location == 0x0:
            # Definitely don't use these. They were useful for pointer_lines calculation,
            # but they have served their purpose
            continue
        #print(gamefile)

        for pointer_loc in pointer_locations:
            worksheet.write(row, 0, '0x' + hex(text_location).lstrip('0x').zfill(5))
            worksheet.write(row, 1, '0x' + hex(pointer_loc).lstrip('0x').zfill(5))
            #try:
            #    worksheet.write(row, 2, obj.text())
            #except:
            #    worksheet.write(row, 2, u'')
            row += 1

PtrXl.close()