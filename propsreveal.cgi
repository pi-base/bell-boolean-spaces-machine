#!/usr/local/bin/perl -w

read (STDIN, $q, $ENV{'CONTENT_LENGTH'});
@pairs = split(/&/, $q);
foreach $k (@pairs) {
  ($a, $b) = split(/=/, $k);
  if ($a eq 'space') {
    $spacenum=$b;
  }
  else {
    $hash{$a}=$b;
  }  
}

@keys=keys(%hash);
@values=values(%hash);

$file = 'colors.dat';
open (FILE, "<$file") || die "Can't open $file!";
@colors = <FILE>;
chop(@colors);

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
print "<html><head><title>Space Bits</title></head>\n";
print "<BODY bgcolor=\"AAAAAA\">";
print "<br><center><h2>$spaces[$spacenum]</h2></center>\n";
for ($k=0; $k<=$#props; ++$k) {
  $v=ord(substr($psbits[$k],$spacenum,1))-48;
  if ($v>7) {$v=7}
  $w=$colors[$v];
  print "<font color=$w>$props[$k]\n";
}
print "<hr>\n";
print "<form action=http://www.umanitoba.ca/cgi-bin/math/bell/propssolns.cgi method=post>\n";
print "<center><input type=submit value=\"Back To Solutions\"></center>\n";
for ($k=0; $k<=$#keys; ++$k) {
  if ($values[$k]==1) {
    print "<input type=hidden name=$keys[$k] value=1>\n";
  }
  elsif ($values[$k]==0) {
    print "<input type=hidden name=$keys[$k] value=0>\n";
  }
}  
print "</form>\n";
print "<form action=http://www.umanitoba.ca/cgi-bin/math/bell/props.cgi method=post>\n";
print "<center><input type=submit value=\"Back To Properties\"></center>\n";
print "</form>\n";
print "<form action=http://www.umanitoba.ca/cgi-bin/math/bell/structs.cgi method=post>\n";
print "<center><input type=submit value=\"Structure Selection\"></center>\n";
print "</form>\n";

if ($spacenum==$#spaces) {$next=0} else {$next=$spacenum+1}
if ($spacenum==0) {$prev=$#spaces} else {$prev=$spacenum-1}
print "<form action=http://www.umanitoba.ca/cgi-bin/math/bell/propsreveal.cgi method=post>\n";
print "<center><input type=submit value=\"Next Space\"></center>\n";
print "<input type=hidden name=space value=$next>\n";
for ($k=0; $k<=$#keys; ++$k) {
  if ($values[$k]==1) {
    print "<input type=hidden name=$keys[$k] value=1>\n";
  }
  elsif ($values[$k]==0) {
    print "<input type=hidden name=$keys[$k] value=0>\n";
  }
}  
print "</form>\n";

print "<form action=http://www.umanitoba.ca/cgi-bin/math/bell/propsreveal.cgi method=post>\n";
print "<center><input type=submit value=\"Previous Space\"></center>\n";
print "<input type=hidden name=space value=$prev>\n";
for ($k=0; $k<=$#keys; ++$k) {
  if ($values[$k]==1) {
    print "<input type=hidden name=$keys[$k] value=1>\n";
  }
  elsif ($values[$k]==0) {
    print "<input type=hidden name=$keys[$k] value=0>\n";
  }
}  
print "</form>\n";
print "</body></html>\n";
exit;
