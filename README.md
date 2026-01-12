dice-roller
===========

Simple console program for dice rolling.


Installing and running the program
----------------------------------

### Installation

```shell
make install
```

Above command builds and installs the program.

### Rolling the dice

```
$ roll --help
usage: roll [-s] [-S] [-h] [-V] ROLL [ROLL ...] [-r REPS [REPS ...]]

Simple dice rolling program.

rolling options:
  ROLL                  dice roll to be made, accepted patterns are:
                        	- NdM+|-X - where N represents the number of rolls, M the number of dice sides and X is the natural number to add | subtract from the throw result, eg. 1d20+5
                        	- NkM+|-X - N, M and X like above, eg. 1k12-2
  -r, --reps, --repetitions REPS [REPS ...]
                        the number of times to repeat a corresponding dice roll,
                        eg. typing "roll 1k20 3k6 -r 3 4" would result in 3 throws of 1k20 roll and 4 throws of 3k6 roll
  -s, --show-rolls      shows subsequence rolls
  -S, --show-statistics
                        shows roll statistics like minimal, maximum and average possible throw results

other:
  -h, --help            print this help message and exit
  -V, --version         print program version and exit

Copyright (C) 2023-2026 _kodokami
```

Example usages:

```
$ roll 1k20+4
1k20+4 - 23

$ roll -S 1k20+4
1k20+4 - 16
[MIN: 5, MAX: 24, AVG: 15]

$ roll -Ss 4k6
4k6 - 10 | Rolls: 6, 1, 1, 2
[MIN: 4, MAX: 24, AVG: 14]

$ roll -sS 1k20+3 3k6 -r 1 3
1k20+3 - 19 | Rolls: 16
[MIN: 4, MAX: 23, AVG: 14]
3k6 - 10 | Rolls: 4, 4, 2
3k6 - 6 | Rolls: 1, 1, 4
3k6 - 17 | Rolls: 5, 6, 6
[MIN: 3, MAX: 18, AVG: 11]
```

### Uninstalling the dice-roller

```shell
make uninstall
```

This command removes the program from system. Alternatively one could use the
`pip uninstall dice-roller` command.


---
Copyright (C) 2023-2026 _kodokami
