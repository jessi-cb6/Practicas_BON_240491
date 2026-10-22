"""Genera el diccionario y sus inventarios desde db_test_jessi.sql."""
import csv, json, re, runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "documentacion"
DOCS.mkdir(exist_ok=True)
data = runpy.run_path(str(ROOT / "scripts" / "build_eer.py"), run_name="schema_parser")["analyze"]()

PURPOSE = {
 "tb_buyer_orders":"Cabecera de pedidos recibidos por un vendedor. Registra importes de subtotal y envío, etapa de cumplimiento, vigencia y fechas; las restricciones CHECK requieren importes no negativos.",
 "tb_carts":"Carrito de compra vinculado a una cuenta. La clave UNIQUE de user_ID limita a un carrito por usuario.",
 "tb_logs":"Bitácora de auditoría que almacena la entidad y operación afectadas, actor, fecha, descripción y resultado. product_id es una referencia informativa opcional, no una FK declarada.",
 "tb_products":"Catálogo de productos con SKU único, descripción, precio actual, existencias, estado y marcas temporales.",
 "tb_user_addresses":"Direcciones de entrega de las cuentas, con etiqueta, destinatario, instrucciones, coordenadas opcionales y marcas de vigencia. CHECK valida rangos y presencia conjunta de coordenadas.",
 "tb_users":"Cuentas de usuario con correo y alias únicos, credencial, estado y fechas de alta, actualización y último acceso.",
 "tbc_categories":"Catálogo jerárquico de categorías. Cada categoría puede referir opcionalmente a una categoría superior de la misma tabla.",
 "tbc_payment_methods_types":"Catálogo de tipos de método de pago con código único, descripción, estado y fechas de mantenimiento.",
 "tbd_address_components":"Componentes que desglosan una dirección. Una FK vincula con la dirección y otra, compuesta, enlaza opcionalmente el componente padre dentro de la misma dirección.",
 "tbd_carts_items":"Líneas de carrito identificadas por carrito, proveedor y producto. quantity debe ser mayor que cero.",
 "tbd_order_items":"Líneas históricas de pedido con producto/proveedor, nombre copiado, cantidad y precio unitario. subtotal es una columna generada almacenada como cantidad por precio.",
 "tbd_products_categories":"Tabla puente entre productos y categorías. Su clave primaria compuesta impide duplicar una pareja producto-categoría.",
 "tbd_products_users_providers":"Tabla puente que registra la relación de un usuario con un producto como titular, revendedor o distribuidor, junto con disponibilidad y estado.",
 "tbd_user_payment_methods":"Métodos de pago asociados a usuarios y a un tipo del catálogo. El par proveedor/referencia externa es único.",
 "tbd_users_wishlist_products":"Tabla puente de productos guardados por usuarios en listas de deseos, con estado y fechas.",
}

