"""Construye el ERD Archify directamente desde el respaldo SQL validado."""
import json, re, runpy
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'respaldos'/'db_test_jessi.sql'
OUT=ROOT/'documentacion'/'diagrama_archify_db_test_jessi.candidate.json'
parser=runpy.run_path(str(ROOT/'scripts'/'build_eer.py'),run_name='schema_parser')
d=parser['analyze']()
sql=SOURCE.read_text(encoding='utf-8',errors='replace')
lines=sql.splitlines()

domains={
 'Catálogo':['tb_products','tbc_categories','tbd_products_categories','tbc_payment_methods_types'],
 'Cuentas':['tb_users','tb_user_addresses','tbd_address_components','tbd_user_payment_methods','tbd_products_users_providers','tbd_users_wishlist_products'],
 'Compras':['tb_carts','tbd_carts_items','tb_buyer_orders','tbd_order_items'],
 'Auditoría':['tb_logs']
}
domain_pos={name:{table:(row,col) for row,table in enumerate(members)} for col,(name,members) in enumerate(domains.items())}

def source_range(table):
 start=next(i for i,line in enumerate(lines,1) if re.search(r'^CREATE TABLE `'+re.escape(table)+r'`\s*\(',line))
 end=next(i for i in range(start,len(lines)+1) if lines[i-1].strip().startswith(') ENGINE='))
 return {'path':'respaldos/db_test_jessi.sql','line':start,'end_line':end,'label':'DDL SQL'}

entities=[]
for t in d['tables']:
 tag=next(k for k,v in domains.items() if t['name'] in v)
 row,col=domain_pos[tag][t['name']]
 attributes=[]
 for c in t['columns']:
  a={'name':c['name'],'type':c['type']}
  roles=[]
  if c['pk']: roles.append('pk')
  if c['uk']: roles.append('uk')
  fk=next((r for r in d['relations'] if r['confirmed'] and r['fromTable']==t['name'] and c['name'] in r['fromCols']),None)
  if fk: roles.append('fk')
  if roles: a['key']=roles[0] if len(roles)==1 else roles
  if fk:
   idx=fk['fromCols'].index(c['name'])
   a['references']=f"{fk['toTable']}.{fk['toCols'][idx]}"
  attributes.append(a)
 entity={'id':t['name'],'label':t['name'],'tag':tag,'row':row,'col':col,'sublabel':f"{len(t['columns'])} columnas · {t['rows']:,} filas en respaldo",'attributes':attributes}
 widths={'tb_buyer_orders':679,'tb_logs':407,'tbd_products_users_providers':414}
 if t['name'] in widths: entity['width']=widths[t['name']]
 entities.append(entity)

relationships=[]
for i,r in enumerate(d['relations'],1):
 if r['fromTable']==r['toTable']: continue
 src=next(t for t in d['tables'] if t['name']==r['fromTable'])
 unique_fk=any(all(c['name'] in cols for c in src['columns'] if c['uk']) for cols in [])
 for con in src['constraints']:
  if re.search(r'UNIQUE(?: KEY| INDEX)?\s*(?:`[^`]+`\s*)?\(([^)]*)\)',con,re.I):
   keycols=re.findall(r'`([^`]+)`',re.search(r'\(([^)]*)\)',con).group(1))
   if set(keycols)==set(r['fromCols']): unique_fk=True
 identifying=all(next(c for c in src['columns'] if c['name']==n)['pk'] for n in r['fromCols']) if r['confirmed'] else False
 rel={'id':f"rel_{i:02d}",'from':r['fromTable'],'to':r['toTable'],'label':r['name'] if r['confirmed'] else 'product_id sugerido por nombre; no FK','fromCardinality':'one' if unique_fk else 'many','toCardinality':'one','fromOptional':any(next(c for c in src['columns'] if c['name']==n)['nullable'] for n in r['fromCols']),'identifying':identifying}
 if not r['confirmed']: rel['variant']='dashed'
 relationships.append(rel)

candidate={
 'schema_version':1,'diagram_type':'erd',
 'meta':{'title':'Diccionario relacional de db_test_7b','locale':'es','output':'documentacion/diagrama_archify_db_test_jessi.html','quality_profile':'standard'},
 'layout':{'mode':'grid','gapY':44,'gapX':90,'entityW':340,'rowH':22},
 'entities':entities,'relationships':relationships,
 'cards':[{'dot':'amber','title':'Lectura del modelo','items':['Cada entidad incluye todas las columnas físicas y su tipo SQL, según db_test_jessi.sql.','Las claves y referencias sólidas representan restricciones declaradas en el DDL.','tbc_categories y tbd_address_components tienen FK autorreferentes; se describen en los atributos y en el diccionario porque el ERD no admite relaciones de una entidad consigo misma.','La línea discontinua entre tb_logs.product_id y tb_products.ID es una asociación inferida, no una clave foránea.','Los conteos indican filas incluidas en INSERT del respaldo; las vistas se documentan por separado.']}]
}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(candidate,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'candidate':str(OUT.relative_to(ROOT)),'entities':len(entities),'attributes':sum(len(e['attributes']) for e in entities),'relationships':len(relationships),'all_columns':sum(len(t['columns']) for t in d['tables'])==sum(len(e['attributes']) for e in entities)},ensure_ascii=False,indent=2))
