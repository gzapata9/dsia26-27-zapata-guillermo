# Ejercicios (30 min) — 8 sep 2026  
## Repaso de la teoría: venv + Git/GitHub

Trabaja en pareja si quieres, pero cada uno debe tener **su** repo.

---

### Ej. 1 — Conceptos (5 min, escrito)

Responde en `sesion01.md` (3–5 líneas por pregunta):

1. ¿Qué diferencia hay entre el Python global y el de `.venv`?
2. ¿Para qué sirve `requirements.txt`?
3. ¿Qué tres rutas/ficheros no debes subir nunca a GitHub en este curso?

### Ej. 2 — Entorno (8 min)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python sesiones/2026-09-08/ejemplos/check_entorno.py
```

**OK si** el script imprime `ENTORNO OK`.

### Ej. 3 — Repo + rama (10 min)

1. Crea en GitHub `dsia-26-27-apellido-nombre`.
2. Clónalo, copia/adapta un README con nombre, máster y 3 objetivos.
3. Rama `practica/sesion-01`, añade `sesion01.md` (incluye Ej. 1), commit y push.

### Ej. 4 — PR y verificación de teoría (7 min)

1. Abre un Pull Request a `main`.
2. En la descripción del PR, completa:

> El comando que activa el venv en mi SO es: `________`  
> Un buen mensaje de commit de hoy sería: `________`

3. Pide a un compañero que abra tu README y marque ✓ si puede entender cómo clonar tu repo.

### Criterio de cierre

- [ ] `check_entorno.py` en verde  
- [ ] URL del repo + PR visibles  
- [ ] Respuestas del Ej. 1 en el repo  

**Para el 15 sep:** deja el venv listo y abre `Datos/ventas.csv`.
