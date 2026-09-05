# E0 — Entornos virtuales y Git/GitHub (30 min)

**Sesión:** 8 sep 2026 · Guía: `../../sesiones/2026-09-08_presentacion_venv_git.md`

## Parte 1 — Entorno virtual (8 min)

Desde la carpeta del curso (o la que uses como base):

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -c "import pandas, pytest; print('ok')"
```

**Checkpoint:** el comando imprime `ok` y `which python` / `where python` apunta a `.venv`.

## Parte 2 — Repo personal (8 min)

1. En GitHub, crea un repositorio **privado o público** llamado:
   `dsia-26-27-apellido-nombre`
2. Añade un `README.md` con:
   - Nombre y máster
   - Objetivos personales del curso (3 bullets)
   - Enlace al repo del curso (cuando exista)
3. Clónalo en local y ábrelo en el IDE.

## Parte 3 — Primera rama y commit (8 min)

```bash
git checkout -b practica/sesion-01
```

Crea `sesion01.md` con 5–8 líneas: qué es DSIA, qué es un venv, y un comando Git que hayas usado hoy.

```bash
git add sesion01.md README.md
git commit -m "Add session 01 notes and personal README"
git push -u origin practica/sesion-01
```

## Parte 4 — Pull Request (6 min)

1. Abre un PR de `practica/sesion-01` → `main`.
2. En la descripción del PR: una frase con lo que has configurado hoy.
3. (Opcional) Pide review a un compañero.

## Extensión si terminas pronto

- Añade `.gitignore` mínimo (`.venv/`, `.env`, `__pycache__/`, `.DS_Store`) si el repo no lo tiene.
- Configura SSH con GitHub o el credential helper que uses.

## Hecho cuando…

URL del repo + PR (o commit en `main`) visibles, y venv verificado en tu máquina.
