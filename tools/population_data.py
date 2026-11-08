"""整理「人口金字塔」模型用的聯合國資料（不是網站的一部分，只在更新資料時執行）。

資料：聯合國《世界人口展望 2024》（UN DESA, World Population Prospects 2024，中推估），CC BY 3.0 IGO。
下載這三個檔（https://population.un.org/wpp/downloads/ → CSV format）放到同一個資料夾：
  WPP2024_PopulationByAge5GroupSex_Medium.csv.gz
  WPP2024_Demographic_Indicators_Medium.csv.gz
  WPP2024_Life_Table_Abridged_Medium_1950-2023.csv.gz
執行：python3 tools/population_data.py <資料夾>  → 印出 JSON，貼進 models/population.html 的 DATA 區塊。
"""
import json
import sys

import pandas as pd

D = sys.argv[1]
ISO = ['TWN', 'VNM', 'NER', 'IND', 'USA', 'JPN', 'KOR', 'CHN']
NAME = {'TWN': '臺灣', 'VNM': '越南', 'NER': '尼日', 'IND': '印度', 'USA': '美國',
        'JPN': '日本', 'KOR': '南韓', 'CHN': '中國'}

pop = pd.read_csv(f'{D}/WPP2024_PopulationByAge5GroupSex_Medium.csv.gz', low_memory=False,
                  usecols=['ISO3_code', 'Time', 'AgeGrpStart', 'PopMale', 'PopFemale'])
pop = pop[pop.ISO3_code.isin(ISO)]
ind = pd.read_csv(f'{D}/WPP2024_Demographic_Indicators_Medium.csv.gz', low_memory=False,
                  usecols=['ISO3_code', 'Time', 'CBR', 'CDR', 'TFR', 'LEx', 'CNMR', 'MedianAgePop', 'IMR'])
ind = ind[ind.ISO3_code.isin(ISO)]

out = {'years': [1950, 2100], 'countries': {}}
for iso in ISO:
    p = pop[pop.ISO3_code == iso].sort_values(['Time', 'AgeGrpStart'])
    q = ind[(ind.ISO3_code == iso) & (ind.Time <= 2100)].sort_values('Time')
    rows = []
    for t, g in p.groupby('Time'):
        assert len(g) == 21, (iso, t)
        # 單位：百人（千人 × 10，取整數）；前 21 個是男性 0–4…100+，後 21 個是女性
        rows.append([round(v * 10) for v in list(g.PopMale) + list(g.PopFemale)])
    r1 = lambda s: [round(float(v), 1) for v in s]
    out['countries'][iso] = {
        'name': NAME[iso], 'pop': rows,
        'cbr': r1(q.CBR), 'cdr': r1(q.CDR), 'tfr': [round(float(v), 2) for v in q.TFR],
        'e0': r1(q.LEx), 'mig': r1(q.CNMR), 'med': r1(q.MedianAgePop), 'imr': r1(q.IMR)}

# 模擬分頁用的兩種「死亡年齡模式」（只取 lx 的形狀）：高死亡＝世界 1950 年、低死亡＝日本 2019 年。
# 模擬時把兩者的 logit 值依比例混合，再調整比例讓粗死亡率等於拉桿的值（Brass 關係模型的做法）。
lt = pd.read_csv(f'{D}/WPP2024_Life_Table_Abridged_Medium_1950-2023.csv.gz', low_memory=False,
                 usecols=['Location', 'Time', 'Sex', 'AgeGrpStart', 'lx'])
out['std'] = {}
for key, (loc, t) in {'high': ('World', 1950), 'low': ('Japan', 2019)}.items():
    q = lt[(lt.Location == loc) & (lt.Time == t)]
    out['std'][key] = {s[0].lower(): [round(float(v) / 1e5, 6) for v in q[q.Sex == s].sort_values('AgeGrpStart').lx]
                       for s in ('Male', 'Female')}
print(json.dumps(out, ensure_ascii=False, separators=(',', ':')))
