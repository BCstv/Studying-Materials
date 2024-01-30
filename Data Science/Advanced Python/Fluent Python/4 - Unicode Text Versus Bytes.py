# Character Issues

# The concept of "string" is simple enough: a string is a sequence of characters. The problem lies in the definition of

# "character"
# The best definition of "character" we have is a Unicode character. Accordingly, the items we get out of a Python3 str
# are Unicode characters

# The identity of a character --its code point-- is a number from 0 to 1,114,111(base-10), shown in the Unicode standard
# as 4 to 6 hex digits with U+ prefix, from U+0000 to U+10FFF


# The actual bytes that represent a character depend on the encoding in use.
# An encoding is an algorithm that converts code points to byte sequences and vice versa

# 'A'-(U+0041) -> \x41 (1 byte) | UTF-8
# 'A'-(U+0041) -> \x41\x00 (2 bytes) | UTF-16LE

# '€'-(U+20AC) -> \xe2\x82\xac (3 bytes) | UTF-8
# '€'-(U+20AC) -> \xac\x20 (2 bytes) | UTF-16LE

s = 'café'
print(s)
print(len(s))

b = s.encode('UTF-8')
print(b)  # é => \xc3\xa9
print(len(b))  # b has five bytes

print(b.decode('UTF-8'))

a = b'\xe2\x82\xac'
print(a.decode('UTF-8'))

# ----------------------------------------------------------------------------------------------------------------------
# Byte Essentials

cafe = bytes('café', 'UTF-8')  # bytes can be built from a str, given an encoding
print(cafe[0])  # Each item is an integer in range(256)
print(cafe[-2:])  # Slice bites are also bytes - even slices of a single byte

cafe_arr = bytearray(cafe)

print(cafe_arr)  # There is no literal syntax for bytearray: they are shown as bytearray() with bytes literal as argument
print(cafe_arr[:-1])  # A slice of byte array is also a bytearray
print(len(cafe_arr))

# * For bytes with decimal codes 32 to 126 -- from space to ~ (tilde) -- the ASCII character itself is used
# * For bytes corresponding to tab, newline, carriage return, and \, the escape sequences \t, \n, \r, and \\ are used
# * If both string delimiters ' and " appear in the byte sequence, the whole sequence is delimited by ', and any ' inside are escaped as \'
# * For other byte values, a hexadecimal escape sequence is used (\x00 is null byte)

# That is why in the previous code, the word café was encoded as b'caf\xc3\xa9': the first three bytes b'caf' are in the printable ASCII range

print(chr(65))

# ! Both bytes and bytearray support string methods except formatting ones (format, format_map), and those which depend on
# the Unicode data (isnumeric, isdecimal, isprintable, isidentifier, and encode)

print(bytes.fromhex('31 4B CE A9').decode('UTF-8'))

from array import array
octets = bytes(array('h', [41, -1, 0, 1, 2]))
print(octets)

'''
latin1 a.k.a. iso8859_1
    Important because it is the basis for other encodings, such as cp1252 and Unicode itself (note how the latin1 byte
    values appear in the cp1252 bytes and even in the code points

cp1252
    A useful latin1 superset created by Microsoft, adding useful symbols like curly quotes and euro; some Windows apps
    call it 'ANSI', but it was never a real ANSI instead
    
cp437
    The original character set of the IBM PC, with box drawing characters. Incompatible with latin1, which appeared later
    
gb2312
    Legacy standard to encode the simplified Chinese ideographs used in mainland China; one of several widely deployed 
    multibyte encodings for Asian languages

utf-8
    The most common 8-bit encoding on the web, by far, as of  July 2021, "W^3Techs" claims that 98% of sites use UTF-8

utf-16le
    One form of the UTF 16-bit encoding scheme; all UTF-16 encoding support code points beyond U+FFFF through escape
    sequences called "surrogate pairs"
'''
# ----------------------------------------------------------------------------------------------------------------------

# Understanding Encode/Decode Problems

# Coping with UnicodeEncodeError