COLUMN = {
 "ID":"Identificador técnico de la fila.", "SKU":"Código comercial único del producto.", "name":"Nombre legible del producto o categoría.", "description":"Descripción textual complementaria; no se impone formato en el DDL.",
 "current_price":"Precio monetario vigente del producto.", "current_stock":"Unidades registradas en existencia.", "status":"Indicador binario de estado; el esquema no define el significado funcional de 0 y 1.",
 "creation_date":"Fecha y hora de creación del registro.", "last_update":"Fecha y hora de última actualización; cuando declara ON UPDATE, MySQL la modifica automáticamente.",
 "email":"Correo asociado a la cuenta; la clave UNIQUE exige que no se repita.", "nick":"Alias de la cuenta; la clave UNIQUE exige que no se repita.", "password":"Cadena de credencial. El DDL no indica si el contenido está cifrado o resumido; se omite en ejemplos.", "last_login":"Fecha y hora del último acceso; NULL indica que no hay valor almacenado.",
 "table_name":"Nombre textual de la tabla/entidad registrada en la bitácora.", "table_operation":"Operación auditada, limitada al ENUM declarado.", "db_user":"Actor de base de datos consignado en el evento.", "operation_date":"Fecha y hora en que se registró la operación.", "operation_description":"Detalle textual del evento auditado.", "operation_status":"Indicador binario de resultado; el DDL no define qué valor representa éxito o error.", "product_id":"Identificador opcional relacionado con el evento; no tiene FOREIGN KEY declarada.",
 "sup_id_category":"Categoría superior opcional; FK autorreferente a tbc_categories.ID.", "product_ID":"Identificador del producto; puede ser FK, parte de PK compuesta o ambas según la tabla.", "categories_ID":"Identificador de categoría; FK y parte de la PK de la tabla puente.", "user_ID":"Identificador de usuario; según la tabla es FK, parte de PK o clave UNIQUE.", "type_ownership":"Tipo de relación permitido por ENUM: Owner, Reseller o Distributor.", "available_date":"Fecha y hora desde la que se declara disponible la relación usuario-producto.",
 "seller_ID":"Usuario vendedor asociado al pedido; FK a tb_users.ID.", "subtotal":"Importe subtotal del pedido; CHECK requiere valor no negativo.", "shipping_cost":"Importe del envío; CHECK requiere valor no negativo.", "fulfillment_status":"Estado de cumplimiento del pedido, limitado a Pending, Accepted, Preparing, Sent, Delivered, Canceled o Returned.",
 "address_label":"Etiqueta libre para distinguir la dirección, por ejemplo casa o trabajo.", "recipient_name":"Nombre de quien recibirá el envío; opcional.", "recipient_phone":"Teléfono de contacto opcional, guardado como texto para conservar prefijos y formato.", "delivery_instructions":"Instrucciones opcionales para la entrega.", "latitude":"Latitud decimal opcional; CHECK limita el rango a −90..90 y requiere que ambas coordenadas estén presentes o ausentes.", "longitude":"Longitud decimal opcional; CHECK limita el rango a −180..180 y requiere que ambas coordenadas estén presentes o ausentes.", "is_default":"Indicador numérico 0/1 de dirección o método predeterminado; tinyint(1) no constituye por sí solo una restricción booleana.",
 "code":"Código textual único del tipo de método de pago.", "address_ID":"Dirección a la que pertenece el componente; participa en FK a tb_user_addresses y en referencia compuesta al padre.", "value":"Valor textual del componente de dirección.", "component_type":"Tipo textual de componente; no hay catálogo ENUM en el DDL.", "address_sup_ID":"Componente padre opcional dentro de la misma dirección; participa en FK compuesta a tbd_address_components(address_ID, ID).",
 "cart_ID":"Carrito de la línea; FK a tb_carts.ID y parte de la clave primaria compuesta.", "provider_ID":"Usuario proveedor del producto; participa en la FK compuesta de producto-proveedor.", "quantity":"Cantidad entera de unidades; CHECK requiere un valor mayor que cero.", "seller_order_ID":"Pedido al que pertenece la línea; FK a tb_buyer_orders.ID.", "product_name":"Nombre del producto guardado como instantánea en la línea; no es FK.", "unit_price":"Precio unitario monetario de la línea; CHECK exige valor no negativo.", "payment_method_type_ID":"Tipo de método de pago; FK a tbc_payment_methods_types.ID.", "provider":"Identificador textual del proveedor externo.", "provider_method_ref":"Referencia externa del método; junto con provider está sujeta a UNIQUE.", "label":"Etiqueta opcional para mostrar o reconocer el método de pago.", "last_four":"Últimos cuatro caracteres del identificador de pago, en formato textual.",
}

