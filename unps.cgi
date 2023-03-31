#!/usr/local/bin/perl -w

$file = 'spaces.dat';
open (FILE, "<$file") || die "Can't open $file!";
@spaces = <FILE>;
chop(@spaces);

$file = 'props.dat';
open (FILE, "<$file") || die "Can't open $file!";
@props = <FILE>;
chop(@props);

$file = 'bpsbits.dat';
open (FILE, "<$file") || die "Can't open $file!";
@psbits = <FILE>;

close FILE;

print "Pragma: no-cache\n";
print "Content-type: text/html\n\n";
print "<html><head><title>PropsSpaces Gaps</title></head><body bgcolor=\"AAAAAA\">\n";
print "<center><font size=+1><a href=http://home.cc.umanitoba.ca/~mbell/lists.html>
Return To Lists </a></font></center>\n";
print "<center><h2><b> Unknown Property Space Bits </b></h2></center>\n";
print "<dl>\n";
for ($k=0; $k<=$#props; ++$k) {
  if ($props[$k] ne '            ') {
    $x=0;
    for ($j=0; $j<=$#spaces; ++$j) {
      $v=ord(substr($psbits[$k],$j,1))-48;
      if ($x==0 && $v<3) {$x=1}
      if ($x==1) {print "<dt><font color=#000000><b>$props[$k]</b></font>\n<dd>";$x=2}
      if ($v==0) {print "<font color=#ff0000> $spaces[$j] "}
      if ($v==1) {print "<font color=#0000ff> $spaces[$j] "}
      if ($v==2) {print "<font color=#00ff00> $spaces[$j] "}
    }  
  }
}
print "\n</dl>\n";
print "<center><font size=+1><a href=http://home.cc.umanitoba.ca/~mbell/lists.html>
Return To Lists </a></font></center>\n";
print "</body></html>\n";
exit;
