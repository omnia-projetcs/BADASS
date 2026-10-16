<?php
echo $argv[1] === 'welcome.txt' ? file_get_contents('public/welcome.txt') : 'DENIED';