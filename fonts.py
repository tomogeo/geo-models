"""重新產生網站自帶字型（vendor/fonts/*.woff2）。

新增或修改模型、出現新的中文字後執行：
    pip install fonttools brotli
    python3 fonts.py
會從 Google Fonts 官方 GitHub 下載思源黑體／宋體原檔，只保留網站用到的字，存進 vendor/fonts/。
（build.py 發現有字不在字型裡時會提醒執行這支。）
"""
import glob
import html
import os
import tempfile
import urllib.request

from fontTools import subset

SRC = {
    'NotoSansTC': 'https://raw.githubusercontent.com/google/fonts/main/ofl/notosanstc/NotoSansTC%5Bwght%5D.ttf',
    'NotoSerifTC': 'https://raw.githubusercontent.com/google/fonts/main/ofl/notoseriftc/NotoSerifTC%5Bwght%5D.ttf',
}
EXTRA = '，。、；：？！「」『』（）《》〈〉…—～・０１２３４５６７８９％＋－×÷＝＜＞°℃’“”‘'


def used_chars():
    s = set(chr(c) for c in range(0x20, 0x7f)) | set(EXTRA)
    for f in glob.glob('models/*.html') + ['template.html', 'registry.json']:
        t = html.unescape(open(f, encoding='utf-8').read())
        s |= {c for c in t if ord(c) > 0x7e}
    return ''.join(sorted(s))


if __name__ == '__main__':
    text = used_chars()
    os.makedirs('vendor/fonts', exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for name, url in SRC.items():
            src = os.path.join(tmp, name + '.ttf')
            print('下載', name, '…')
            urllib.request.urlretrieve(url, src)
            out = f'vendor/fonts/{name}.woff2'
            subset.main([src, '--text=' + text, '--flavor=woff2', "--layout-features=*", '--output-file=' + out])
            print(out, os.path.getsize(out), 'bytes')
    with open('vendor/fonts/chars.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print('共', len(text), '字')