def compose(c):
 t=c['type'].lower()
 if t.startswith('enum'): return 'Valores textuales cerrados: ' + ', '.join(c['enum']) + '.'
 if t.startswith('varchar'): return f"Cadena de longitud variable, máximo {t[t.find('(')+1:t.find(')')]} caracteres; no se declara otro patrón."
 if t.startswith('char('): return f"Cadena de longitud fija de {t[t.find('(')+1:t.find(')')]} caracteres."
 if t == 'text': return 'Texto de longitud variable; el DDL no fija un límite funcional menor.'
 if t.startswith('decimal'):
  p,s=map(int,t[t.find('(')+1:t.find(')')].split(',')); return f"Decimal exacto DECIMAL({p},{s}): hasta {p-s} dígitos enteros y {s} decimales."
 if t.startswith('bit(1)'): return 'Campo de un bit, con valores 0 o 1; su significado funcional depende de la aplicación.'
 if t == 'datetime': return 'Fecha y hora SQL (YYYY-MM-DD HH:MM:SS); no almacena zona horaria.'
 if t.startswith('bigint'): return 'Entero BIGINT de 64 bits' + (' sin signo (UNSIGNED).' if 'unsigned' in t else ' con signo.')
 if t.startswith('int'): return 'Entero INT de 32 bits' + (' sin signo (UNSIGNED).' if 'unsigned' in t else ' con signo.')
 if t.startswith('tinyint(1)'): return 'Entero de 8 bits declarado tinyint(1); no es un booleano estricto.'
 return f'Tipo SQL declarado: {c["type"]}.'

def classification(c):
 n=c['name'].lower(); t=c['type'].lower()
 if t == 'datetime': return 'Temporal; fecha y hora (escala no asignada)'
 if c['pk'] or c['fk'] or n.endswith('_id') or n in {'id','sku','email','nick','code','provider_method_ref','last_four'}: return 'Cualitativa nominal; identificador/código'
 if t.startswith('enum') or t.startswith('bit') or n in {'status','operation_status','is_default','table_operation','fulfillment_status','type_ownership'}: return 'Cualitativa nominal; categoría/indicador'
 if t.startswith('decimal'):
  if n in {'latitude','longitude'}: return 'Cuantitativa continua; coordenada'
  return 'Cuantitativa continua; importe' if any(x in n for x in ('price','cost','subtotal')) else 'Cuantitativa continua; medida decimal'
 if t.startswith('int') or t.startswith('tinyint'): return 'Cuantitativa discreta; conteo/valor entero'
 return 'Cualitativa nominal; texto descriptivo'

def constraints_for(t,c):
 out=[]
 if c['pk']: out.append('PK')
 if c['uk']: out.append('UNIQUE')
 if c['fk']: out.append('FK')
 out.append('NULL' if c['nullable'] else 'NOT NULL')
 if c['autoIncrement']: out.append('AUTO_INCREMENT')
 if c['default'] is not None: out.append('DEFAULT '+c['default'])
 if c['onUpdate']: out.append('ON UPDATE CURRENT_TIMESTAMP')
 if 'GENERATED ALWAYS AS' in c['declaration'].upper(): out.append(c['declaration'][c['declaration'].upper().find('GENERATED ALWAYS AS'):])
 return '; '.join(out)

def unique_fk(r):
 t=next(t for t in data['tables'] if t['name']==r['fromTable'])
 for con in t['constraints']:
  m=re.search(r'UNIQUE(?: KEY| INDEX)?\s*(?:`[^`]+`\s*)?\(([^)]*)\)',con,re.I)
  if m and set(re.findall(r'`([^`]+)`',m.group(1)))==set(r['fromCols']): return True
 return False

def example(c):
 n=c['name']; t=c['type'].lower()
 if n.lower()=='password': return '[omitido por sensibilidad]'
 if t.startswith('enum'): return c['enum'][0]
 if t.startswith('bit'): return "b'1'"
 if t=='datetime': return '2026-01-15 12:00:00'
 if t.startswith('decimal'): return '19.99'
 if t.startswith('int') or t.startswith('bigint') or t.startswith('tinyint'): return '1'
 if n=='email': return 'persona@example.test'
 if n=='provider_method_ref': return '[referencia ficticia]'
 return 'Ejemplo textual'

