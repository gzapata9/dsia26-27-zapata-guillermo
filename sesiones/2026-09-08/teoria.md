# Teoría (30 min) — 8 sep 2026  
## Presentación breve + entornos virtuales + Git/GitHub

**Objetivo de la teoría:** salir sabiendo crear un entorno reproducible y versionar código con Git.

---

## 1. Introducción (5 min)

En DSIA no entregamos “un script que me funciona”. Entregamos **soluciones reproducibles**:

- mismo Python / mismas librerías → mismo comportamiento;
- historial en Git → se puede revisar, revertir y colaborar;
- secretos fuera del código → `.env` nunca va al remoto.

Hoy montamos la base de las 13 semanas restantes.

---

## 2. Conceptos

### 2.1 Entorno virtual (`venv`)

| Concepto | Significado |
| --- | --- |
| Intérprete global | Python del sistema / instalado para todo el SO |
| Entorno virtual | Copia aislada de Python + `site-packages` del proyecto |
| `requirements.txt` | Lista de dependencias para recrear el entorno |
| Activar | Hace que `python` y `pip` apunten al `.venv` |

**Por qué importa:** dos proyectos pueden necesitar `pandas` 2.0 y 2.2; sin venv hay conflictos.

### 2.2 Git — modelo mental

```text
  working tree          staging area           historial local          remoto
 (archivos editados) → (git add) → (git commit) → (git push) → GitHub
```

| Término | Idea |
| --- | --- |
| `commit` | Foto del proyecto con mensaje |
| `branch` | Línea de trabajo paralela |
| `main` | Rama principal de integración |
| `PR` | Propuesta de integrar una rama en otra |
| `.gitignore` | Qué no debe versionarse (`.venv/`, `.env`, …) |

### 2.3 Buenas prácticas (examen + proyectos)

1. Commits pequeños, mensaje en imperativo: `Add README`, `Fix validator`.
2. Nunca subir `.venv/`, `.env`, claves API, `__pycache__/`.
3. Trabajar en ramas (`practica/…`, `feature/…`).
4. El README explica cómo instalar y ejecutar en < 5 pasos.

---

## 3. Código y ejemplos (live)

### 3.1 Crear e instalar el entorno

```bash
cd dsia-26-27
python3 --version                 # conviene 3.11+
python3 -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Comprobación:

```bash
which python                      # debe contener .venv
python -c "import pandas, pytest; print(pandas.__version__)"
```

Desactivar / reactivar:

```bash
deactivate
source .venv/bin/activate
```

### 3.2 Primer flujo Git

```bash
git status
git checkout -b practica/sesion-01
printf '# Notas DSIA\n\n- venv\n- git\n' > NOTAS.md
git add NOTAS.md
git commit -m "Add session notes scaffold"
git push -u origin practica/sesion-01
```

### 3.3 Ejemplo de `.gitignore` mínimo

```gitignore
.venv/
.env
__pycache__/
.pytest_cache/
.DS_Store
```

Script de auto-chequeo: `ejemplos/check_entorno.py`.

---

## 4. Resumen (checklist)

- [ ] Sé explicar qué problema resuelve un venv  
- [ ] Sé instalar desde `requirements.txt`  
- [ ] Sé crear rama, commit y push  
- [ ] Sé qué no debe entrar en Git  

→ Pasa a `ejercicios.md` (30 min) para fijar la teoría.
