"""Actualiza el ERD y el diccionario de datos desde practica3_terminada2.sql."""
from __future__ import annotations

import csv
import html
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "respaldos" / "practica3_terminada2.sql"
OUT = ROOT / ".archify" / "erd-db-test-7b-20261022-120000"
DOCS = ROOT / "documentacion"
PARSER = runpy.run_path(str(ROOT / "scripts" / "build_eer.py"), run_name="schema_parser")
PARSER["analyze"].__globals__["SOURCE"] = SOURCE
DATA = PARSER["analyze"]()

DOMAINS = {
    "cuentas": ["tb_users", "tb_people", "tb_user_addresses", "tbd_address_components"],
    "catalogo": ["tb_products", "tbc_categories", "tbd_products_categories"],
    "ventas": ["tb_buyer_orders", "tb_orders", "tb_order_cancellations", "tb_carts", "tbd_cart_items", "tbd_order_items", "tbd_cancellation_items", "tbd_return_items"],
    "proveedores": ["tbd_products_users_providers", "tbd_users_wishlist_products"],
    "pagos": ["tbc_payment_methods_types", "tb_payment_methods", "tb_payment_transaction", "tb_payments", "tb_refunds", "tb_returns", "tb_shipments", "tbd_user_payment_methods"],
    "auditoria": ["tb_logs"],
}
PURPOSE = {
    "tb_buyer_orders": "Cabecera de pedidos recibidos por un vendedor, con importes y etapa de cumplimiento.",
    "tb_carts": "Carrito de compra asociado a una cuenta de usuario.",
    "tb_logs": "Bitácora de operaciones y cambios registrados en las entidades.",
    "tb_products": "Catálogo de productos, precios vigentes, existencias y disponibilidad.",
    "tb_user_addresses": "Direcciones de envío y contacto asociadas a usuarios.",
    "tb_users": "Cuentas de usuario, acceso y estado de la cuenta.",
    "tbc_categories": "Catálogo jerárquico de categorías de productos.",
    "tbc_payment_methods_types": "Catálogo de tipos de métodos de pago admitidos.",
    "tbd_address_components": "Componentes jerárquicos que desglosan una dirección.",
    "tbd_carts_items": "Productos y cantidades que forman parte de un carrito.",
    "tbd_order_items": "Detalle histórico de productos, cantidades y precios por pedido.",
    "tbd_products_categories": "Tabla puente entre productos y categorías.",
    "tbd_products_users_providers": "Relación de productos con usuarios proveedores o distribuidores.",
    "tbd_user_payment_methods": "Métodos de pago registrados para los usuarios.",
    "tbd_users_wishlist_products": "Productos guardados por usuarios en listas de deseos.",
}
FIELD = {
    "ID": "Identificador técnico de la fila.", "SKU": "Código comercial único del producto.",
    "name": "Nombre visible del producto, categoría o elemento.", "description": "Descripción textual complementaria.",
    "current_price": "Precio vigente del producto.", "current_stock": "Unidades registradas actualmente en existencia.",
    "status": "Indicador binario de estado; su significado exacto depende de la aplicación.",
    "creation_date": "Fecha y hora de creación del registro.", "last_update": "Fecha y hora de la última modificación.",
    "email": "Correo electrónico asociado a la cuenta.", "nick": "Alias o nombre corto de la cuenta.",
    "password": "Campo de credencial; el DDL no especifica el mecanismo de protección.",
    "last_login": "Fecha y hora del último inicio de sesión.",
    "sup_id_category": "Categoría superior opcional; permite construir la jerarquía de categorías.",
    "product_ID": "Identificador del producto asociado.", "categories_ID": "Identificador de la categoría asociada.",
    "user_ID": "Identificador del usuario asociado.", "person_ID": "Identificador del perfil personal asociado.",
    "seller_ID": "Identificador del usuario vendedor.", "provider_ID": "Identificador del usuario proveedor.",
    "cart_ID": "Identificador del carrito asociado.", "address_ID": "Identificador de la dirección asociada.",
    "address_sup_ID": "Componente superior opcional dentro de la misma dirección.",
    "seller_order_ID": "Identificador del pedido de venta asociado.",
    "payment_method_type_ID": "Identificador del tipo de método de pago.",
    "quantity": "Cantidad de unidades del producto.", "unit_price": "Precio unitario aplicado en la operación.",
    "subtotal": "Importe subtotal calculado o almacenado para la operación.", "shipping_cost": "Importe del costo de envío.",
    "fulfillment_status": "Etapa de preparación y entrega del pedido.",
    "table_name": "Entidad o tabla afectada por el evento auditado.", "table_operation": "Tipo de operación registrada en la bitácora.",
    "db_user": "Usuario de base de datos consignado como actor.", "operation_date": "Fecha y hora en que se registró el evento.",
    "operation_description": "Descripción del evento de auditoría.", "operation_status": "Indicador binario del resultado registrado.",
    "product_id": "Identificador relacionado con el evento; el respaldo no declara una FK para este campo.",
    "type_ownership": "Rol del usuario con respecto al producto.", "available_date": "Fecha desde la que se declara disponible la relación producto-proveedor.",
    "provider": "Proveedor o procesador externo del método de pago.", "provider_method_ref": "Referencia externa del método en el proveedor de pagos.",
    "last_four": "Últimos cuatro dígitos del medio de pago.", "latitude": "Coordenada geográfica de latitud.",
    "longitude": "Coordenada geográfica de longitud.", "is_default": "Indicador de selección predeterminada.",
    "birth_date": "Fecha de nacimiento del perfil personal.", "gender": "Género declarado en el perfil personal.",
    "phone": "Número telefónico de contacto.", "country_code": "Código de país asociado al perfil o teléfono.",
    "component_type": "Tipo de componente que representa el valor de dirección.",
}
THEME = """
:root{--bg:#070b18;--panel:#10182b;--ink:#e7f2ff;--muted:#8ea5c6;--line:#243959;--blue:#50c8ff;--teal:#42f5d7;--gold:#ffd166;--shadow:0 14px 42px #0008}
body{background:radial-gradient(ellipse at 15% -10%,#153265 0,transparent 38%),radial-gradient(ellipse at 90% 10%,#172554 0,transparent 34%),var(--bg);color:var(--ink)}header{background:linear-gradient(110deg,#091326,#142b55 56%,#10394b);border-bottom:1px solid #38d9ff66;box-shadow:0 6px 30px #13cfff18}
header small,.muted,.stat span{color:var(--muted)}.stat,.panel{background:linear-gradient(145deg,#111b30ee,#0b1325f5);border-color:#29466d;box-shadow:var(--shadow)}.stat{border-top:2px solid #3ad8ff88}.stat b{color:#e8faff;text-shadow:0 0 14px #39d8ff66}
button,select,input{background:#0d1830;color:var(--ink);border-color:#315078}button:hover{border-color:#44ddff;color:#67e8ff;box-shadow:0 0 16px #32d9ff28}.canvas{background-color:#091222;background-image:radial-gradient(#315078 1px,transparent 1px)}
.node rect{fill:#101d34;stroke:#39739e;filter:drop-shadow(0 0 7px #1a9bcc30)}.node-title{fill:#c7f5ff}.node-meta{fill:#8ea5c6}.attr{fill:#c3d8f3}.tag,.key{fill:#51e5d4}.edge{stroke:#48abc4}.edge-label{fill:#b7cce8}.side{color:var(--ink)}.col{border-color:#233b5a}.col code{color:#9cb6d6}.pill{background:#123744;color:#79f3e0}.rel{background:#292143;border-color:#8869d5}.legend,.table th,.table td{border-color:#233b5a}.warn{background:#352b15;color:#ffe29b;border-color:#84652d}
"""


