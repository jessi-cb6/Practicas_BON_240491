# Informe de validación del diccionario

- Fuente: `respaldos/db_test_jessi.sql` (3,546,495 bytes).
- Encabezado de base de datos: `db_test_7b`.
- Tablas físicas analizadas: 15; columnas: 113.
- Filas INSERT contabilizadas: 20,252 en 16 sentencias.
- Claves foráneas declaradas: 20; relaciones inferidas: 1.
- Vistas: 5; procedimientos: 2; triggers: 39.
- INSERT solo en tablas analizadas: True; filas INSERT = filas acumuladas por tabla: True.

Los totales describen filas presentes en el SQL, no el servidor en ejecución. Las vistas se ejecutan para obtener su contenido y por ello no tienen conteo almacenado en el respaldo. Archify se utiliza para el ERD interactivo; este Markdown y sus CSV se generan directamente del DDL/INSERT mediante el parser local.

Archify generó el ERD interactivo con 15 entidades, 113 atributos y 19 relaciones dibujadas. Las validaciones de esquema, entrega y artefacto pasaron. El browser-check no pudo completar la inspección de Chrome porque DevTools cerró su tubería al ejecutarse con elevación; el HTML quedó generado. Las dos FK autorreferentes se explican en el ERD y se detallan como relaciones en este diccionario.
