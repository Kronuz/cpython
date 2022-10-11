# Benchmark Lazy Imports on top of CPython Main

These experiments ran on top of CPython Main branch with Lazy Imports implementation on a dedicated AWS becnhmarking machine.

+ GitHub Fork: [https://github.com/Kronuz/cpython.git](https://github.com/Kronuz/cpython.git)
+ CPython Main: [553d3c10172254b190078c50eb9f8e60522c8f41](https://github.com/Kronuz/cpython/tree/553d3c10172254b190078c50eb9f8e60522c8f41)
+ Lazy Imports: [77213f781e876869018cce5aefe5828b3b7b6b49](https://github.com/Kronuz/cpython/tree/77213f781e876869018cce5aefe5828b3b7b6b49)

---

## Benchmark

Configured each version to compare (`cpython-main`, `cpython-lazy_imports-disabled` and
`cpython-lazy_imports-enabled`) with all optimizations enabled, using LTO and `pyperf system tune`:

```
$ ./configure --enable-optimizations --with-lto

$ make -j

$ sudo pyperf system tune

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

OK! System ready for benchmarking
```

---

### CPython Main

```
$ pyperformance run --python=~/cpython-main/python -o ~/cpython-main2.json
Python benchmark suite 1.0.5
...

$ pyperformance show ~/cpython-main2.json

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-12 18:02:56.879938
End date: 2022-10-12 18:23:09.986783

### 2to3 ###
Mean +- std dev: 303 ms +- 1 ms

### chameleon ###
Mean +- std dev: 8.06 ms +- 0.07 ms

### chaos ###
Mean +- std dev: 81.9 ms +- 1.0 ms

### crypto_pyaes ###
Mean +- std dev: 91.5 ms +- 1.1 ms

### deltablue ###
Mean +- std dev: 4.03 ms +- 0.05 ms

### django_template ###
Mean +- std dev: 39.9 ms +- 0.7 ms

### dulwich_log ###
Mean +- std dev: 81.0 ms +- 0.5 ms

### fannkuch ###
Mean +- std dev: 473 ms +- 3 ms

### float ###
Mean +- std dev: 90.7 ms +- 1.4 ms

### genshi_text ###
Mean +- std dev: 26.2 ms +- 0.3 ms

### genshi_xml ###
Mean +- std dev: 61.8 ms +- 0.9 ms

### go ###
Mean +- std dev: 164 ms +- 1 ms

### hexiom ###
Mean +- std dev: 7.51 ms +- 0.04 ms

### html5lib ###
Mean +- std dev: 73.6 ms +- 3.2 ms

### json_dumps ###
Mean +- std dev: 11.8 ms +- 0.1 ms

### json_loads ###
Mean +- std dev: 29.4 us +- 0.2 us

### logging_format ###
Mean +- std dev: 8.46 us +- 0.11 us

### logging_silent ###
Mean +- std dev: 113 ns +- 0 ns

### logging_simple ###
Mean +- std dev: 7.66 us +- 0.07 us

### mako ###
Mean +- std dev: 12.4 ms +- 0.1 ms

### meteor_contest ###
Mean +- std dev: 126 ms +- 1 ms

### nbody ###
Mean +- std dev: 116 ms +- 1 ms

### nqueens ###
Mean +- std dev: 96.1 ms +- 0.9 ms

### pathlib ###
Mean +- std dev: 27.4 ms +- 0.5 ms

### pickle ###
Mean +- std dev: 12.4 us +- 0.1 us

### pickle_dict ###
Mean +- std dev: 37.0 us +- 0.2 us

### pickle_list ###
Mean +- std dev: 5.07 us +- 0.06 us

### pickle_pure_python ###
Mean +- std dev: 355 us +- 3 us

### pidigits ###
Mean +- std dev: 249 ms +- 0 ms

### pyflate ###
Mean +- std dev: 495 ms +- 4 ms

### python_startup ###
Mean +- std dev: 11.4 ms +- 0.1 ms

### python_startup_no_site ###
Mean +- std dev: 8.52 ms +- 0.06 ms

### raytrace ###
Mean +- std dev: 347 ms +- 4 ms

### regex_compile ###
Mean +- std dev: 157 ms +- 1 ms

### regex_dna ###
Mean +- std dev: 259 ms +- 1 ms

### regex_effbot ###
Mean +- std dev: 4.26 ms +- 0.01 ms

### regex_v8 ###
Mean +- std dev: 26.2 ms +- 0.1 ms

### richards ###
Mean +- std dev: 52.9 ms +- 1.2 ms

### scimark_fft ###
Mean +- std dev: 388 ms +- 7 ms

### scimark_lu ###
Mean +- std dev: 133 ms +- 2 ms

### scimark_monte_carlo ###
Mean +- std dev: 81.9 ms +- 1.0 ms

### scimark_sor ###
Mean +- std dev: 130 ms +- 2 ms

### scimark_sparse_mat_mult ###
Mean +- std dev: 4.87 ms +- 0.19 ms

### spectral_norm ###
Mean +- std dev: 118 ms +- 1 ms

### sqlalchemy_declarative ###
Mean +- std dev: 161 ms +- 3 ms

### sqlalchemy_imperative ###
Mean +- std dev: 20.9 ms +- 0.7 ms

### sqlite_synth ###
Mean +- std dev: 3.22 us +- 0.06 us

### sympy_expand ###
Mean +- std dev: 552 ms +- 3 ms

### sympy_integrate ###
Mean +- std dev: 24.8 ms +- 0.1 ms

### sympy_sum ###
Mean +- std dev: 200 ms +- 2 ms

### sympy_str ###
Mean +- std dev: 341 ms +- 4 ms

### telco ###
Mean +- std dev: 7.80 ms +- 0.14 ms

### tornado_http ###
Mean +- std dev: 146 ms +- 2 ms

### unpack_sequence ###
Mean +- std dev: 54.9 ns +- 0.6 ns

### unpickle ###
Mean +- std dev: 16.4 us +- 1.5 us

### unpickle_list ###
Mean +- std dev: 6.17 us +- 0.08 us

### unpickle_pure_python ###
Mean +- std dev: 247 us +- 1 us

### xml_etree_parse ###
Mean +- std dev: 181 ms +- 2 ms

### xml_etree_iterparse ###
Mean +- std dev: 126 ms +- 2 ms

### xml_etree_generate ###
Mean +- std dev: 94.1 ms +- 0.9 ms

### xml_etree_process ###
Mean +- std dev: 65.7 ms +- 1.1 ms
```

---

### Lazy Imports (disabled)

```
$ pyperformance run --python=~/cpython-lazy_imports-disabled/python -o ~/cpython-lazy_imports-disabled2.json
Python benchmark suite 1.0.5
...

$ pyperformance show ~/cpython-lazy_imports-disabled2.json

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-12 18:26:53.329769
End date: 2022-10-12 18:46:49.430035

### 2to3 ###
Mean +- std dev: 305 ms +- 1 ms

### chameleon ###
Mean +- std dev: 8.13 ms +- 0.17 ms

### chaos ###
Mean +- std dev: 81.8 ms +- 0.6 ms

### crypto_pyaes ###
Mean +- std dev: 91.2 ms +- 1.6 ms

### deltablue ###
Mean +- std dev: 4.06 ms +- 0.04 ms

### django_template ###
Mean +- std dev: 41.0 ms +- 0.4 ms

### dulwich_log ###
Mean +- std dev: 82.0 ms +- 0.7 ms

### fannkuch ###
Mean +- std dev: 464 ms +- 6 ms

### float ###
Mean +- std dev: 90.8 ms +- 1.1 ms

### genshi_text ###
Mean +- std dev: 27.4 ms +- 0.5 ms

### genshi_xml ###
Mean +- std dev: 62.6 ms +- 1.0 ms

### go ###
Mean +- std dev: 163 ms +- 1 ms

### hexiom ###
Mean +- std dev: 7.50 ms +- 0.08 ms

### html5lib ###
Mean +- std dev: 73.4 ms +- 3.1 ms

### json_dumps ###
Mean +- std dev: 11.7 ms +- 0.3 ms

### json_loads ###
Mean +- std dev: 29.8 us +- 1.1 us

### logging_format ###
Mean +- std dev: 8.42 us +- 0.09 us

### logging_silent ###
Mean +- std dev: 121 ns +- 3 ns

### logging_simple ###
Mean +- std dev: 7.67 us +- 0.08 us

### mako ###
Mean +- std dev: 12.7 ms +- 0.1 ms

### meteor_contest ###
Mean +- std dev: 128 ms +- 3 ms

### nbody ###
Mean +- std dev: 116 ms +- 2 ms

### nqueens ###
Mean +- std dev: 103 ms +- 1 ms

### pathlib ###
Mean +- std dev: 27.4 ms +- 0.6 ms

### pickle ###
Mean +- std dev: 12.5 us +- 0.1 us

### pickle_dict ###
Mean +- std dev: 40.5 us +- 0.2 us

### pickle_list ###
Mean +- std dev: 5.13 us +- 0.06 us

### pickle_pure_python ###
Mean +- std dev: 359 us +- 4 us

### pidigits ###
Mean +- std dev: 237 ms +- 0 ms

### pyflate ###
Mean +- std dev: 492 ms +- 4 ms

### python_startup ###
Mean +- std dev: 11.4 ms +- 0.1 ms

### python_startup_no_site ###
Mean +- std dev: 8.54 ms +- 0.06 ms

### raytrace ###
Mean +- std dev: 343 ms +- 1 ms

### regex_compile ###
Mean +- std dev: 159 ms +- 1 ms

### regex_dna ###
Mean +- std dev: 250 ms +- 1 ms

### regex_effbot ###
Mean +- std dev: 4.25 ms +- 0.02 ms

### regex_v8 ###
Mean +- std dev: 26.2 ms +- 0.3 ms

### richards ###
Mean +- std dev: 54.7 ms +- 1.3 ms

### scimark_fft ###
Mean +- std dev: 386 ms +- 3 ms

### scimark_lu ###
Mean +- std dev: 137 ms +- 3 ms

### scimark_monte_carlo ###
Mean +- std dev: 82.7 ms +- 1.3 ms

### scimark_sor ###
Mean +- std dev: 131 ms +- 2 ms

### scimark_sparse_mat_mult ###
Mean +- std dev: 5.07 ms +- 0.05 ms

### spectral_norm ###
Mean +- std dev: 117 ms +- 1 ms

### sqlalchemy_declarative ###
Mean +- std dev: 164 ms +- 3 ms

### sqlalchemy_imperative ###
Mean +- std dev: 21.0 ms +- 0.6 ms

### sqlite_synth ###
Mean +- std dev: 3.20 us +- 0.06 us

### sympy_expand ###
Mean +- std dev: 558 ms +- 4 ms

### sympy_integrate ###
Mean +- std dev: 24.8 ms +- 0.1 ms

### sympy_sum ###
Mean +- std dev: 202 ms +- 2 ms

### sympy_str ###
Mean +- std dev: 345 ms +- 3 ms

### telco ###
Mean +- std dev: 8.07 ms +- 0.17 ms

### tornado_http ###
Mean +- std dev: 144 ms +- 2 ms

### unpack_sequence ###
Mean +- std dev: 59.4 ns +- 0.9 ns

### unpickle ###
Mean +- std dev: 17.6 us +- 2.5 us

### unpickle_list ###
Mean +- std dev: 6.08 us +- 0.08 us

### unpickle_pure_python ###
Mean +- std dev: 253 us +- 2 us

### xml_etree_parse ###
Mean +- std dev: 183 ms +- 2 ms

### xml_etree_iterparse ###
Mean +- std dev: 126 ms +- 2 ms

### xml_etree_generate ###
Mean +- std dev: 93.8 ms +- 0.6 ms

### xml_etree_process ###
Mean +- std dev: 65.2 ms +- 0.6 ms
```

---

### Lazy Imports (enabled)

```
$ pyperformance run --python=~/cpython-lazy_imports-enabled/python -o ~/cpython-lazy_imports-enabled2.json
Python benchmark suite 1.0.5
...

$ pyperformance show ~/cpython-lazy_imports-enabled2.json

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-12 18:50:25.571026
End date: 2022-10-12 19:06:31.612342

### 2to3 ###
Mean +- std dev: 303 ms +- 2 ms

### chameleon ###
Mean +- std dev: 8.19 ms +- 0.10 ms

### chaos ###
Mean +- std dev: 83.0 ms +- 1.1 ms

### crypto_pyaes ###
Mean +- std dev: 93.2 ms +- 1.3 ms

### deltablue ###
Mean +- std dev: 4.15 ms +- 0.06 ms

### django_template ###
Mean +- std dev: 41.7 ms +- 0.5 ms

### dulwich_log ###
Mean +- std dev: 81.7 ms +- 0.6 ms

### fannkuch ###
Mean +- std dev: 465 ms +- 4 ms

### float ###
Mean +- std dev: 91.4 ms +- 1.2 ms

### go ###
Mean +- std dev: 171 ms +- 1 ms

### hexiom ###
Mean +- std dev: 7.71 ms +- 0.08 ms

### html5lib ###
Mean +- std dev: 74.3 ms +- 2.4 ms

### json_dumps ###
Mean +- std dev: 12.1 ms +- 0.1 ms

### json_loads ###
Mean +- std dev: 29.7 us +- 0.4 us

### logging_format ###
Mean +- std dev: 8.59 us +- 0.11 us

### logging_silent ###
Mean +- std dev: 119 ns +- 2 ns

### logging_simple ###
Mean +- std dev: 7.86 us +- 0.08 us

### mako ###
Mean +- std dev: 12.7 ms +- 0.2 ms

### meteor_contest ###
Mean +- std dev: 128 ms +- 1 ms

### nbody ###
Mean +- std dev: 115 ms +- 2 ms

### nqueens ###
Mean +- std dev: 99.7 ms +- 2.7 ms

### pathlib ###
Mean +- std dev: 27.8 ms +- 0.3 ms

### pickle ###
Mean +- std dev: 13.0 us +- 0.2 us

### pickle_dict ###
Mean +- std dev: 41.4 us +- 3.1 us

### pickle_list ###
Mean +- std dev: 5.24 us +- 0.05 us

### pickle_pure_python ###
Mean +- std dev: 357 us +- 2 us

### pidigits ###
Mean +- std dev: 243 ms +- 0 ms

### pyflate ###
Mean +- std dev: 507 ms +- 5 ms

### python_startup ###
Mean +- std dev: 11.5 ms +- 0.1 ms

### python_startup_no_site ###
Mean +- std dev: 8.63 ms +- 0.06 ms

### raytrace ###
Mean +- std dev: 356 ms +- 3 ms

### regex_compile ###
Mean +- std dev: 161 ms +- 1 ms

### regex_dna ###
Mean +- std dev: 256 ms +- 1 ms

### regex_effbot ###
Mean +- std dev: 4.44 ms +- 0.03 ms

### regex_v8 ###
Mean +- std dev: 26.9 ms +- 0.1 ms

### richards ###
Mean +- std dev: 54.8 ms +- 1.0 ms

### scimark_fft ###
Mean +- std dev: 389 ms +- 4 ms

### scimark_lu ###
Mean +- std dev: 137 ms +- 2 ms

### scimark_monte_carlo ###
Mean +- std dev: 82.4 ms +- 0.7 ms

### scimark_sor ###
Mean +- std dev: 129 ms +- 2 ms

### scimark_sparse_mat_mult ###
Mean +- std dev: 5.06 ms +- 0.09 ms

### spectral_norm ###
Mean +- std dev: 117 ms +- 1 ms

### sqlite_synth ###
Mean +- std dev: 3.24 us +- 0.05 us

### telco ###
Mean +- std dev: 7.88 ms +- 0.11 ms

### tornado_http ###
Mean +- std dev: 146 ms +- 2 ms

### unpack_sequence ###
Mean +- std dev: 54.0 ns +- 0.6 ns

### unpickle ###
Mean +- std dev: 16.4 us +- 0.1 us

### unpickle_list ###
Mean +- std dev: 6.32 us +- 0.06 us

### unpickle_pure_python ###
Mean +- std dev: 258 us +- 2 us

### xml_etree_parse ###
Mean +- std dev: 184 ms +- 2 ms

### xml_etree_iterparse ###
Mean +- std dev: 126 ms +- 2 ms

### xml_etree_generate ###
Mean +- std dev: 94.8 ms +- 0.4 ms

### xml_etree_process ###
Mean +- std dev: 66.1 ms +- 0.8 ms
```

---

## Results

### CPython Main vs. Lazy Imports (disabled)

```
$ pyperformance compare ~/cpython-main2.json ~/cpython-lazy_imports-disabled2.json -O table

cpython-main2.json
==================

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-12 18:02:56.879938
End date: 2022-10-12 18:23:09.986783

cpython-lazy_imports-disabled2.json
===================================

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-12 18:26:53.329769
End date: 2022-10-12 18:46:49.430035

+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| Benchmark               | cpython-main2.json | cpython-lazy_imports-disabled2.json | Change       | Significance            |
+=========================+====================+=====================================+==============+=========================+
| 2to3                    | 303 ms             | 305 ms                              | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| chameleon               | 8.06 ms            | 8.13 ms                             | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| chaos                   | 81.9 ms            | 81.8 ms                             | 1.00x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| crypto_pyaes            | 91.5 ms            | 91.2 ms                             | 1.00x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| deltablue               | 4.03 ms            | 4.06 ms                             | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| django_template         | 39.9 ms            | 41.0 ms                             | 1.03x slower | Significant (t=-10.70)  |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| dulwich_log             | 81.0 ms            | 82.0 ms                             | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| fannkuch                | 473 ms             | 464 ms                              | 1.02x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| float                   | 90.7 ms            | 90.8 ms                             | 1.00x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| genshi_text             | 26.2 ms            | 27.4 ms                             | 1.05x slower | Significant (t=-16.26)  |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| genshi_xml              | 61.8 ms            | 62.6 ms                             | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| go                      | 164 ms             | 163 ms                              | 1.00x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| hexiom                  | 7.51 ms            | 7.50 ms                             | 1.00x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| html5lib                | 73.6 ms            | 73.4 ms                             | 1.00x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| json_dumps              | 11.8 ms            | 11.7 ms                             | 1.01x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| json_loads              | 29.4 us            | 29.8 us                             | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| logging_format          | 8.46 us            | 8.42 us                             | 1.01x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| logging_silent          | 113 ns             | 121 ns                              | 1.07x slower | Significant (t=-20.37)  |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| logging_simple          | 7.66 us            | 7.67 us                             | 1.00x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| mako                    | 12.4 ms            | 12.7 ms                             | 1.03x slower | Significant (t=-26.61)  |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| meteor_contest          | 126 ms             | 128 ms                              | 1.02x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| nbody                   | 116 ms             | 116 ms                              | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| nqueens                 | 96.1 ms            | 103 ms                              | 1.07x slower | Significant (t=-34.66)  |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| pathlib                 | 27.4 ms            | 27.4 ms                             | 1.00x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| pickle                  | 12.4 us            | 12.5 us                             | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| pickle_dict             | 37.0 us            | 40.5 us                             | 1.09x slower | Significant (t=-115.51) |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| pickle_list             | 5.07 us            | 5.13 us                             | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| pickle_pure_python      | 355 us             | 359 us                              | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| pidigits                | 249 ms             | 237 ms                              | 1.05x faster | Significant (t=510.09)  |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| pyflate                 | 495 ms             | 492 ms                              | 1.01x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| python_startup          | 11.4 ms            | 11.4 ms                             | 1.00x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| python_startup_no_site  | 8.52 ms            | 8.54 ms                             | 1.00x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| raytrace                | 347 ms             | 343 ms                              | 1.01x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| regex_compile           | 157 ms             | 159 ms                              | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| regex_dna               | 259 ms             | 250 ms                              | 1.04x faster | Significant (t=51.26)   |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| regex_effbot            | 4.26 ms            | 4.25 ms                             | 1.00x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| regex_v8                | 26.2 ms            | 26.2 ms                             | 1.00x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| richards                | 52.9 ms            | 54.7 ms                             | 1.03x slower | Significant (t=-8.09)   |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| scimark_fft             | 388 ms             | 386 ms                              | 1.00x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| scimark_lu              | 133 ms             | 137 ms                              | 1.03x slower | Significant (t=-6.91)   |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| scimark_monte_carlo     | 81.9 ms            | 82.7 ms                             | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| scimark_sor             | 130 ms             | 131 ms                              | 1.00x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| scimark_sparse_mat_mult | 4.87 ms            | 5.07 ms                             | 1.04x slower | Significant (t=-7.51)   |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| spectral_norm           | 118 ms             | 117 ms                              | 1.01x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| sqlalchemy_declarative  | 161 ms             | 164 ms                              | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| sqlalchemy_imperative   | 20.9 ms            | 21.0 ms                             | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| sqlite_synth            | 3.22 us            | 3.20 us                             | 1.00x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| sympy_expand            | 552 ms             | 558 ms                              | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| sympy_integrate         | 24.8 ms            | 24.8 ms                             | 1.00x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| sympy_str               | 341 ms             | 345 ms                              | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| sympy_sum               | 200 ms             | 202 ms                              | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| telco                   | 7.80 ms            | 8.07 ms                             | 1.03x slower | Significant (t=-9.44)   |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| tornado_http            | 146 ms             | 144 ms                              | 1.01x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| unpack_sequence         | 54.9 ns            | 59.4 ns                             | 1.08x slower | Significant (t=-32.86)  |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| unpickle                | 16.4 us            | 17.6 us                             | 1.08x slower | Significant (t=-3.32)   |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| unpickle_list           | 6.17 us            | 6.08 us                             | 1.02x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| unpickle_pure_python    | 247 us             | 253 us                              | 1.03x slower | Significant (t=-19.20)  |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| xml_etree_generate      | 94.1 ms            | 93.8 ms                             | 1.00x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| xml_etree_iterparse     | 126 ms             | 126 ms                              | 1.00x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| xml_etree_parse         | 181 ms             | 183 ms                              | 1.01x slower | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
| xml_etree_process       | 65.7 ms            | 65.2 ms                             | 1.01x faster | Not significant         |
+-------------------------+--------------------+-------------------------------------+--------------+-------------------------+
```

---

```
$ pyperf compare_to ~/cpython-main2.json ~/cpython-lazy_imports-disabled2.json --table

+-------------------------+---------------+--------------------------------+
| Benchmark               | cpython-main2 | cpython-lazy_imports-disabled2 |
+=========================+===============+================================+
| 2to3                    | 303 ms        | 305 ms: 1.01x slower           |
+-------------------------+---------------+--------------------------------+
| chameleon               | 8.06 ms       | 8.13 ms: 1.01x slower          |
+-------------------------+---------------+--------------------------------+
| deltablue               | 4.03 ms       | 4.06 ms: 1.01x slower          |
+-------------------------+---------------+--------------------------------+
| django_template         | 39.9 ms       | 41.0 ms: 1.03x slower          |
+-------------------------+---------------+--------------------------------+
| dulwich_log             | 81.0 ms       | 82.0 ms: 1.01x slower          |
+-------------------------+---------------+--------------------------------+
| fannkuch                | 473 ms        | 464 ms: 1.02x faster           |
+-------------------------+---------------+--------------------------------+
| genshi_text             | 26.2 ms       | 27.4 ms: 1.05x slower          |
+-------------------------+---------------+--------------------------------+
| genshi_xml              | 61.8 ms       | 62.6 ms: 1.01x slower          |
+-------------------------+---------------+--------------------------------+
| json_dumps              | 11.8 ms       | 11.7 ms: 1.01x faster          |
+-------------------------+---------------+--------------------------------+
| json_loads              | 29.4 us       | 29.8 us: 1.01x slower          |
+-------------------------+---------------+--------------------------------+
| logging_format          | 8.46 us       | 8.42 us: 1.01x faster          |
+-------------------------+---------------+--------------------------------+
| logging_silent          | 113 ns        | 121 ns: 1.07x slower           |
+-------------------------+---------------+--------------------------------+
| mako                    | 12.4 ms       | 12.7 ms: 1.03x slower          |
+-------------------------+---------------+--------------------------------+
| meteor_contest          | 126 ms        | 128 ms: 1.02x slower           |
+-------------------------+---------------+--------------------------------+
| nbody                   | 116 ms        | 116 ms: 1.01x slower           |
+-------------------------+---------------+--------------------------------+
| nqueens                 | 96.1 ms       | 103 ms: 1.07x slower           |
+-------------------------+---------------+--------------------------------+
| pickle                  | 12.4 us       | 12.5 us: 1.01x slower          |
+-------------------------+---------------+--------------------------------+
| pickle_dict             | 37.0 us       | 40.5 us: 1.09x slower          |
+-------------------------+---------------+--------------------------------+
| pickle_list             | 5.07 us       | 5.13 us: 1.01x slower          |
+-------------------------+---------------+--------------------------------+
| pickle_pure_python      | 355 us        | 359 us: 1.01x slower           |
+-------------------------+---------------+--------------------------------+
| pidigits                | 249 ms        | 237 ms: 1.05x faster           |
+-------------------------+---------------+--------------------------------+
| pyflate                 | 495 ms        | 492 ms: 1.01x faster           |
+-------------------------+---------------+--------------------------------+
| python_startup          | 11.4 ms       | 11.4 ms: 1.00x slower          |
+-------------------------+---------------+--------------------------------+
| python_startup_no_site  | 8.52 ms       | 8.54 ms: 1.00x slower          |
+-------------------------+---------------+--------------------------------+
| raytrace                | 347 ms        | 343 ms: 1.01x faster           |
+-------------------------+---------------+--------------------------------+
| regex_compile           | 157 ms        | 159 ms: 1.01x slower           |
+-------------------------+---------------+--------------------------------+
| regex_dna               | 259 ms        | 250 ms: 1.04x faster           |
+-------------------------+---------------+--------------------------------+
| regex_effbot            | 4.26 ms       | 4.25 ms: 1.00x faster          |
+-------------------------+---------------+--------------------------------+
| richards                | 52.9 ms       | 54.7 ms: 1.03x slower          |
+-------------------------+---------------+--------------------------------+
| scimark_lu              | 133 ms        | 137 ms: 1.03x slower           |
+-------------------------+---------------+--------------------------------+
| scimark_monte_carlo     | 81.9 ms       | 82.7 ms: 1.01x slower          |
+-------------------------+---------------+--------------------------------+
| scimark_sparse_mat_mult | 4.87 ms       | 5.07 ms: 1.04x slower          |
+-------------------------+---------------+--------------------------------+
| spectral_norm           | 118 ms        | 117 ms: 1.01x faster           |
+-------------------------+---------------+--------------------------------+
| sqlalchemy_declarative  | 161 ms        | 164 ms: 1.01x slower           |
+-------------------------+---------------+--------------------------------+
| sympy_expand            | 552 ms        | 558 ms: 1.01x slower           |
+-------------------------+---------------+--------------------------------+
| sympy_sum               | 200 ms        | 202 ms: 1.01x slower           |
+-------------------------+---------------+--------------------------------+
| sympy_str               | 341 ms        | 345 ms: 1.01x slower           |
+-------------------------+---------------+--------------------------------+
| telco                   | 7.80 ms       | 8.07 ms: 1.03x slower          |
+-------------------------+---------------+--------------------------------+
| tornado_http            | 146 ms        | 144 ms: 1.01x faster           |
+-------------------------+---------------+--------------------------------+
| unpack_sequence         | 54.9 ns       | 59.4 ns: 1.08x slower          |
+-------------------------+---------------+--------------------------------+
| unpickle                | 16.4 us       | 17.6 us: 1.08x slower          |
+-------------------------+---------------+--------------------------------+
| unpickle_list           | 6.17 us       | 6.08 us: 1.02x faster          |
+-------------------------+---------------+--------------------------------+
| unpickle_pure_python    | 247 us        | 253 us: 1.03x slower           |
+-------------------------+---------------+--------------------------------+
| xml_etree_parse         | 181 ms        | 183 ms: 1.01x slower           |
+-------------------------+---------------+--------------------------------+
| xml_etree_generate      | 94.1 ms       | 93.8 ms: 1.00x faster          |
+-------------------------+---------------+--------------------------------+
| xml_etree_process       | 65.7 ms       | 65.2 ms: 1.01x faster          |
+-------------------------+---------------+--------------------------------+
| Geometric mean          | (ref)         | 1.01x slower                   |
+-------------------------+---------------+--------------------------------+

Benchmark hidden because not significant (15): chaos, crypto_pyaes, float, go, hexiom, html5lib, logging_simple, pathlib, regex_v8, scimark_fft, scimark_sor, sqlalchemy_imperative, sqlite_synth, sympy_integrate, xml_etree_iterparse
```

---

### CPython Main vs. Lazy Imports (enabled)

```
$ pyperformance compare ~/cpython-main2.json ~/cpython-lazy_imports-enabled2.json -O table

cpython-main2.json
==================

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-12 18:02:56.879938
End date: 2022-10-12 18:23:09.986783

cpython-lazy_imports-enabled2.json
==================================

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-12 18:50:25.571026
End date: 2022-10-12 19:06:31.612342

+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| Benchmark               | cpython-main2.json | cpython-lazy_imports-enabled2.json | Change       | Significance           |
+=========================+====================+====================================+==============+========================+
| 2to3                    | 303 ms             | 303 ms                             | 1.00x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| chameleon               | 8.06 ms            | 8.19 ms                            | 1.02x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| chaos                   | 81.9 ms            | 83.0 ms                            | 1.01x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| crypto_pyaes            | 91.5 ms            | 93.2 ms                            | 1.02x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| deltablue               | 4.03 ms            | 4.15 ms                            | 1.03x slower | Significant (t=-11.77) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| django_template         | 39.9 ms            | 41.7 ms                            | 1.05x slower | Significant (t=-16.87) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| dulwich_log             | 81.0 ms            | 81.7 ms                            | 1.01x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| fannkuch                | 473 ms             | 465 ms                             | 1.02x faster | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| float                   | 90.7 ms            | 91.4 ms                            | 1.01x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| go                      | 164 ms             | 171 ms                             | 1.04x slower | Significant (t=-29.21) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| hexiom                  | 7.51 ms            | 7.71 ms                            | 1.03x slower | Significant (t=-18.48) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| html5lib                | 73.6 ms            | 74.3 ms                            | 1.01x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| json_dumps              | 11.8 ms            | 12.1 ms                            | 1.02x slower | Significant (t=-12.72) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| json_loads              | 29.4 us            | 29.7 us                            | 1.01x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| logging_format          | 8.46 us            | 8.59 us                            | 1.02x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| logging_silent          | 113 ns             | 119 ns                             | 1.05x slower | Significant (t=-24.27) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| logging_simple          | 7.66 us            | 7.86 us                            | 1.03x slower | Significant (t=-15.32) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| mako                    | 12.4 ms            | 12.7 ms                            | 1.02x slower | Significant (t=-10.08) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| meteor_contest          | 126 ms             | 128 ms                             | 1.02x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| nbody                   | 116 ms             | 115 ms                             | 1.00x faster | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| nqueens                 | 96.1 ms            | 99.7 ms                            | 1.04x slower | Significant (t=-9.57)  |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| pathlib                 | 27.4 ms            | 27.8 ms                            | 1.01x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| pickle                  | 12.4 us            | 13.0 us                            | 1.05x slower | Significant (t=-16.82) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| pickle_dict             | 37.0 us            | 41.4 us                            | 1.12x slower | Significant (t=-10.64) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| pickle_list             | 5.07 us            | 5.24 us                            | 1.03x slower | Significant (t=-16.96) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| pickle_pure_python      | 355 us             | 357 us                             | 1.01x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| pidigits                | 249 ms             | 243 ms                             | 1.02x faster | Significant (t=314.71) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| pyflate                 | 495 ms             | 507 ms                             | 1.02x slower | Significant (t=-14.52) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| python_startup          | 11.4 ms            | 11.5 ms                            | 1.01x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| python_startup_no_site  | 8.52 ms            | 8.63 ms                            | 1.01x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| raytrace                | 347 ms             | 356 ms                             | 1.03x slower | Significant (t=-14.85) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| regex_compile           | 157 ms             | 161 ms                             | 1.02x slower | Significant (t=-24.09) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| regex_dna               | 259 ms             | 256 ms                             | 1.01x faster | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| regex_effbot            | 4.26 ms            | 4.44 ms                            | 1.04x slower | Significant (t=-38.18) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| regex_v8                | 26.2 ms            | 26.9 ms                            | 1.02x slower | Significant (t=-35.22) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| richards                | 52.9 ms            | 54.8 ms                            | 1.04x slower | Significant (t=-9.83)  |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| scimark_fft             | 388 ms             | 389 ms                             | 1.00x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| scimark_lu              | 133 ms             | 137 ms                             | 1.03x slower | Significant (t=-8.65)  |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| scimark_monte_carlo     | 81.9 ms            | 82.4 ms                            | 1.01x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| scimark_sor             | 130 ms             | 129 ms                             | 1.01x faster | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| scimark_sparse_mat_mult | 4.87 ms            | 5.06 ms                            | 1.04x slower | Significant (t=-6.61)  |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| spectral_norm           | 118 ms             | 117 ms                             | 1.00x faster | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| sqlite_synth            | 3.22 us            | 3.24 us                            | 1.01x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| telco                   | 7.80 ms            | 7.88 ms                            | 1.01x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| tornado_http            | 146 ms             | 146 ms                             | 1.00x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| unpack_sequence         | 54.9 ns            | 54.0 ns                            | 1.02x faster | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| unpickle                | 16.4 us            | 16.4 us                            | 1.00x faster | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| unpickle_list           | 6.17 us            | 6.32 us                            | 1.02x slower | Significant (t=-10.85) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| unpickle_pure_python    | 247 us             | 258 us                             | 1.04x slower | Significant (t=-37.80) |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| xml_etree_generate      | 94.1 ms            | 94.8 ms                            | 1.01x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| xml_etree_iterparse     | 126 ms             | 126 ms                             | 1.00x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| xml_etree_parse         | 181 ms             | 184 ms                             | 1.02x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+
| xml_etree_process       | 65.7 ms            | 66.1 ms                            | 1.01x slower | Not significant        |
+-------------------------+--------------------+------------------------------------+--------------+------------------------+

Skipped 8 benchmarks only in cpython-main2.json: genshi_text, genshi_xml, sqlalchemy_declarative, sqlalchemy_imperative, sympy_expand, sympy_integrate, sympy_str, sympy_sum
```

---

```
$ pyperf compare_to ~/cpython-main2.json ~/cpython-lazy_imports-enabled2.json --table

+-------------------------+---------------+-------------------------------+
| Benchmark               | cpython-main2 | cpython-lazy_imports-enabled2 |
+=========================+===============+===============================+
| chameleon               | 8.06 ms       | 8.19 ms: 1.02x slower         |
+-------------------------+---------------+-------------------------------+
| chaos                   | 81.9 ms       | 83.0 ms: 1.01x slower         |
+-------------------------+---------------+-------------------------------+
| crypto_pyaes            | 91.5 ms       | 93.2 ms: 1.02x slower         |
+-------------------------+---------------+-------------------------------+
| deltablue               | 4.03 ms       | 4.15 ms: 1.03x slower         |
+-------------------------+---------------+-------------------------------+
| django_template         | 39.9 ms       | 41.7 ms: 1.05x slower         |
+-------------------------+---------------+-------------------------------+
| dulwich_log             | 81.0 ms       | 81.7 ms: 1.01x slower         |
+-------------------------+---------------+-------------------------------+
| fannkuch                | 473 ms        | 465 ms: 1.02x faster          |
+-------------------------+---------------+-------------------------------+
| float                   | 90.7 ms       | 91.4 ms: 1.01x slower         |
+-------------------------+---------------+-------------------------------+
| go                      | 164 ms        | 171 ms: 1.04x slower          |
+-------------------------+---------------+-------------------------------+
| hexiom                  | 7.51 ms       | 7.71 ms: 1.03x slower         |
+-------------------------+---------------+-------------------------------+
| json_dumps              | 11.8 ms       | 12.1 ms: 1.02x slower         |
+-------------------------+---------------+-------------------------------+
| json_loads              | 29.4 us       | 29.7 us: 1.01x slower         |
+-------------------------+---------------+-------------------------------+
| logging_format          | 8.46 us       | 8.59 us: 1.02x slower         |
+-------------------------+---------------+-------------------------------+
| logging_silent          | 113 ns        | 119 ns: 1.05x slower          |
+-------------------------+---------------+-------------------------------+
| logging_simple          | 7.66 us       | 7.86 us: 1.03x slower         |
+-------------------------+---------------+-------------------------------+
| mako                    | 12.4 ms       | 12.7 ms: 1.02x slower         |
+-------------------------+---------------+-------------------------------+
| meteor_contest          | 126 ms        | 128 ms: 1.02x slower          |
+-------------------------+---------------+-------------------------------+
| nqueens                 | 96.1 ms       | 99.7 ms: 1.04x slower         |
+-------------------------+---------------+-------------------------------+
| pathlib                 | 27.4 ms       | 27.8 ms: 1.01x slower         |
+-------------------------+---------------+-------------------------------+
| pickle                  | 12.4 us       | 13.0 us: 1.05x slower         |
+-------------------------+---------------+-------------------------------+
| pickle_dict             | 37.0 us       | 41.4 us: 1.12x slower         |
+-------------------------+---------------+-------------------------------+
| pickle_list             | 5.07 us       | 5.24 us: 1.03x slower         |
+-------------------------+---------------+-------------------------------+
| pickle_pure_python      | 355 us        | 357 us: 1.01x slower          |
+-------------------------+---------------+-------------------------------+
| pidigits                | 249 ms        | 243 ms: 1.02x faster          |
+-------------------------+---------------+-------------------------------+
| pyflate                 | 495 ms        | 507 ms: 1.02x slower          |
+-------------------------+---------------+-------------------------------+
| python_startup          | 11.4 ms       | 11.5 ms: 1.01x slower         |
+-------------------------+---------------+-------------------------------+
| python_startup_no_site  | 8.52 ms       | 8.63 ms: 1.01x slower         |
+-------------------------+---------------+-------------------------------+
| raytrace                | 347 ms        | 356 ms: 1.03x slower          |
+-------------------------+---------------+-------------------------------+
| regex_compile           | 157 ms        | 161 ms: 1.02x slower          |
+-------------------------+---------------+-------------------------------+
| regex_dna               | 259 ms        | 256 ms: 1.01x faster          |
+-------------------------+---------------+-------------------------------+
| regex_effbot            | 4.26 ms       | 4.44 ms: 1.04x slower         |
+-------------------------+---------------+-------------------------------+
| regex_v8                | 26.2 ms       | 26.9 ms: 1.02x slower         |
+-------------------------+---------------+-------------------------------+
| richards                | 52.9 ms       | 54.8 ms: 1.04x slower         |
+-------------------------+---------------+-------------------------------+
| scimark_lu              | 133 ms        | 137 ms: 1.03x slower          |
+-------------------------+---------------+-------------------------------+
| scimark_monte_carlo     | 81.9 ms       | 82.4 ms: 1.01x slower         |
+-------------------------+---------------+-------------------------------+
| scimark_sor             | 130 ms        | 129 ms: 1.01x faster          |
+-------------------------+---------------+-------------------------------+
| scimark_sparse_mat_mult | 4.87 ms       | 5.06 ms: 1.04x slower         |
+-------------------------+---------------+-------------------------------+
| spectral_norm           | 118 ms        | 117 ms: 1.00x faster          |
+-------------------------+---------------+-------------------------------+
| sqlite_synth            | 3.22 us       | 3.24 us: 1.01x slower         |
+-------------------------+---------------+-------------------------------+
| telco                   | 7.80 ms       | 7.88 ms: 1.01x slower         |
+-------------------------+---------------+-------------------------------+
| unpack_sequence         | 54.9 ns       | 54.0 ns: 1.02x faster         |
+-------------------------+---------------+-------------------------------+
| unpickle_list           | 6.17 us       | 6.32 us: 1.02x slower         |
+-------------------------+---------------+-------------------------------+
| unpickle_pure_python    | 247 us        | 258 us: 1.04x slower          |
+-------------------------+---------------+-------------------------------+
| xml_etree_parse         | 181 ms        | 184 ms: 1.02x slower          |
+-------------------------+---------------+-------------------------------+
| xml_etree_generate      | 94.1 ms       | 94.8 ms: 1.01x slower         |
+-------------------------+---------------+-------------------------------+
| Geometric mean          | (ref)         | 1.02x slower                  |
+-------------------------+---------------+-------------------------------+

Benchmark hidden because not significant (8): 2to3, html5lib, nbody, scimark_fft, tornado_http, unpickle, xml_etree_iterparse, xml_etree_process
Ignored benchmarks (8) of /home/kronuz/cpython-main2.json: genshi_text, genshi_xml, sqlalchemy_declarative, sqlalchemy_imperative, sympy_expand, sympy_integrate, sympy_str, sympy_sum
```

---

### Lazy Imports (disabled) vs. Lazy Imports (enabled)

```
$ pyperformance compare ~/cpython-lazy_imports-disabled2.json ~/cpython-lazy_imports-enabled2.json -O table

cpython-lazy_imports-disabled2.json
===================================

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-12 18:26:53.329769
End date: 2022-10-12 18:46:49.430035

cpython-lazy_imports-enabled2.json
==================================

Performance version: 1.0.5
Report on Linux-5.15.0-1020-aws-x86_64-with-glibc2.31
Number of logical CPUs: 72
Start date: 2022-10-12 18:50:25.571026
End date: 2022-10-12 19:06:31.612342

+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| Benchmark               | cpython-lazy_imports-disabled2.json | cpython-lazy_imports-enabled2.json | Change       | Significance            |
+=========================+=====================================+====================================+==============+=========================+
| 2to3                    | 305 ms                              | 303 ms                             | 1.00x faster | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| chameleon               | 8.13 ms                             | 8.19 ms                            | 1.01x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| chaos                   | 81.8 ms                             | 83.0 ms                            | 1.01x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| crypto_pyaes            | 91.2 ms                             | 93.2 ms                            | 1.02x slower | Significant (t=-7.25)   |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| deltablue               | 4.06 ms                             | 4.15 ms                            | 1.02x slower | Significant (t=-9.40)   |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| django_template         | 41.0 ms                             | 41.7 ms                            | 1.02x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| dulwich_log             | 82.0 ms                             | 81.7 ms                            | 1.00x faster | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| fannkuch                | 464 ms                              | 465 ms                             | 1.00x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| float                   | 90.8 ms                             | 91.4 ms                            | 1.01x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| go                      | 163 ms                              | 171 ms                             | 1.05x slower | Significant (t=-32.00)  |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| hexiom                  | 7.50 ms                             | 7.71 ms                            | 1.03x slower | Significant (t=-14.79)  |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| html5lib                | 73.4 ms                             | 74.3 ms                            | 1.01x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| json_dumps              | 11.7 ms                             | 12.1 ms                            | 1.04x slower | Significant (t=-11.10)  |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| json_loads              | 29.8 us                             | 29.7 us                            | 1.00x faster | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| logging_format          | 8.42 us                             | 8.59 us                            | 1.02x slower | Significant (t=-9.65)   |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| logging_silent          | 121 ns                              | 119 ns                             | 1.02x faster | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| logging_simple          | 7.67 us                             | 7.86 us                            | 1.03x slower | Significant (t=-13.08)  |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| mako                    | 12.7 ms                             | 12.7 ms                            | 1.01x faster | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| meteor_contest          | 128 ms                              | 128 ms                             | 1.00x faster | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| nbody                   | 116 ms                              | 115 ms                             | 1.01x faster | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| nqueens                 | 103 ms                              | 99.7 ms                            | 1.03x faster | Significant (t=8.76)    |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| pathlib                 | 27.4 ms                             | 27.8 ms                            | 1.01x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| pickle                  | 12.5 us                             | 13.0 us                            | 1.04x slower | Significant (t=-14.65)  |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| pickle_dict             | 40.5 us                             | 41.4 us                            | 1.02x slower | Significant (t=-2.22)   |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| pickle_list             | 5.13 us                             | 5.24 us                            | 1.02x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| pickle_pure_python      | 359 us                              | 357 us                             | 1.01x faster | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| pidigits                | 237 ms                              | 243 ms                             | 1.02x slower | Significant (t=-224.13) |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| pyflate                 | 492 ms                              | 507 ms                             | 1.03x slower | Significant (t=-19.30)  |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| python_startup          | 11.4 ms                             | 11.5 ms                            | 1.01x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| python_startup_no_site  | 8.54 ms                             | 8.63 ms                            | 1.01x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| raytrace                | 343 ms                              | 356 ms                             | 1.04x slower | Significant (t=-33.29)  |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| regex_compile           | 159 ms                              | 161 ms                             | 1.01x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| regex_dna               | 250 ms                              | 256 ms                             | 1.03x slower | Significant (t=-25.99)  |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| regex_effbot            | 4.25 ms                             | 4.44 ms                            | 1.05x slower | Significant (t=-35.40)  |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| regex_v8                | 26.2 ms                             | 26.9 ms                            | 1.03x slower | Significant (t=-15.21)  |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| richards                | 54.7 ms                             | 54.8 ms                            | 1.00x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| scimark_fft             | 386 ms                              | 389 ms                             | 1.01x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| scimark_lu              | 137 ms                              | 137 ms                             | 1.00x faster | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| scimark_monte_carlo     | 82.7 ms                             | 82.4 ms                            | 1.00x faster | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| scimark_sor             | 131 ms                              | 129 ms                             | 1.01x faster | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| scimark_sparse_mat_mult | 5.07 ms                             | 5.06 ms                            | 1.00x faster | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| spectral_norm           | 117 ms                              | 117 ms                             | 1.00x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| sqlite_synth            | 3.20 us                             | 3.24 us                            | 1.01x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| telco                   | 8.07 ms                             | 7.88 ms                            | 1.02x faster | Significant (t=7.11)    |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| tornado_http            | 144 ms                              | 146 ms                             | 1.01x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| unpack_sequence         | 59.4 ns                             | 54.0 ns                            | 1.10x faster | Significant (t=39.88)   |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| unpickle                | 17.6 us                             | 16.4 us                            | 1.08x faster | Significant (t=3.87)    |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| unpickle_list           | 6.08 us                             | 6.32 us                            | 1.04x slower | Significant (t=-18.56)  |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| unpickle_pure_python    | 253 us                              | 258 us                             | 1.02x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| xml_etree_generate      | 93.8 ms                             | 94.8 ms                            | 1.01x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| xml_etree_iterparse     | 126 ms                              | 126 ms                             | 1.00x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| xml_etree_parse         | 183 ms                              | 184 ms                             | 1.01x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+
| xml_etree_process       | 65.2 ms                             | 66.1 ms                            | 1.01x slower | Not significant         |
+-------------------------+-------------------------------------+------------------------------------+--------------+-------------------------+

Skipped 8 benchmarks only in cpython-lazy_imports-disabled2.json: genshi_text, genshi_xml, sqlalchemy_declarative, sqlalchemy_imperative, sympy_expand, sympy_integrate, sympy_str, sympy_sum
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
