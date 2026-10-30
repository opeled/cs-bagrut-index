"""Check catalog coverage and page mappings that required manual reconciliation."""
from pathlib import Path
import json
from collections import defaultdict
R=Path(__file__).parent
c=json.loads((R/'catalog.json').read_text());p=json.loads((R/'provenance.json').read_text())
qs=c['questions'];byid={q['id']:q for q in qs};exams={e['id']:e for e in p['exams']}
assert len(qs)==len(byid)==770
assert len(exams)==56 and len(p['officialEntries'])==62
assert len(c['topics'])==23 and len({t['color'] for t in c['topics']})==23
seen=defaultdict(list)
for q in qs:
 e=exams[q['exam']];seen[q['exam']].append(q['q'])
 assert 1<=q['p']<=e['pdfPages'],q['id']
 assert q['tags'] and all(0<=t<23 for t in q['tags']),q['id']
 assert q['url']==e['source'] and q['url'].startswith('https://'),q['id']
 for v in q.get('variants',[]):assert q['p']<=v['page']<=e['pdfPages'],q['id']
for key,nums in seen.items():assert sorted(nums)==list(range(1,exams[key]['questions']+1)),key
# Reconciled against actual question headings, not numbered subclauses.
expected={
'2016-06-899122-q7':5,'2016-06-899381-q3':5,
'2016-06-899205-q8':17,'2016-06-899381-q8':15,
'2016-08-899222-q9':9,'2016-08-899222-q10':10,
'2013-06-899205-q15':28,'2020-06-899381-q12':21,
'2021-06-899381-q10':20,'2023-06-899282-q9':7,
'2024-06-899282-q9':7,'2025-06-899372-q9':7,
'2025-06-899271-q10':14,'2025-06-899271-q11':18,
'2025-06-899271-q12':22,'2026-06-899271-q12':24,
'2024-06-899381-q6':8,'2022-06-899381-q6':10}
for key,page in expected.items():assert byid[key]['p']==page,(key,page)
for key,pages in {'2024-06-899381-q6':[8,9],'2022-06-899381-q6':[10,12],'2026-06-899271-q12':[24,26]}.items():
 assert [v['page'] for v in byid[key]['variants']]==pages,key
# Method calls/overloads in these questions are not recursion.
assert 9 not in byid['2011-06-899205-q2']['tags']
assert 9 not in byid['2026-06-899271-q12']['tags']
assert sum(bool(q.get('mirror')) for q in qs)==10
print('Validated 770 questions, 56 exams, 23 topics, page ranges and reconciled headings.')

# Semantic corrections found during the 130-link independent spot check.
for key,tag in {"2013-06-899205-q1":11,"2013-06-899205-q7":16,"2021-06-899381-q6":11,"2023-06-899371-q3":3}.items():
 assert tag in byid[key]["tags"],key
