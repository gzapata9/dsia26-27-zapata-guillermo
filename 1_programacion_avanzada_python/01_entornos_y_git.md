# Sesión 8 sep 2026 — Entornos virtuales Python y control de versiones (Git/GitHub)

**Materiales de aula (teoría + ejercicios + demos):**  
[`sesiones/2026-09-08/`](../sesiones/2026-09-08/)

| Bloque | Fichero |
| --- | --- |
| Teoría 30′ | [`sesiones/2026-09-08/teoria.md`](../sesiones/2026-09-08/teoria.md) |
| Ejercicios 30′ | [`sesiones/2026-09-08/ejercicios.md`](../sesiones/2026-09-08/ejercicios.md) |
| Guía docente minutada | [`sesiones/2026-09-08_presentacion_venv_git.md`](../sesiones/2026-09-08_presentacion_venv_git.md) |
| Ejercicio E0 (alternativo / checklist) | [`ejercicios/E0_entornos_git.md`](ejercicios/E0_entornos_git.md) |

Este documento es la **referencia ampliada** de la sesión: conceptos, comandos, ejemplos y resolución de problemas.

---

## 1. Por qué esta sesión importa en DSIA

En la asignatura entregamos soluciones que otro debe poder:

1. **clonar**,
2. **instalar**,
3. **ejecutar**,
4. **revisar en GitHub**.

Sin entorno virtual y sin Git, el resto del curso (tests, pipelines, APIs, despliegue) se vuelve frágil.

```text
Máquina del alumno          Remoto                    Compañero / profesor
─────────────────           ──────                    ────────────────────
código + .venv local  ──►  GitHub (sin .venv)  ──►  clone + venv nuevo
     ↑                                                    │
   .env (secreto, local)                                  pip install -r …
```

---

## 2. Entornos virtuales con `venv`

### 2.1 Ideas clave

| Concepto | Significado |
| --- | --- |
| Python global | Intérprete del sistema; compartido por todos los proyectos |
| `.venv` | Entorno **aislado** del proyecto (intérprete + paquetes) |
| Activar | Hace que `python` / `pip` apunten al `.venv` |
| `requirements.txt` | Receta para recrear dependencias |
| `pip freeze` | Lista exacta de lo instalado (útil, pero a veces ruidosa) |

**Analogía:** el venv es una “caja de herramientas” por proyecto. No mezcles destornilladores de obras distintas.

### 2.2 Crear, activar, instalar (macOS / Linux)

```bash
cd dsia-26-27                    # o la carpeta de tu repo personal
python3 --version                # recomendado 3.11+
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2.3 Windows (PowerShell / cmd)

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si `activate` está bloqueado en PowerShell:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 2.4 Cómo saber que estás dentro del venv

```bash
which python          # macOS/Linux — debe contener ".venv"
where python          # Windows
echo $VIRTUAL_ENV     # ruta del entorno si está activo
python -c "import sys; print(sys.executable)"
```

En muchos terminals el prompt muestra `(.venv)`.

### 2.5 Desactivar y borrar

```bash
deactivate                 # salir del entorno (no borra nada)
rm -rf .venv               # borrar entorno; luego se recrea
```

### 2.6 `requirements.txt`: dos estilos

**A) Orientado a curso (el del repo):** rangos mínimos legibles.

```text
pandas>=2.2
pytest>=8.0
```

**B) Congelado para reproducir un bug:**

```bash
pip freeze > requirements-lock.txt
```

En DSIA usamos sobre todo el estilo A en el repo del curso; en tu Proyecto III puedes pinnear más si despliegas.

### 2.7 Comprobación automática

```bash
python sesiones/2026-09-08/ejemplos/check_entorno.py
```

Debe imprimir `ENTORNO OK`. Opciones:

```bash
python sesiones/2026-09-08/ejemplos/check_entorno.py --strict   # exige estar en .venv
```

### 2.8 Problemas frecuentes (venv)

| Síntoma | Causa probable | Qué hacer |
| --- | --- | --- |
| `pip install` funciona pero `import` falla en el IDE | IDE no usa el intérprete del `.venv` | Selecciona `.venv/bin/python` en Cursor/VS Code |
| `python3: command not found` | Python no instalado / PATH | Instala Python 3.12+ y reabre la terminal |
| Paquetes se instalan “fuera” | No activaste el venv | `source .venv/bin/activate` y repite |
| Conflicto de versiones | Mezcla conda + pip global | Usa solo venv para DSIA |
| Permisos raros en Windows | ExecutionPolicy / antivirus | Política RemoteSigned; ejecuta terminal como usuario normal |

### 2.9 venv vs Anaconda (nota rápida)

| | `venv` + pip | Anaconda/conda |
| --- | --- | --- |
| Enfoque DSIA | **Preferido** | Alternativa personal |
| Ligereza | Alta | Más pesado |
| Repro en PaaS | Natural con `requirements.txt` | Posible, menos directo |

Puedes usar conda en casa, pero los materiales y demos del curso asumen **venv**.

---

## 3. Git y GitHub

### 3.1 Modelo mental

```text
 working tree          staging             commits locales           GitHub
(archivos editados) → git add → git commit → historial en .git → git push
                                              ↑
                                         branch / merge / PR