def describe(table: dict, col: dict) -> str:
    if col["name"] in FIELD:
        return FIELD[col["name"]]
    rel = next((r for r in DATA["relations"] if r["confirmed"] and r["fromTable"] == table["name"] and col["name"] in r["fromCols"]), None)
    if rel:
        i = rel["fromCols"].index(col["name"])
        return f"Referencia a {rel['toTable']}.{rel['toCols'][i]}."
    return f"Dato {col['name'].replace('_', ' ')} asociado a {table['name'].replace('_', ' ')}; descripción inferida del nombre y tipo SQL."


def keys(col: dict) -> str:
    result = [name for name, flag in (("PK", col.get("pk")), ("FK", col.get("fk")), ("UK", col.get("uk"))) if flag]
    return ", ".join(result) or "—"


def make_candidate() -> dict:
    domain_of = {table: domain for domain, tables in DOMAINS.items() for table in tables}
    row = {domain: 0 for domain in DOMAINS}
    table_ix = {t["name"]: t for t in DATA["tables"]}
    entities = []
    for table in DATA["tables"]:
        domain = domain_of.get(table["name"], "general")
        attrs = []
        for col in table["columns"]:
            attr = {"name": col["name"], "type": "enum" if col["type"].lower().startswith("enum(") else col["type"]}
            role = [x for x, flag in (("pk", col.get("pk")), ("fk", col.get("fk")), ("uk", col.get("uk"))) if flag]
            if role:
                attr["key"] = role[0] if len(role) == 1 else role
            rel = next((r for r in DATA["relations"] if r["confirmed"] and r["fromTable"] == table["name"] and col["name"] in r["fromCols"]), None)
            if rel:
                attr["references"] = f"{rel['toTable']}.{rel['toCols'][rel['fromCols'].index(col['name'])]}"
            attrs.append(attr)
        entities.append({"id": table["name"], "label": table["name"], "tag": domain, "row": row[domain], "col": list(DOMAINS).index(domain),
                         "sublabel": f"{table['rows']:,} filas · {len(table['columns'])} columnas", "width": 350, "attributes": attrs})
        row[domain] += 1
    relations, self_refs = [], []
    for i, rel in enumerate(DATA["relations"], 1):
        if not rel["confirmed"]:
            continue
        if rel["fromTable"] == rel["toTable"]:
            self_refs.append(rel)
            continue
        nullable = {c["name"]: c["nullable"] for c in table_ix[rel["fromTable"]]["columns"]}
        relations.append({"id": f"rel_{i:02}", "from": rel["fromTable"], "to": rel["toTable"], "label": ", ".join(rel["fromCols"]),
                          "fromCardinality": "many", "toCardinality": "one", "fromOptional": any(nullable.get(c, False) for c in rel["fromCols"])})
    cards = []
    if self_refs:
        cards.append({"dot": "violet", "title": "Relaciones jerárquicas", "items": [f"{r['fromTable']}.{', '.join(r['fromCols'])} referencia {r['toTable']}.{', '.join(r['toCols'])}." for r in self_refs]})
    for rel in DATA["relations"]:
        if not rel["confirmed"]:
            cards.append({"dot": "amber", "title": "Relación inferida", "items": [f"{rel['fromTable']}.{', '.join(rel['fromCols'])} → {rel['toTable']}.{', '.join(rel['toCols'])}; no es una FK declarada."]})
    return {"schema_version": 1, "diagram_type": "erd", "meta": {"title": "MERE · db_test_7b", "subtitle": f"Actualizado desde {SOURCE.name} · {len(DATA['tables'])} tablas · {DATA['totalRows']:,} filas del respaldo.", "locale": "es", "quality_profile": "standard", "output": "modelo_mere_db_test_7b.html"}, "layout": {"mode": "grid", "gapX": 84, "gapY": 48}, "entities": entities, "relationships": relations, "cards": cards}


