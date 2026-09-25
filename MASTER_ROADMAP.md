# ChxChx Security — Master Roadmap & Release Plan

**Proyecto:** ChxChx Security  
**Documento:** Roadmap maestro de versiones, fases y actualizaciones  
**Versión del documento:** 1.0  
**Base actual:** ChxChx Security `v0.1.0`  
**Plataforma primaria:** Fedora Linux  
**Lenguaje principal:** Python  
**Componentes nativos:** Solo cuando exista una justificación técnica real  
**Objetivo:** construir una herramienta auditable de privacidad defensiva, aislamiento de sesiones y reducción de fugas de red.

---

# 1. Principios del proyecto

ChxChx Security NO debe intentar crear su propio protocolo de anonimato, su propia criptografía ni reemplazar componentes maduros como Tor, NetworkManager, nftables, systemd o SELinux.

La aplicación funciona como **control plane**:

```text
┌───────────────────────────────┐
│        ChxChx Security        │
│          Python CLI           │
└───────────────┬───────────────┘
                │
        Orquesta y valida
                │
    ┌───────────┼───────────────┐
    │           │               │
    ▼           ▼               ▼
   Tor     NetworkManager    systemd
    │           │               │
    └─────┬─────┴───────────────┘
          │
          ▼
      nftables
          │
          ▼
 Linux Network Namespace
```

La aplicación no debe prometer "anonimato absoluto".

Debe ofrecer garantías específicas y comprobables, por ejemplo:

- la aplicación protegida está usando Tor;
- el proceso no tiene salida directa a Internet;
- DNS está siendo resuelto por la ruta protegida;
- una caída de Tor no provoca fallback a la conexión normal;
- la sesión protegida se elimina al finalizar;
- el proyecto no recopila identificadores de la máquina innecesariamente.

---

# 2. Reglas permanentes

## RULE-001 — Fail closed

Si una protección requerida no está disponible:

```text
NO ejecutar.
```

Nunca:

```text
Tor falla
   ↓
usar Internet normal
```

Debe ocurrir:

```text
Tor falla
   ↓
bloquear ejecución
```

---

## RULE-002 — No criptografía casera

No implementar:

- protocolos propios de anonimato;
- cifrados propios;
- VPN propia;
- reemplazo de TLS;
- proxies criptográficos personalizados.

Usar implementaciones auditadas.

---

## RULE-003 — Privilegios mínimos

La CLI normal debe ejecutarse sin root.

Las operaciones privilegiadas deben ser:

- pequeñas;
- explícitas;
- auditables;
- separadas del proceso principal.

---

## RULE-004 — Python es el control plane

Python manejará:

- configuración;
- CLI;
- validaciones;
- orquestación;
- estado;
- diagnóstico;
- pruebas.

Un componente Rust/C/C++ solo debe existir si una fase posterior demuestra que Python no es adecuado para una operación específica.

---

## RULE-005 — Configuración ≠ secretos

El repositorio público no contiene plantillas de configuración de entorno. La configuración local
puede vivir en un archivo `.env` ignorado por Git o en variables de entorno del proceso.

El repositorio jamás debe contener:

```text
.env
tokens
passwords
keys privadas
cookies
credenciales
```

---

## RULE-006 — Redacción automática

La salida del programa debe poder ocultar:

- IP pública;
- MAC;
- hostname;
- username;
- rutas personales;
- identificadores persistentes.

Modo detallado solo cuando el usuario lo solicite.

---

## RULE-007 — No anti-forensics

La aplicación puede minimizar los datos que ella misma genera.

No debe intentar:

- borrar registros de seguridad del sistema;
- destruir evidencia;
- manipular logs de terceros;
- borrar historiales ajenos;
- evadir auditorías del sistema.

La estrategia correcta es:

```text
generar menos datos
```

no:

```text
generarlos y luego intentar destruirlos
```

---

# 3. Versionado

