"""組裝「地理模型教室」。

執行：python3 build.py
產生兩個檔案：
- index.html      線上版（GitHub Pages 首頁），模型從 models/<id>.html 載入
- geo-models.html 離線單檔版，所有模型與 three.js 都內嵌，可放隨身碟、教室沒網路也能用
"""
import json

VENDOR_TAG = '<script src="../vendor/three.r128.min.js"></script>'

reg = json.load(open('registry.json', encoding='utf-8'))
three = open('vendor/three.r128.min.js', encoding='utf-8').read()


def safe(o):
    return json.dumps(o, ensure_ascii=False).replace('</', '<\\/')


def offline(html):
    # 離線版：把 vendor 的 three.js 直接內嵌
    return html.replace(VENDOR_TAG, '<script>' + three.replace('</script', '<\\/script') + '</script>')


t = open('template.html', encoding='utf-8').read()

online = t.replace('__REGISTRY__', safe(reg)).replace('__PAYLOAD__', 'null')
open('index.html', 'w', encoding='utf-8').write(online)

payload = {m['id']: offline(open(f"models/{m['id']}.html", encoding='utf-8').read()) for m in reg['models']}
single = t.replace('__REGISTRY__', safe(reg)).replace('__PAYLOAD__', safe(payload))
open('geo-models.html', 'w', encoding='utf-8').write(single)

print('index.html', len(online.encode()), 'bytes')
print('geo-models.html', len(single.encode()), 'bytes')
