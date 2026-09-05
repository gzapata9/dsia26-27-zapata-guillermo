# Sesión 1 (8 sep 2026): Entornos virtuales y Git/GitHub

Duración orientativa: **1 h 45 min**.

## Objetivos

- Crear y activar un entorno virtual con `venv`.
- Instalar dependencias desde `requirements.txt`.
- Inicializar un repositorio Git y subirlo a GitHub.
- Entender el flujo `clone` → `branch` → `commit` → `push` → `PR`.

## 1. Entorno virtual

```bash
cd dsia-26-27
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Comprueba:

```bash
which python
python -c "import pandas, pytest; print('ok')"
```

## 2. Git básico

```bash
git status
git checkout -b practica/sesion-01
echo "# Mi cuaderno de DSIA" > NOTAS.md
git add NOTAS.md
git commit -m "Add session notes scaffold"
git push -u origin practica/sesion-01
```

Buenas prácticas:

- Commits pequeños y con mensaje en imperativo (`Add`, `Fix`, `Update`).
- Nunca subir secretos (`.env`, claves API).
- Usar `.gitignore` (ya incluido en el repo del curso).

## 3. Ejercicio en clase (20–25 min)

1. Crea un repo **personal** en GitHub para tus proyectos de DSIA (`dsia-26-27-apellido-nombre`).
2. Añade un `README.md` con tu nombre, máster y objetivos del curso.
3. Crea una rama, añade un fichero `sesion01.md` con 5 líneas de resumen de la clase y abre un Pull Request hacia `main`.

## Para la próxima sesión

Instala/verifica pandas y revisa el dataset `1_programacion_avanzada_python/Datos/ventas.csv`.
