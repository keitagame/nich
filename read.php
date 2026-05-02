<?php
$dir = __DIR__ . '/board';

$dat = $_GET['dat'] ?? '';
$file = $dir . '/' . basename($dat) . '.dat';

if (!file_exists($file)) {
    http_response_code(404);
    exit;
}

header('Content-Type: text/plain; charset=Shift_JIS');

$data = file_get_contents($file);
echo $data;
