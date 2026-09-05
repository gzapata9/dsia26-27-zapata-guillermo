# Teoría (30 min) — 8 sep 2026  
## Presentación breve + entornos virtuales + Git/GitHub

**Referencia ampliada:** [`../../1_programacion_avanzada_python/01_entornos_y_git.md`](../../1_programacion_avanzada_python/01_entornos_y_git.md)  
**Ejemplos:** [`ejemplos/`](ejemplos/) · **Ejercicios:** [`ejercicios.md`](ejercicios.md)

**Objetivo:** salir sabiendo crear un entorno reproducible y versionar código con un flujo Git profesional básico.

---

## 1. Introducción (5 min)

### 1.1 El problema que resolvemos hoy

| Situación típica | Consecuencia |
| --- | --- |
| “Instalé pandas en el Python del sistema” | Rompes otros proyectos |
| “Te paso el zip del código” | Sin historial, sin revisión, sin CI |
| “La API key está en el notebook” | Fuga de secretos en GitHub |

En DSIA entregamos **soluciones reproducibles**:

1. mismo intérprete / dependencias → mismo comportamiento;
2. historial en Git → revisar, revertir, colaborar;
3. secretos fuera del código → `.env` local, nunca en el remoto.

### 1.2 Mapa de la sesión de teoría

```text
5'  intro + por qué
10' venv (conceptos + demo)
12' Git/GitHub (modelo + demo)
3'  checklist y puente a ejercicios
```

---

## 2. Conceptos — entornos virtuales (10 min)

### 2.1 Definiciones

| Concepto | Significado |
| --- | --- |
| Intérprete global | Python del SO / instalación general |
| Entorno virtual (`.venv`) | Aislamiento: Python + `site-packages` del proyecto |
| Activar | `python` y `pip` apuntan al `.venv` |
| `requirements.txt` | Receta para recrear dependencias |
| `sys.executable` | Ruta real del intérprete en uso |

### 2.2 ¿Qué hay dentro de un `.venv`?

```text
.venv/
  bin/  (Scripts/ en Windows)  → python, pip, activate
  lib/python3.x/site-packages/ → pandas, pytest, …
  pyvenv.cfg                   → metadatos del entorno
```

**Importante:** `.venv/` se **regenera**; no se versiona.

### 2.3 Ciclo de vida

```text
crear → activar → instalar → trabajar → deactivate
              ↘ (si se rompe) borrar .venv y recrear
```

### 2.4 Demo en vivo (comandos)

```bash
cd dsia-26-27
python3 --version
python3 -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
which python                           # debe contener .venv
python -c "import sys; print(sys.executable)"
python -c "import pandas, pytest; print(pandas.__version__, pytest.__version__)"
python sesiones/2026-09-08/ejemplos/check_entorno.py --strict
```

**Preguntas al aula**

1. Si no activáis el venv, ¿dónde se instalan los paquetes?
2. ¿Por qué el IDE puede “no ver” pandas aunque en la terminal sí?

### 2.5 Anti-patrones

- Instalar con `sudo pip` en el sistema.
- Subir `.venv` a GitHub “para que sea más fácil”.
- Mezclar conda base + pip global + venv sin criterio.
- Tener tres Pythons y no saber cuál usa el IDE.

---

## 3. Conceptos — Git y GitHub (12 min)

### 3.1 Tres zonas + remoto

```text
 working tree     staging area      commits (.git)       remoto (origin)
  (editas)   →   (git add)   →   (git commit)   →   (git push / PR)
```

### 3.2 Glosario operativo

| Término | Idea en una frase |
| --- | --- |
| `commit` | Foto del proyecto con mensaje |
| `branch` | Línea de trabajo paralela |
| `main` | Rama estable de integración |
| `origin` | Nombre habitual del remoto GitHub |
| `PR` | Pedir merge con revisión y conversación |
| `.gitignore` | Qué Git debe fingir que no existe |
| `clone` | Copiar repo remoto → disco local |

### 3.3 Flujo que usaremos todo el semestre

```text
main ──► branch practica/… ──► commits ──► push ──► Pull Request ──► main
```

### 3.4 Demo en vivo

```bash
git status
git switch -c practica/sesion-01     # equivalente moderno a checkout -b
printf '# Notas DSIA\n\n- venv\n- git\n' > NOTAS.md
git add NOTAS.md
git status
git diff --cached
git commit -m "Add session notes scaffold"
git log --oneline -3
# git push -u origin practica/sesion-01
```

En GitHub (pantalla): crear repo → abrir PR → mirar el diff → merge.

### 3.5 Commits: calidad mínima

| Bien | Mal |
| --- | --- |
| `Add README with install steps` | `update` |
| `Ignore venv and env files` | `wip` |
| `Fix broken activate instructions` | `asdf` |

Regla: **un propósito claro por commit** cuando sea razonable.

### 3.6 Secretos y `.gitignore`

Nunca versionar:

- `.venv/`
- `.env` / API keys
- `__pycache__/`, `.pytest_cache/`

Plantilla: `ejemplos/gitignore_dsia.txt`.

Si un secreto se sube: **rotar la clave de inmediato**.

### 3.7 Diagrama SSH vs HTTPS (1 min)

```text
HTTPS: https://github.com/user/repo.git   (+ login / token)
SSH:   git@github.com:user/repo.git       (+ clave SSH)
```

Ambos valen; lo importante es que `git push` funcione de forma sostenible.

---

## 4. Código de apoyo en `ejemplos/`

| Fichero | Para qué |
| --- | --- |
| `check_entorno.py` | Verifica Python, venv, imports, `requirements.txt` |
| `gitignore_dsia.txt` | Plantilla de ignore para repos del alumnado |
| `demo_flujo.sh` | Script guiado (macOS/Linux) del flujo venv+git local |

```bash
python sesiones/2026-09-08/ejemplos/check_entorno.py --strict
bash sesiones/2026-09-08/ejemplos/demo_flujo.sh --help
```

---

## 5. Resumen (3 min) — checklist

- [ ] Explico para qué sirve un venv  
- [ ] Activo `.venv` e instalo desde `requirements.txt`  
- [ ] Distingo working tree / staging / commit / remoto  
- [ ] Creo rama, commit con buen mensaje y (idealmente) PR  
- [ ] Sé qué no debe entrar en Git  

→ Continúa en [`ejercicios.md`](ejercicios.md) (30 min) para **repasar esta teoría**.