Se utilizará Semantic Versioning.

```text
MAJOR.MINOR.PATCH
```

Ejemplo:

```text
0.2.4
```

Significa:

```text
0 = todavía no estable
2 = segunda generación funcional
4 = cuarta corrección de esa generación
```

Antes de `1.0.0`, las APIs internas pueden cambiar.

---

# 4. FASE 0 — v0.1.0

## Nombre

Foundation / Process Privacy

## Estado

✅ Implementada

## Objetivo

Crear una primera versión funcional que pueda:

- comprobar dependencias;
- iniciar/verificar Tor;
- ejecutar aplicaciones mediante Tor;
- evitar fallback silencioso;
- proporcionar una shell protegida;
- gestionar políticas de MAC de NetworkManager.

## Componentes

```text
chxsec
 ├── doctor
 ├── tor
 │   ├── status
 │   ├── start
 │   └── verify
 ├── run
 ├── shell
 └── mac
```

## Seguridad incluida

- `torsocks`;
- aislamiento de streams;
- comprobación de conectividad SOCKS;
- verificación de salida Tor;
- shell efímera;
- historial deshabilitado en la shell protegida;
- `umask 077`;
- directorio temporal de sesión;
- redacción de IP;
- no recolección innecesaria de identidad del host.

## Limitación principal

La protección ocurre principalmente a nivel de **proceso**.

Una aplicación que no sea compatible con `torsocks` puede no ser adecuada para esta fase.

---

# 5. FASE 0.1 — v0.1.x

## Objetivo

Estabilización antes de aumentar privilegios o complejidad.

## v0.1.1

### Mejoras

- clasificación de errores;
- mensajes consistentes;
- códigos de salida documentados;
- timeouts configurables;
- mejor detección de servicio Tor;
- comprobación automática de versión.

### Tests

Agregar:

```text
test_doctor.py
test_config.py
test_process.py
test_cli.py
```

---

## v0.1.2

### Structured output

Añadir:

```bash
chxsec doctor --json
chxsec tor verify --json
```

Ejemplo:

```json
{
  "tor": true,
  "socks": true,
  "route_verified": true
}
```

No incluir identificadores del equipo.

---

## v0.1.3

### Configuration profiles

Introducir:

```text
profiles/
├── default.toml
├── strict.toml
└── development.toml
```

Ejemplo conceptual:

```toml
[network]
require_tor = true
fail_closed = true

[privacy]
redact_ip = true
redact_paths = true
```

---

## Criterio para cerrar 0.1.x

- unit tests estables;
- CLI consistente;
- errores reproducibles;
- configuración validada;
- ninguna operación peligrosa como root.

---

# 6. FASE 1 — v0.2.0

## Nombre

Isolated Session

## Objetivo

Dejar de depender únicamente de `torsocks`.

Crear una **sesión de red aislada**.

Arquitectura:

```text
Fedora Host
│
├── Red normal
│
└── Network Namespace
      │
      ├── aplicación
      │
      ├── DNS protegido
      │
      └── salida Tor
```

---

# 7. Network Namespace

Cada sesión protegida debe crear algo conceptualmente similar a:

```text
chxsec-<session>
```

La aplicación ejecutada dentro no debe poder usar directamente la interfaz principal del host.

Ejemplo conceptual:

```bash
chxsec session create
chxsec session exec firefox
chxsec session destroy
```

---

# 8. v0.2.1 — Namespace lifecycle

Implementar:

```text
create
inspect
exec
stop
destroy
```

Estado:

```text
CREATED
STARTING
ACTIVE
STOPPING
DESTROYED
FAILED
```

---

# 9. v0.2.2 — nftables scoped firewall

Agregar reglas únicamente para el namespace protegido.

Objetivo:

```text
APP
 │
 ├── Tor → permitido
 │
 └── Internet directo → bloqueado
```

El firewall del host no debe ser reemplazado por ChxChx Security.

