#!/usr/local/bin/perl -w

$file = 'structs.dat';
open (FILE, "<$file") || die "Can't open $file!";
@structs = <FILE>;
chop(@structs);
close FILE;

print "Content-type: text/html\n\n";
print "<html><head><title>Boolean Spaces, Properties and Structures</title></head><body>\n";
print "<center><h2>Yes/No Structure Selection</h2></center>\n";
print "<form action=http://www.umanitoba.ca/cgi-bin/math/bell/structssolns.cgi method=post>\n";
print "<center><input type=submit value=SUBMIT>
<a href = http://home.cc.umanitoba.ca/~mbell/instructions.html>&nbsp;Instructions </a> ||
<a href = http://home.cc.umanitoba.ca/~mbell/revisions.html> Revision 1.4 </a> ||
<a href= mailto:mbell\@cc.umanitoba.ca> Comments?&nbsp;</a>
<input type=reset value=RESET>
</center>\n";
print "<center><a href=http://www.umanitoba.ca/cgi-bin/math/bell/props.cgi>
Properties </a> ||
<a href=http://home.cc.umanitoba.ca/~mbell/help.html> Definitions </a> ||
<a href=http://home.cc.umanitoba.ca/~mbell/lists.html> Lists</a>
</center>\n";

print "<br><center><table border=1 cellspacing=1>\n";
for ($k=0; $k<=16; ++$k) {
  print "<tr>\n";
  for ($j=0; $j<=4; ++$j) {
    $i=$k+17*$j;
    if ($i<=$#structs) {
      if ($structs[$i] ne '            ') {
        print "<td><input type=radio name=$i value=1><input type=radio name=$i value=0></td><td bgcolor=beige>$structs[$i]</td>";
      }
      else {
        print "<td>&nbsp;</td><td>&nbsp;</td>";
      }
    }
  }
  print "</tr>\n";
}
print "</table></center>";

print "<br><center><input type=submit value=SUBMIT></center>";
print "</form>\n";
print "</body></html>\n";
exit;
