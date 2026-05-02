<?php
$dir = __DIR__ . '/board';

$thread = $_POST['key'] ?? '';
$name   = $_POST['FROM'] ?? '名無しさん';
$mail   = $_POST['mail'] ?? '';
$body   = $_POST['MESSAGE'] ?? '';

if (!$thread || !$body) {
    echo "error\n";
    exit;
}

$file = $dir . '/' . basename($thread) . '.dat';
if (!file_exists($file)) {
    echo "error\n";
    exit;
}

$posts = file($file, FILE_IGNORE_NEW_LINES);
$no = count($posts) + 1;

$time = date('Y/m/d(D) H:i:s');
$id = substr(sha1($_SERVER['REMOTE_ADDR'] . date('Ymd')), 0, 8);
$timeCol = $time . " ID:" . $id;

// 1行目からタイトル取得
$cols = explode('<>', $posts[0]);
$title = $cols[5] ?? '無題';

$line = implode('<>', [
    $no,
    $name,
    $mail,
    $timeCol,
    $body,
    $title,
    ''
]);

$posts[] = $line;

$data = implode("\n", $posts) . "\n";
$data = mb_convert_encoding($data, 'SJIS-win', 'UTF-8');

file_put_contents($file, $data);

echo "書きこみました\n";
