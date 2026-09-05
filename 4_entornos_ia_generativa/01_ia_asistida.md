# Sesiones 10–11 (10 y 17 nov 2026): IA generativa en el desarrollo

## Principios

1. **Tú eres responsable** del código que entregas, aunque lo haya sugerido una IA.
2. Usa IA para acelerar, no para sustituir el entendimiento.
3. **Cita** la herramienta cuando haya generado partes relevantes del trabajo.
4. No pegues secretos, datos personales ni código propietario sensible en prompts en la nube sin permiso.

## Flujo recomendado

```text
Contexto → Prompt → Borrador IA → Revisión humana → Tests → Commit
```

## Herramientas (orientativas)

| Herramienta | Uso típico en clase |
| --- | --- |
| Cursor | Edición asistida sobre el repo |
| Claude Code | Agente CLI sobre el proyecto |
| Gemini CLI | Prototipado y exploración |

## Checklist antes de aceptar código generado

- [ ] Compila / importa sin errores
- [ ] Hay tests (o se han actualizado)
- [ ] No introduce dependencias innecesarias
- [ ] Estilo coherente con el resto del repo
- [ ] Se ha documentado el uso de IA si aplica
