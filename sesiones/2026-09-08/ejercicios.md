# Ejercicios (30 min) — 8 sep 2026  
## Repaso de la teoría: venv + Git/GitHub

**Antes de empezar:** ten abierta la teoría [`teoria.md`](teoria.md) y la referencia [`01_entornos_y_git.md`](../../1_programacion_avanzada_python/01_entornos_y_git.md).

Trabaja en individual (el repo debe ser **tuyo**). Parejas solo para peer-check del final.

---

## Ej. 1 — Conceptos escritos (6 min)

Crea `sesion01.md` en tu repo personal y responde (3–5 líneas cada una):

1. ¿Qué problema concreto resuelve un entorno virtual frente al Python global?
2. Explica con tus palabras las tres zonas: working tree, staging, historial de commits.
3. Indica **cuatro** elementos que no deben subirse a GitHub en DSIA y por qué.
4. Reescribe estos malos mensajes de commit a estilo imperativo correcto:
   - `update`
   - `cambios varios`
   - `fix`

**Criterio:** alguien que no estuvo en clase entiende tus respuestas.

---

## Ej. 2 — Laboratorio venv (8 min)

En el repo del **curso** (`dsia-26-27`):

```bash
cd dsia-26-27
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -c "import sys; print(sys.executable)"
python sesiones/2026-09-08/ejemplos/check_entorno.py --strict
```

Tareas de repaso teórico (anota en `sesion01.md`):

1. Pega la ruta de `sys.executable` y marca dónde aparece `.venv`.
2. Ejecuta `deactivate` y vuelve a lanzar `check_entorno.py` **sin** `--strict`. ¿Qué aviso sale?
3. Reactiva el venv y confirma `ENTORNO OK` con `--strict`.

**OK si:** `ENTORNO OK` con `--strict` y has documentado el aviso sin venv.

---

## Ej. 3 — Repo personal + `.gitignore` (8 min)

1. Crea en GitHub `dsia-26-27-apellido-nombre` y clónalo.
2. Copia la plantilla:

```bash
cp /ruta/a/dsia-26-27/sesiones/2026-09-08/ejemplos/gitignore_dsia.txt .gitignore
```

3. Escribe un `README.md` con:
   - nombre y máster,
   - 3 objetivos del curso,
   - bloque “Cómo instalar” (venv + `pip install -r` — aunque aún no tengas `requirements.txt`, documenta el patrón).
4. Añade `sesion01.md` (Ej. 1 + notas del Ej. 2).
5. Opcional recomendado: `AI_USAGE.md` vacío con un encabezado (política de citación).

```bash
git switch -c practica/sesion-01
git add .gitignore README.md sesion01.md
git status
git commit -m "Add session 01 notes, README and gitignore"
git push -u origin practica/sesion-01
```

**Trampa a evitar:** si `git status` muestra `.venv`, **no** hagas commit; corrige `.gitignore` y `git rm -r --cached .venv` si hace falta.

---

## Ej. 4 — Pull Request + peer review de teoría (8 min)

1. Abre un Pull Request `practica/sesion-01` → `main`.
2. En la descripción del PR completa este formulario (copia-pega):

```text
## Repaso teórico sesión 1
- Activo el venv con: `________________`
- Compruebo el intérprete con: `________________`
- Un buen commit message de hoy: `________________`
- Tres cosas que NUNCA subo: `____` / `____` / `____`
- Diferencia clone vs commit (1 frase): ________________
```

3. Intercambia URL con un compañero. Cada uno verifica en el README del otro:
   - [ ] Se entiende cómo clonar
   - [ ] Hay `.gitignore` con `.venv` y `.env`
   - [ ] `sesion01.md` responde las 4 preguntas del Ej. 1

### Extensión si terminas (2–3 min)

Ejecuta en seco (sin romper nada):

```bash
git log --oneline -5
git remote -v
```

Añade al final de `sesion01.md` qué URL tiene tu `origin`.

---

## Criterio de cierre de los 30′

- [ ] `check_entorno.py --strict` → `ENTORNO OK`
- [ ] Repo personal con README + `.gitignore` + `sesion01.md`
- [ ] Rama empujada + PR con el formulario de repaso
- [ ] Peer-check hecho (o auto-check si no hay pareja)

**Para el 15 sep:** deja el venv listo y abre `1_programacion_avanzada_python/Datos/ventas.csv`.