md=[f"# Diccionario de datos — {data['database']}", '', f"**Fuente SQL:** `respaldos/{data['source']}` ({data['sizeBytes']:,} bytes).  ", '**Motor:** MySQL 8.0.36, según la cabecera del respaldo.  ', '**Alcance:** definiciones y filas incluidas en el archivo; las cantidades no representan el servidor actual.', '', '## Resumen', '', f"El respaldo contiene {len(data['tables'])} tablas físicas, {sum(len(t['columns']) for t in data['tables'])} columnas, {data['totalRows']:,} filas en {data['insertStatements']} sentencias INSERT, {sum(r['confirmed'] for r in data['relations'])} claves foráneas declaradas, {len(data['views'])} vistas, {len(data['procedures'])} procedimientos y {len(data['triggers'])} triggers.", '', '| Tabla | Columnas | Filas del respaldo | Descripción |', '|---|---:|---:|---|']
for t in data['tables']: md.append(f"| `{t['name']}` | {len(t['columns'])} | {t['rows']:,} | {PURPOSE.get(t['name'],'Función no precisada por los nombres del esquema.')} |")
md += ['', '## Diccionario detallado', '']
csvrows=[]
for t in data['tables']:
 md += [f"### {t['name']}", '', f"**Descripción.** {PURPOSE.get(t['name'],'Función no precisada por los nombres del esquema.')}", '', f"**Filas incluidas en SQL:** {t['rows']:,}.", '', '| Columna | Tipo SQL | Composición | Descripción | Clasificación | Restricciones | Referencia |', '|---|---|---|---|---|---|---|']
 for c in t['columns']:
  rel=next((r for r in data['relations'] if r['confirmed'] and r['fromTable']==t['name'] and c['name'] in r['fromCols']),None)
  ref='; '.join(f"`{rel['toTable']}`.`{col}`" for col in rel['toCols']) if rel else ('Posible `tb_products`.`ID` por nombre/uso; no declarada como FK.' if t['name']=='tb_logs' and c['name']=='product_id' else '—')
  functional=COLUMN.get(c['name'],f"Campo `{c['name']}`; su significado funcional no se define con mayor precisión en el DDL.")
  md.append(f"| `{c['name']}` | `{c['type']}` | {compose(c)} | {functional} | {classification(c)} | {constraints_for(t,c)} | {ref} |")
  csvrows.append({'tabla':t['name'],'columna':c['name'],'tipo_sql':c['type'],'declaracion':c['declaration'],'composicion':compose(c),'descripcion':functional,'clasificacion':classification(c),'restricciones':constraints_for(t,c),'referencia':ref,'filas_respaldo':t['rows']})
 md += ['', '**Restricciones e índices de tabla (DDL):**', '']
 md += [f"- `{x}`" for x in t['constraints']] or ['- Sin claves, índices ni restricciones declarados.']
 md.append('')

md += ['## Relaciones entre tablas', '', '| Estado | Nombre FK | Origen | Destino | Cardinalidad | Reglas |', '|---|---|---|---|---|---|']
for r in data['relations']:
 state='Declarada en DDL' if r['confirmed'] else 'Inferida; no FK'
 rule=r['rules'] or 'ON DELETE/UPDATE no indicado explícitamente (InnoDB aplica RESTRICT/NO ACTION por defecto).'
 cardinality=('1:1 (FK UNIQUE)' if unique_fk(r) else 'N:1 desde origen; 1:N desde destino') if r['confirmed'] else 'Candidata N:1; sin integridad FK'
 md.append(f"| {state} | `{r['name']}` | `{r['fromTable']}.{','.join(r['fromCols'])}` | `{r['toTable']}.{','.join(r['toCols'])}` | {cardinality} | {rule} |")
