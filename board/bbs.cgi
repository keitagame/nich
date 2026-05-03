#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use Encode qw(encode decode);

my $q = CGI->new;

# パラメータ（UTF-8 で来るので decode）
my $bbs  = decode('UTF-8', $q->param('bbs'));
my $key  = decode('UTF-8', $q->param('key'));
my $name = decode('UTF-8', $q->param('FROM') || '名無しさん');
my $mail = decode('UTF-8', $q->param('mail') || '');
my $body = decode('UTF-8', $q->param('MESSAGE') || '');

# 絶対パス
my $dir = "/var/www/html/$bbs";
my $dat = "$dir/dat/$key.dat";

# dat が無い
if (!-e $dat) {
    print "Content-Type: text/html; charset=Shift_JIS\n\n";
    print encode('cp932', "<html><body>スレッドがありません。</body></html>");
    exit;
}

# dat 読み込み（Shift_JIS）
open my $fh, "<:encoding(cp932)", $dat or die "Cannot open dat: $!";
my @lines = <$fh>;
close $fh;

my $no = scalar(@lines) + 1;

# 日付 + ID
my @t = localtime();
my $time = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",
    $t[5]+1900, $t[4]+1, $t[3],
    (qw(日 月 火 水 木 金 土))[$t[6]],
    $t[2], $t[1], $t[0]
);

my $ip = $ENV{'REMOTE_ADDR'} || "0.0.0.0";
my $id = substr( unpack("H*", pack("C*", split(/\./, $ip))), 0, 8 );
my $timecol = "$time ID:$id";

# タイトル
my @c = split(/<>/, $lines[0]);
my $title = $c[5];

# 新規レス行（Shift_JIS に変換して書く）
my $newline = join("<>",
    $no,
    $name,
    $mail,
    $timecol,
    $body,
    $title,
    ""
) . "\n";

# dat 追記（Shift_JIS）
open my $fh2, ">>:encoding(cp932)", $dat or die "Cannot write dat: $!";
print $fh2 encode('cp932', decode('UTF-8', $newline));
close $fh2;

# subject.txt 更新
my $subject = "$dir/subject.txt";
my @subjects;

if (-e $subject) {
    open my $sfh, "<:encoding(cp932)", $subject;
    @subjects = <$sfh>;
    close $sfh;
}

# レス数更新
my @newsubjects;
foreach my $line (@subjects) {
    if ($line =~ /^$key\.dat<>\Q$title\E/) {
        push @newsubjects, encode('cp932', "$key.dat<>$title ($no)\n");
    } else {
        push @newsubjects, $line;
    }
}

# 書き戻し
open my $sfh2, ">:encoding(cp932)", $subject;
print $sfh2 @newsubjects;
close $sfh2;

# レスポンス（Shift_JIS）
print "Content-Type: text/html; charset=Shift_JIS\n\n";
print encode('cp932', <<'HTML');
<html>
<head><title>書きこみました。</title></head>
<body>書きこみました。</body>
</html>
HTML
