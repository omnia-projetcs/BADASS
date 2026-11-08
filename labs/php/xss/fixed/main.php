<?php
echo '<p>' . htmlspecialchars($argv[1], ENT_NOQUOTES | ENT_SUBSTITUTE, 'UTF-8') . '</p>';