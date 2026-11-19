"""Generate the row inventory, data dictionary and Archify ERD from the dated SQL dump."""
from __future__ import annotations

import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "respaldos" / "respaldo_final_22_10_2026.sql"
OUT = ROOT / ".archify" / "erd-db-test-7b-20261022-120000"
PARSER = runpy.run_path(str(ROOT / "scripts" / "build_eer.py"), run_name="schema_parser")
PARSER["analyze"].__globals__["SOURCE"] = SOURCE
DATA = PARSER["analyze"]()

DOMAINS = {
    "cuentas": ["tb_users", "tb_people", "tb_user_addresses", "tbd_address_components"],
    "catalogo": ["tb_products", "tbc_categories", "tbd_products_categories"],
    "ventas": ["tb_buyer_orders", "tbd_order_items", "tb_carts", "tbd_carts_items"],
    "proveedores": ["tbd_products_users_providers", "tbd_users_wishlist_products"],
    "pagos": ["tbc_payment_methods_types", "tbd_user_payment_methods"],
    "auditoria": ["tb_logs"],
}

FIELD_DESCRIPTIONS = {
    "ID": "Identificador único del registro.",
    "user_ID": "Usuario propietario o asociado al registro.",
    "seller_ID": "Usuario vendedor responsable de la orden.",
    "product_ID": "Producto asociado al registro.",
    "categories_ID": "Categoría asociada al producto.",
    "cart_ID": "Carrito al que pertenece el artículo.",
    "provider_ID": "Usuario proveedor asociado al artículo.",
    "seller_order_ID": "Orden de venta a la que pertenece el detalle.",
    "payment_method_type_ID": "Tipo de método de pago utilizado.",
    "address_ID": "Dirección a la que pertenece el componente.",
    "address_sup_ID": "Componente superior de esta jerarquía de dirección.",
    "sup_id_category": "Categoría superior; permite organizar categorías jerárquicamente.",
    "SKU": "Código de identificación comercial del producto.",
    "name": "Nombre visible del producto o categoría.",
    "description": "Descripción textual del producto, categoría o tipo.",
    "current_price": "Precio vigente del producto.",
    "current_stock": "Existencia actual del producto.",
    "status": "Indicador de vigencia o habilitación del registro.",
    "creation_date": "Fecha y hora de creación del registro.",
    "last_update": "Fecha y hora de la última modificación.",
    "email": "Correo electrónico de acceso o contacto del usuario.",
    "nick": "Nombre corto o alias del usuario.",
    "password": "Credencial de autenticación almacenada.",
    "last_login": "Fecha y hora del último inicio de sesión.",
    "person_ID": "Identificador único del perfil personal.",
    "courtesy_title": "Tratamiento o título de cortesía de la persona.",
    "given_names": "Nombres de la persona.",
    "family_names": "Apellidos de la persona.",
    "birth_date": "Fecha de nacimiento de la persona.",
    "gender": "Género declarado por la persona.",
    "country_code": "Código de país asociado al teléfono o perfil.",
    "phone": "Número telefónico de contacto de la persona.",
    "address_label": "Etiqueta que identifica la dirección para el usuario.",
    "recipient_name": "Nombre de la persona que recibirá el envío.",
    "recipient_phone": "Teléfono de contacto del destinatario.",
    "delivery_instructions": "Indicaciones para entregar en la dirección.",
    "latitude": "Coordenada geográfica de latitud.",
    "longitude": "Coordenada geográfica de longitud.",
    "is_default": "Indica si es la opción predeterminada.",
    "value": "Valor textual del componente de dirección.",
    "component_type": "Clase de componente de dirección (por ejemplo, calle o ciudad).",
    "subtotal": "Importe subtotal de la orden o línea.",
    "shipping_cost": "Costo de envío de la orden.",
    "fulfillment_status": "Estado del proceso de preparación y entrega.",
    "table_name": "Nombre de la tabla afectada por la operación registrada.",
    "table_operation": "Tipo de operación registrada sobre la base de datos.",
    "db_user": "Usuario de base de datos que ejecutó la operación.",
    "operation_date": "Fecha y hora en que se registró la operación.",
    "operation_description": "Detalle textual de la operación auditada.",
    "operation_status": "Resultado o estado de la operación auditada.",
    "product_id": "Identificador de producto relacionado con el evento; el dump no declara FK.",
    "provider": "Proveedor o procesador externo del método de pago.",
    "provider_method_ref": "Referencia del método en el sistema del proveedor de pagos.",
    "label": "Nombre descriptivo del método guardado por el usuario.",
    "last_four": "Últimos cuatro dígitos del medio de pago.",
    "code": "Código único o abreviado del tipo de método de pago.",
    "type_ownership": "Rol de propiedad o distribución del usuario sobre el producto.",
    "available_date": "Fecha desde la que el producto está disponible por ese proveedor.",
    "quantity": "Cantidad de unidades del producto.",
    "unit_price": "Precio unitario aplicado al producto en la operación.",
}