```

| Término | Definición operativa |
| --- | --- |
| Repositorio | Carpeta con historial (`.git/`) |
| Commit | Instantánea + mensaje |
| Branch | Línea de desarrollo |
| `main` | Rama de integración estable |
| Remote (`origin`) | Copia en GitHub |
| Pull Request (PR) | Pedir integrar una rama en otra con revisión |
| Clone | Copiar un repo remoto a local |
| Fork | Copia bajo tu usuario (menos habitual en DSIA individual) |

### 3.2 Configuración inicial (una vez por máquina)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.es"
git config --global init.defaultBranch main
```

Autenticación con GitHub: **HTTPS + credential helper** o **SSH keys**.  
Si usas SSH:

```bash
ssh -T git@github.com
```

### 3.3 Crear repo personal del curso

1. En GitHub: *New repository* → nombre `dsia-26-27-apellido-nombre`.
2. No subas `.venv`. Añade README inicial (o créalo en local).
3. Clona:

```bash
git clone git@github.com:TU_USUARIO/dsia-26-27-apellido-nombre.git
cd dsia-26-27-apellido-nombre
```

### 3.4 Flujo diario recomendado

```bash
git status
git checkout -b practica/sesion-01        # o: git switch -c practica/sesion-01
# ... editar ficheros ...
git status
git diff                                  # revisa cambios
git add README.md sesion01.md             # añade con intención (evita git add . ciego)
git commit -m "Add session 01 notes and environment checklist"
git push -u origin practica/sesion-01
```

Luego en GitHub: **Compare & pull request** → base `main` ← compare `practica/sesion-01`.

### 3.5 Mensajes de commit

| Bien | Mal |
| --- | --- |
| `Add session 01 notes` | `update` |
| `Fix README install steps` | `cambios` |
| `Ignore venv and env files` | `asdf` |

Estilo: **imperativo**, corto, un cambio lógico por commit cuando sea posible.

### 3.6 `.gitignore` mínimo para DSIA

Crea/verifica un `.gitignore` en tu repo personal:

```gitignore
# Entornos
.venv/
venv/
env/
Envs/

# Secretos
.env
.env.*
!.env.example

# Python
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.ipynb_checkpoints/
*.egg-info/

# OS / IDE
.DS_Store
.idea/
.vscode/
```

Plantilla lista: [`sesiones/2026-09-08/ejemplos/gitignore_dsia.txt`](../sesiones/2026-09-08/ejemplos/gitignore_dsia.txt)

### 3.7 Qué NUNCA sube a GitHub

1. `.venv/` (se recrea con pip)  
2. `.env` y API keys  
3. Datos personales / datasets confidenciales sin permiso  
4. Credenciales, tokens, capturas con secretos  

Si subes un secreto por error: **rota la clave** (no basta con borrar el fichero en un commit nuevo; sigue en el historial).

### 3.8 Comandos de lectura del historial

```bash
git log --oneline -5
git show HEAD
git branch -vv
git remote -v
```

Deshacer *antes* de commit (cuidado):

```bash
git restore fichero.py            # descarta cambios locales del fichero
git restore --staged fichero.py   # saca del staging
```

### 3.9 Problemas frecuentes (Git)

| Síntoma | Qué hacer |
| --- | --- |
| `rejected (fetch first)` | `git pull --rebase origin main` (con cuidado) y resuelve conflictos |
| PR sin cambios | Empujaste a `main` directo; crea rama y commit ahí |
| `Permission denied (publickey)` | Configura SSH o usa HTTPS |
| Aparece `.venv` en el PR | Añádelo a `.gitignore`, quítalo del índice: `git rm -r --cached .venv` |
| Email “privado” de GitHub | Usa el noreply de GitHub en `user.email` |

---

## 4. Ejemplo guiado completo (15 min en casa o en clase)

```bash
# 0) curso
cd dsia-26-27
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python sesiones/2026-09-08/ejemplos/check_entorno.py --strict

# 1) repo personal (ya clonado)
cd ~/repos/dsia-26-27-apellido-nombre
cp /ruta/al/curso/sesiones/2026-09-08/ejemplos/gitignore_dsia.txt .gitignore
printf '# DSIA — Apellido, Nombre\n\nMáster ...\n' > README.md
git checkout -b practica/sesion-01
printf '## Sesión 1\n\n- venv\n- git\n- no subir .env\n' > sesion01.md
git add .gitignore README.md sesion01.md
git commit -m "Add course scaffold for session 01"
git push -u origin practica/sesion-01
# 2) abrir PR en la web
```

---

## 5. Relación con la evaluación

| Entregable | Cómo entra Git/entorno |
| --- | --- |
| Proyecto I–III | Repo GitHub con historial legible |
| Rúbricas | “Uso responsable de Git”, reproducibilidad |
| Uso de IA | `AI_USAGE.md` versionado (sin secretos) |

---

## 6. Checklist de salida de la sesión

- [ ] `python` apunta a `.venv`
- [ ] `pandas` y `pytest` importan
- [ ] Repo personal creado y clonado
- [ ] `.gitignore` correcto
- [ ] Al menos un commit en rama + PR (o merge) visible
- [ ] Sé explicar qué no se sube a GitHub

## 7. Para el 15 sep

1. Mantén el venv listo.  
2. Abre `1_programacion_avanzada_python/Datos/ventas.csv`.  
3. Ojea `proyectos/proyecto_i/` y `sesiones/2026-09-15/teoria.md`.
