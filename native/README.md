# Native helper status

No C++ helper is included in v0.1.0 because it would add privileged/native attack surface without solving a performance problem.

A future native helper is justified only if Phase 1 requires operations that cannot be safely expressed through narrowly scoped system commands. If introduced, it must:

- contain no network protocol implementation;
- contain no cryptography;
- never run as a long-lived root daemon;
- accept a tiny validated command set;
- use Linux capabilities instead of unrestricted root where practical;
- have fuzz/unit tests and an independent review;
- never erase logs or evidence.