md += ['', 'Las tablas puente forman relaciones muchos a muchos: productos-categorías, usuarios-productos/proveedores, usuarios-lista de deseos y carrito-producto-proveedor. `tbd_address_components` contiene una jerarquía autorreferente limitada a la misma dirección. La FK compuesta para líneas de carrito/pedido relaciona `provider_ID` y `product_ID` por separado en el DDL; la integridad efectiva depende de ambas restricciones y de las claves referenciadas.', '', '## Vistas', '', 'Las vistas no tienen filas INSERT propias en el respaldo; su resultado depende de la consulta al ejecutarlas.', '']
for v in data['views']: md.append(f"- `{v}`")
md += ['', '## Procedimientos y triggers', '', '**Procedimientos:** '+(', '.join(f'`{x}`' for x in data['procedures']) or 'ninguno'), '', '**Triggers:** '+(', '.join(f'`{x}`' for x in data['triggers']) or 'ninguno'), '', '## Criterios y límites', '', '- Los conteos se obtuvieron contando tuplas INSERT del archivo SQL y se refieren exclusivamente al respaldo.', '- `NULL`, `DEFAULT`, `AUTO_INCREMENT`, índices y restricciones se copiaron del DDL. Las restricciones CHECK y los índices completos se listan por tabla.', '- La clasificación cualitativa/cuantitativa describe el uso semántico inferido; identificadores numéricos se clasifican como cualitativos nominales.', '- Los campos sin descripción explícita en el DDL se interpretan por su nombre. Las referencias no declaradas se identifican como inferencias.', '- Las vistas no tienen un total de registros estático dentro del respaldo.', '- Los ejemplos son esquemáticos, no datos del respaldo; se omite el contenido de `password`.']
(DOCS/'diccionario_datos.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
with (DOCS/'inventario_columnas.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(csvrows[0]));w.writeheader();w.writerows(csvrows)
with (DOCS/'filas_respaldo.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['tabla','columnas','filas_insertadas_en_respaldo']);w.writerows((t['name'],len(t['columns']),t['rows']) for t in data['tables'])
with (DOCS/'relaciones.csv').open('w',newline='',encoding='utf-8-sig') as f:
 fields=['estado','nombre_fk','tabla_origen','columnas_origen','tabla_destino','columnas_destino','cardinalidad','reglas']
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in data['relations']: w.writerow({'estado':'Declarada' if r['confirmed'] else 'Inferida','nombre_fk':r['name'],'tabla_origen':r['fromTable'],'columnas_origen':','.join(r['fromCols']),'tabla_destino':r['toTable'],'columnas_destino':','.join(r['toCols']),'cardinalidad':('1:1; FK UNIQUE' if unique_fk(r) else 'N:1 desde origen; 1:N desde destino') if r['confirmed'] else 'Candidata N:1; sin FK','reglas':r['rules'] or 'No declaradas explícitamente'})
report=['# Informe de validación del diccionario','',f"- Fuente: `respaldos/{data['source']}` ({data['sizeBytes']:,} bytes).",f"- Encabezado de base de datos: `{data['database']}`.",f"- Tablas físicas analizadas: {len(data['tables'])}; columnas: {sum(len(t['columns']) for t in data['tables'])}.",f"- Filas INSERT contabilizadas: {data['totalRows']:,} en {data['insertStatements']} sentencias.",f"- Claves foráneas declaradas: {sum(r['confirmed'] for r in data['relations'])}; relaciones inferidas: {sum(not r['confirmed'] for r in data['relations'])}.",f"- Vistas: {len(data['views'])}; procedimientos: {len(data['procedures'])}; triggers: {len(data['triggers'])}.",f"- INSERT solo en tablas analizadas: {data['validation']['allInsertsMatched']}; filas INSERT = filas acumuladas por tabla: {data['validation']['insertRows']==data['validation']['tableRows']}.",'','Los totales describen filas presentes en el SQL, no el servidor en ejecución. Las vistas se ejecutan para obtener su contenido y por ello no tienen conteo almacenado en el respaldo. Archify se utiliza para el ERD interactivo; este Markdown y sus CSV se generan directamente del DDL/INSERT mediante el parser local.']
report += ['', 'Archify generó el ERD interactivo con 15 entidades, 113 atributos y 19 relaciones dibujadas. Las validaciones de esquema, entrega y artefacto pasaron. El browser-check no pudo completar la inspección de Chrome porque DevTools cerró su tubería al ejecutarse con elevación; el HTML quedó generado. Las dos FK autorreferentes se explican en el ERD y se detallan como relaciones en este diccionario.']
(DOCS/'informe_validacion.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
print(json.dumps({'source':data['source'],'tables':len(data['tables']),'columns':sum(len(t['columns']) for t in data['tables']),'rows':data['totalRows'],'fks':sum(r['confirmed'] for r in data['relations']),'views':len(data['views']),'procedures':len(data['procedures']),'triggers':len(data['triggers']),'validation':data['validation']},ensure_ascii=False,indent=2))
