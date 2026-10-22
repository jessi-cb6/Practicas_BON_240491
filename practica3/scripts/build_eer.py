#!/usr/bin/env python3
"""Analyze a MySQL dump and build a self-contained interactive EER viewer."""
from __future__ import annotations
import csv, html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'respaldos' / 'db_test_jessi.sql'
OUT = ROOT / 'eer_db_test.html'

def split_sql(s: str) -> list[str]:
    out=[]; start=0; quote=None; esc=False; depth=0
    for i,c in enumerate(s):
        if quote:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c==quote:
                if i+1<len(s) and s[i+1]==quote: continue
                quote=None
        elif c in "'\"`": quote=c
        elif c=='(': depth+=1
        elif c==')': depth-=1
        elif c==',' and depth==0: out.append(s[start:i].strip()); start=i+1
    out.append(s[start:].strip()); return [x for x in out if x]

def matching(text: str, opening: int) -> int:
    depth=0; quote=None; esc=False
    for i in range(opening,len(text)):
        c=text[i]
        if quote:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c==quote:
                if i+1<len(text) and text[i+1]==quote: continue
                quote=None
        elif c in "'\"`": quote=c
        elif c=='(': depth+=1
        elif c==')':
            depth-=1
            if depth==0:return i
    return -1

def count_values(text: str, start: int) -> int:
    # Count complete top-level row tuples, honoring quoted commas/parentheses.
    i=start; depth=0; quote=None; esc=False; count=0
    while i<len(text):
        c=text[i]
        if quote:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c==quote:
                if i+1<len(text) and text[i+1]==quote: i+=1
                else: quote=None
        elif c in "'\"`": quote=c
        elif c=='(':
            if depth==0: count+=1
            depth+=1
        elif c==')': depth-=1
        elif c==';' and depth==0: break
        i+=1
    return count

