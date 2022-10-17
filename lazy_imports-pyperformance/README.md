# Benchmark Lazy Imports on top of CPython Main

These experiments ran on top of CPython Main branch with Lazy Imports implementation on a dedicated AWS becnhmarking machine.

+ GitHub Fork: [https://github.com/Kronuz/cpython.git](https://github.com/Kronuz/cpython.git)
+ CPython Main: [553d3c10172254b190078c50eb9f8e60522c8f41](https://github.com/Kronuz/cpython/tree/553d3c10172254b190078c50eb9f8e60522c8f41)
+ Lazy Imports: [44b7e9b87676e0bccde43103a4c954c8d79de017](https://github.com/Kronuz/cpython/tree/44b7e9b87676e0bccde43103a4c954c8d79de017)

---

## Benchmark

Configured each version to compare (`cpython-main`, `cpython-lazy_imports-disabled` and
`cpython-lazy_imports-enabled`) with all optimizations enabled, using LTO and `pyperf system tune`:

```
$ ./configure --enable-optimizations --with-lto

$ make -j

$ sudo pyperf system tune

Tune the system configuration to run benchmarks

Actions
=======

CPU Frequency: Minimum frequency of CPU 0-71 set to the maximum frequency

System state
============

CPU: use 72 logical CPUs: 0-71
Perf event: Maximum sample rate: 1 per second
ASLR: Full randomization
Linux scheduler: No CPU is isolated
CPU Frequency: 0-71=min=max=3000 MHz
CPU scaling governor (intel_pstate): performance
Turbo Boost (intel_pstate): Turbo Boost disabled
IRQ affinity: irqbalance service: inactive
IRQ affinity: Default IRQ affinity: CPU 0-71
IRQ affinity: IRQ affinity: IRQ 0-15,25-90,92-119,124-159=CPU 0-71; IRQ 120,122=CPU 0-17,36-53; IRQ 121,123=CPU 18-35,54-71

Advices
=======

Linux scheduler: Use isolcpus=<cpu list> kernel parameter to isolate CPUs
Linux scheduler: Use rcu_nocbs=<cpu list> kernel parameter (with isolcpus) to not schedule RCU on isolated CPUs
```

---

### CPython Main

```
$ pyperformance run --python=~/cpython-main/python -o ~/cpython-main-opt.json
Python benchmark suite 1.0.5
...

$ pyperformance show ~/cpython-main-opt.json

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-17 18:36:04.525376
End date: 2022-10-17 18:56:19.999318

### 2to3 ###
Mean +- std dev: 304 ms +- 1 ms

### chameleon ###
Mean +- std dev: 8.06 ms +- 0.06 ms

### chaos ###
Mean +- std dev: 82.2 ms +- 1.7 ms

### crypto_pyaes ###
Mean +- std dev: 91.7 ms +- 0.9 ms

### deltablue ###
Mean +- std dev: 4.03 ms +- 0.05 ms

### django_template ###
Mean +- std dev: 39.9 ms +- 1.1 ms

### dulwich_log ###
Mean +- std dev: 81.1 ms +- 0.5 ms

### fannkuch ###
Mean +- std dev: 473 ms +- 4 ms

### float ###
Mean +- std dev: 90.0 ms +- 1.1 ms

### genshi_text ###
Mean +- std dev: 26.2 ms +- 0.3 ms

### genshi_xml ###
Mean +- std dev: 61.9 ms +- 1.2 ms

### go ###
Mean +- std dev: 165 ms +- 3 ms

### hexiom ###
Mean +- std dev: 7.55 ms +- 0.10 ms

### html5lib ###
Mean +- std dev: 74.0 ms +- 3.2 ms

### json_dumps ###
Mean +- std dev: 11.8 ms +- 0.2 ms

### json_loads ###
Mean +- std dev: 29.5 us +- 0.6 us

### logging_format ###
Mean +- std dev: 8.48 us +- 0.09 us

### logging_silent ###
Mean +- std dev: 114 ns +- 2 ns

### logging_simple ###
Mean +- std dev: 7.69 us +- 0.11 us

### mako ###
Mean +- std dev: 12.4 ms +- 0.3 ms

### meteor_contest ###
Mean +- std dev: 127 ms +- 2 ms

### nbody ###
Mean +- std dev: 116 ms +- 1 ms

### nqueens ###
Mean +- std dev: 96.7 ms +- 2.0 ms

### pathlib ###
Mean +- std dev: 27.2 ms +- 0.4 ms

### pickle ###
Mean +- std dev: 12.4 us +- 0.2 us

### pickle_dict ###
Mean +- std dev: 37.1 us +- 0.2 us

### pickle_list ###
Mean +- std dev: 5.06 us +- 0.06 us

### pickle_pure_python ###
Mean +- std dev: 355 us +- 9 us

### pidigits ###
Mean +- std dev: 249 ms +- 0 ms

### pyflate ###
Mean +- std dev: 496 ms +- 5 ms

### python_startup ###
Mean +- std dev: 11.5 ms +- 0.1 ms

### python_startup_no_site ###
Mean +- std dev: 8.55 ms +- 0.07 ms

### raytrace ###
Mean +- std dev: 346 ms +- 2 ms

### regex_compile ###
Mean +- std dev: 159 ms +- 3 ms

### regex_dna ###
Mean +- std dev: 259 ms +- 0 ms

### regex_effbot ###
Mean +- std dev: 4.26 ms +- 0.02 ms

### regex_v8 ###
Mean +- std dev: 26.2 ms +- 0.1 ms

### richards ###
Mean +- std dev: 52.5 ms +- 0.7 ms

### scimark_fft ###
Mean +- std dev: 386 ms +- 3 ms

### scimark_lu ###
Mean +- std dev: 134 ms +- 3 ms

### scimark_monte_carlo ###
Mean +- std dev: 81.9 ms +- 1.2 ms

### scimark_sor ###
Mean +- std dev: 131 ms +- 2 ms

### scimark_sparse_mat_mult ###
Mean +- std dev: 4.83 ms +- 0.05 ms

### spectral_norm ###
Mean +- std dev: 118 ms +- 3 ms

### sqlalchemy_declarative ###
Mean +- std dev: 162 ms +- 3 ms

### sqlalchemy_imperative ###
Mean +- std dev: 20.9 ms +- 0.8 ms

### sqlite_synth ###
Mean +- std dev: 3.23 us +- 0.11 us

### sympy_expand ###
Mean +- std dev: 552 ms +- 8 ms

### sympy_integrate ###
Mean +- std dev: 24.7 ms +- 0.1 ms

### sympy_sum ###
Mean +- std dev: 199 ms +- 2 ms

### sympy_str ###
Mean +- std dev: 341 ms +- 4 ms

### telco ###
Mean +- std dev: 7.85 ms +- 0.19 ms

### tornado_http ###
Mean +- std dev: 146 ms +- 2 ms

### unpack_sequence ###
Mean +- std dev: 55.0 ns +- 0.8 ns

### unpickle ###
Mean +- std dev: 16.4 us +- 1.4 us

### unpickle_list ###
Mean +- std dev: 6.13 us +- 0.05 us

### unpickle_pure_python ###
Mean +- std dev: 247 us +- 2 us

### xml_etree_parse ###
Mean +- std dev: 182 ms +- 4 ms

### xml_etree_iterparse ###
Mean +- std dev: 126 ms +- 3 ms

### xml_etree_generate ###
Mean +- std dev: 93.8 ms +- 0.8 ms

### xml_etree_process ###
Mean +- std dev: 65.6 ms +- 0.7 ms
```

---

### Lazy Imports (disabled)

```
$ pyperformance run --python=~/cpython-lazy_imports-disabled/python -o ~/cpython-lazy_imports-opt-disabled.json
Python benchmark suite 1.0.5
...

$ pyperformance show ~/cpython-lazy_imports-opt-disabled.json

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-17 17:53:13.392924
End date: 2022-10-17 18:13:15.644914

### 2to3 ###
Mean +- std dev: 304 ms +- 1 ms

### chameleon ###
Mean +- std dev: 8.03 ms +- 0.09 ms

### chaos ###
Mean +- std dev: 81.0 ms +- 1.7 ms

### crypto_pyaes ###
Mean +- std dev: 90.8 ms +- 1.5 ms

### deltablue ###
Mean +- std dev: 3.98 ms +- 0.04 ms

### django_template ###
Mean +- std dev: 40.3 ms +- 0.8 ms

### dulwich_log ###
Mean +- std dev: 80.8 ms +- 0.6 ms

### fannkuch ###
Mean +- std dev: 455 ms +- 5 ms

### float ###
Mean +- std dev: 90.4 ms +- 1.1 ms

### genshi_text ###
Mean +- std dev: 26.5 ms +- 0.4 ms

### genshi_xml ###
Mean +- std dev: 60.8 ms +- 0.4 ms

### go ###
Mean +- std dev: 163 ms +- 2 ms

### hexiom ###
Mean +- std dev: 7.46 ms +- 0.19 ms

### html5lib ###
Mean +- std dev: 72.7 ms +- 3.1 ms

### json_dumps ###
Mean +- std dev: 11.8 ms +- 0.2 ms

### json_loads ###
Mean +- std dev: 29.9 us +- 0.5 us

### logging_format ###
Mean +- std dev: 8.32 us +- 0.09 us

### logging_silent ###
Mean +- std dev: 115 ns +- 1 ns

### logging_simple ###
Mean +- std dev: 7.61 us +- 0.06 us

### mako ###
Mean +- std dev: 12.7 ms +- 0.1 ms

### meteor_contest ###
Mean +- std dev: 126 ms +- 1 ms

### nbody ###
Mean +- std dev: 117 ms +- 1 ms

### nqueens ###
Mean +- std dev: 101 ms +- 1 ms

### pathlib ###
Mean +- std dev: 27.3 ms +- 0.6 ms

### pickle ###
Mean +- std dev: 12.7 us +- 0.1 us

### pickle_dict ###
Mean +- std dev: 38.9 us +- 0.1 us

### pickle_list ###
Mean +- std dev: 5.09 us +- 0.11 us

### pickle_pure_python ###
Mean +- std dev: 359 us +- 4 us

### pidigits ###
Mean +- std dev: 250 ms +- 0 ms

### pyflate ###
Mean +- std dev: 489 ms +- 4 ms

### python_startup ###
Mean +- std dev: 11.5 ms +- 0.1 ms

### python_startup_no_site ###
Mean +- std dev: 8.60 ms +- 0.06 ms

### raytrace ###
Mean +- std dev: 338 ms +- 2 ms

### regex_compile ###
Mean +- std dev: 158 ms +- 3 ms

### regex_dna ###
Mean +- std dev: 255 ms +- 2 ms

### regex_effbot ###
Mean +- std dev: 4.52 ms +- 0.01 ms

### regex_v8 ###
Mean +- std dev: 26.8 ms +- 0.4 ms

### richards ###
Mean +- std dev: 54.0 ms +- 1.1 ms

### scimark_fft ###
Mean +- std dev: 390 ms +- 4 ms

### scimark_lu ###
Mean +- std dev: 137 ms +- 2 ms

### scimark_monte_carlo ###
Mean +- std dev: 83.1 ms +- 3.3 ms

### scimark_sor ###
Mean +- std dev: 130 ms +- 2 ms

### scimark_sparse_mat_mult ###
Mean +- std dev: 5.05 ms +- 0.08 ms

### spectral_norm ###
Mean +- std dev: 118 ms +- 1 ms

### sqlalchemy_declarative ###
Mean +- std dev: 162 ms +- 3 ms

### sqlalchemy_imperative ###
Mean +- std dev: 21.2 ms +- 1.1 ms

### sqlite_synth ###
Mean +- std dev: 3.20 us +- 0.05 us

### sympy_expand ###
Mean +- std dev: 555 ms +- 3 ms

### sympy_integrate ###
Mean +- std dev: 24.8 ms +- 0.2 ms

### sympy_sum ###
Mean +- std dev: 200 ms +- 2 ms

### sympy_str ###
Mean +- std dev: 342 ms +- 2 ms

### telco ###
Mean +- std dev: 8.01 ms +- 0.14 ms

### tornado_http ###
Mean +- std dev: 144 ms +- 2 ms

### unpack_sequence ###
Mean +- std dev: 56.9 ns +- 1.0 ns

### unpickle ###
Mean +- std dev: 16.7 us +- 1.4 us

### unpickle_list ###
Mean +- std dev: 6.04 us +- 0.06 us

### unpickle_pure_python ###
Mean +- std dev: 250 us +- 1 us

### xml_etree_parse ###
Mean +- std dev: 184 ms +- 2 ms

### xml_etree_iterparse ###
Mean +- std dev: 124 ms +- 1 ms

### xml_etree_generate ###
Mean +- std dev: 94.6 ms +- 0.9 ms

### xml_etree_process ###
Mean +- std dev: 65.7 ms +- 1.1 ms
```

---

### Lazy Imports (enabled)

```
$ pyperformance run --python=~/cpython-lazy_imports-enabled/python -o ~/cpython-lazy_imports-opt-enabled.json
Python benchmark suite 1.0.5
...

$ pyperformance show ~/cpython-lazy_imports-opt-enabled.json

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-17 18:15:13.290025
End date: 2022-10-17 18:31:15.360180

### 2to3 ###
Mean +- std dev: 303 ms +- 2 ms

### chameleon ###
Mean +- std dev: 8.06 ms +- 0.06 ms

### chaos ###
Mean +- std dev: 82.3 ms +- 1.0 ms

### crypto_pyaes ###
Mean +- std dev: 91.0 ms +- 1.0 ms

### deltablue ###
Mean +- std dev: 4.11 ms +- 0.06 ms

### django_template ###
Mean +- std dev: 41.2 ms +- 0.5 ms

### dulwich_log ###
Mean +- std dev: 80.9 ms +- 0.6 ms

### fannkuch ###
Mean +- std dev: 455 ms +- 4 ms

### float ###
Mean +- std dev: 91.8 ms +- 1.7 ms

### go ###
Mean +- std dev: 165 ms +- 1 ms

### hexiom ###
Mean +- std dev: 7.58 ms +- 0.21 ms

### html5lib ###
Mean +- std dev: 72.9 ms +- 2.5 ms

### json_dumps ###
Mean +- std dev: 12.0 ms +- 0.2 ms

### json_loads ###
Mean +- std dev: 29.8 us +- 0.5 us

### logging_format ###
Mean +- std dev: 8.55 us +- 0.10 us

### logging_silent ###
Mean +- std dev: 116 ns +- 1 ns

### logging_simple ###
Mean +- std dev: 7.86 us +- 0.11 us

### mako ###
Mean +- std dev: 12.7 ms +- 0.1 ms

### meteor_contest ###
Mean +- std dev: 129 ms +- 2 ms

### nbody ###
Mean +- std dev: 118 ms +- 5 ms

### nqueens ###
Mean +- std dev: 99.2 ms +- 2.0 ms

### pathlib ###
Mean +- std dev: 27.5 ms +- 0.7 ms

### pickle ###
Mean +- std dev: 12.9 us +- 0.2 us

### pickle_dict ###
Mean +- std dev: 40.0 us +- 0.2 us

### pickle_list ###
Mean +- std dev: 5.08 us +- 0.06 us

### pickle_pure_python ###
Mean +- std dev: 355 us +- 3 us

### pidigits ###
Mean +- std dev: 255 ms +- 0 ms

### pyflate ###
Mean +- std dev: 495 ms +- 5 ms

### python_startup ###
Mean +- std dev: 11.6 ms +- 0.1 ms

### python_startup_no_site ###
Mean +- std dev: 8.72 ms +- 0.06 ms

### raytrace ###
Mean +- std dev: 346 ms +- 4 ms

### regex_compile ###
Mean +- std dev: 161 ms +- 3 ms

### regex_dna ###
Mean +- std dev: 260 ms +- 3 ms

### regex_effbot ###
Mean +- std dev: 4.41 ms +- 0.08 ms

### regex_v8 ###
Mean +- std dev: 26.2 ms +- 0.3 ms

### richards ###
Mean +- std dev: 52.6 ms +- 1.1 ms

### scimark_fft ###
Mean +- std dev: 393 ms +- 4 ms

### scimark_lu ###
Mean +- std dev: 134 ms +- 2 ms

### scimark_monte_carlo ###
Mean +- std dev: 81.9 ms +- 1.0 ms

### scimark_sor ###
Mean +- std dev: 128 ms +- 1 ms

### scimark_sparse_mat_mult ###
Mean +- std dev: 4.98 ms +- 0.12 ms

### spectral_norm ###
Mean +- std dev: 117 ms +- 1 ms

### sqlite_synth ###
Mean +- std dev: 3.23 us +- 0.06 us

### telco ###
Mean +- std dev: 7.94 ms +- 0.09 ms

### tornado_http ###
Mean +- std dev: 145 ms +- 2 ms

### unpack_sequence ###
Mean +- std dev: 55.0 ns +- 0.8 ns

### unpickle ###
Mean +- std dev: 16.2 us +- 0.1 us

### unpickle_list ###
Mean +- std dev: 6.22 us +- 0.04 us

### unpickle_pure_python ###
Mean +- std dev: 253 us +- 1 us

### xml_etree_parse ###
Mean +- std dev: 184 ms +- 5 ms

### xml_etree_iterparse ###
Mean +- std dev: 126 ms +- 4 ms

### xml_etree_generate ###
Mean +- std dev: 94.1 ms +- 0.8 ms

### xml_etree_process ###
Mean +- std dev: 65.7 ms +- 2.4 ms
```

---

## Results

### CPython Main vs. Lazy Imports (disabled)

```
$ pyperformance compare ~/cpython-main-opt.json ~/cpython-lazy_imports-opt-disabled.json -O table

cpython-main-opt.json
=====================

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-17 18:36:04.525376
End date: 2022-10-17 18:56:19.999318

cpython-lazy_imports-opt-disabled.json
======================================

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-17 17:53:13.392924
End date: 2022-10-17 18:13:15.644914

+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| Benchmark               | cpython-main-opt.json | cpython-lazy_imports-opt-disabled.json | Change       | Significance           |
+=========================+=======================+========================================+==============+========================+
| 2to3                    | 304 ms                | 304 ms                                 | 1.00x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| chameleon               | 8.06 ms               | 8.03 ms                                | 1.00x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| chaos                   | 82.2 ms               | 81.0 ms                                | 1.01x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| crypto_pyaes            | 91.7 ms               | 90.8 ms                                | 1.01x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| deltablue               | 4.03 ms               | 3.98 ms                                | 1.01x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| django_template         | 39.9 ms               | 40.3 ms                                | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| dulwich_log             | 81.1 ms               | 80.8 ms                                | 1.00x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| fannkuch                | 473 ms                | 455 ms                                 | 1.04x faster | Significant (t=21.43)  |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| float                   | 90.0 ms               | 90.4 ms                                | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| genshi_text             | 26.2 ms               | 26.5 ms                                | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| genshi_xml              | 61.9 ms               | 60.8 ms                                | 1.02x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| go                      | 165 ms                | 163 ms                                 | 1.01x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| hexiom                  | 7.55 ms               | 7.46 ms                                | 1.01x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| html5lib                | 74.0 ms               | 72.7 ms                                | 1.02x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| json_dumps              | 11.8 ms               | 11.8 ms                                | 1.00x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| json_loads              | 29.5 us               | 29.9 us                                | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| logging_format          | 8.48 us               | 8.32 us                                | 1.02x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| logging_silent          | 114 ns                | 115 ns                                 | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| logging_simple          | 7.69 us               | 7.61 us                                | 1.01x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| mako                    | 12.4 ms               | 12.7 ms                                | 1.02x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| meteor_contest          | 127 ms                | 126 ms                                 | 1.00x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| nbody                   | 116 ms                | 117 ms                                 | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| nqueens                 | 96.7 ms               | 101 ms                                 | 1.04x slower | Significant (t=-13.39) |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| pathlib                 | 27.2 ms               | 27.3 ms                                | 1.00x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| pickle                  | 12.4 us               | 12.7 us                                | 1.02x slower | Significant (t=-8.97)  |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| pickle_dict             | 37.1 us               | 38.9 us                                | 1.05x slower | Significant (t=-55.55) |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| pickle_list             | 5.06 us               | 5.09 us                                | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| pickle_pure_python      | 355 us                | 359 us                                 | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| pidigits                | 249 ms                | 250 ms                                 | 1.00x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| pyflate                 | 496 ms                | 489 ms                                 | 1.01x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| python_startup          | 11.5 ms               | 11.5 ms                                | 1.00x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| python_startup_no_site  | 8.55 ms               | 8.60 ms                                | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| raytrace                | 346 ms                | 338 ms                                 | 1.03x faster | Significant (t=22.16)  |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| regex_compile           | 159 ms                | 158 ms                                 | 1.01x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| regex_dna               | 259 ms                | 255 ms                                 | 1.02x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| regex_effbot            | 4.26 ms               | 4.52 ms                                | 1.06x slower | Significant (t=-94.52) |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| regex_v8                | 26.2 ms               | 26.8 ms                                | 1.02x slower | Significant (t=-11.82) |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| richards                | 52.5 ms               | 54.0 ms                                | 1.03x slower | Significant (t=-8.79)  |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| scimark_fft             | 386 ms                | 390 ms                                 | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| scimark_lu              | 134 ms                | 137 ms                                 | 1.02x slower | Significant (t=-6.26)  |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| scimark_monte_carlo     | 81.9 ms               | 83.1 ms                                | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| scimark_sor             | 131 ms                | 130 ms                                 | 1.00x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| scimark_sparse_mat_mult | 4.83 ms               | 5.05 ms                                | 1.04x slower | Significant (t=-17.39) |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| spectral_norm           | 118 ms                | 118 ms                                 | 1.01x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| sqlalchemy_declarative  | 162 ms                | 162 ms                                 | 1.00x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| sqlalchemy_imperative   | 20.9 ms               | 21.2 ms                                | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| sqlite_synth            | 3.23 us               | 3.20 us                                | 1.01x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| sympy_expand            | 552 ms                | 555 ms                                 | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| sympy_integrate         | 24.7 ms               | 24.8 ms                                | 1.00x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| sympy_str               | 341 ms                | 342 ms                                 | 1.00x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| sympy_sum               | 199 ms                | 200 ms                                 | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| telco                   | 7.85 ms               | 8.01 ms                                | 1.02x slower | Significant (t=-5.37)  |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| tornado_http            | 146 ms                | 144 ms                                 | 1.01x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| unpack_sequence         | 55.0 ns               | 56.9 ns                                | 1.03x slower | Significant (t=-11.18) |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| unpickle                | 16.4 us               | 16.7 us                                | 1.02x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| unpickle_list           | 6.13 us               | 6.04 us                                | 1.01x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| unpickle_pure_python    | 247 us                | 250 us                                 | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| xml_etree_generate      | 93.8 ms               | 94.6 ms                                | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| xml_etree_iterparse     | 126 ms                | 124 ms                                 | 1.01x faster | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| xml_etree_parse         | 182 ms                | 184 ms                                 | 1.01x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
| xml_etree_process       | 65.6 ms               | 65.7 ms                                | 1.00x slower | Not significant        |
+-------------------------+-----------------------+----------------------------------------+--------------+------------------------+
```

---

```
$ pyperf compare_to ~/cpython-main-opt.json ~/cpython-lazy_imports-opt-disabled.json --table

+-------------------------+------------------+-----------------------------------+
| Benchmark               | cpython-main-opt | cpython-lazy_imports-opt-disabled |
+=========================+==================+===================================+
| chameleon               | 8.06 ms          | 8.03 ms: 1.00x faster             |
+-------------------------+------------------+-----------------------------------+
| chaos                   | 82.2 ms          | 81.0 ms: 1.01x faster             |
+-------------------------+------------------+-----------------------------------+
| crypto_pyaes            | 91.7 ms          | 90.8 ms: 1.01x faster             |
+-------------------------+------------------+-----------------------------------+
| deltablue               | 4.03 ms          | 3.98 ms: 1.01x faster             |
+-------------------------+------------------+-----------------------------------+
| django_template         | 39.9 ms          | 40.3 ms: 1.01x slower             |
+-------------------------+------------------+-----------------------------------+
| dulwich_log             | 81.1 ms          | 80.8 ms: 1.00x faster             |
+-------------------------+------------------+-----------------------------------+
| fannkuch                | 473 ms           | 455 ms: 1.04x faster              |
+-------------------------+------------------+-----------------------------------+
| float                   | 90.0 ms          | 90.4 ms: 1.01x slower             |
+-------------------------+------------------+-----------------------------------+
| genshi_text             | 26.2 ms          | 26.5 ms: 1.01x slower             |
+-------------------------+------------------+-----------------------------------+
| genshi_xml              | 61.9 ms          | 60.8 ms: 1.02x faster             |
+-------------------------+------------------+-----------------------------------+
| go                      | 165 ms           | 163 ms: 1.01x faster              |
+-------------------------+------------------+-----------------------------------+
| hexiom                  | 7.55 ms          | 7.46 ms: 1.01x faster             |
+-------------------------+------------------+-----------------------------------+
| html5lib                | 74.0 ms          | 72.7 ms: 1.02x faster             |
+-------------------------+------------------+-----------------------------------+
| json_loads              | 29.5 us          | 29.9 us: 1.01x slower             |
+-------------------------+------------------+-----------------------------------+
| logging_format          | 8.48 us          | 8.32 us: 1.02x faster             |
+-------------------------+------------------+-----------------------------------+
| logging_silent          | 114 ns           | 115 ns: 1.01x slower              |
+-------------------------+------------------+-----------------------------------+
| logging_simple          | 7.69 us          | 7.61 us: 1.01x faster             |
+-------------------------+------------------+-----------------------------------+
| mako                    | 12.4 ms          | 12.7 ms: 1.02x slower             |
+-------------------------+------------------+-----------------------------------+
| nbody                   | 116 ms           | 117 ms: 1.01x slower              |
+-------------------------+------------------+-----------------------------------+
| nqueens                 | 96.7 ms          | 101 ms: 1.04x slower              |
+-------------------------+------------------+-----------------------------------+
| pickle                  | 12.4 us          | 12.7 us: 1.02x slower             |
+-------------------------+------------------+-----------------------------------+
| pickle_dict             | 37.1 us          | 38.9 us: 1.05x slower             |
+-------------------------+------------------+-----------------------------------+
| pickle_pure_python      | 355 us           | 359 us: 1.01x slower              |
+-------------------------+------------------+-----------------------------------+
| pidigits                | 249 ms           | 250 ms: 1.00x slower              |
+-------------------------+------------------+-----------------------------------+
| pyflate                 | 496 ms           | 489 ms: 1.01x faster              |
+-------------------------+------------------+-----------------------------------+
| python_startup          | 11.5 ms          | 11.5 ms: 1.00x slower             |
+-------------------------+------------------+-----------------------------------+
| python_startup_no_site  | 8.55 ms          | 8.60 ms: 1.01x slower             |
+-------------------------+------------------+-----------------------------------+
| raytrace                | 346 ms           | 338 ms: 1.03x faster              |
+-------------------------+------------------+-----------------------------------+
| regex_dna               | 259 ms           | 255 ms: 1.02x faster              |
+-------------------------+------------------+-----------------------------------+
| regex_effbot            | 4.26 ms          | 4.52 ms: 1.06x slower             |
+-------------------------+------------------+-----------------------------------+
| regex_v8                | 26.2 ms          | 26.8 ms: 1.02x slower             |
+-------------------------+------------------+-----------------------------------+
| richards                | 52.5 ms          | 54.0 ms: 1.03x slower             |
+-------------------------+------------------+-----------------------------------+
| scimark_fft             | 386 ms           | 390 ms: 1.01x slower              |
+-------------------------+------------------+-----------------------------------+
| scimark_lu              | 134 ms           | 137 ms: 1.02x slower              |
+-------------------------+------------------+-----------------------------------+
| scimark_monte_carlo     | 81.9 ms          | 83.1 ms: 1.01x slower             |
+-------------------------+------------------+-----------------------------------+
| scimark_sparse_mat_mult | 4.83 ms          | 5.05 ms: 1.04x slower             |
+-------------------------+------------------+-----------------------------------+
| sympy_expand            | 552 ms           | 555 ms: 1.01x slower              |
+-------------------------+------------------+-----------------------------------+
| sympy_sum               | 199 ms           | 200 ms: 1.01x slower              |
+-------------------------+------------------+-----------------------------------+
| sympy_str               | 341 ms           | 342 ms: 1.00x slower              |
+-------------------------+------------------+-----------------------------------+
| telco                   | 7.85 ms          | 8.01 ms: 1.02x slower             |
+-------------------------+------------------+-----------------------------------+
| tornado_http            | 146 ms           | 144 ms: 1.01x faster              |
+-------------------------+------------------+-----------------------------------+
| unpack_sequence         | 55.0 ns          | 56.9 ns: 1.03x slower             |
+-------------------------+------------------+-----------------------------------+
| unpickle_list           | 6.13 us          | 6.04 us: 1.01x faster             |
+-------------------------+------------------+-----------------------------------+
| unpickle_pure_python    | 247 us           | 250 us: 1.01x slower              |
+-------------------------+------------------+-----------------------------------+
| xml_etree_parse         | 182 ms           | 184 ms: 1.01x slower              |
+-------------------------+------------------+-----------------------------------+
| xml_etree_iterparse     | 126 ms           | 124 ms: 1.01x faster              |
+-------------------------+------------------+-----------------------------------+
| xml_etree_generate      | 93.8 ms          | 94.6 ms: 1.01x slower             |
+-------------------------+------------------+-----------------------------------+
| Geometric mean          | (ref)            | 1.00x slower                      |
+-------------------------+------------------+-----------------------------------+

Benchmark hidden because not significant (14): 2to3, json_dumps, meteor_contest, pathlib, pickle_list, regex_compile, scimark_sor, spectral_norm, sqlalchemy_declarative, sqlalchemy_imperative, sqlite_synth, sympy_integrate, unpickle, xml_etree_process
```

---

### CPython Main vs. Lazy Imports (enabled)

```
$ pyperformance compare ~/cpython-main-opt.json ~/cpython-lazy_imports-opt-enabled.json -O table

cpython-main-opt.json
=====================

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-17 18:36:04.525376
End date: 2022-10-17 18:56:19.999318

cpython-lazy_imports-opt-enabled.json
=====================================

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-17 18:15:13.290025
End date: 2022-10-17 18:31:15.360180

+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| Benchmark               | cpython-main-opt.json | cpython-lazy_imports-opt-enabled.json | Change       | Significance            |
+=========================+=======================+=======================================+==============+=========================+
| 2to3                    | 304 ms                | 303 ms                                | 1.00x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| chameleon               | 8.06 ms               | 8.06 ms                               | 1.00x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| chaos                   | 82.2 ms               | 82.3 ms                               | 1.00x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| crypto_pyaes            | 91.7 ms               | 91.0 ms                               | 1.01x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| deltablue               | 4.03 ms               | 4.11 ms                               | 1.02x slower | Significant (t=-9.14)   |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| django_template         | 39.9 ms               | 41.2 ms                               | 1.03x slower | Significant (t=-8.30)   |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| dulwich_log             | 81.1 ms               | 80.9 ms                               | 1.00x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| fannkuch                | 473 ms                | 455 ms                                | 1.04x faster | Significant (t=24.65)   |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| float                   | 90.0 ms               | 91.8 ms                               | 1.02x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| go                      | 165 ms                | 165 ms                                | 1.00x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| hexiom                  | 7.55 ms               | 7.58 ms                               | 1.00x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| html5lib                | 74.0 ms               | 72.9 ms                               | 1.02x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| json_dumps              | 11.8 ms               | 12.0 ms                               | 1.02x slower | Significant (t=-5.89)   |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| json_loads              | 29.5 us               | 29.8 us                               | 1.01x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| logging_format          | 8.48 us               | 8.55 us                               | 1.01x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| logging_silent          | 114 ns                | 116 ns                                | 1.02x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| logging_simple          | 7.69 us               | 7.86 us                               | 1.02x slower | Significant (t=-8.89)   |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| mako                    | 12.4 ms               | 12.7 ms                               | 1.02x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| meteor_contest          | 127 ms                | 129 ms                                | 1.02x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| nbody                   | 116 ms                | 118 ms                                | 1.02x slower | Significant (t=-4.38)   |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| nqueens                 | 96.7 ms               | 99.2 ms                               | 1.03x slower | Significant (t=-6.69)   |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| pathlib                 | 27.2 ms               | 27.5 ms                               | 1.01x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| pickle                  | 12.4 us               | 12.9 us                               | 1.04x slower | Significant (t=-11.14)  |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| pickle_dict             | 37.1 us               | 40.0 us                               | 1.08x slower | Significant (t=-74.00)  |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| pickle_list             | 5.06 us               | 5.08 us                               | 1.00x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| pickle_pure_python      | 355 us                | 355 us                                | 1.00x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| pidigits                | 249 ms                | 255 ms                                | 1.02x slower | Significant (t=-219.96) |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| pyflate                 | 496 ms                | 495 ms                                | 1.00x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| python_startup          | 11.5 ms               | 11.6 ms                               | 1.01x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| python_startup_no_site  | 8.55 ms               | 8.72 ms                               | 1.02x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| raytrace                | 346 ms                | 346 ms                                | 1.00x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| regex_compile           | 159 ms                | 161 ms                                | 1.01x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| regex_dna               | 259 ms                | 260 ms                                | 1.00x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| regex_effbot            | 4.26 ms               | 4.41 ms                               | 1.04x slower | Significant (t=-14.01)  |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| regex_v8                | 26.2 ms               | 26.2 ms                               | 1.00x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| richards                | 52.5 ms               | 52.6 ms                               | 1.00x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| scimark_fft             | 386 ms                | 393 ms                                | 1.02x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| scimark_lu              | 134 ms                | 134 ms                                | 1.01x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| scimark_monte_carlo     | 81.9 ms               | 81.9 ms                               | 1.00x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| scimark_sor             | 131 ms                | 128 ms                                | 1.02x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| scimark_sparse_mat_mult | 4.83 ms               | 4.98 ms                               | 1.03x slower | Significant (t=-8.73)   |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| spectral_norm           | 118 ms                | 117 ms                                | 1.01x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| sqlite_synth            | 3.23 us               | 3.23 us                               | 1.00x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| telco                   | 7.85 ms               | 7.94 ms                               | 1.01x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| tornado_http            | 146 ms                | 145 ms                                | 1.00x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| unpack_sequence         | 55.0 ns               | 55.0 ns                               | 1.00x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| unpickle                | 16.4 us               | 16.2 us                               | 1.02x faster | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| unpickle_list           | 6.13 us               | 6.22 us                               | 1.01x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| unpickle_pure_python    | 247 us                | 253 us                                | 1.02x slower | Significant (t=-16.98)  |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| xml_etree_generate      | 93.8 ms               | 94.1 ms                               | 1.00x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| xml_etree_iterparse     | 126 ms                | 126 ms                                | 1.00x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| xml_etree_parse         | 182 ms                | 184 ms                                | 1.01x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+
| xml_etree_process       | 65.6 ms               | 65.7 ms                               | 1.00x slower | Not significant         |
+-------------------------+-----------------------+---------------------------------------+--------------+-------------------------+

Skipped 8 benchmarks only in cpython-main-opt.json: genshi_text, genshi_xml, sqlalchemy_declarative, sqlalchemy_imperative, sympy_expand, sympy_integrate, sympy_str, sympy_sum
```

---

```
$ pyperf compare_to ~/cpython-main-opt.json ~/cpython-lazy_imports-opt-enabled.json --table

+-------------------------+------------------+----------------------------------+
| Benchmark               | cpython-main-opt | cpython-lazy_imports-opt-enabled |
+=========================+==================+==================================+
| crypto_pyaes            | 91.7 ms          | 91.0 ms: 1.01x faster            |
+-------------------------+------------------+----------------------------------+
| deltablue               | 4.03 ms          | 4.11 ms: 1.02x slower            |
+-------------------------+------------------+----------------------------------+
| django_template         | 39.9 ms          | 41.2 ms: 1.03x slower            |
+-------------------------+------------------+----------------------------------+
| dulwich_log             | 81.1 ms          | 80.9 ms: 1.00x faster            |
+-------------------------+------------------+----------------------------------+
| fannkuch                | 473 ms           | 455 ms: 1.04x faster             |
+-------------------------+------------------+----------------------------------+
| float                   | 90.0 ms          | 91.8 ms: 1.02x slower            |
+-------------------------+------------------+----------------------------------+
| html5lib                | 74.0 ms          | 72.9 ms: 1.02x faster            |
+-------------------------+------------------+----------------------------------+
| json_dumps              | 11.8 ms          | 12.0 ms: 1.02x slower            |
+-------------------------+------------------+----------------------------------+
| json_loads              | 29.5 us          | 29.8 us: 1.01x slower            |
+-------------------------+------------------+----------------------------------+
| logging_format          | 8.48 us          | 8.55 us: 1.01x slower            |
+-------------------------+------------------+----------------------------------+
| logging_silent          | 114 ns           | 116 ns: 1.02x slower             |
+-------------------------+------------------+----------------------------------+
| logging_simple          | 7.69 us          | 7.86 us: 1.02x slower            |
+-------------------------+------------------+----------------------------------+
| mako                    | 12.4 ms          | 12.7 ms: 1.02x slower            |
+-------------------------+------------------+----------------------------------+
| meteor_contest          | 127 ms           | 129 ms: 1.02x slower             |
+-------------------------+------------------+----------------------------------+
| nbody                   | 116 ms           | 118 ms: 1.02x slower             |
+-------------------------+------------------+----------------------------------+
| nqueens                 | 96.7 ms          | 99.2 ms: 1.03x slower            |
+-------------------------+------------------+----------------------------------+
| pathlib                 | 27.2 ms          | 27.5 ms: 1.01x slower            |
+-------------------------+------------------+----------------------------------+
| pickle                  | 12.4 us          | 12.9 us: 1.04x slower            |
+-------------------------+------------------+----------------------------------+
| pickle_dict             | 37.1 us          | 40.0 us: 1.08x slower            |
+-------------------------+------------------+----------------------------------+
| pidigits                | 249 ms           | 255 ms: 1.02x slower             |
+-------------------------+------------------+----------------------------------+
| python_startup          | 11.5 ms          | 11.6 ms: 1.01x slower            |
+-------------------------+------------------+----------------------------------+
| python_startup_no_site  | 8.55 ms          | 8.72 ms: 1.02x slower            |
+-------------------------+------------------+----------------------------------+
| regex_compile           | 159 ms           | 161 ms: 1.01x slower             |
+-------------------------+------------------+----------------------------------+
| regex_dna               | 259 ms           | 260 ms: 1.00x slower             |
+-------------------------+------------------+----------------------------------+
| regex_effbot            | 4.26 ms          | 4.41 ms: 1.04x slower            |
+-------------------------+------------------+----------------------------------+
| scimark_fft             | 386 ms           | 393 ms: 1.02x slower             |
+-------------------------+------------------+----------------------------------+
| scimark_sor             | 131 ms           | 128 ms: 1.02x faster             |
+-------------------------+------------------+----------------------------------+
| scimark_sparse_mat_mult | 4.83 ms          | 4.98 ms: 1.03x slower            |
+-------------------------+------------------+----------------------------------+
| spectral_norm           | 118 ms           | 117 ms: 1.01x faster             |
+-------------------------+------------------+----------------------------------+
| telco                   | 7.85 ms          | 7.94 ms: 1.01x slower            |
+-------------------------+------------------+----------------------------------+
| unpickle_list           | 6.13 us          | 6.22 us: 1.01x slower            |
+-------------------------+------------------+----------------------------------+
| unpickle_pure_python    | 247 us           | 253 us: 1.02x slower             |
+-------------------------+------------------+----------------------------------+
| xml_etree_parse         | 182 ms           | 184 ms: 1.01x slower             |
+-------------------------+------------------+----------------------------------+
| Geometric mean          | (ref)            | 1.01x slower                     |
+-------------------------+------------------+----------------------------------+

Benchmark hidden because not significant (20): 2to3, chameleon, chaos, go, hexiom, pickle_list, pickle_pure_python, pyflate, raytrace, regex_v8, richards, scimark_lu, scimark_monte_carlo, sqlite_synth, tornado_http, unpack_sequence, unpickle, xml_etree_iterparse, xml_etree_generate, xml_etree_process
Ignored benchmarks (8) of /home/kronuz/cpython-main-opt.json: genshi_text, genshi_xml, sqlalchemy_declarative, sqlalchemy_imperative, sympy_expand, sympy_integrate, sympy_str, sympy_sum
```

---

### Lazy Imports (disabled) vs. Lazy Imports (enabled)

```
$ pyperformance compare ~/cpython-lazy_imports-opt-disabled.json ~/cpython-lazy_imports-opt-enabled.json -O table

cpython-lazy_imports-opt-disabled.json
======================================

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-17 17:53:13.392924
End date: 2022-10-17 18:13:15.644914

cpython-lazy_imports-opt-enabled.json
=====================================

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-17 18:15:13.290025
End date: 2022-10-17 18:31:15.360180

+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| Benchmark               | cpython-lazy_imports-opt-disabled.json | cpython-lazy_imports-opt-enabled.json | Change       | Significance           |
+=========================+========================================+=======================================+==============+========================+
| 2to3                    | 304 ms                                 | 303 ms                                | 1.00x faster | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| chameleon               | 8.03 ms                                | 8.06 ms                               | 1.00x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| chaos                   | 81.0 ms                                | 82.3 ms                               | 1.02x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| crypto_pyaes            | 90.8 ms                                | 91.0 ms                               | 1.00x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| deltablue               | 3.98 ms                                | 4.11 ms                               | 1.03x slower | Significant (t=-14.65) |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| django_template         | 40.3 ms                                | 41.2 ms                               | 1.02x slower | Significant (t=-7.68)  |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| dulwich_log             | 80.8 ms                                | 80.9 ms                               | 1.00x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| fannkuch                | 455 ms                                 | 455 ms                                | 1.00x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| float                   | 90.4 ms                                | 91.8 ms                               | 1.01x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| go                      | 163 ms                                 | 165 ms                                | 1.02x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| hexiom                  | 7.46 ms                                | 7.58 ms                               | 1.02x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| html5lib                | 72.7 ms                                | 72.9 ms                               | 1.00x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| json_dumps              | 11.8 ms                                | 12.0 ms                               | 1.02x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| json_loads              | 29.9 us                                | 29.8 us                               | 1.00x faster | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| logging_format          | 8.32 us                                | 8.55 us                               | 1.03x slower | Significant (t=-13.97) |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| logging_silent          | 115 ns                                 | 116 ns                                | 1.00x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| logging_simple          | 7.61 us                                | 7.86 us                               | 1.03x slower | Significant (t=-15.85) |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| mako                    | 12.7 ms                                | 12.7 ms                               | 1.00x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| meteor_contest          | 126 ms                                 | 129 ms                                | 1.02x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| nbody                   | 117 ms                                 | 118 ms                                | 1.01x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| nqueens                 | 101 ms                                 | 99.2 ms                               | 1.02x faster | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| pathlib                 | 27.3 ms                                | 27.5 ms                               | 1.01x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| pickle                  | 12.7 us                                | 12.9 us                               | 1.01x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| pickle_dict             | 38.9 us                                | 40.0 us                               | 1.03x slower | Significant (t=-35.12) |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| pickle_list             | 5.09 us                                | 5.08 us                               | 1.00x faster | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| pickle_pure_python      | 359 us                                 | 355 us                                | 1.01x faster | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| pidigits                | 250 ms                                 | 255 ms                                | 1.02x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| pyflate                 | 489 ms                                 | 495 ms                                | 1.01x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| python_startup          | 11.5 ms                                | 11.6 ms                               | 1.01x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| python_startup_no_site  | 8.60 ms                                | 8.72 ms                               | 1.01x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| raytrace                | 338 ms                                 | 346 ms                                | 1.02x slower | Significant (t=-11.82) |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| regex_compile           | 158 ms                                 | 161 ms                                | 1.02x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| regex_dna               | 255 ms                                 | 260 ms                                | 1.02x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| regex_effbot            | 4.52 ms                                | 4.41 ms                               | 1.02x faster | Significant (t=10.12)  |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| regex_v8                | 26.8 ms                                | 26.2 ms                               | 1.03x faster | Significant (t=11.25)  |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| richards                | 54.0 ms                                | 52.6 ms                               | 1.03x faster | Significant (t=6.73)   |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| scimark_fft             | 390 ms                                 | 393 ms                                | 1.01x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| scimark_lu              | 137 ms                                 | 134 ms                                | 1.02x faster | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| scimark_monte_carlo     | 83.1 ms                                | 81.9 ms                               | 1.01x faster | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| scimark_sor             | 130 ms                                 | 128 ms                                | 1.01x faster | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| scimark_sparse_mat_mult | 5.05 ms                                | 4.98 ms                               | 1.01x faster | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| spectral_norm           | 118 ms                                 | 117 ms                                | 1.00x faster | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| sqlite_synth            | 3.20 us                                | 3.23 us                               | 1.01x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| telco                   | 8.01 ms                                | 7.94 ms                               | 1.01x faster | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| tornado_http            | 144 ms                                 | 145 ms                                | 1.01x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| unpack_sequence         | 56.9 ns                                | 55.0 ns                               | 1.03x faster | Significant (t=11.60)  |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| unpickle                | 16.7 us                                | 16.2 us                               | 1.03x faster | Significant (t=3.00)   |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| unpickle_list           | 6.04 us                                | 6.22 us                               | 1.03x slower | Significant (t=-19.01) |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| unpickle_pure_python    | 250 us                                 | 253 us                                | 1.01x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| xml_etree_generate      | 94.6 ms                                | 94.1 ms                               | 1.01x faster | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| xml_etree_iterparse     | 124 ms                                 | 126 ms                                | 1.01x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| xml_etree_parse         | 184 ms                                 | 184 ms                                | 1.00x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+
| xml_etree_process       | 65.7 ms                                | 65.7 ms                               | 1.00x slower | Not significant        |
+-------------------------+----------------------------------------+---------------------------------------+--------------+------------------------+

Skipped 8 benchmarks only in cpython-lazy_imports-opt-disabled.json: genshi_text, genshi_xml, sqlalchemy_declarative, sqlalchemy_imperative, sympy_expand, sympy_integrate, sympy_str, sympy_sum
```

---

```
$ pyperf compare_to ~/cpython-lazy_imports-disabled.json ~/cpython-lazy_imports-enabled.json --table

+-------------------------+-------------------------------+------------------------------+
| Benchmark               | cpython-lazy_imports-disabled | cpython-lazy_imports-enabled |
+=========================+===============================+==============================+
| chameleon               | 8.06 ms                       | 8.23 ms: 1.02x slower        |
+-------------------------+-------------------------------+------------------------------+
| chaos                   | 82.1 ms                       | 83.2 ms: 1.01x slower        |
+-------------------------+-------------------------------+------------------------------+
| crypto_pyaes            | 90.7 ms                       | 92.8 ms: 1.02x slower        |
+-------------------------+-------------------------------+------------------------------+
| deltablue               | 4.06 ms                       | 4.15 ms: 1.02x slower        |
+-------------------------+-------------------------------+------------------------------+
| django_template         | 41.1 ms                       | 42.1 ms: 1.02x slower        |
+-------------------------+-------------------------------+------------------------------+
| dulwich_log             | 82.4 ms                       | 82.1 ms: 1.00x faster        |
+-------------------------+-------------------------------+------------------------------+
| float                   | 91.1 ms                       | 91.6 ms: 1.00x slower        |
+-------------------------+-------------------------------+------------------------------+
| go                      | 164 ms                        | 171 ms: 1.04x slower         |
+-------------------------+-------------------------------+------------------------------+
| hexiom                  | 7.52 ms                       | 7.67 ms: 1.02x slower        |
+-------------------------+-------------------------------+------------------------------+
| html5lib                | 73.4 ms                       | 74.4 ms: 1.01x slower        |
+-------------------------+-------------------------------+------------------------------+
| json_dumps              | 11.6 ms                       | 12.0 ms: 1.04x slower        |
+-------------------------+-------------------------------+------------------------------+
| logging_format          | 8.39 us                       | 8.61 us: 1.03x slower        |
+-------------------------+-------------------------------+------------------------------+
| logging_silent          | 120 ns                        | 119 ns: 1.01x faster         |
+-------------------------+-------------------------------+------------------------------+
| logging_simple          | 7.67 us                       | 7.86 us: 1.03x slower        |
+-------------------------+-------------------------------+------------------------------+
| mako                    | 12.8 ms                       | 12.7 ms: 1.01x faster        |
+-------------------------+-------------------------------+------------------------------+
| nbody                   | 116 ms                        | 115 ms: 1.01x faster         |
+-------------------------+-------------------------------+------------------------------+
| nqueens                 | 103 ms                        | 99.8 ms: 1.04x faster        |
+-------------------------+-------------------------------+------------------------------+
| pathlib                 | 27.3 ms                       | 27.8 ms: 1.02x slower        |
+-------------------------+-------------------------------+------------------------------+
| pickle                  | 12.5 us                       | 12.9 us: 1.03x slower        |
+-------------------------+-------------------------------+------------------------------+
| pickle_list             | 5.11 us                       | 5.21 us: 1.02x slower        |
+-------------------------+-------------------------------+------------------------------+
| pickle_pure_python      | 361 us                        | 357 us: 1.01x faster         |
+-------------------------+-------------------------------+------------------------------+
| pidigits                | 237 ms                        | 243 ms: 1.02x slower         |
+-------------------------+-------------------------------+------------------------------+
| pyflate                 | 492 ms                        | 509 ms: 1.03x slower         |
+-------------------------+-------------------------------+------------------------------+
| python_startup_no_site  | 8.55 ms                       | 8.61 ms: 1.01x slower        |
+-------------------------+-------------------------------+------------------------------+
| raytrace                | 344 ms                        | 356 ms: 1.04x slower         |
+-------------------------+-------------------------------+------------------------------+
| regex_compile           | 159 ms                        | 161 ms: 1.02x slower         |
+-------------------------+-------------------------------+------------------------------+
| regex_dna               | 250 ms                        | 256 ms: 1.03x slower         |
+-------------------------+-------------------------------+------------------------------+
| regex_effbot            | 4.24 ms                       | 4.45 ms: 1.05x slower        |
+-------------------------+-------------------------------+------------------------------+
| regex_v8                | 26.1 ms                       | 26.8 ms: 1.03x slower        |
+-------------------------+-------------------------------+------------------------------+
| richards                | 52.8 ms                       | 54.9 ms: 1.04x slower        |
+-------------------------+-------------------------------+------------------------------+
| scimark_fft             | 385 ms                        | 388 ms: 1.01x slower         |
+-------------------------+-------------------------------+------------------------------+
| scimark_monte_carlo     | 82.2 ms                       | 82.7 ms: 1.01x slower        |
+-------------------------+-------------------------------+------------------------------+
| scimark_sor             | 131 ms                        | 129 ms: 1.01x faster         |
+-------------------------+-------------------------------+------------------------------+
| scimark_sparse_mat_mult | 5.08 ms                       | 5.05 ms: 1.01x faster        |
+-------------------------+-------------------------------+------------------------------+
| sqlite_synth            | 3.21 us                       | 3.26 us: 1.01x slower        |
+-------------------------+-------------------------------+------------------------------+
| telco                   | 8.17 ms                       | 7.93 ms: 1.03x faster        |
+-------------------------+-------------------------------+------------------------------+
| tornado_http            | 144 ms                        | 146 ms: 1.01x slower         |
+-------------------------+-------------------------------+------------------------------+
| unpack_sequence         | 59.6 ns                       | 54.1 ns: 1.10x faster        |
+-------------------------+-------------------------------+------------------------------+
| unpickle_list           | 6.09 us                       | 6.33 us: 1.04x slower        |
+-------------------------+-------------------------------+------------------------------+
| unpickle_pure_python    | 254 us                        | 259 us: 1.02x slower         |
+-------------------------+-------------------------------+------------------------------+
| xml_etree_parse         | 183 ms                        | 185 ms: 1.01x slower         |
+-------------------------+-------------------------------+------------------------------+
| xml_etree_iterparse     | 125 ms                        | 128 ms: 1.02x slower         |
+-------------------------+-------------------------------+------------------------------+
| xml_etree_generate      | 93.5 ms                       | 95.0 ms: 1.02x slower        |
+-------------------------+-------------------------------+------------------------------+
| xml_etree_process       | 65.3 ms                       | 65.9 ms: 1.01x slower        |
+-------------------------+-------------------------------+------------------------------+
| Geometric mean          | (ref)                         | 1.01x slower                 |
+-------------------------+-------------------------------+------------------------------+

Benchmark hidden because not significant (9): 2to3, fannkuch, json_loads, meteor_contest, pickle_dict, python_startup, scimark_lu, spectral_norm, unpickle
Ignored benchmarks (6) of /home/kronuz/cpython-lazy_imports-disabled.json: genshi_text, genshi_xml, sympy_expand, sympy_integrate, sympy_str, sympy_sum
```
