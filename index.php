<?php
$dir = __DIR__ . '/board';

header('Content-Type: text/plain; charset=Shift_JIS');

$files = glob($dir . '/*.dat');
$lines = [];

foreach ($files as $file) {
    $dat = basename($file);
    $posts = file($file, FILE_IGNORE_NEW_LINES);
    if (!$posts) continue;

    // 1行目からタイトル取得
    $cols = explode('<>', $posts[0]);
    $title = $cols[5] ?? '無題';
    $count = count($posts);

    $lines[] = $dat . '<>' . $title . " ($count)";
}

// 新しい順
rsort($lines);

echo mb_convert_encoding(implode("\n", $lines), 'SJIS-win', 'UTF-8');
