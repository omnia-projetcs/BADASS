<?php
$proc = proc_open(['/usr/bin/printf', '%s', $argv[1]], [1 => ['pipe', 'w']], $pipes);
echo stream_get_contents($pipes[1]);
fclose($pipes[1]);
proc_close($proc);