---

# 10. v0.2.3 — Kill switch

Si Tor desaparece:

```text
APP
 ↓
NO INTERNET
```

Nunca:

```text
APP
 ↓
Internet normal
```

Este comportamiento debe probarse automáticamente.

---

# 11. v0.2.4 — DNS protection

Toda resolución de nombres de una sesión protegida debe utilizar el mecanismo configurado para la ruta protegida.

Test obligatorio:

```text
dns_leak_test
```

---

# 12. v0.2.5 — IPv6 strategy

Antes de habilitar IPv6 dentro de sesiones protegidas:

1. demostrar que la ruta está correctamente controlada;
2. comprobar DNS;
3. comprobar rutas;
4. comprobar caída de Tor.

Mientras no exista esa garantía, el perfil `strict` podrá deshabilitar IPv6 dentro de la sesión aislada.

---

# 13. Tests obligatorios de la fase 0.2

```text
tests/integration/
├── test_namespace.py
├── test_tor_crash.py
├── test_dns_leak.py
├── test_ipv4_leak.py
├── test_ipv6_leak.py
├── test_direct_connection.py
└── test_cleanup.py
```

---

# 14. FASE 2 — v0.3.0

## Nombre

Hardening

## Objetivo

Convertir el prototipo en una herramienta mantenible y verificable.

---

# 15. v0.3.1 — SELinux

Crear una política específica o reglas compatibles con SELinux.

Objetivo:

```text
CLI
 ↓
solo recursos necesarios
```

Evitar permisos globales.

---

# 16. v0.3.2 — Dependency hardening

Agregar:

- lockfiles;
- hashes;
- versiones fijadas;
- escaneo de dependencias;
- actualización controlada.

Pipeline:

```text
Dependency
    │
    ▼
Version pin
    │
    ▼
Vulnerability scan
    │
    ▼
Tests
```

---

# 17. v0.3.3 — SBOM

Generar Software Bill of Materials.

Salida:

```text
dist/
└── chxchx-security.spdx.json
```

Debe permitir conocer todas las dependencias incluidas en cada release.

---

# 18. v0.3.4 — Signed releases

Los releases deben incluir:

```text
chxchx-security-X.Y.Z.tar.gz
SHA256SUMS
SHA256SUMS.sig
SBOM
```

---

# 19. v0.3.5 — Reproducible builds

Meta:

Dos máquinas limpias construyendo el mismo commit deberían producir artefactos equivalentes o verificablemente reproducibles.

---

# 20. FASE 3 — v0.4.0

## Nombre

Session Profiles

## Objetivo

Convertir ChxChx Security en un gestor de perfiles de privacidad.

Ejemplo:

```bash
chxsec profile list
```

Salida:

```text
default
strict
browser
developer
```

---

# 21. Perfil default

Prioriza compatibilidad.

```text
Tor
DNS protection
fail closed
MAC privacy
```

---

# 22. Perfil strict

Prioriza aislamiento.

```text
namespace dedicado
firewall restrictivo
Tor obligatorio
DNS protegido
sin fallback
filesystem temporal opcional
```

---

# 23. Perfil developer

Permite:

- herramientas CLI;
- Git;
- pip;
- npm;
- documentación explícita de qué conexiones salen por la sesión.

No debe intentar ocultar la identidad de cuentas autenticadas.

---

# 24. FASE 4 — v0.5.0

## Nombre

Application Sandbox

## Objetivo

Limitar qué puede ver una aplicación protegida.

Arquitectura conceptual:

```text
App
 │
 ├── red aislada
 ├── HOME temporal
 ├── /tmp privado
 └── filesystem limitado
```

Tecnologías a evaluar:

- bubblewrap;
- namespaces;
- systemd sandboxing;
- SELinux.

No reinventar contenedores.

---

# 25. v0.5.1 — Ephemeral HOME

Comando futuro:

```bash
chxsec run --ephemeral-home firefox
```

