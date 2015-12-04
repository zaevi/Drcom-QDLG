from PIL import Image
import os


Code = []

if not Code:
    with open('captchaCode') as f:
        texts = f.readlines()
        for text in texts:
            Code.append([int(t) for t in text[:-1]])


def captcha(source):
    if isinstance(source, Image.Image):
        img = source
    else:
        img = Image.open(source)

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
    matched, n = 0, 0
    for i in range(len(code1)):
        if code1[i]:
            n += 1
            if code2[i]:
                matched += 1
    return matched / n