def analyze():
    raw=SOURCE.read_bytes(); text=raw.decode('utf-8', errors='replace')
    db=re.search(r'-- Host:.*?Database:\s*`?([\w$-]+)',text)
    db_name=db.group(1) if db else 'No declarado en el encabezado'
    tables=[]; table_by={}
    for m in re.finditer(r'CREATE TABLE\s+`([^`]+)`\s*\(',text,re.I):
        name=m.group(1); op=m.end()-1; cl=matching(text,op)
        if cl<0: continue
        body=text[op+1:cl]; entries=split_sql(body); cols=[]; constraints=[]; indexes=[]
        for e in entries:
            if re.match(r'^(PRIMARY KEY|UNIQUE KEY|UNIQUE INDEX|KEY|INDEX|CONSTRAINT|FOREIGN KEY|CHECK)\b',e,re.I):
                constraints.append(e)
                if re.match(r'^(KEY|INDEX|UNIQUE KEY|UNIQUE INDEX)\b',e,re.I): indexes.append(e)
                continue
            cm=re.match(r'^`([^`]+)`\s+(.+)$',e,re.S)
            if not cm: continue
            cn,decl=cm.groups(); typm=re.match(r'([\w]+(?:\s+unsigned)?(?:\s+zerofill)?(?:\s*\([^)]*\))?)',decl,re.I)
            typ=typm.group(1).strip() if typm else decl.split()[0]
            enum=re.search(r"\benum\s*\((.*?)\)",decl,re.I|re.S)
            enums=re.findall(r"'((?:\\.|[^'])*)'",enum.group(1)) if enum else []
            col={'name':cn,'type':typ,'nullable':not bool(re.search(r'\bNOT NULL\b',decl,re.I)),
                 'autoIncrement':bool(re.search(r'\bAUTO_INCREMENT\b',decl,re.I)),
                 'default':None,'enum':enums,'declaration':decl.strip()}
            dm=re.search(r'\bDEFAULT\s+((?:\'.*?\')|(?:".*?")|[^\s,]+)',decl,re.I)
            if dm: col['default']=dm.group(1)
            col['onUpdate']=bool(re.search(r'\bON UPDATE\b',decl,re.I))
            cols.append(col)
        table={'name':name,'columns':cols,'constraints':constraints,'indexes':indexes,'rows':0,'engine':None,'options':''}
        tail=text[cl+1:cl+500]
        em=re.search(r'ENGINE\s*=\s*(\w+)',tail,re.I); table['engine']=em.group(1) if em else None
        table['options']=re.search(r'\)\s*(ENGINE=.*?);',tail,re.I|re.S).group(1) if re.search(r'\)\s*(ENGINE=.*?);',tail,re.I|re.S) else ''
        table_by[name]=table; tables.append(table)
    # Keys and indexes from inline table definitions.
    for t in tables:
        for c in t['columns']: c['pk']=False; c['uk']=False; c['fk']=False
        for con in t['constraints']:
            pm=re.search(r'PRIMARY KEY\s*\(([^)]*)\)',con,re.I)
            um=re.search(r'UNIQUE(?: KEY| INDEX)?\s*(?:`[^`]+`\s*)?\(([^)]*)\)',con,re.I)
            if pm:
                for n in re.findall(r'`([^`]+)`',pm.group(1)):
                    next((c for c in t['columns'] if c['name']==n),{}).update(pk=True)
            elif um:
                for n in re.findall(r'`([^`]+)`',um.group(1)):
                    next((c for c in t['columns'] if c['name']==n),{}).update(uk=True)
    # INSERT data counts; tuple count is independent of line breaks and string content.
    ins_re=re.compile(r'INSERT\s+INTO\s+`([^`]+)`(?:\s*\([^;]*?\))?\s+VALUES\s*',re.I)
    inserts=[]
    for m in ins_re.finditer(text):
        i=m.end(); rows=count_values(text,i); inserts.append((m.group(1),rows))
        if m.group(1) in table_by: table_by[m.group(1)]['rows']+=rows
    # Capture FKs declared inline or later via ALTER TABLE.
    rels=[]
    fk_re=re.compile(r'(?:CONSTRAINT\s+`([^`]+)`\s+)?FOREIGN KEY\s*\(([^)]*)\)\s*REFERENCES\s+`([^`]+)`\s*\(([^)]*)\)([^,\n)]*(?:ON\s+(?:DELETE|UPDATE)\s+\w+[^,\n)]*)*)',re.I)
    for tm in tables:
        for m in fk_re.finditer('\n'.join(tm['constraints'])):
            rels.append({'name':m.group(1) or '', 'fromTable':tm['name'],'fromCols':re.findall(r'`([^`]+)`',m.group(2)),
                         'toTable':m.group(3),'toCols':re.findall(r'`([^`]+)`',m.group(4)),
                         'rules':m.group(5).strip(),'confirmed':True})
    for m in re.finditer(r'ALTER TABLE\s+`([^`]+)`\s+(.*?);',text,re.I|re.S):
        src,body=m.groups()
        for f in fk_re.finditer(body):
            rels.append({'name':f.group(1) or '', 'fromTable':src,'fromCols':re.findall(r'`([^`]+)`',f.group(2)),
                         'toTable':f.group(3),'toCols':re.findall(r'`([^`]+)`',f.group(4)),
                         'rules':f.group(5).strip(),'confirmed':True})
    # Deduplicate relations and mark FK attrs.
    unique=[]; seen=set()
    for r in rels:
        k=(r['fromTable'],tuple(r['fromCols']),r['toTable'],tuple(r['toCols']))
        if k in seen: continue
        seen.add(k); unique.append(r)
        for c in table_by.get(r['fromTable'],{}).get('columns',[]):
            if c['name'] in r['fromCols']: c['fk']=True
    rels=unique
    # A log product_id is a semantic candidate only; the dump declares no FK for it.
    if 'tb_logs' in table_by and 'tb_products' in table_by and any(c['name']=='product_id' for c in table_by['tb_logs']['columns']):
        rels.append({'name':'inferida_product_id','fromTable':'tb_logs','fromCols':['product_id'],
                     'toTable':'tb_products','toCols':['ID'],'rules':'Sin FOREIGN KEY; inferencia por nombre y semántica de trazabilidad. Pendiente de validar.','confirmed':False})
    # Catalog SQL object types and report header values.
    views=sorted(set(re.findall(r'\bVIEW\s+`([^`]+)`',text,re.I)))
    procs=sorted(set(re.findall(r'\bPROCEDURE\s+`([^`]+)`',text,re.I)))
    triggers=sorted(set(re.findall(r'\bTRIGGER\s+`([^`]+)`',text,re.I)))
    return {'database':db_name,'source':SOURCE.name,'sizeBytes':len(raw),'tables':tables,'relations':rels,
            'views':views,'procedures':procs,'triggers':triggers,'insertStatements':len(inserts),
            'totalRows':sum(t['rows'] for t in tables),
            'validation':{'allTablesParsed':len(tables)>0,'allInsertsMatched':all(n in table_by for n,_ in inserts),
                          'unmatchedInsertTables':sorted(set(n for n,_ in inserts if n not in table_by)),
                          'insertRows':sum(n for _,n in inserts),'tableRows':sum(t['rows'] for t in tables)}}