city = 'São Paulo'

print(city.encode('UTF-8'))  # The Utf encodings handle any str
print(city.encode('UTF-16'))
print(city.encode('iso8859_1'))  # also works for the given string
# print(city.encode('cp437'))  # can't encode the ã. The default error handler ('strict') raises UnicodeEncodeError

print(city.encode('cp437', errors='ignore'))  # The error='ignore' handler skips characters that cannot be encoded

print(city.encode('cp437', errors='replace'))  # When encoding, error='replace' substitutes unencodable characters with '?'

print(city.encode('cp437', errors='xmlcharrefreplace'))  # xmlcharrefreplace replaces unencodable characters with an XML entity
# ^ This is the only option when you cannot use UTF and you can't afford to lose data

# Coping with UnicodeDecodeError
octets = b'Montr\xe9al'  # The word Montréal is encoded as latin1; \xe9 <- é
print(octets.decode('cp1252'))  # Decoding with Windows 1252 works because it is a superset of latin1
print(octets.decode('iso8859_7'))  # ISE8859_7 is intended for Greek, so the \xe9 byte is misinterpreted, and no error is issued
print(octets.decode('koi8_r'))  # KOI8-R is for Russian. Now \xe9 <- И
# print(octets.decode('utf-8'))  # The utf-8 codec detects that octets is not valid utf-8, and raises UnicodeDecodeError
print(octets.decode('utf-8', errors='replace'))  # Using replace to replace \xe9 with �

# ----------------------------------------------------------------------------------------------------------------------

# BOM: A Useful Gremlin
print('El Niño'.encode('utf-16'))

# Why does 'El Niño'.encode('utf-16') looks like (b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00')?
r'''
The bytes are b'\xff\xfe'. That is BOM -byte-order mark- denoting the 'little endian' byte ordering of the Intel CPU 
where the encoding was performed.

On a little-endian machine, for each code point the least significant byte comes first:
the letter 'E', code point U+0045(decimal 69), is encoded in byte offsets 2 and 3 as 69 and 0

list == [255, 254, 69, 0, 108, 0, 32, 0, 78, 0, 105, 0, 241, 0, 111, 0]
       b'\xff\xfeE\x00l\x00\x00N\x00i\x00\xf1\x00o\x00'
       
On a big-endian CPU, the encoding would be reversed;
'E' would be encoded as 0 and 69

To avoid confusion, the utf-16 encoding is prepends the text to be encoded with the special invisible character ZERO
WIDTH NO-BREAK SPACE (U+FEFF) that is encoded as b'\xff\xfe' (decimal 255,254)
'''

# There is a variant of UTF-16 = UTF-16LE that is explicitly little-endian

print('El Niño'.encode('utf-16le'))
print(list('El Niño'.encode('utf-16le')))

print('El Niño'.encode('utf-16be'))
print(list('El Niño'.encode('utf-16be')))

# Caleb's Tip:
def quote(aaa):
    return '!' + aaa + '!'


print(quote('''
    One very respected man in the field is suggesting always using the UTF-8-SIG codec when reading files without a BOM
    correctly, and does not return the BOM itself, but when writing, he recommends to use UTF-8 
'''))

# ----------------------------------------------------------------------------------------------------------------------

# Handling Text Files

# Unicode sandwich (bytes should be decoded to str as early as possible on input) is the best practice for handling text I/O

r'''
 /‾‾‾‾‾‾\  bytes -> str | DECODES BYTES ON INPUT
 ‾‾‾‾‾‾‾‾  100% str     | PROCESS TEXT ONLY
 \‾‾‾‾‾‾‾/ str -> bytes | ENCODE TEXT ON OUTPUT
  ‾‾‾‾‾‾‾
'''

print(open('cafe.txt', 'a', encoding='utf-8').write('café'))
print(open('cafe.txt').read())  # Because I didn't specify an encoding mode, Python assumed to use the default Windows
# file encoding --code page 1252--, that's why it's cafÃ© instead of café

# Page 133

