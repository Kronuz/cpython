# `sys._current_loops()` (`3.14-current-loops`)

Adds `sys._current_loops()`, a dict mapping each thread id to the asyncio loop
running on it. Base v3.14.7, one commit.

## Why

An event-loop monitor has to know which loop each thread is running. Keying by thread
id, the way `sys._current_frames()` keys its own, lets the two snapshots join: one
says where a thread is, the other says which loop it belongs to. Nothing in CPython
exposes this today.

## Mechanism

The loop is read from `asyncio_running_loop` on the `_PyThreadStateImpl` struct, where
3.13+ stores the running loop (replacing the thread-local dict entry 3.12 and earlier
used). The implementation walks every interpreter's thread states under the same
stop-the-world and head lock that `sys._current_frames()` and
`sys._current_exceptions()` use, so it sees a consistent set of threads. Empty when no
loop is running; inside a running loop, the running thread's id maps to that exact
loop object.

## ABI

No structure changes; it reads an existing field and adds a method. `abi-check.py`
reports IDENTICAL.

## A note on the build

The function is defined through Argument Clinic. Applying the patch to a pristine tree
fails only on the clinic checksum in the generated `Python/clinic/sysmodule.c.h`,
because that file-level checksum reflects everything else in the file. The fix is not
to force the hunk but to regenerate the clinic output from the source:
`python Tools/clinic/clinic.py Python/sysmodule.c`. The regenerated checksum is correct
for the tree by construction. (On 3.15 the clinic summary line also has a 72-character
limit the docstring must respect.)

## Remove when

CPython grows a supported way to enumerate running loops. Nothing is proposed today.
