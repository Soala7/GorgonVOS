<p align="center">
  <img src="assets/logo.png" width="180" alt="VOS Logo">
</p>

<h1 align="center">Virtual Operating System (VOS)</h1>

<p align="center">
  A modular virtual operating system built from scratch using Python, C and eventally Rust for security.
</p>

---

```markdown
# Gorgon VOS

## Virtual Operating System

Gorgon VOS is a virtual operating system environment designed to explore operating system architecture, system design, and low-level computing concepts.

Unlike a traditional application, Gorgon VOS aims to simulate the structure of a complete operating system by combining a virtual filesystem, kernel services, custom terminal environment, desktop interface, application framework, and hardware abstraction concepts.

The project focuses on understanding how operating systems are built by creating each major subsystem independently while maintaining clear architectural separation.

---

# Project Vision

The goal of Gorgon VOS is to create a self-contained virtual computing environment that provides:

- A custom operating environment
- A virtual filesystem and storage system
- A modular kernel architecture
- A developer-focused terminal
- A customizable desktop environment
- A secure application ecosystem
- Virtual hardware abstraction

Gorgon VOS is designed as both a learning platform and an experimental operating system architecture project.

---

# Current Features

## Kernel Architecture

Gorgon VOS includes a modular kernel foundation responsible for coordinating core system services.

Current kernel components include:

- Service management
- Event communication system
- Logging system
- Filesystem registration
- Process management foundation
- Core subsystem initialization

Architecture:

```

Kernel

├── Service Manager
├── Event Bus
├── Logger
├── Filesystem Service
├── Process Manager
└── VOS API

```

---

# Virtual Filesystem (VFS)

Gorgon VOS contains a custom virtual filesystem that manages files and directories independently from the host operating system.

Implemented features:

- File creation
- Folder creation
- File reading
- File writing
- File deletion
- Folder deletion
- File moving
- File copying
- Directory navigation
- Filesystem tree visualization

Example:

```

/

├── apps/

├── home/

├── system/

├── temp/

└── users/
└── guest/

```

The filesystem operates entirely inside the VOS environment.

---

# Persistent Storage System

Gorgon VOS includes a storage layer that allows filesystem data to survive between sessions.

The virtual disk format:

```

VOS.os

```

stores:

- Directory structure
- Files
- File contents
- Virtual filesystem state

Storage workflow:

```

Filesystem

```
|
```

Storage Manager

```
|
```

VOS.os

```
|
```

Host Storage

```

Current capabilities:

- Filesystem saving
- Filesystem loading
- Persistent virtual disk
- Automatic restoration of previous state

---

# Terminal System

Gorgon VOS includes a custom terminal subsystem designed around operating system shell concepts.

The terminal architecture separates:

```

User Input

```
|
```

Shell

```
|
```

Parser

```
|
```

Command Registry

```
|
```

Command Handler

```
|
```

VOS API

```
|
```

System Services

```

Implemented commands include:

```

ls
cd
cat
touch
write
mkdir
rm
rmdir
mv
cp
tree

```

---

# C/Python Shell Integration

The terminal system includes a low-level C shell architecture connected to the Python-based VOS environment.

Communication flow:

```

C Shell

```
|
```

Callback Interface

```
|
```

Python Bridge

```
|
```

VOS API

```
|
```

Filesystem / Kernel Services

```

This allows Gorgon VOS to experiment with multi-language operating system design while keeping system services modular.

---

# System Architecture Overview

High-level structure:

```

```
             Applications

                  |

          Desktop Environment

                  |

              VOS APIs

                  |

    ----------------------------

         Kernel Layer

    ----------------------------

    Filesystem
    Storage
    Security
    Networking
    Process Management

    ----------------------------

          Host Operating System
```

```

Gorgon VOS is designed around the principle of separation between:

- Applications
- System services
- Kernel components
- Virtual resources
- Host environment
```

---


