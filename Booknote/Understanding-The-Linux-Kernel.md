# Understanding the Linux Kernel, 3rd Edition

## Overview

- Kernel
    - Overview (1)
    - Interrupts and Exceptions (4), Go [Booknote/Understanding-The-Linux-Kernel/Interrupt-and-Exception]
    - Kernel Synchronization (5)
    - Timing Measurements (8)
    - System Calls (10)
    - Signals (11)
- Memory
    - Memory Addressing (2)
    - Memory Management (8)
    - Page Cache (15)
    - Page Frame Reclaiming (17)
- Process
    - Overview (3)
    - Process Scheduling (7)
    - Process Address Space (9)
    - Process Communication (19)
    - Process Execution (20)
- File System
    - Virtual Filesystem (12)
    - IO Architecture and Device Drivers (13)
    - Block Device Drivers (14)
    - Accessing Files (16)
    - Ext2 and Ext3 Filesystems (18)
- Appendix
    - System Startup (A)
    - Modules (B)

## Content

### Linux Vs Other Unix-Like Kernels

- Agree on some common standards like POSIX with other Unix-like kernels.
- Adopt some best features and design choices of several different Unix kernels.
    - Monolithic Kernel: composed of several logically different components.
    - Compiled and Statically linked traditional Unix Kernels: dynamically load and unload kernel modules.
    - Kernel Threading: a kernel thread is an execution context that can be independently scheduled, it may be associated with a user program, or it may run only some kernel functions.
    - Multithreaded application support: lightweight processes are the basic execution context.
    - Preemptive Kernel: arbitrarily interleave execution flows.
    - Multiprocessor support: symmetric multiprocessing (SMP)
    - Filesystem
    - STREAMS

### Basic OS Concepts

- `kernel`
    - Load into RAM.
    - Interact with the hardware components.
    - Provide an execution environment to user programs.
    - How program use the resource?
        - Program **issues** a request to os.
        - Kernel **evaluates** the request.
        - Kernel **interacts** with the proper hardware components.
    - Introduces two execution modes for CPU: User Mode and Kernel Mode.
- `multiuser systems`
    - concurrently and independently execute several applications belongs to two or more users.
        - concurrently: application can be active at the same time and contend for the various resources.
        - independently: each application can perform its task with no concern for what the applications of the other users are doing.
    - this is where many of the complexities of modern os kernels comes from.
    - features
        - authentication
        - protection against blocking from others
        - protection against interfereing with or spying on others
        - accounting for limiting the usage of resource
- `users and groups`
    - identified by uid, belongs to gid.
    - root: do almost everything.
- `processes`
    - execution context of a running program
    - a process executes a single sequence of instructions in an address space (a set of memory addresses that the process is allowed to reference).
    - multiprocessing: allow concurrent active processes
    - scheduler: chooses the process that can progress
    - preemptable: system tracks how long each process holds the CPU and periodically activates the scheduler
    - process model: each process has illusion that it's the only process on the machine, and it has exclusive access to operating system services.
- `kernel architecture`
    - each kernel layer is integrated into the whole kernel program and runs in Kernel Mode on behalf of the current process.
    - why monolithic is faster than microkernel: no cost from explicit message passing between the different layers of the operating systems
    - dynamic link and unlink module

### Overview of file system

- associates a `cwd` with each process.
- introduce `soft link`: short files that contain an arbitrary pathname of another file
- file types: regular file, dir, symlink, block-oriented devlice file, character-oriented device file, pipe and named pipe, socket.
- `inode`: all information needed by the filesystem to handle a file is included in a data structure to identify the file.
- read/write/execute X owner/group/others
- read file = access data stored in a hardware block device, performing syscall in Kernel mode.
- open/creat/flock/read/write/lseek/close/rename/unlink

### Overview of Unix Kernel

- Process/Kernel Model
- Process Implementation
    - represented by process descriptor
    - context
        - pc and stack pointer (sp) register
        - general purpose registers
        - floating point registers
        - processor control register containing information about the CPU state
        - memory management registers used to keep track of RAM accessed by the process
- Reentrant Kernels
- Process Address Space
    - each process runs in its private address space
- Synchronization and Critical Regions
    - race condition - atomic operations
    - critical region: any section of code that should be finished by each process that begins it before another process can enter it.
    - semaphore: simply a counter associated with a data structure. It is checked by all kernel threads before they try to access the data structure.
    - spin locks
    - deadlock: avoid this problem by requesting locks in a predefined order.
- Signals and Interprocess Communication
    - POSIX defines some signals. Kernel performs a default action for signal if no alternatives specified.
    - default actions:
        - terminate
        - ignore
        - suspend
        - resume
        - core dump (write execution context and the contents of the address space in a file) and terminate
    - SIGKILL/SIGSTOP signal cannot be directly handled/ignored.
    - System V IPC: semaphores, message queues, shared memory.
- Process Management
    - fork/`_exit`: create / terminate a process
    - `exec`: load a new program
    - copy-on-write
    - zombie process: terminated process remains in that state until its parent process executes a wait4/waitpid system call on it.
    - orphanzed process becomes children of `init`.
    - `job`: process group.
    - `login session`: contains all processes that are descendants of the process that has started a working session on a specific terminal. Processes receive SIGTTIN/SIGTTOU to respond bg/fg.
- Memory Management
    - provides `virtual memory`, acts as a logical layer between the application memory requests and the hardware Memory Management Unit(MMU).
    - `virtual address space`: a set of memory that a process can use.
    - RAM = kernel image + virtual memory system
- Device Drivers
    - The kernel interacts with I/O devices.
    - The kernel deals with all devices in a uniform way and access them through same interface.
    - `/dev`


