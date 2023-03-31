#!/usr/local/bin/perl -w

read (STDIN, $q, $ENV{'CONTENT_LENGTH'});
@pairs = split(/&/, $q);
foreach $k (@pairs) {
  ($a, $b) = split(/=/, $k);
  if ($a eq 'property') {
    $propnum=$b;
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
print "<html><head><title>Property Bits</title></head>\n";
print "<BODY bgcolor=\"AAAAAA\">";
print "<br><center><h2>$props[$propnum]</h2></center>\n";
for ($k=0; $k<=$#structs; ++$k) {
  $v=ord(substr($opbits[$k],$propnum,1))-48;
  if ($v==6) {$v=4}
  if ($v==7) {$v=5}
  $w=$colors[$v];
  print "<font color=$w>$structs[$k]\n";
}
print "<hr>\n";
print "<form action=http://www.umanitoba.ca/cgi-bin/math/bell/structssolns.cgi method=post>\n";
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
print "<form action=http://www.umanitoba.ca/cgi-bin/math/bell/structs.cgi method=post>\n";
print "<center><input type=submit value=\"Back To Structures\"></center>\n";
print "</form>\n";
print "<form action=http://www.umanitoba.ca/cgi-bin/math/bell/props.cgi method=post>\n";
print "<center><input type=submit value=\"Property Selection\"></center>\n";
print "</form>\n";

if ($propnum==$#props) {$next=0} else {$next=$propnum+1}
if ($propnum==0) {$prev=$#props} else {$prev=$propnum-1}
print "<form action=http://www.umanitoba.ca/cgi-bin/math/bell/structsreveal.cgi method=post>\n";
print "<center><input type=submit value=\"Next Property\"></center>\n";
print "<input type=hidden name=property value=$next>\n";
for ($k=0; $k<=$#keys; ++$k) {
  if ($values[$k]==1) {
    print "<input type=hidden name=$keys[$k] value=1>\n";
  }
  elsif ($values[$k]==0) {
    print "<input type=hidden name=$keys[$k] value=0>\n";
  }
}
print "</form>\n";

print "<form action=http://www.umanitoba.ca/cgi-bin/math/bell/structsreveal.cgi method=post>\n";
print "<center><input type=submit value=\"Previous Property\"></center>\n";
print "<input type=hidden name=property value=$prev>\n";
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