def describe(table: str, column: dict) -> str:
    name = column["name"]
    if name in FIELD_DESCRIPTIONS:
        desc = FIELD_DESCRIPTIONS[name]
    elif name == "creation_date":
        desc = FIELD_DESCRIPTIONS[name]
    elif name == "last_update":
        desc = FIELD_DESCRIPTIONS[name]
    else:
        desc = f"Atributo {name.replace('_', ' ')} asociado a {table.replace('_', ' ')}; significado inferido del nombre y tipo SQL."
    if name == "status" and table == "tb_buyer_orders":
        return "Indicador de vigencia de la orden."
    if name == "status" and table == "tb_carts":
        return "Indicador de vigencia del carrito."
    if name == "name" and table == "tb_products":
        return "Nombre comercial del producto."
    return desc

def key_role(column: dict) -> list[str] | str | None:
    roles = []
    if column.get("pk"):
        roles.append("pk")
    if column.get("fk"):
        roles.append("fk")
    if column.get("uk"):
        roles.append("uk")
    if len(roles) > 1:
        return roles
    return roles[0] if roles else None

def make_candidate() -> dict:
    table_domains = {t: d for d, tables in DOMAINS.items() for t in tables}
    entities = []
    indexes = {t["name"]: i for i, t in enumerate(DATA["tables"])}
    domain_col = {name: col for col, name in enumerate(DOMAINS)}
    domain_row = {name: 0 for name in DOMAINS}
    for table in DATA["tables"]:
        domain = table_domains[table["name"]]
        attrs = []
        for c in table["columns"]:
            # Keep enum domains in the dictionary; the diagram uses the SQL family
            # so a long list of values does not make the whole ERD unreadable.
            sql_type = "enum" if c["type"].lower().startswith("enum(") else c["type"]
            attr = {"name": c["name"], "type": sql_type}
            role = key_role(c)
            if role:
                attr["key"] = role
            ref = next((r for r in DATA["relations"] if r["confirmed"] and r["fromTable"] == table["name"] and c["name"] in r["fromCols"]), None)
            if ref:
                attr["references"] = f"{ref['toTable']}.{ref['toCols'][ref['fromCols'].index(c['name'])]}"
            attrs.append(attr)
        longest = max((len(c["name"]) + len("enum" if c["type"].lower().startswith("enum(") else c["type"]) for c in table["columns"]), default=20)
        entities.append({
            "id": table["name"], "label": table["name"],
            "sublabel": f"{table['rows']:,} filas · {len(table['columns'])} atributos",
            "tag": domain, "row": domain_row[domain], "col": domain_col[domain],
            "width": max(280, min(430, 70 + longest * 8)),
            "attributes": attrs,
        })
        domain_row[domain] += 1
    relationships = []
    self_references = []
    for i, rel in enumerate(DATA["relations"]):
        if not rel["confirmed"]:
            continue
        if rel["fromTable"] == rel["toTable"]:
            self_references.append(rel)
            continue
        from_table = DATA["tables"][indexes[rel["fromTable"]]]
        nullables = {c["name"]: c["nullable"] for c in from_table["columns"]}
        relationship = {
            "id": f"rel{i+1}", "from": rel["fromTable"], "to": rel["toTable"],
            "label": ", ".join(rel["fromCols"]), "fromCardinality": "many", "toCardinality": "one",
            "fromOptional": any(nullables.get(c, False) for c in rel["fromCols"]),
            "toOptional": False,
        }
        if rel["fromTable"] == "tb_user_addresses" and rel["toTable"] == "tb_users":
            relationship["labelDy"] = -288
        relationships.append(relationship)
    return {
        "schema_version": 1, "diagram_type": "erd",
        "meta": {
            "title": "MERE — db_test_7b",
            "subtitle": "Modelo físico extendido derivado del respaldo SQL; cardinalidad N:1 según FK declaradas.",
            "locale": "es", "quality_profile": "standard",
            "output": "modelo_mere_db_test_7b.html",
        },
        "layout": {"mode": "grid", "gapX": 80, "gapY": 44},
        "entities": entities, "relationships": relationships,
        "cards": ([{"dot": "violet", "title": "Autorrelaciones declaradas", "items": [f"{r['fromTable']}.{', '.join(r['fromCols'])} referencia {r['toTable']}.{', '.join(r['toCols'])} (jerarquía o relación recursiva)." for r in self_references]}] if self_references else []),
    }