def dictionary_data() -> list[dict]:
    domain_of = {table: domain for domain, tables in DOMAINS.items() for table in tables}
    result = []
    for table in DATA["tables"]:
        columns = []
        for col in table["columns"]:
            rel = next((r for r in DATA["relations"] if r["confirmed"] and r["fromTable"] == table["name"] and col["name"] in r["fromCols"]), None)
            ref = f"{rel['toTable']}.{rel['toCols'][rel['fromCols'].index(col['name'])]}" if rel else None
            columns.append({"name": col["name"], "type": col["type"], "nullable": col["nullable"], "keys": keys(col), "default": col.get("default"), "ai": col.get("autoIncrement"), "description": describe(table, col), "enum": col.get("enum", []), "reference": ref})
        result.append({"name": table["name"], "domain": domain_of.get(table["name"], "general"), "rows": table["rows"], "description": PURPOSE.get(table["name"], "Entidad del modelo relacional."), "columns": columns, "constraints": table["constraints"]})
    return result


def markdown() -> str:
    domain_of = {table: domain for domain, tables in DOMAINS.items() for table in tables}
    lines = ["# Diccionario de datos · db_test_7b", "", f"**Fuente:** `{SOURCE.relative_to(ROOT).as_posix()}`  ", f"**Motor:** MySQL 8.0 · **Tablas:** {len(DATA['tables'])} · **Columnas:** {sum(len(t['columns']) for t in DATA['tables'])} · **Filas en respaldo:** {DATA['totalRows']:,}", "", "Los conteos son las filas incluidas en los INSERT del respaldo; no representan una consulta al servidor activo.", "", "## Resumen", "", "| Tabla | Área | Columnas | Filas | Descripción |", "|---|---|---:|---:|---|"]
    for table in DATA["tables"]:
        lines.append(f"| `{table['name']}` | {domain_of.get(table['name'], 'general')} | {len(table['columns'])} | {table['rows']:,} | {PURPOSE.get(table['name'], 'Entidad del modelo relacional.')} |")
    lines += ["", "## Diccionario por tabla", ""]
    for table in DATA["tables"]:
        lines += [f"### `{table['name']}`", "", PURPOSE.get(table["name"], "Entidad del modelo relacional."), "", f"**Filas del respaldo:** {table['rows']:,} · **Columnas:** {len(table['columns'])}", "", "| Columna | Tipo SQL | Nulo | Llaves | Predeterminado | Descripción |", "|---|---|---|---|---|---|"]
        for col in table["columns"]:
            default = f"`{col['default']}`" if col.get("default") is not None else "—"
            desc = describe(table, col) + ((" Valores: " + ", ".join(f"`{v}`" for v in col["enum"]) + ".") if col.get("enum") else "")
            lines.append(f"| `{col['name']}` | `{col['type']}` | {'Sí' if col['nullable'] else 'No'} | {keys(col)} | {default} | {desc} |")
        if table["constraints"]:
            lines += ["", "**Índices y restricciones**", ""] + [f"- `{item}`" for item in table["constraints"]]
        lines.append("")
    lines += ["## Relaciones", "", "Las relaciones declaradas se derivan de FOREIGN KEY y se muestran desde la tabla que contiene la llave (N:1 hacia la tabla referenciada).", ""]
    for rel in DATA["relations"]:
        state = "FK declarada" if rel["confirmed"] else "Inferida; no es FK física"
        lines.append(f"- **{state}:** `{rel['fromTable']}.{', '.join(rel['fromCols'])}` → `{rel['toTable']}.{', '.join(rel['toCols'])}`.")
    lines += ["", "## Objetos del respaldo", "", f"- Vistas ({len(DATA['views'])}): " + (", ".join(f"`{v}`" for v in DATA["views"]) or "ninguna"), f"- Procedimientos ({len(DATA['procedures'])}): " + (", ".join(f"`{p}`" for p in DATA["procedures"]) or "ninguno"), f"- Triggers: {len(DATA['triggers'])}", "", f"**Validación del análisis:** {DATA['insertStatements']} sentencias INSERT; {DATA['validation']['insertRows']:,} filas contabilizadas y asociadas a tablas del respaldo.", ""]
    return "\n".join(lines)


