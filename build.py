"""組裝「地理模型教室」。

執行：python3 build.py
產生兩個檔案：
- index.html      線上版（GitHub Pages 首頁），模型從 models/<id>.html 載入
- geo-models.html 離線單檔版，所有模型與 three.js 都內嵌，可放隨身碟、教室沒網路也能用
"""
import glob
import html
import json
import re

VENDOR_TAG = '<script src="../vendor/three.r128.min.js"></script>'

reg = json.load(open('registry.json', encoding='utf-8'))
three = open('vendor/three.r128.min.js', encoding='utf-8').read()


def safe(o):
    return json.dumps(o, ensure_ascii=False).replace('</', '<\\/')


EXTERNAL_SCRIPT = re.compile(r'<script[^>]+src=["\']?(https?:)?//', re.I)
SECRET = re.compile(
    r'sk-(ant-|proj-)?[A-Za-z0-9_-]{20,}'          # Claude／OpenAI 金鑰
    r'|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_\w{30,}'  # GitHub 權杖
    r'|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}'     # AWS／Google 金鑰
    r'|xox[abprs]-[A-Za-z0-9-]{10,}|hooks\.slack\.com/services/\S+'
    r'|discord(app)?\.com/api/webhooks/\S+'
    r'|-----BEGIN [A-Z ]*PRIVATE KEY'
    r'|(api[_-]?key|secret|password|passwd|token)["\']?\s*[:=]\s*["\'][^"\'\s]{12,}["\']',
    re.I)

FONT_LINK = re.compile(r'<link rel="stylesheet" href="(\.\./)?vendor/fonts\.css">\n?')


def offline(page):
    # 離線版：把 vendor 的 three.js 直接內嵌；單檔讀不到字型檔，改用電腦內建字型
    page = FONT_LINK.sub('', page)
    return page.replace(VENDOR_TAG, '<script>' + three.replace('</script', '<\\/script') + '</script>')


# 資安檢查：模型不得連到外部網站，且每頁要有「不收錄＋內容安全政策」標記
for f in glob.glob('models/*.html') + ['template.html']:
    src = open(f, encoding='utf-8').read()
    if 'fonts.googleapis' in src or 'fonts.gstatic' in src:
        raise SystemExit(f'⚠ {f} 還在用 Google 字型，請改成 <link rel="stylesheet" href="../vendor/fonts.css">')
    if 'Content-Security-Policy' not in src or 'noindex' not in src:
        raise SystemExit(f'⚠ {f} 缺少資安標記（robots noindex 與 Content-Security-Policy），請照其他模型補上')
    if EXTERNAL_SCRIPT.search(src):
        raise SystemExit(f'⚠ {f} 從外部網站載入程式，請改用 vendor/ 裡的檔案')

# 資安檢查：網站是公開的，任何像金鑰、密碼、私鑰的字串都不能放進來
for f in glob.glob('models/*.html') + glob.glob('*.py') + glob.glob('*.md') + ['template.html', 'registry.json']:
    hit = SECRET.search(open(f, encoding='utf-8').read())
    if hit:
        raise SystemExit(f'⚠ {f} 裡有像金鑰或密碼的字串（{hit.group(0)[:8]}…），網站是公開的，請先拿掉再組裝')

# 字型檢查：有新字不在自帶字型裡就提醒
have = set(open('vendor/fonts/chars.txt', encoding='utf-8').read())
need = set()
for f in glob.glob('models/*.html') + ['template.html', 'registry.json']:
    need |= {c for c in html.unescape(open(f, encoding='utf-8').read()) if ord(c) > 0x7e}
missing = need - have
if missing:
    print(f'提醒：有 {len(missing)} 個字不在自帶字型裡（會用電腦內建字型顯示），可執行 python3 fonts.py 更新：', ''.join(sorted(missing))[:60])


t = open('template.html', encoding='utf-8').read()

online = t.replace('__REGISTRY__', safe(reg)).replace('__PAYLOAD__', 'null')
open('index.html', 'w', encoding='utf-8').write(online)

payload = {m['id']: offline(open(f"models/{m['id']}.html", encoding='utf-8').read()) for m in reg['models']}
single = FONT_LINK.sub('', t).replace('__REGISTRY__', safe(reg)).replace('__PAYLOAD__', safe(payload))
open('geo-models.html', 'w', encoding='utf-8').write(single)

print('index.html', len(online.encode()), 'bytes')
print('geo-models.html', len(single.encode()), 'bytes')
