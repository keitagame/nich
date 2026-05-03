#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use Encode qw(encode decode);

my $q = CGI->new;

# UTF-8 で受け取る
my $bbs  = $q->param('bbs');
my $key  = $q->param('key');
my $name = $q->param('FROM') || '名無しさん';
my $mail = $q->param('mail') || '';
my $body = $q->param('MESSAGE') || '';

# fcgiwrap は /usr/sbin から実行されるため絶対パス必須
my $dir = "/var/www/html/$bbs";
my $dat = "$dir/dat/$key.dat";

# dat が存在しない
if (!-e $dat) {
    print "Content-Type: text/html; charset=UTF-8\n\n";
    print "<html><body>スレッドがありません。</body></html>";
    exit;
}

# dat 読み込み（UTF-8）
open my $fh, "<:encoding(UTF-8)", $dat or die "Cannot open dat: $!";
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

# REMOTE_ADDR が無い場合もあるので保険
my $ip = $ENV{'REMOTE_ADDR'} || "0.0.0.0";
my $id = substr( unpack("H*", pack("C*", split(/\./, $ip))), 0, 8 );
my $timecol = "$time ID:$id";

# タイトル取得
my @c = split(/<>/, $lines[0]);
my $title = $c[5];

# 新規レス行（UTF-8）
my $newline = join("<>",
    $no,
    $name,
    $mail,
    $timecol,
    $body,
    $title,
    ""
) . "\n";

# dat 追記
open my $fh2, ">>:encoding(UTF-8)", $dat or die "Cannot write dat: $!";
print $fh2 $newline;
close $fh2;

# subject.txt 更新
my $subject = "$dir/subject.txt";
my @subjects;

if (-e $subject) {
    open my $sfh, "<:encoding(UTF-8)", $subject;
    @subjects = <$sfh>;
    close $sfh;
}

# レス数更新
my @newsubjects;
foreach my $line (@subjects) {
    if ($line =~ /^$key\.dat<>\Q$title\E/) {
        push @newsubjects, "$key.dat<>$title ($no)\n";
    } else {
        push @newsubjects, $line;
    }
}

# 書き戻し
open my $sfh2, ">:encoding(UTF-8)", $subject;
print $sfh2 @newsubjects;
close $sfh2;

# レスポンス（UTF-8）
print "Content-Type: text/html; charset=UTF-8\n\n";
print <<'HTML';
<html>
<head><title>書きこみました。</title></head>
<body>書きこみました。</body>
</html>
HTML
