"""
    I didn't get anything useful from this. No idea what's going on in .SCVs yet
"""

with open("TBS/SCN/SEN000A.SCV", 'rb') as f:
    contents = f.read()
    lines = contents.split(b'\xa0')
    for l in lines:
        print(b' '.join(l.split()))