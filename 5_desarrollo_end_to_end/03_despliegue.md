# Sesión 9 (3 nov 2026): Despliegue y puesta en producción

## Estrategias vistas en clase

1. **Empaquetado**: `requirements.txt` pinado + runtime Python definido.
2. **Proceso**: Gunicorn / uvicorn detrás de un PaaS (Render, Fly.io, Cloud Run…).
3. **Configuración**: variables de entorno (nunca secretos en el repo).
4. **Salud**: `/health` + logs centralizados del proveedor.
5. **Rollback**: tags Git y posibilidad de redesplegar versión anterior.

## Checklist pre-producción

- [ ] `.env.example` documentado
- [ ] Tests CI en verde
- [ ] Dependencias mínimas
- [ ] README con URL de demo (si aplica)
- [ ] Política de uso de IA citada

## Nota

El proveedor concreto puede variar; lo evaluable es la **preparación reproducible** y la evidencia de despliegue (URL o captura + logs).