def html_dictionary() -> str:
    payload = json.dumps(dictionary_data(), ensure_ascii=False).replace("</", "<\\/")
    summary = {"tables": len(DATA["tables"]), "columns": sum(len(t["columns"]) for t in DATA["tables"]), "rows": DATA["totalRows"], "relations": sum(r["confirmed"] for r in DATA["relations"]), "views": len(DATA["views"]), "triggers": len(DATA["triggers"])}
    return HTML_TEMPLATE.replace("__DATA__", payload).replace("__SUMMARY__", json.dumps(summary)).replace("__SOURCE__", html.escape(SOURCE.name))


def launch_page() -> str:
    return '''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>db_test_7b · Documentación</title>
<style>
:root{color-scheme:dark;--bg:#070b18;--panel:#111b30;--ink:#eaf4ff;--muted:#98afcd;--line:#284568;--cyan:#52dcff;--mint:#48f0cf}*{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(ellipse at 14% 0,#193d70 0,transparent 38%),radial-gradient(ellipse at 90% 22%,#17384a 0,transparent 34%),var(--bg);color:var(--ink);font:15px/1.6 Inter,Segoe UI,Arial,sans-serif}.wrap{width:min(1080px,92vw);margin:0 auto;padding:8vh 0}.eyebrow{color:var(--mint);letter-spacing:.2em;text-transform:uppercase;font-size:11px}h1{font-size:clamp(32px,6vw,58px);line-height:1.05;margin:12px 0}.lead{max-width:720px;color:var(--muted)}.stats{display:flex;gap:10px;flex-wrap:wrap;margin:28px 0}.stats span{border:1px solid var(--line);background:#0e1a2e;border-radius:10px;padding:9px 13px;color:#9ddff0;font-size:12px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:24px}.card{display:block;padding:22px;border:1px solid var(--line);border-radius:16px;background:linear-gradient(145deg,#14223a,#0d1628);text-decoration:none;color:inherit;box-shadow:0 18px 50px #0005;transition:.2s}.card:hover{transform:translateY(-3px);border-color:var(--cyan);box-shadow:0 18px 48px #24cfff22}.icon{color:var(--cyan);font:12px Consolas,monospace;letter-spacing:.12em}.card h2{margin:10px 0 5px;font-size:21px}.card p{margin:0;color:var(--muted);font-size:13px}.card b{display:inline-block;margin-top:16px;color:var(--mint);font-size:12px}footer{margin-top:42px;padding-top:16px;border-top:1px solid var(--line);color:#7188a7;font-size:11px}
</style></head><body><main class="wrap"><div class="eyebrow">DATA ATLAS · DB_TEST_7B</div><h1>Centro de documentación</h1><p class="lead">Modelo entidad relación y diccionario de datos generados desde el respaldo <code>practica3_terminada2.sql</code>. Los conteos describen el archivo SQL.</p><div class="stats"><span>26 tablas</span><span>203 columnas</span><span>98,893 filas</span><span>36 llaves foráneas</span></div><section class="cards"><a class="card" href="modelo_mere_db_test_7b.html"><div class="icon">01 / ESQUEMA</div><h2>Modelo entidad relación</h2><p>Explora tablas, atributos, claves y conexiones. Busca campos, filtra tipos y ajusta la vista del diagrama.</p><b>Abrir modelo →</b></a><a class="card" href="diccionario_datos_db_test_7b.html"><div class="icon">02 / DATA ATLAS</div><h2>Diccionario de datos</h2><p>Consulta tipos SQL, nulabilidad, llaves, valores ENUM, referencias e índices con búsqueda por área.</p><b>Abrir diccionario →</b></a><a class="card" href="diccionario_datos.md"><div class="icon">03 / DOCUMENTO</div><h2>Versión Markdown</h2><p>Diccionario detallado en formato de texto para lectura, revisión o entrega.</p><b>Abrir documento →</b></a></section><footer>Fuente: respaldos/practica3_terminada2.sql · Generado para abrirse localmente con VS Code Live Server, sin dependencias externas.</footer></main></body></html>'''


