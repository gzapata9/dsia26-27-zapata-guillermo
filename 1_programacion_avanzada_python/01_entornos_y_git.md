# Sesión 8 sep 2026 — Entornos virtuales y Git/GitHub

Guía docente completa (presentación + 30′ teoría + 30′ práctica):  
[`sesiones/2026-09-08_presentacion_venv_git.md`](../sesiones/2026-09-08_presentacion_venv_git.md)

Ejercicio cronometrado: [`ejercicios/E0_entornos_git.md`](ejercicios/E0_entornos_git.md)

## Cheatsheet de la demo

### Entorno virtual

```bash
cd dsia-26-27
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
which python
python -c "import pandas, pytest; print('ok')"
```

### Git básico

```bash
git status
git checkout -b practica/sesion-01
echo "# Mi cuaderno de DSIA" > NOTAS.md
git add NOTAS.md
git commit -m "Add session notes scaffold"
git push -u origin practica/sesion-01
```

## Buenas prácticas

- Commits pequeños; mensaje en imperativo (`Add`, `Fix`, `Update`).
- Nunca subir secretos (`.env`, claves API) ni `.venv/`.
- Trabajar en ramas; integrar con Pull Request cuando sea posible.

## Para la próxima sesión (15 sep)

Entorno OK + ojeada a `Datos/ventas.csv` y a `proyectos/proyecto_i/`.
