#!/usr/local/bin/perl -w

$file = 'structs.dat';
open (FILE, "<$file") || die "Can't open $file!";
@structs = <FILE>;
chop(@structs);

$file = 'props.dat';
open (FILE, "<$file") || die "Can't open $file!";
@props = <FILE>;
chop(@props);

$file = 'bopbits.dat';
open (FILE, "<$file") || die "Can't open $file!";
@opbits = <FILE>;

close FILE;

print "Pragma: no-cache\n";
print "Content-type: text/html\n\n";
print "<html><head><title>StructsProps Gaps</title></head><body bgcolor=\"AAAAAA\">\n";
print "<center><font size=+1><a href=http://home.cc.umanitoba.ca/~mbell/lists.html>
Return To Lists </a></font></center>\n";
print "<center><h2>Unknown Structure Property Bits</h2></center>\n";
print "<dl>\n";
for ($k=0; $k<=$#structs; ++$k) {
  if ($structs[$k] ne '            ') {
    $x=0;
    for ($j=0; $j<=$#props; ++$j) {
      if ($props[$j] ne '            ') {
        $v=ord(substr($opbits[$k],$j,1))-48;
        if ($x==0 && $v<3) {$x=1}
        if ($x==1) {print "<dt><font color=#000000><b>$structs[$k]</b></font>\n<dd>";$x=2}
        if ($v==0) {print "<font color=#ff0000> $props[$j] "}
        if ($v==1) {print "<font color=#0000ff> $props[$j] "}
        if ($v==2) {print "<font color=#00ff00> $props[$j] "}
      }
    }  
  }
}
print "\n</dl>\n";
print "<center><font size=+1><a href=http://home.cc.umanitoba.ca/~mbell/lists.html>
Return To Lists </a></font></center>\n";
print "</body></html>\n";
exit;