Crear:

```text
/tmp/chxsec-session-*/
```

Al finalizar la sesión:

```text
directorio eliminado
```

Esto elimina datos temporales creados por ChxChx Security, sin manipular historiales o registros externos.

---

# 26. v0.5.2 — Read-only mounts

Permitir políticas como:

```text
Documents → read-only
Downloads → isolated
SSH → inaccessible
GPG → inaccessible
```

---

# 27. FASE 5 — v0.6.0

## Nombre

Privacy Diagnostics

## Objetivo

Crear un diagnóstico completo de una sesión.

Comando:

```bash
chxsec audit
```

Debe probar:

```text
Tor
DNS
IPv4
IPv6
direct socket
namespace
firewall
MAC policy
temporary directories
```

Resultado:

```text
Network Isolation       PASS
Tor Route               PASS
DNS Route               PASS
IPv4 Direct Access      BLOCKED
IPv6 Direct Access      BLOCKED
Cleanup                 PASS
```

---

# 28. Auditoría por sesión

Cada sesión debe tener un ID aleatorio no derivado del host.

Ejemplo:

```text
session: 7ad84d
```

No utilizar:

- username;
- hostname;
- machine-id;
- serial;
- MAC.

---

# 29. FASE 6 — v0.7.0

## Nombre

Observability Without Identity

## Objetivo

Poder depurar el sistema sin convertirlo en una herramienta de tracking.

Eventos permitidos:

```text
session_created
tor_ready
namespace_ready
application_started
application_finished
session_destroyed
```

Eventos no necesarios:

```text
user_name
machine_serial
permanent_mac
public_ip
```

---

# 30. Logging

Por defecto:

```text
minimal
```

Opciones:

```bash
--log-level none
--log-level error
--log-level debug
```

Debug debe ser activado explícitamente.

---

# 31. FASE 7 — v0.8.0

## Nombre

Packaging

## Objetivo

Instalación nativa de Fedora.

Crear RPM:

```bash
sudo dnf install chxchx-security
```

Archivos:

```text
/usr/bin/chxsec

/usr/lib/chxchx-security/

/etc/chxchx-security/
```

Configuración de usuario:

```text
~/.config/chxchx-security/
```

---

# 32. Repositorio RPM

Futuro:

```text
packages.chxchx.dev
```

o releases directos desde Git.

Nunca ejecutar instaladores remotos mediante patrones tipo:

```bash
curl ... | sudo bash
```

para releases estables.

---

# 33. FASE 8 — v0.9.0

## Nombre

Release Candidate

Esta versión no añade features grandes.

Su función es encontrar problemas.

Congelar:

```text
arquitectura
CLI
config
permisos
```

---

# 34. Security test matrix

Probar:

```text
Tor funcionando
Tor detenido
Tor cae durante sesión
DNS inaccesible
IPv4 solamente
IPv6 solamente
Wi-Fi cambia
Ethernet cambia
suspend/resume
aplicación termina inesperadamente
CLI termina inesperadamente
reboot
```

---

# 35. Disposable VM tests

Crear imágenes de prueba Fedora limpias.

Pipeline:

```text
VM
 ↓
Install Fedora
 ↓
Install ChxChx Security
 ↓
Start session
 ↓
Run leak tests
 ↓
Destroy VM
```

Cada release candidate debe pasar esta batería.

---

# 36. FASE 9 — v1.0.0

## Nombre

Stable

No se publica `1.0.0` porque el proyecto "funciona".

Se publica cuando existen garantías comprobadas.

---

# 37. Requisitos de v1.0.0

Obligatorios:

- auditoría de código;
- pruebas de fugas en VM;
- fail-closed demostrado;
- rollback probado;
- documentación de threat model;
- dependencias fijadas;
- SBOM;
- releases firmados;
- RPM;
- política SELinux revisada;
- test suite automatizada;
- documentación de recuperación.

