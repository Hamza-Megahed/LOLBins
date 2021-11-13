---
description: |
  This is the `check_memory` Nagios plugin, available e.g. in `/usr/lib/nagios/plugins/`. The read file content is limited to the first line.
functions:
  file-read:
    - code: |
        LFILE=file_to_read
        check_memory --extra-opts=@$LFILE
  sudo:
    - code: |
        LFILE=file_to_read
        sudo check_memory --extra-opts=@$LFILE
---
