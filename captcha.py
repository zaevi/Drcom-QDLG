from PIL import Image


captchaCode = '''110011101101011110011110011110011110011110101101110011
110011101011111011111011111011111011111011111011100000
000011111101111101111101111011110111101111011111000001
000011111101111101111011100111111011111101111101100011
111101111001110101101101011101000000111101111101111101
000001011111011111000111111011111101111101111011000111
110000101111011111010011001101011110011110101101110011
000000111110111101111011111011110111110111101111101111
100001011110011110101101100001011110011110011110100001
110011101101011110011110101100110010111110111101000011
'''

Code = []

if not Code:
    captchaCode = captchaCode.splitlines()
    for code in captchaCode:
        Code.append([int(t) for t in code])


def captcha(source):
    img = source if isinstance(source, Image.Image) else Image.open(source)
    imgs = [img.crop((x, 2, x + 6, 2 + 9)) for x in [5, 12, 19, 26]]
    imgCodes = [imageToCode(img) for img in imgs]
    code = [match(code) for code in imgCodes]
    return ''.join([str(c) for c in code])


def imageToCode(img):
    sx, sy = img.size
    code = []
    for y in range(sy):
        for x in range(sx):
            r, g, b = img.getpixel((x, y))
            deep = (r + g + b) // 3
            code.append(0 if deep > 200 else 1)
    return code


def match(code):
    matchValue = [compareCode(stdCode, code) for stdCode in Code]
    return matchValue.index(max(matchValue))


def compareCode(code1, code2):
    matched = [code1[i] and code2[i] for i in range(len(code1))].count(True)
    return matched / code1.count(1)