---

# 38. Garantías que sí puede anunciar v1.0

Ejemplos:

```text
✓ La sesión aislada bloquea salida directa.
✓ Las aplicaciones soportadas utilizan la ruta protegida.
✓ DNS está controlado dentro de la sesión.
✓ Una caída de Tor bloquea el tráfico.
✓ La sesión se destruye al cerrarse.
```

---

# 39. Cosas que v1.0 NO debe prometer

Nunca anunciar:

```text
100% anonymous
untraceable
invisible
no one can identify you
zero traces
```

El anonimato también depende de:

- navegador;
- cuentas;
- cookies;
- comportamiento;
- fingerprinting;
- archivos subidos;
- información revelada por el propio usuario;
- servicios externos.

---

# 40. Posible FASE 10 — v1.1

## Application policies

Permitir reglas:

```toml
[applications.firefox]
profile = "strict"

[applications.curl]
profile = "default"
```

---

# 41. Posible FASE 11 — v1.2

## Session dashboard

TUI avanzada:

```text
╭────────────────────────────────────╮
│         ChxChx Security            │
├────────────────────────────────────┤
│ Tor             ● Connected        │
│ Namespace       ● Active           │
│ DNS             ● Protected        │
│ Direct route    ● Blocked          │
│ IPv6            ● Controlled       │
│                                    │
│ Session           7ad84d           │
╰────────────────────────────────────╯
```

Tecnologías:

```text
Textual
Rich
```

---

# 42. Posible FASE 12 — v1.3

## Plugin architecture

Crear interfaces:

```text
NetworkProvider
PrivacyProvider
SandboxProvider
AuditProvider
```

Ejemplo:

```python
class NetworkProvider:
    def start(self):
        ...

    def verify(self):
        ...

    def stop(self):
        ...
```

Esto evita acoplar toda la aplicación a un único backend.

---

# 43. Posible FASE 13 — v1.4

## Advanced automated validation

Crear:

```bash
chxsec self-test
```

Proceso:

```text
create isolated session
        ↓
test Tor
        ↓
test DNS
        ↓
test direct socket
        ↓
simulate Tor failure
        ↓
verify kill switch
        ↓
destroy session
```

---

# 44. Rama experimental — helper nativo

No implementar todavía.

Solo considerar cuando exista una necesidad demostrable.

Arquitectura:

```text
Python CLI
   │
   ▼
privileged helper
   │
   ├── namespace
   └── nftables
```

El helper debería hacer únicamente operaciones privilegiadas muy concretas.

---

# 45. ¿C++?

C++ no debe utilizarse simplemente porque "parece más seguro".

Un helper nativo aumenta riesgos:

- memory safety;
- parsing;
- permisos;
- mantenimiento;
- packaging.

Si aparece una necesidad real de componente nativo, evaluar primero:

```text
Rust
```

por sus garantías de memoria.

C/C++ solo si existe una razón técnica concreta.

---

# 46. Arquitectura objetivo 1.x

```text
                       ┌───────────────────────┐
                       │      ChxChx CLI       │
                       │        Python         │
                       └──────────┬────────────┘
                                  │
                          Session Manager
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
       Privacy Manager      Network Manager     Sandbox Manager
              │                   │                   │
              ▼                   ▼                   ▼
             Tor             namespace           bubblewrap
                                  │
                                  ▼
                              nftables
                                  │
                                  ▼
                           protected app
```

---

# 47. Estructura futura del repositorio

```text
chxchx-security/
│
├── src/
│   └── chxchx_security/
│       │
│       ├── cli/
│       ├── config/
│       ├── core/
│       ├── privacy/
│       ├── network/
│       ├── sandbox/
│       ├── audit/
│       ├── sessions/
│       └── utils/
│
├── native/
│
├── profiles/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── vm/
│
├── packaging/
│   ├── rpm/
│   └── selinux/
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── ROADMAP.md
│   ├── THREAT_MODEL.md
│   ├── SECURITY.md
│   └── RELEASES.md
│
└── scripts/
```

