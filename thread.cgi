#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use Encode qw(encode decode);

my $q = CGI->new;

my $bbs   = $q->param('bbs');
my $title = $q->param('title');
my $name  = $q->param('FROM') || '名無しさん';
my $mail  = $q->param('mail') || '';
my $body  = $q->param('MESSAGE') || '';

# 必須チェック
if (!$bbs || !$title || !$body) {
    print "Content-Type: text/html; charset=UTF-8\n\n";
    print "<html><body>入力が不足しています。</body></html>";
    exit;
}

# 絶対パス
my $dir = "/var/www/html/$bbs";
my $datdir = "$dir/dat";

# dat ディレクトリが無ければ作成
mkdir $datdir if !-d $datdir;

# 新規スレ key（UNIX time）
my $key = time();

my $dat = "$datdir/$key.dat";

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

# dat の 1 行目（スレ主）
my $firstline = join("<>",
    1,
    $name,
    $mail,
    $timecol,
    $body,
    $title,
    ""
) . "\n";

# dat 作成
open my $fh, ">:encoding(UTF-8)", $dat or die "Cannot write dat: $!";
print $fh $firstline;
close $fh;

# subject.txt 更新
my $subject = "$dir/subject.txt";
open my $sfh, ">>:encoding(UTF-8)", $subject or die "Cannot write subject: $!";
print $sfh "$key.dat<>$title (1)\n";
close $sfh;

# レスポンス
print "Content-Type: text/html; charset=UTF-8\n\n";
print <<"HTML";
<html>
<head><title>スレ立て完了</title></head>
<body>
スレッドを作成しました。<br>
<a href="/thread.html?bbs=$bbs&key=$key">スレを開く</a>
</body>
</html>
HTML