def write_dictionary() -> None:
    lines = [
        "# Diccionario de datos — db_test_7b",
        "",
        f"Fuente: `{SOURCE.relative_to(ROOT).as_posix()}` · {len(DATA['tables'])} tablas · {DATA['totalRows']:,} filas en el respaldo.",
        "",
        "Los conteos son filas contenidas en las sentencias `INSERT` del archivo, no conteos de una instancia activa. Las descripciones funcionales se derivan del nombre, tipo y contexto del campo porque el dump no incluye comentarios `COMMENT` para las columnas.",
        "",
        "## Resumen de registros",
        "",
        "| Tabla | Registros | Columnas |",
        "|---|---:|---:|",
    ]
    for t in DATA["tables"]:
        lines.append(f"| `{t['name']}` | {t['rows']:,} | {len(t['columns'])} |")
    lines += ["", "## Definición de tablas", ""]
    for t in DATA["tables"]:
        lines += [f"### `{t['name']}`", "", f"Registros en el respaldo: **{t['rows']:,}**", "", "| Columna | Tipo SQL | Nulo | Llave | Descripción funcional |", "|---|---|---|---|---|"]
        for c in t["columns"]:
            roles = ", ".join(x for x, flag in (("PK", c.get("pk")), ("FK", c.get("fk")), ("UK", c.get("uk"))) if flag) or "—"
            lines.append(f"| `{c['name']}` | `{c['type']}` | {'Sí' if c['nullable'] else 'No'} | {roles} | {describe(t['name'], c)} |")
        lines.append("")
    lines += ["## Relaciones y cardinalidades", "", "Cada FK declarada en el respaldo produce una relación de muchos registros de origen hacia un registro referenciado (N:1). La participación del lado que contiene la FK es opcional si la columna admite `NULL`.", ""]
    for r in DATA["relations"]:
        status = "Declarada" if r["confirmed"] else "Inferida (no es FK física)"
        lines.append(f"- **{status}:** `{r['fromTable']}.{', '.join(r['fromCols'])}` → `{r['toTable']}.{', '.join(r['toCols'])}` (N:1).")
    (OUT / "diccionario_datos_db_test_7b.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    candidate = make_candidate()
    (OUT / "candidate.json").write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_dictionary()
    counts = ["# Conteo de registros — db_test_7b", "", f"Fuente: `{SOURCE.relative_to(ROOT).as_posix()}`", "", "| Tabla | Registros |", "|---|---:|"]
    counts.extend(f"| `{t['name']}` | {t['rows']:,} |" for t in DATA["tables"])
    counts += [f"| **Total** | **{DATA['totalRows']:,}** |", "", f"Validación: {DATA['insertStatements']} sentencias INSERT, {DATA['validation']['insertRows']:,} filas; todas las tablas e INSERT coinciden."]
    (OUT / "conteo_registros.md").write_text("\n".join(counts) + "\n", encoding="utf-8")
    print(json.dumps({"tables": len(DATA["tables"]), "insertStatements": DATA["insertStatements"], "totalRows": DATA["totalRows"], "validation": DATA["validation"], "out": str(OUT)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