---

# 48. Git workflow

Branches:

```text
main
develop
feature/*
fix/*
release/*
```

Ejemplo:

```text
feature/network-namespace
feature/nftables-policy
feature/session-manager
```

---

# 49. Pull request rules

Todo PR relacionado con seguridad debe indicar:

```text
Threat addressed:
Privileges required:
Failure mode:
Rollback:
Tests:
```

---

# 50. CI/CD futuro

Pipeline:

```text
lint
 ↓
type-check
 ↓
unit tests
 ↓
integration tests
 ↓
security scan
 ↓
dependency scan
 ↓
SBOM
 ↓
VM tests
 ↓
package
 ↓
sign
```

---

# 51. Definición de DONE

Una feature de seguridad NO está terminada porque:

```text
"funciona en mi PC"
```

Debe cumplir:

```text
implementada
+
testeada
+
fallos controlados
+
rollback
+
documentación
+
threat model actualizado
```

---

# 52. Orden recomendado de desarrollo

No saltarse fases por emoción.

Orden:

```text
v0.1.x
   ↓
stabilization
   ↓
v0.2 namespace
   ↓
v0.2 firewall
   ↓
v0.2 DNS/IPv6 tests
   ↓
v0.3 hardening
   ↓
v0.4 profiles
   ↓
v0.5 sandbox
   ↓
v0.6 audit
   ↓
v0.7 observability
   ↓
v0.8 RPM
   ↓
v0.9 RC
   ↓
v1.0 stable
```

---

# 53. Prioridad real

Orden de importancia:

```text
1. evitar fugas
2. fail closed
3. aislamiento
4. tests
5. permisos mínimos
6. recuperación
7. experiencia CLI/TUI
8. funcionalidades adicionales
```

Nunca:

```text
UI bonita
>
seguridad comprobable
```

---

# 54. Próximo objetivo concreto

La siguiente etapa inmediata después de estabilizar `v0.1.x` es:

```text
v0.2.0
```

Objetivo único:

> Crear una sesión de red aislada mediante Linux Network Namespaces cuya salida pueda utilizar exclusivamente la ruta Tor configurada y donde un fallo de Tor bloquee la conectividad en lugar de utilizar la red normal del host.

No agregar todavía:

- GUI;
- plugins;
- múltiples backends;
- C++;
- configuraciones complejas.

Primero demostrar correctamente el aislamiento.

---

# 55. Milestones

## Milestone A

```text
v0.1.x
```

**Resultado:** CLI confiable.

---

## Milestone B

```text
v0.2.x
```

**Resultado:** red aislada.

---

## Milestone C

```text
v0.3.x
```

**Resultado:** proyecto endurecido y verificable.

---

## Milestone D

```text
v0.5.x
```

**Resultado:** aplicación aislada en red + filesystem.

---

## Milestone E

```text
v0.8.x
```

**Resultado:** instalación Fedora profesional.

---

## Milestone F

```text
v1.0.0
```

**Resultado:** primera versión estable y auditable.

---

# 56. Resumen

La evolución correcta de ChxChx Security es:

```text
        v0.1
Process privacy
       │
       ▼
        v0.2
Network isolation
       │
       ▼
        v0.3
Hardening
       │
       ▼
        v0.4
Profiles
       │
       ▼
        v0.5
Application sandbox
       │
       ▼
        v0.6
Leak auditing
       │
       ▼
        v0.7
Safe observability
       │
       ▼
        v0.8
Fedora packaging
       │
       ▼
        v0.9
Release candidate
       │
       ▼
        v1.0
Stable
```

El proyecto debe crecer a través de **garantías comprobadas**, no acumulando características.

La regla central de todo el roadmap será:

> **Una protección que no puede probarse automáticamente no debe anunciarse como garantía.**
