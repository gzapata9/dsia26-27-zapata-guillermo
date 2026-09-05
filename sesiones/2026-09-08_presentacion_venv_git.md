**Materiales de aula:** [`2026-09-08/teoria.md`](2026-09-08/teoria.md) · [`2026-09-08/ejercicios.md`](2026-09-08/ejercicios.md) · [`2026-09-08/ejemplos/`](2026-09-08/ejemplos/)  
**Referencia ampliada:** [`../1_programacion_avanzada_python/01_entornos_y_git.md`](../1_programacion_avanzada_python/01_entornos_y_git.md)

# 8 sep 2026 — Presentación + entornos virtuales + Git/GitHub

**Duración total:** 1 h 45 min  
**Material:** `1_programacion_avanzada_python/01_entornos_y_git.md` · `sesiones/2026-09-08/` · `ejercicios/E0_entornos_git.md`

| Bloque | Min | Qué hacer |
| --- | --- | --- |
| Presentación de la asignatura | 0–20 | Objetivos, temario, evaluación, política de IA |
| Exposición + demo técnica | 20–50 | Seguir `2026-09-08/teoria.md` (`venv` + Git/GitHub) |
| Ejercicios | 50–80 | `2026-09-08/ejercicios.md` (repaso teórico) |
| Cierre y prep. próxima sesión | 80–105 | Incidencias, repos, dataset ventas |

> Ajuste fino: si la presentación institucional se alarga, recorta 5′ del cierre; **no** recortes el bloque de ejercicios por debajo de 25′.

---

## Objetivos de aprendizaje

Al terminar la sesión, el alumnado debe ser capaz de:

1. Explicar qué evalúa DSIA (Proyectos I–III + examen) y la política de uso de IA.
2. Crear, activar y verificar un entorno virtual (`check_entorno.py --strict`).
3. Explicar working tree / staging / commit / remoto y usar ramas + PR.
4. Tener un **repositorio personal** con `.gitignore` correcto y README instalable.

---

## Bloque 0 — Presentación de la asignatura (20 min)

### P1. Para qué sirve DSIA (5 min)

- De scripts sueltos a **soluciones** de datos e IA desplegables.
- Hilo del semestre: Python robusto → tests → automatización → APIs de IA → E2E.
- Formato de clase: **30′ teoría + 30′ práctica** + trabajo de proyecto.

### P2. Mapa del repositorio del curso (5 min)

| Carpeta | Rol |
| --- | --- |
| `1_…` … `5_…` | Temas |
| `sesiones/YYYY-MM-DD/` | Teoría + ejercicios + ejemplos de cada clase |
| `proyectos/` | Enunciados I / II / III |
| `requirements.txt` | Dependencias base |

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

Fechas clave: 15 sep (Proyecto I), 20 oct (Trabajo Final), 17 nov (RC), 1/8 dic (exposiciones).

### P4. Política de uso de IA (5 min)

- Citar herramienta cuando aporte partes relevantes (`AI_USAGE.md`).
- Uso no autorizado o sin referencia = plagio.

---

## Bloque A — Exposición técnica (30 min)

Seguir íntegramente [`2026-09-08/teoria.md`](2026-09-08/teoria.md):

| Min | Contenido |
| --- | --- |
| 0–5 | Intro + reproducibilidad |
| 5–15 | venv: conceptos, demo, `check_entorno.py --strict` |
| 15–27 | Git: tres zonas, rama, commit, PR, `.gitignore` |
| 27–30 | Checklist y puente a ejercicios |

Demo rápida opcional:

```bash
bash sesiones/2026-09-08/ejemplos/demo_flujo.sh
```

---

## Bloque B — Ejercicios (30 min)

Enunciado principal: [`2026-09-08/ejercicios.md`](2026-09-08/ejercicios.md)

| Min | Checkpoint |
| --- | --- |
| 0–6 | Conceptos en `sesion01.md` |
| 6–14 | venv + `check_entorno.py --strict` |
| 14–22 | Repo personal + `.gitignore` + README |
| 22–30 | PR con formulario de repaso + peer-check |

---

## Bloque C — Cierre (~25 min)

1. Incidencias: PATH Windows, SSH vs HTTPS, IDE sin intérprete `.venv`.
2. Para el **15 sep**: venv OK + ojeada a `Datos/ventas.csv`.
3. Recordar: no subir `.venv` ni `.env`.

**Salida esperada hoy:** GitHub operativo, repo personal con PR, venv verificado en estricto.