def main():
    data=analyze()
    OUT.write_text(make_html(data),encoding='utf-8')
    # CSV companions.
    with (ROOT/'inventario_eer.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f); w.writerow(['Codigo','Tabla','Columna','Tipo','Nullable','PK','FK','UK','AI','Default','Restricciones','Registros'])
        for ti,t in enumerate(data['tables'],1):
            for ai,c in enumerate(t['columns'],1):
                tags=[]
                if c['pk']:tags.append('PK')
                if c['fk']:tags.append('FK')
                if c['uk']:tags.append('UK')
                if not c['nullable']:tags.append('NN')
                if c['autoIncrement']:tags.append('AI')
                w.writerow([f'E{ti:02}',t['name'],f'A{ai:02} {c["name"]}',c['type'],'NULL' if c['nullable'] else 'NOT NULL',c['pk'],c['fk'],c['uk'],c['autoIncrement'],c['default'],' '.join(tags),t['rows']])
    with (ROOT/'registros_por_tabla.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f); w.writerow(['Codigo','Tabla','Columnas','Registros_contenidos_en_respaldo'])
        for i,t in enumerate(data['tables'],1):w.writerow([f'E{i:02}',t['name'],len(t['columns']),t['rows']])
    with (ROOT/'relaciones_eer.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f); w.writerow(['Codigo','Estado','Origen','Columnas_FK','Destino','Columnas_referenciadas','Cardinalidad','Reglas'])
        for i,r in enumerate(data['relations'],1):w.writerow([f'R{i:02}','Confirmada' if r['confirmed'] else 'Inferida',r['fromTable'],','.join(r['fromCols']),r['toTable'],','.join(r['toCols']),'N:1 candidata' if not r['confirmed'] else 'N:1',r['rules']])
    print(json.dumps({k:data[k] for k in ['database','sizeBytes','totalRows','insertStatements','validation','views','procedures','triggers']},ensure_ascii=False,indent=2))

def make_html(data):
    page=TEMPLATE.replace('__DATA__',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
    palette='''.node.color-0 rect{fill:#eff6ff;stroke:#6999dc}.node.color-0 .node-title{fill:#2254a2}.node.color-1 rect{fill:#eefaf7;stroke:#54a996}.node.color-1 .node-title{fill:#167365}.node.color-2 rect{fill:#fff7eb;stroke:#dfa54e}.node.color-2 .node-title{fill:#946313}.node.color-3 rect{fill:#f5f0ff;stroke:#9c7bd1}.node.color-3 .node-title{fill:#64459b}.node.color-4 rect{fill:#fff0f2;stroke:#d97c8a}.node.color-4 .node-title{fill:#a33d50}.node.color-5 rect{fill:#eff8ef;stroke:#83ad70}.node.color-5 .node-title{fill:#49743b}.node.color-6 rect{fill:#eff7fa;stroke:#73a9bc}.node.color-6 .node-title{fill:#346c81}.node .key{fill:#9a6810}.node .tag{fill:#316e86}.edge{stroke:#55718f}.edge.inferred{stroke:#da9625;stroke-dasharray:7 5}.edge.active{stroke:#e38924;stroke-width:3}'''
    page=page.replace('</style>',palette+'</style>')
    page=page.replace('<g class="node ${selected===i?', '<g class="node color-${i%7} ${selected===i?')
    page=page.replace('<span class="pill">${tags}</span>', '${tags.split(\' · \').map(tag=>`<span class="pill badge-${tag.toLowerCase()}">${tag}</span>`).join(\' \')}')
    page=page.replace('.pill{display:inline-block;background:#edf3fb;border-radius:20px;padding:3px 8px;margin:3px 3px 0 0;font-size:11px}', '.pill{display:inline-block;background:#edf3fb;border-radius:20px;padding:3px 8px;margin:3px 3px 0 0;font-size:11px}.badge-pk{background:#fff0c7;color:#835500}.badge-fk{background:#d9f4ef;color:#12675d}.badge-uk{background:#eee4ff;color:#60419a}.badge-nn{background:#e3eaf4;color:#42556f}.badge-ai{background:#ffe4df;color:#a34234}')
    page=page.replace("['Relaciones confirmadas',D.relations.length],['Inferidas',0]", "['Relaciones confirmadas',D.relations.filter(r=>r.confirmed).length],['Inferidas',D.relations.filter(r=>!r.confirmed).length]")
    page=page.replace('.edge.active{stroke:#e39a27;stroke-width:3}', '.edge.active{stroke:#e39a27;stroke-width:3}.edge.inferred{stroke-dasharray:6 4}')
    page=page.replace('class="edge ${active?\'\':\'dim\'} ${selected===a||selected===b?\'active\':\'\'}"', 'class="edge ${active?\'\':\'dim\'} ${selected===a||selected===b?\'active\':\'\'} ${r.confirmed?\'\':\'inferred\'}"')
    page=page.replace('>R${String(i+1).padStart(2,\'0\')} · 1:N</text>', '>${r.confirmed?\'\':\'∼ \' }R${String(i+1).padStart(2,\'0\')} · N:1</text>')
    page=page.replace('Cardinalidad derivada: 1:N, sujeta a UNIQUE para verificar 1:1.', 'Cardinalidad derivada desde el lado origen: N:1; una FK UNIQUE podría convertirla en 1:1.')
    page=page.replace('${esc(c.name)} <tspan class="node-meta">', 'A${String(j+1).padStart(2,\'0\')} ${esc(c.name)} <tspan class="node-meta">')
    page=page.replace('R${String(i+1).padStart(2,\'0\')} · Relación confirmada por FK', 'R${String(i+1).padStart(2,\'0\')} · ${r.confirmed?\'Relación confirmada por FK\':\'Relación inferida · pendiente de validación\'}')
    page=page.replace('>FK: <b>${esc(r.fromCols.join(\', \'))}</b> · PK/UK referenciada: <b>${esc(r.toCols.join(\', \'))}</b>', '>${r.confirmed?\'FK\':\'Columna candidata\'}: <b>${esc(r.fromCols.join(\', \'))}</b> · ${r.confirmed?\'PK/UK referenciada\':\'Columna destino propuesta\'}: <b>${esc(r.toCols.join(\', \'))}</b>')
    page=page.replace('Relationships without FK declarations are not promoted to confirmed links.', 'Las relaciones inferidas se muestran con línea discontinua y no representan integridad referencial confirmada.')
    return page

TEMPLATE = r'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Modelo EER · __DB__</title>
<style>
:root{--bg:#f3f6fa;--panel:#fff;--ink:#17263c;--muted:#6b7b90;--line:#dce4ee;--blue:#2f68c5;--teal:#11877b;--gold:#bd8a20;--shadow:0 8px 28px #23344c12}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 Inter,Segoe UI,Arial,sans-serif}header{padding:18px 24px;background:#10243f;color:white;display:flex;justify-content:space-between;align-items:center}header h1{font-size:20px;margin:0}header small{color:#bac9dc}button,select,input{font:inherit;border:1px solid var(--line);border-radius:8px;background:white;padding:8px 10px;color:var(--ink)}button{cursor:pointer}button:hover{border-color:var(--blue);color:var(--blue)}.wrap{padding:16px 20px}.summary{display:grid;grid-template-columns:repeat(6,minmax(120px,1fr));gap:10px;margin-bottom:14px}.stat,.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow)}.stat{padding:12px}.stat span{display:block;color:var(--muted);font-size:12px}.stat b{font-size:20px}.toolbar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:10px 12px;margin-bottom:12px}.toolbar input{min-width:220px}.layout{display:grid;grid-template-columns:minmax(500px,1fr) 340px;gap:12px}.canvas{height:calc(100vh - 260px);min-height:480px;position:relative;overflow:hidden;cursor:grab;background-color:#fbfdff;background-image:radial-gradient(#d6deea 1px,transparent 1px);background-size:18px 18px}.canvas:active{cursor:grabbing}svg{width:100%;height:100%;touch-action:none}.edge{stroke:#8799af;stroke-width:1.7;fill:none}.edge.active{stroke:#e39a27;stroke-width:3}.edge-label{font-size:12px;fill:#52647c}.node{cursor:pointer}.node rect{fill:#fff;stroke:#aebed1;stroke-width:1.4;rx:10;filter:drop-shadow(0 3px 5px #23344c18)}.node.selected rect{stroke:#2671dc;stroke-width:2.5}.node.dim{opacity:.16}.node-title{fill:#122b49;font-size:14px;font-weight:700}.node-meta{fill:#6b7b90;font-size:10px}.attr{fill:#263b53;font-size:11px}.key{fill:#1f65bd;font-weight:700}.tag{fill:#677b93;font-size:9px}.side{height:calc(100vh - 260px);min-height:480px;overflow:auto;padding:16px}.side h2{margin:0 0 3px;font-size:19px}.side h3{font-size:13px;margin:18px 0 8px}.muted{color:var(--muted)}.pill{display:inline-block;background:#edf3fb;border-radius:20px;padding:3px 8px;margin:3px 3px 0 0;font-size:11px}.col{padding:8px 0;border-bottom:1px solid #edf1f6}.col strong{font-size:12px}.col code{display:block;font:11px Consolas,monospace;color:#617087;word-break:break-word}.rel{border-left:3px solid #e1a135;padding:8px;margin:8px 0;background:#fff8eb;border-radius:4px}.legend{padding:12px;margin-top:12px;display:flex;gap:14px;flex-wrap:wrap}.warn{background:#fff6de;border:1px solid #efdaa3;border-radius:10px;padding:12px;margin-bottom:12px}.tabs{display:flex;gap:6px}.hidden{display:none}.table{width:100%;border-collapse:collapse}.table th,.table td{text-align:left;padding:8px;border-bottom:1px solid var(--line)}
@media(max-width:950px){.summary{grid-template-columns:repeat(3,1fr)}.layout{grid-template-columns:1fr}.side{height:auto;min-height:0}.canvas{height:65vh}}@media(max-width:550px){.summary{grid-template-columns:repeat(2,1fr)}header{padding:14px}.wrap{padding:10px}}
</style></head><body><header><div><h1>Modelo EER · <span id="dbname"></span></h1><small id="source"></small></div><div class="tabs"><button onclick="exportSvg()">Exportar SVG</button><button onclick="downloadCsv()">Inventario CSV</button></div></header><main class="wrap"><div id="warning"></div><section class="summary" id="summary"></section><div class="toolbar panel"><input id="search" placeholder="Buscar tabla o atributo…" oninput="render()"><label><input type="checkbox" id="attrs" checked onchange="render()"> Atributos</label><label>Tipo <select id="typeFilter" onchange="render()"><option value="">Todos</option></select></label><label><input type="checkbox" id="relations" checked onchange="render()"> Relaciones</label><button onclick="zoom(1.2)">＋</button><button onclick="zoom(.83)">−</button><button onclick="fit()">Ajustar</button><button onclick="showOverview()">Vista general</button></div><div class="layout"><section class="canvas panel" id="canvas"><svg id="diagram" viewBox="0 0 1200 800" aria-label="Diagrama entidad relación"></svg></section><aside class="side panel" id="detail"><div class="muted">Selecciona una entidad o una relación del diagrama.</div></aside></div><section class="legend panel"><b>Leyenda:</b><span><b>PK</b> primaria</span><span><b>FK</b> foránea</span><span><b>UK</b> única</span><span><b>NN</b> no nulo</span><span><b>AI</b> autoincremental</span><span>Registros contabilizados desde INSERT del respaldo</span></section><section class="panel" style="margin-top:12px;padding:14px"><h3>Registros contenidos en el respaldo</h3><div id="counts"></div><h3>Vistas, rutinas y validación</h3><div id="validation"></div></section></main>
<script>const D=__DATA__;let selected=null,scale=1,tx=0,ty=0,positions=[],drag=null;const svg=document.getElementById('diagram');document.getElementById('dbname').textContent=D.database;document.getElementById('source').textContent=D.source+' · '+D.sizeBytes.toLocaleString('es-MX')+' bytes · los datos corresponden al archivo, no al servidor en ejecución';
function init(){const stats=[['Tablas',D.tables.length],['Columnas',D.tables.reduce((a,t)=>a+t.columns.length,0)],['Relaciones confirmadas',D.relations.length],['Inferidas',0],['Registros en respaldo',D.totalRows],['Vistas',D.views.length]];document.getElementById('summary').innerHTML=stats.map(x=>`<div class="stat"><span>${x[0]}</span><b>${x[1].toLocaleString('es-MX')}</b></div>`).join('');let types=[...new Set(D.tables.flatMap(t=>t.columns.map(c=>c.type.split('(')[0].toLowerCase())))].sort();document.getElementById('typeFilter').innerHTML+='<option>'+types.join('</option><option>')+'</option>';if(!types.length)document.getElementById('typeFilter').innerHTML='<option value="">Todos</option>';document.getElementById('counts').innerHTML='<table class="table"><thead><tr><th>Entidad</th><th>Tabla</th><th>Columnas</th><th>Registros</th></tr></thead><tbody>'+D.tables.map((t,i)=>`<tr><td>E${String(i+1).padStart(2,'0')}</td><td>${esc(t.name)}</td><td>${t.columns.length}</td><td>${t.rows.toLocaleString('es-MX')}</td></tr>`).join('')+'</tbody></table>';document.getElementById('validation').innerHTML=`<p>${D.validation.allTablesParsed?'Tablas físicas extraídas de CREATE TABLE.':'No se encontraron tablas.'} INSERT contabilizados: ${D.validation.insertStatements}; filas: ${D.validation.insertRows.toLocaleString('es-MX')}. ${D.validation.unmatchedInsertTables.length?'INSERT fuera de tablas físicas: '+D.validation.unmatchedInsertTables.join(', '):'Todos los INSERT coinciden con tablas físicas.'}</p><p>Vistas: ${D.views.length?D.views.map(esc).join(', '):'ninguna detectada'}. Procedimientos: ${D.procedures.length?D.procedures.map(esc).join(', '):'ninguno detectado'}. Disparadores: ${D.triggers.length?D.triggers.map(esc).join(', '):'ninguno detectado'}.</p><p>Índices y restricciones adicionales aparecen en el panel de cada entidad. Relationships without FK declarations are not promoted to confirmed links.</p>`;if(!D.validation.allTablesParsed||D.validation.insertRows!==D.validation.tableRows)document.getElementById('warning').innerHTML='<div class="warn">Advertencia: se detectó una diferencia o falta en el análisis SQL. Revisa la validación antes de usar el modelo como definitivo.</div>';positions=layout();render()}
function layout(){let n=D.tables.length,cols=Math.ceil(Math.sqrt(n)),cw=300,ch=240;return D.tables.map((t,i)=>({x:35+(i%cols)*cw,y:35+Math.floor(i/cols)*ch,w:260,h:Math.max(100,65+t.columns.length*18)}))}function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function render(){let q=document.getElementById('search').value.toLowerCase(),showA=document.getElementById('attrs').checked,showR=document.getElementById('relations').checked,type=document.getElementById('typeFilter').value.toLowerCase();let p=positions;let out=[];out.push(`<g transform="translate(${tx},${ty}) scale(${scale})">`);if(showR)D.relations.forEach((r,i)=>{let a=D.tables.findIndex(t=>t.name===r.fromTable),b=D.tables.findIndex(t=>t.name===r.toTable);if(a<0||b<0)return;let A=p[a],B=p[b],x1=A.x+A.w/2,y1=A.y+A.h/2,x2=B.x+B.w/2,y2=B.y+B.h/2,active=!selected||selected===a||selected===b;out.push(`<path class="edge ${active?'':'dim'} ${selected===a||selected===b?'active':''}" d="M${x1} ${y1} C${(x1+x2)/2} ${y1},${(x1+x2)/2} ${y2},${x2} ${y2}" onclick="detailRelation(${i})"/><text class="edge-label" x="${(x1+x2)/2}" y="${(y1+y2)/2-5}" onclick="detailRelation(${i})">R${String(i+1).padStart(2,'0')} · 1:N</text>`)});D.tables.forEach((t,i)=>{let P=p[i],matches=!q||t.name.toLowerCase().includes(q)||t.columns.some(c=>c.name.toLowerCase().includes(q));let typeMatches=!type||t.columns.some(c=>c.type.toLowerCase().startsWith(type));let dim=(selected!==null&&selected!==i&&!D.relations.some(r=>(r.fromTable===t.name&&D.tables[selected]?.name===r.toTable)||(r.toTable===t.name&&D.tables[selected]?.name===r.fromTable)))||!matches||!typeMatches;out.push(`<g class="node ${selected===i?'selected':''} ${dim?'dim':''}" transform="translate(${P.x},${P.y})" onclick="selectTable(${i})"><rect width="${P.w}" height="${P.h}"/><text class="node-title" x="12" y="21">E${String(i+1).padStart(2,'0')} · ${esc(t.name)}</text><text class="node-meta" x="12" y="39">${t.rows.toLocaleString('es-MX')} filas · ${t.columns.length} columnas</text>`);if(showA)t.columns.forEach((c,j)=>{let tags=[c.pk?'PK':null,c.fk?'FK':null,c.uk?'UK':null,!c.nullable?'NN':null,c.autoIncrement?'AI':null].filter(Boolean).join(' ');out.push(`<text class="attr ${c.pk?'key':''}" x="12" y="${59+j*16}">${esc(c.name)} <tspan class="node-meta">${esc(c.type)}</tspan><tspan class="tag"> ${tags}</tspan></text>`)});out.push('</g>')});out.push('</g>');svg.innerHTML=out.join('')}
function selectTable(i){selected=i;let t=D.tables[i],rel=D.relations.map((r,j)=>({...r,j})).filter(r=>r.fromTable===t.name||r.toTable===t.name);document.getElementById('detail').innerHTML=`<div class="muted">E${String(i+1).padStart(2,'0')} · Entidad</div><h2>${esc(t.name)}</h2><p class="muted">${t.rows.toLocaleString('es-MX')} registros contenidos en el respaldo · ${t.columns.length} columnas</p><h3>Atributos</h3>${t.columns.map((c,j)=>{let tags=[c.pk?'PK':null,c.fk?'FK':null,c.uk?'UK':null,!c.nullable?'NN':null,c.autoIncrement?'AI':null].filter(Boolean).join(' · ');let relation=D.relations.find(r=>r.fromTable===t.name&&r.fromCols.includes(c.name));return `<div class="col" ${relation?'onclick="goTo(\''+esc(relation.toTable)+'\')" style="cursor:pointer"':''}><strong>A${String(j+1).padStart(2,'0')} ${esc(c.name)} ${tags?`<span class="pill">${tags}</span>`:''}</strong><code>${esc(c.declaration)}</code>${c.default!==null?`<small>DEFAULT ${esc(c.default)}</small>`:''}${c.enum.length?`<small>ENUM: ${c.enum.map(esc).join(', ')}</small>`:''}${relation?`<small>→ ${esc(relation.toTable)} (ir a entidad)</small>`:''}</div>`}).join('')}<h3>Índices y restricciones</h3>${t.constraints.map(x=>`<div class="col"><code>${esc(x)}</code></div>`).join('')||'<span class="muted">Sin restricciones/index declarados.</span>'}<h3>Relaciones</h3>${rel.map(r=>`<div class="rel" onclick="detailRelation(${r.j})"><b>R${String(r.j+1).padStart(2,'0')}</b> ${esc(r.fromTable)}.${r.fromCols.join(',')} → ${esc(r.toTable)}.${r.toCols.join(',')}<br>Cardinalidad: 1:N (FK en origen) · ${esc(r.rules||'sin regla ON DELETE/UPDATE declarada')}</div>`).join('')||'<span class="muted">Sin FK declaradas.</span>'}`;render()}
function detailRelation(i){let r=D.relations[i];document.getElementById('detail').innerHTML=`<div class="muted">R${String(i+1).padStart(2,'0')} · Relación confirmada por FK</div><h2>${esc(r.fromTable)} → ${esc(r.toTable)}</h2><p>FK: <b>${esc(r.fromCols.join(', '))}</b> · PK/UK referenciada: <b>${esc(r.toCols.join(', '))}</b></p><p>Cardinalidad derivada: 1:N, sujeta a UNIQUE para verificar 1:1. Participación del lado FK ${r.fromCols.every(c=>D.tables.find(t=>t.name===r.fromTable).columns.find(x=>x.name===c)?.nullable)?'opcional':'obligatoria'} según NULL/NOT NULL.</p><p>Reglas referenciales: ${esc(r.rules||'ON DELETE/UPDATE no declarados explícitamente')}</p><button onclick="goTo('${esc(r.fromTable)}')">Ir a origen</button> <button onclick="goTo('${esc(r.toTable)}')">Ir a destino</button>`;render()}
function goTo(name){let i=D.tables.findIndex(t=>t.name===name);if(i>=0){selectTable(i);fitNode(i)}}function fitNode(i){let p=positions[i];tx=100-p.x*scale;ty=140-p.y*scale;render()}function showOverview(){selected=null;document.getElementById('detail').innerHTML='<div class="muted">Vista general del modelo completo. Selecciona una entidad o relación para ver detalles.</div>';fit()}function zoom(f){scale=Math.max(.35,Math.min(2.5,scale*f));render()}function fit(){scale=Math.min(1,(svg.clientWidth-30)/(Math.max(...positions.map(p=>p.x+p.w))+30),(svg.clientHeight-30)/(Math.max(...positions.map(p=>p.y+p.h))+30));tx=10;ty=10;render()}function exportSvg(){let b=new Blob([new XMLSerializer().serializeToString(svg)],{type:'image/svg+xml'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='diagrama_eer.svg';a.click();URL.revokeObjectURL(a.href)}function downloadCsv(){let rows=[['Codigo','Tabla','Atributo','Tipo','PK','FK','UK','NN','AI','Default','Registros']];D.tables.forEach((t,i)=>t.columns.forEach((c,j)=>rows.push([`E${String(i+1).padStart(2,'0')}`,t.name,`A${String(j+1).padStart(2,'0')} ${c.name}`,c.type,c.pk,c.fk,c.uk,!c.nullable,c.autoIncrement,c.default,t.rows])));let csv=rows.map(r=>r.map(x=>'"'+String(x??'').replaceAll('"','""')+'"').join(',')).join('\r\n');let a=document.createElement('a');a.href=URL.createObjectURL(new Blob(['\ufeff'+csv],{type:'text/csv'}));a.download='inventario_eer.csv';a.click();URL.revokeObjectURL(a.href)}
let canvas=document.getElementById('canvas');canvas.addEventListener('wheel',e=>{e.preventDefault();zoom(e.deltaY<0?1.08:.92)},{passive:false});canvas.addEventListener('pointerdown',e=>{if(e.target.closest('.node')||e.target.closest('.edge-label'))return;drag={x:e.clientX,y:e.clientY,tx,ty};canvas.setPointerCapture(e.pointerId)});canvas.addEventListener('pointermove',e=>{if(drag){tx+=e.clientX-drag.x;ty+=e.clientY-drag.y;drag.x=e.clientX;drag.y=e.clientY;render()}});canvas.addEventListener('pointerup',()=>drag=null);init();</script></body></html>'''.replace('__DATA__','__DATA__').replace('__DB__','__DB__')

if __name__=='__main__':
    TEMPLATE=TEMPLATE.replace('__DB__','db_test_7b')
    main()
