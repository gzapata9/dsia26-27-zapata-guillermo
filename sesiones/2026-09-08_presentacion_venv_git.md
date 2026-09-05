**Materiales de aula:** [`2026-09-08/teoria.md`](2026-09-08/teoria.md) · [`2026-09-08/ejercicios.md`](2026-09-08/ejercicios.md) · [`2026-09-08/ejemplos/`](2026-09-08/ejemplos/)

# 8 sep 2026 — Presentación + entornos virtuales + Git/GitHub

**Duración total:** 1 h 45 min  
**Material:** `1_programacion_avanzada_python/01_entornos_y_git.md` · `ejercicios/E0_entornos_git.md` · `README.md` del curso

| Bloque | Min | Qué hacer |
| --- | --- | --- |
| Presentación de la asignatura | 0–20 | Objetivos, temario, evaluación, política de IA |
| Exposición + demo técnica | 20–50 | `venv` + Git/GitHub (live) |
| Ejercicios | 50–80 | E0 con checkpoints |
| Cierre y prep. próxima sesión | 80–105 | Cuentas, repos, dudas, dataset ventas |

> Ajuste fino: si la presentación institucional se alarga, recorta 5′ del cierre; **no** recortes el bloque de ejercicios por debajo de 25′.

---

## Objetivos de aprendizaje

Al terminar la sesión, el alumnado debe ser capaz de:

1. Explicar qué evalúa DSIA (Proyectos I–III + examen) y la política de uso de IA.
2. Crear y activar un entorno virtual con `venv` e instalar `requirements.txt`.
3. Usar el flujo básico Git: `status` → `branch` → `add` → `commit` → `push`.
4. Tener un **repositorio personal** en GitHub listo para el curso.

---

## Bloque 0 — Presentación de la asignatura (20 min)

### P1. Para qué sirve DSIA (5 min)

- De scripts sueltos a **soluciones** de datos e IA desplegables.
- Hilo del semestre: Python robusto → tests → automatización → APIs de IA → E2E.
- Formato de clase: **30′ teoría + 30′ práctica** + trabajo de proyecto.

### P2. Mapa del repositorio del curso (5 min)

Mostrar estructura en pantalla:

| Carpeta | Rol |
| --- | --- |
| `1_…` … `5_…` | Temas |
| `sesiones/` | Guías docentes minutadas |
| `proyectos/` | Enunciados I / II / III |
| `requirements.txt` | Dependencias base |

Clonar (o indicar URL cuando el remoto exista):

```bash
git clone git@github.com:dmartincc/dsia-26-27.git
cd dsia-26-27
```

### P3. Evaluación y calendario (5 min)

| Elemento | Peso |
| --- | --- |
| Proyecto I | 10 % |
| Proyecto II | 20 % |
| Proyecto III | 40 % |
| Examen final | 30 % |

Fechas clave a citar: 15 sep (arranca Proyecto I), 20 oct (Trabajo Final), 17 nov (RC), 1/8 dic (exposiciones).

### P4. Política de uso de IA (5 min)

- Permitido según actividad; **obligatorio citar** herramienta cuando aporte partes relevantes.
- Uso no autorizado o sin referencia = plagio (Reglamento General).
- A partir de hoy: crear `AI_USAGE.md` en el repo personal cuando usen asistentes.

---

## Bloque A — Exposición técnica (30 min)

### A1. ¿Por qué entornos virtuales? (5 min)

- Una app ≠ los paquetes globales del sistema.
- Reproducibilidad: `requirements.txt` + Python acotado.
- Conflicto clásico: “en mi máquina funciona”.

Comparar mentalmente: Anaconda vs `venv` (en DSIA priorizamos `venv` + pip).

### A2. Demo `venv` (10 min) — live

```bash
cd dsia-26-27
python3 --version
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
which python                       # debe apuntar a .venv
python -c "import pandas, pytest; print('ok')"
deactivate
source .venv/bin/activate
```

Señalar: `.venv/` está en `.gitignore` — **no** se sube al remoto.

**Pregunta al aula:** ¿qué pasa si instaláis paquetes sin activar el entorno?

### A3. Git: modelo mental (7 min)

```text
working tree → staging (add) → commit → remoto (push)
                 ↑
              branch / PR
```

Conceptos a fijar:

- `main` protegida mentalmente (trabajar en ramas).
- Commits pequeños, mensaje en imperativo (`Add`, `Fix`, `Update`).
- Nunca secretos (`.env`, claves) en el historial.

### A4. Demo Git/GitHub (8 min) — live

```bash
git status
git checkout -b practica/sesion-01
echo "# Notas DSIA" > NOTAS.md
git add NOTAS.md
git commit -m "Add session notes scaffold"
# git push -u origin practica/sesion-01   # en el repo del alumno
```

Mostrar en GitHub (pantalla): crear repo vacío, abrir PR, revisar diff.

Anti-patrones: `git add .` ciego; commits `update`; subir `.venv` o `.env`.

---

## Bloque B — Ejercicios (30 min)

Enunciado: `1_programacion_avanzada_python/ejercicios/E0_entornos_git.md`.

| Min | Checkpoint |
| --- | --- |
| 0–8 | Crear/activar `.venv`, instalar requirements, `import pandas, pytest` OK |
| 8–16 | Crear repo GitHub `dsia-26-27-apellido-nombre` + README personal |
| 16–24 | Rama `practica/sesion-01`, fichero `sesion01.md` (resumen 5–8 líneas), commit + push |
| 24–30 | Abrir Pull Request hacia `main` (o merge si trabajáis sin PR) |

**Hecho:** el profesor/compañero puede abrir la URL del repo y ver el README + PR/commit de hoy.

---

## Bloque C — Cierre (~25 min)

1. Resolver incidencias típicas (PATH de Python en Windows, SSH vs HTTPS, 2FA).
2. Recordar para el **15 sep**: traer entorno OK y echar un vistazo a `Datos/ventas.csv`.
3. Opcional: fork/clone del repo del curso si aún no lo tienen.

**Salida esperada hoy:** cuenta GitHub operativa, repo personal creado, venv funcionando.