HTML_TEMPLATE = r'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Data Atlas · db_test_7b</title>
<style>
:root{--bg:#070b18;--panel:#10182b;--ink:#e8f2ff;--muted:#8da6c7;--line:#263d5d;--cyan:#52dcff;--mint:#48f0cf;--violet:#9c8cff}*{box-sizing:border-box}body{margin:0;color:var(--ink);font:14px/1.55 Inter,Segoe UI,Arial,sans-serif;background:radial-gradient(ellipse at 12% -10%,#15366a 0,transparent 40%),radial-gradient(ellipse at 92% 8%,#18364d 0,transparent 34%),var(--bg);min-height:100vh}.top{padding:30px clamp(20px,5vw,72px) 24px;border-bottom:1px solid #3ddcff55;background:linear-gradient(110deg,#091326dd,#102448dd 58%,#0c3443dd);box-shadow:0 12px 45px #0006}.eyebrow{color:var(--mint);font-size:11px;letter-spacing:.22em;text-transform:uppercase}h1{font-size:clamp(26px,4vw,42px);line-height:1.15;margin:8px 0;color:#f2fbff}.sub{color:#a9bfdb;max-width:900px}.source{font:12px Consolas,monospace;color:#77cde9;margin-top:12px}.wrap{max-width:1500px;margin:auto;padding:24px clamp(14px,3vw,40px) 64px}.stats{display:grid;grid-template-columns:repeat(6,minmax(110px,1fr));gap:11px;margin-bottom:20px}.stat{background:linear-gradient(145deg,#111e35,#0d1629);border:1px solid #294668;border-top:2px solid #39c9ed88;border-radius:13px;padding:14px;box-shadow:0 12px 30px #0004}.stat span{display:block;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.08em}.stat b{display:block;color:#eafaff;font-size:23px;margin-top:4px;text-shadow:0 0 18px #42d5ff55}.tools{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:16px 0}input,select,button{font:inherit;color:var(--ink);background:#0d1830;border:1px solid #315078;border-radius:9px;padding:10px 12px}input{flex:1;min-width:220px}button{cursor:pointer}button:hover,select:hover,input:focus{border-color:var(--cyan);box-shadow:0 0 18px #34d8ff2a;outline:0}.count{color:var(--muted);margin-left:auto;font-size:12px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,470px),1fr));gap:14px}.entity{background:linear-gradient(145deg,#111c31f2,#0b1425f5);border:1px solid #28415f;border-radius:15px;overflow:hidden;box-shadow:0 16px 36px #0004;transition:border-color .2s,transform .2s}.entity:hover{border-color:#47cbeb88;transform:translateY(-2px)}.entity summary{cursor:pointer;list-style:none;padding:16px 18px;display:grid;grid-template-columns:1fr auto;gap:4px 12px}.entity summary::-webkit-details-marker{display:none}.table-name{font:700 16px Consolas,monospace;color:#d8f6ff}.domain{color:var(--mint);font-size:10px;text-transform:uppercase;letter-spacing:.13em}.purpose{grid-column:1/-1;color:#9eb2ce;font-size:12px}.meta{color:#80c7df;font-size:11px;text-align:right}.body{border-top:1px solid #243a58;padding:12px 16px 17px}.cols{width:100%;border-collapse:collapse;font-size:12px}.cols th{color:#91abc9;font-size:10px;text-align:left;text-transform:uppercase;letter-spacing:.08em;padding:8px;border-bottom:1px solid #2b4565}.cols td{vertical-align:top;padding:9px 8px;border-bottom:1px solid #1e314d}.cols tr:last-child td{border-bottom:0}.field{font:600 12px Consolas,monospace;color:#d7eeff;white-space:nowrap}.type{font:11px Consolas,monospace;color:#78d9e9}.badge{display:inline-block;border:1px solid #346171;background:#10313c;color:#78f0d6;border-radius:20px;padding:1px 7px;font-size:9px;white-space:nowrap}.desc{color:#a9bdd7;min-width:170px}.extra{display:block;color:#7694b6;font-size:10px;margin-top:4px;word-break:break-word}.constraints{margin-top:14px;padding:12px;border-radius:10px;background:#0a1323;border:1px solid #213754}.constraints h3{font-size:11px;color:#73dfff;margin:0 0 6px;text-transform:uppercase;letter-spacing:.1em}.constraints code{display:block;color:#9db6d5;font:10px/1.6 Consolas,monospace;overflow-wrap:anywhere}.empty{padding:30px;border:1px dashed #315078;border-radius:14px;color:var(--muted);text-align:center;grid-column:1/-1}footer{color:#6f87a8;text-align:center;font-size:11px;padding:34px 12px}@media(max-width:850px){.stats{grid-template-columns:repeat(3,1fr)}}@media(max-width:560px){.stats{grid-template-columns:repeat(2,1fr)}.entity summary{padding:13px}.body{padding:8px}.cols{display:block;overflow-x:auto}.desc{min-width:140px}}
</style></head><body><header class="top"><div class="eyebrow">ARCHIFY · DATA ATLAS / 07B</div><h1>Diccionario de datos</h1><div class="sub">Mapa técnico de entidades, atributos, llaves y relaciones de db_test_7b, preparado para explorar el esquema con rapidez.</div><div class="source">FUENTE // __SOURCE__ · MYSQL 8.0 · CONTEOS DEL RESPALDO</div></header><main class="wrap"><section class="stats" id="stats"></section><div class="tools"><input id="search" type="search" placeholder="Buscar tabla, columna, tipo o descripción…"><select id="domain"><option value="">Todas las áreas</option><option>cuentas</option><option>catalogo</option><option>ventas</option><option>proveedores</option><option>pagos</option><option>auditoria</option></select><button id="expand">Expandir todo</button><button id="collapse">Contraer todo</button><span class="count" id="count"></span></div><section class="grid" id="grid"></section><footer>DATA ATLAS · Conteos referidos al respaldo SQL; no son una lectura del servidor en ejecución.</footer></main>
<script>const DATA=__DATA__;const S=__SUMMARY__;const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));document.getElementById('stats').innerHTML=[['Entidades',S.tables],['Atributos',S.columns],['Filas respaldo',S.rows.toLocaleString('es-MX')],['FK declaradas',S.relations],['Vistas',S.views],['Triggers',S.triggers]].map(x=>`<article class="stat"><span>${x[0]}</span><b>${x[1]}</b></article>`).join('');function render(){const q=document.getElementById('search').value.trim().toLowerCase(),d=document.getElementById('domain').value;const rows=DATA.filter(t=>(!d||t.domain===d)&&(!q||JSON.stringify(t).toLowerCase().includes(q)));document.getElementById('count').textContent=`${rows.length} de ${DATA.length} tablas`;document.getElementById('grid').innerHTML=rows.length?rows.map(t=>`<details class="entity"><summary><span class="table-name">${esc(t.name)}</span><span class="meta">${t.columns.length} col · ${t.rows.toLocaleString('es-MX')} filas</span><span class="domain">${esc(t.domain)}</span><span></span><span class="purpose">${esc(t.description)}</span></summary><div class="body"><table class="cols"><thead><tr><th>Atributo</th><th>Tipo SQL</th><th>Llaves</th><th>Descripción</th></tr></thead><tbody>${t.columns.map(c=>`<tr><td><span class="field">${esc(c.name)}</span> ${!c.nullable?'<span class="badge">NOT NULL</span>':''} ${c.ai?'<span class="badge">AUTO</span>':''}</td><td><span class="type">${esc(c.type)}</span></td><td>${c.keys==='—'?'':`<span class="badge">${esc(c.keys)}</span>`}</td><td class="desc">${esc(c.description)}${c.reference?`<span class="extra">REFERENCIA → ${esc(c.reference)}</span>`:''}${c.default!==null?`<span class="extra">DEFAULT ${esc(c.default)}</span>`:''}${c.enum?.length?`<span class="extra">VALORES: ${c.enum.map(esc).join(' · ')}</span>`:''}</td></tr>`).join('')}</tbody></table>${t.constraints.length?`<div class="constraints"><h3>Índices y restricciones</h3>${t.constraints.map(x=>`<code>${esc(x)}</code>`).join('')}</div>`:''}</div></details>`).join(''):'<div class="empty">Sin coincidencias. Prueba otro término o área.</div>'}document.getElementById('search').addEventListener('input',render);document.getElementById('domain').addEventListener('change',render);document.getElementById('expand').onclick=()=>document.querySelectorAll('details.entity').forEach(x=>x.open=true);document.getElementById('collapse').onclick=()=>document.querySelectorAll('details.entity').forEach(x=>x.open=false);render();</script></body></html>'''


def main() -> None:
    validation = DATA["validation"]
    if not validation["allTablesParsed"] or not validation["allInsertsMatched"] or validation["insertRows"] != validation["tableRows"]:
        raise SystemExit("El análisis del respaldo no coincide; no se actualizaron los archivos.")
    OUT.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    candidate = make_candidate()
    (OUT / "candidate.json").write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    erd = PARSER["make_html"](DATA).replace("__DB__", "db_test_7b").replace("</style>", THEME + "</style>", 1)
    (OUT / "modelo_mere_db_test_7b.html").write_text(erd, encoding="utf-8")
    (DOCS / "modelo_mere_db_test_7b.html").write_text(erd, encoding="utf-8")
    md = markdown()
    page = html_dictionary()
    (OUT / "diccionario_datos_db_test_7b.md").write_text(md, encoding="utf-8")
    (OUT / "diccionario_datos_db_test_7b.html").write_text(page, encoding="utf-8")
    (DOCS / "diccionario_datos.md").write_text(md, encoding="utf-8")
    (DOCS / "diccionario_datos_db_test_7b.html").write_text(page, encoding="utf-8")
    landing = launch_page()
    landing = landing.replace("26 tablas", f"{len(DATA['tables'])} tablas")
    landing = landing.replace("203 columnas", f"{sum(len(t['columns']) for t in DATA['tables'])} columnas")
    landing = landing.replace("98,893 filas", f"{DATA['totalRows']:,} filas")
    landing = landing.replace("36 llaves foráneas", f"{sum(r['confirmed'] for r in DATA['relations'])} llaves foráneas")
    (DOCS / "index.html").write_text(landing, encoding="utf-8")

    counts = ["# Conteo de registros · db_test_7b", "", f"Fuente: `{SOURCE.relative_to(ROOT).as_posix()}`", "", "| Tabla | Columnas | Filas del respaldo |", "|---|---:|---:|"]
    counts += [f"| `{t['name']}` | {len(t['columns'])} | {t['rows']:,} |" for t in DATA["tables"]]
    counts += [f"| **Total** | **{sum(len(t['columns']) for t in DATA['tables'])}** | **{DATA['totalRows']:,}** |", "", f"Validación: {DATA['insertStatements']} INSERT; {validation['insertRows']:,} filas. FK declaradas: {sum(r['confirmed'] for r in DATA['relations'])}; relaciones inferidas: {sum(not r['confirmed'] for r in DATA['relations'])}.", ""]
    (OUT / "conteo_registros.md").write_text("\n".join(counts), encoding="utf-8")

    with (DOCS / "inventario_columnas.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream)
        writer.writerow(["Tabla", "Columna", "Tipo SQL", "Nulo", "Llaves", "Predeterminado", "Descripción", "Filas respaldo"])
        for table in DATA["tables"]:
            for col in table["columns"]:
                writer.writerow([table["name"], col["name"], col["type"], col["nullable"], keys(col), col.get("default"), describe(table, col), table["rows"]])

    receipt = {"source": SOURCE.relative_to(ROOT).as_posix(), "candidate": str((OUT / "candidate.json").relative_to(ROOT)), "erd": str((OUT / "modelo_mere_db_test_7b.html").relative_to(ROOT)), "dictionary_html": str((OUT / "diccionario_datos_db_test_7b.html").relative_to(ROOT)), "tables": len(DATA["tables"]), "columns": sum(len(t["columns"]) for t in DATA["tables"]), "rows": DATA["totalRows"], "foreign_keys": sum(r["confirmed"] for r in DATA["relations"]), "inferred_relations": sum(not r["confirmed"] for r in DATA["relations"]), "validation": validation}
    (OUT / "actualizacion_practica3.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
