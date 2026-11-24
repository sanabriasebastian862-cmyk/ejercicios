# 🐛 Reto de Depuración (Bug Hunting): API Taller Mecánico

Este repositorio contiene una API construida con **FastAPI** y **SQLAlchemy Asíncrono**, pero presenta **10 errores críticos** de lógica, asincronía, validación e integridad referencial.

## Flujo de trabajo obligatorio (Git & GitHub)
1. Haz un **Fork** de este repositorio a tu cuenta personal de GitHub.
2. Clona tu fork localmente, crea tu entorno virtual (`venv`) e instala `requirements.txt`.
3. Crea tu archivo `.env` basándote en `.env.example`.
4. Encuentra y corrige los **10 bugs** del sistema.
5. **Regla de Git:** Debes realizar **al menos 1 commit descriptivo por cada bug solucionado** (ej. `fix: agregar await en db.delete para eliminar ordenes`). No se aceptan entregas con un único commit gigante.

## Pruebas que debe superar tu API antes de entregar
- [ ] Al arrancar Uvicorn, las 3 tablas (`ordenes`, `mecanicos`, `repuestos`) deben crearse en SQLite.
- [ ] Crear un mecánico y desactivarlo con `DELETE /mecanicos/{id}` debe ocultarlo de `GET /mecanicos`, manteniendo el registro en BD con `activo = 0`.
- [ ] Intentar crear una orden asignada a un mecánico inexistente o desactivado debe devolver HTTP `400`.
- [ ] `GET /ordenes` debe devolver la lista de órdenes con los datos anidados de su mecánico sin bucles infinitos ni errores asíncronos.
- [ ] `PATCH /ordenes/{id}` enviando solo `{"estado": "Reparada"}` no debe borrar la `falla_reportada` ni el `costo_reparacion` existentes.
- [ ] `DELETE /ordenes/{id}` debe eliminar físicamente el registro de la base de datos.

#Juan Sebastian Sanabria Daza 