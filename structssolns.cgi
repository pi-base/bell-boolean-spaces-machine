#!/usr/local/bin/perl -w

$cmd='/usr/lib/sendmail';
read (STDIN, $q, $ENV{'CONTENT_LENGTH'});
@pairs = split(/&/, $q);
foreach $k (@pairs) {
  ($a, $b) = split(/=/, $k);
  $hash{$a}=$b;
}

@keys=keys(%hash);
@values=values(%hash);

$file = 'props.dat';
open (FILE, "<$file") || die "Can't open $file!";
@props = <FILE>;
chop(@props);

$file = 'structs.dat';
open (FILE, "<$file") || die "Can't open $file!";
@structs = <FILE>;
chop(@structs);

$file = 'bopbits.dat';
open (FILE, "<$file") || die "Can't open $file!";
@opbits = <FILE>;

$file = 'doobits.dat';
open (FILE, "<$file") || die "Can't open $file!";
@doobits = <FILE>;

close FILE;

&send_mail;
sub send_mail {
  open(MAIL,"|$cmd -t");
  print MAIL "To: mbell\@cc.umanitoba.ca \n";
  print MAIL "From: Machine \n";
  print MAIL "Subject: Structure Choice \n\n";
  
  print MAIL "REMOTE_HOST :     $ENV{'REMOTE_HOST'}\n";
  print MAIL "REMOTE_ADDRESS :  $ENV{'REMOTE_ADDR'}\n";
  print MAIL "HTTP_USER_AGENT : $ENV{'HTTP_USER_AGENT'}\n";
  print MAIL "************************************** \n"; 
  $k=0;
  while ($k<=$#keys) {
    $a=$values[$k];$b=$structs[$keys[$k]];
    if ($a==1) {
      print MAIL "$b \n";
    }
    elsif ($a==0) {
      print MAIL "NOT($b) \n";
    }
    ++$k;  
  } 
  close (MAIL);
}

PARSE:

$k=$return=0;
while ($k<=$#keys && $return==0) {
  $a=$values[$k];$c=$structs[$keys[$k]];
  $j=$k+1;
  while ($j<=$#keys && $return==0) {
    $b=$values[$j];$d=$structs[$keys[$j]];
    $x=substr($doobits[$keys[$k]],$keys[$j],1);
    if ($a==1 && $b==1 && $x==2) {
      $return=1;
      $comment="Contradiction!<br> $c implies NOT($d).\n";
    }
    elsif ($a==1 && $b==1 && $x==3) {
      $return=1;
      $comment="Redundancy!<br> $c implies $d.\n";
    }
    elsif ($a==1 && $b==1 && $x==4) {
      $return=1;
      $comment="Redundancy!<br> $d implies $c.\n";
    }
    if ($a==0 && $b==0 && $x==5) {
      $return=1;
      $comment="Contradiction!<br> NOT($c) implies $d.\n";
    }
    elsif ($a==0 && $b==0 && $x==4) {
      $return=1;
      $comment="Redundancy!<br> NOT($c) implies NOT($d).\n";
    }
    elsif ($a==0 && $b==0 && $x==3) {
      $return=1;
      $comment="Redundancy!<br> NOT($d) implies NOT($c).\n";
    }
    if ($a==0 && $b==1 && $x==4) {
      $return=1;
      $comment="Contradiction!<br> $d implies $c.\n";
    }
    elsif ($a==0 && $b==1 && $x==2) {
      $return=1;
      $comment="Redundancy!<br> $d implies NOT($c).\n";
    }
    elsif ($a==0 && $b==1 && $x==5) {
      $return=1;
      $comment="Redundancy!<br> NOT($c) implies $d.\n";
    }
    if ($a==1 && $b==0 && $x==3) {
      $return=1;
      $comment="Contradiction!<br> $c implies $d.\n";
    }
    elsif ($a==1 && $b==0 && $x==2) {
      $return=1;
      $comment="Redundancy!<br> $c implies NOT($d).\n";
    }
    elsif ($a==1 && $b==0 && $x==5) {
      $return=1;
      $comment="Redundancy!<br> NOT($d) implies $c.\n";
    }
    ++$j;
  }
  ++$k;
}

if ($return==1) {goto HTML}

$base[0]=$maybeglobal=0;
for ($k=0;$k<=$#props;++$k) {
  if ($props[$k] eq '            ') {
    $solns[$k]=3;
    next;
  }
  $maybe=$stop=$j=0;
  while ($j<=$#keys && $stop==0) {
    $v=ord(substr($opbits[$keys[$j]],$k,1))-48;
    if ($v<4) {$maybe=1}
    if (($v==4 || $v==6) && $values[$j]==0) {$solns[$k]=0;$stop=1}
    if (($v==5 || $v==7) && $values[$j]==1) {$solns[$k]=0;$stop=1}
    ++$j;
  }  
  if ($stop==0) {
    if ($maybe==1) {$solns[$k]=2; $maybeglobal=1}
    else {
      $solns[$k]=1;$base[0]=$base[0]+1;$base[$base[0]]=$k;
    }  
  }  
}  

COMMONPROPERTIES:

if ($base[0]>0) {
  for ($k=0;$k<=$#structs;++$k) {
    if ($structs[$k] eq "            ") {next}
    $stop=0;
    for ($j=0;$j<=$#keys;++$j) {
      $v=substr($doobits[$keys[$j]],$k,1);
      if ($values[$j]==1 && ($v==2 || $v==3 || $v==6)) {$stop=1;last}
      if ($values[$j]==0 && ($v==4 || $v==5 || $v==6)) {$stop=1;last}
    }
    if ($stop==1) {next}

    $n=$y=$m=$o=0;
    $i=1;
    while ($i<=$base[0] && $stop==0) {
      $v=ord(substr($opbits[$k],$base[$i],1))-48;
      if ($v==5 || $v==7) {$n=1}
      elsif ($v==4 || $v==6) {$y=1}
      elsif ($v==0) {$m=1}
      else {$o=1}
      if ($n==1 && $y==1) {$stop=1}
      ++$i;
    }
    if ($stop==0) {
      if ($n==1 && $m==1 && $o==0) {
        $ignore=$i=0;
        while ($ignore==0 && $i<=$#commonmaybeno) {
          $x=substr($doobits[$commonmaybeno[$i]],$k,1);
          if ($x==4) {$ignore=1}
          if ($x==3) {splice(@commonmaybeno,$i,1);redo if
          defined($commonmaybeno[$i])}
          ++$i;
        }
        $i=0;
        while ($ignore==0 && $i<=$#commonmaybeyes) {
          $x=substr($doobits[$commonmaybeyes[$i]],$k,1);
          if ($x==2) {$ignore=1}
          if ($x==5) {splice(@commonmaybeyes,$i,1);redo if
          defined($commonmaybeyes[$i])}
          ++$i;
        }
        if ($ignore==0) {push(@commonmaybeno,$k)}
      }  
      if ($y==1 && $m==1 && $o==0) {
        $ignore=$i=0;
        while ($ignore==0 && $i<=$#commonmaybeno) {
          $x=substr($doobits[$commonmaybeno[$i]],$k,1);
          if ($x==5) {$ignore=1}
          if ($x==2) {splice(@commonmaybeno,$i,1);redo if
          defined($commonmaybeno[$i])}
          ++$i;
        }
        $i=0;
        while ($ignore==0 && $i<=$#commonmaybeyes) {
          $x=substr($doobits[$commonmaybeyes[$i]],$k,1);
          if ($x==3) {$ignore=1}
          if ($x==4) {splice(@commonmaybeyes,$i,1);redo if
          defined($commonmaybeyes[$i])}
          ++$i;
        }
        if ($ignore==0) {push(@commonmaybeyes,$k)}
      }  
      if ($n+$y+$o==0) {push(@commonmaybemaybe, $k)}
      if ($y+$m+$o==0) {
        $ignore=$i=0;
        while ($ignore==0 && $i<=$#commonno) {
          $x=substr($doobits[$commonno[$i]],$k,1);
          if ($x==4) {$ignore=1}
          if ($x==3) {splice(@commonno,$i,1);redo if defined($commonno[$i])}
          ++$i;
        }
        $i=0;
        while ($ignore==0 && $i<=$#commonyes) {
          $x=substr($doobits[$commonyes[$i]],$k,1);
          if ($x==2) {$ignore=1}
          if ($x==5) {splice(@commonyes,$i,1);redo if defined($commonyes[$i])}
          ++$i;
        }
        if ($ignore==0) {push(@commonno,$k)}
      }  
      if ($n+$m+$o==0) {
        $ignore=$i=0;
        while ($ignore==0 && $i<=$#commonno) {
          $x=substr($doobits[$commonno[$i]],$k,1);
          if ($x==5) {$ignore=1}
          if ($x==2) {splice(@commonno,$i,1);redo if defined($commonno[$i])}
          ++$i;
        }
        $i=0;
        while ($ignore==0 && $i<=$#commonyes) {
          $x=substr($doobits[$commonyes[$i]],$k,1);
          if ($x==3) {$ignore=1}
          if ($x==4) {splice(@commonyes,$i,1);redo if defined($commonyes[$i])}
          ++$i;
        }
        if ($ignore==0) {push(@commonyes,$k)}
      }  
    }
  }
}

HTML:

print "Content-type: text/html\n\n";
print "<html><head><title>Solution Properties</title></head><body>\n";

print "<center><b><font size=+1>
<a href = http://www.umanitoba.ca/cgi-bin/math/bell/structs.cgi>Structure Selection</a>
<a href = http://www.umanitoba.ca/cgi-bin/math/bell/props.cgi>&nbsp;&nbsp;Property Selection</a>
</font></b></center>\n";

print "<b>\n";
for ($k=0; $k<=$#keys; ++$k) {
  if ($values[$k]==1) {$x=$structs[$keys[$k]];print "$x ";}
}  
print "<br>\n";
for ($k=0; $k<=$#keys; ++$k) {
  if ($values[$k]==0) {$x=$structs[$keys[$k]];print "Not&nbsp;($x) ";}
}
print "</b><hr>\n";

if ($return==1) {
  print "<center><h2>$comment";
  print "<br>Try again!!</h2></center>\n";
  print "<center><b><font size=+1>
  <a href = http://www.umanitoba.ca/cgi-bin/math/bell/structs.cgi>Structure Selection</a>
  </font></b></center>\n";
  print "</body></html>\n";
  exit;
}

if ($base[0]==0 && $maybeglobal==0) {
  print "<center><b>NO BASIC SOLUTIONS IN THE DATABASE!!</b></center>";
} 
else {
  print "<form action=http://www.umanitoba.ca/cgi-bin/math/bell/structsreveal.cgi method=post>\n";
  print "<br><center><table border=1 cellspacing=1>\n";
  for ($k=0; $k<=16; ++$k) {
    print "<tr>\n";  
    for ($j=0; $j<=5; ++$j) {
      $i=$k+17*$j;
      if ($i<=$#props) {
        if ($solns[$i]==1) {
          $x="<b>$props[$i]</b>";
        }
        elsif ($solns[$i]==2) {
          $x="<i>$props[$i]</i>";
        }
        else {
          $x='';
        }
        if ($i<10) {
          $y='0'.$i;
        }
        else {
          $y=$i;
        }             
        if ($x ne '') {
          print "<td><input type=submit name=property value=$y></td><td bgcolor=beige>$x</td>";
        }
        elsif ($solns[$i]==3) {
          print "<td>&nbsp;</td><td>&nbsp;</td>";          
        }  
        else {
          print "<td><input type=submit name=property value=$y></td><td>&nbsp;</td>";
        }
      }  
    }
    print "</tr>\n";
  }
  print "</table></center>";

  for ($k=0; $k<=$#keys; ++$k) {
    if ($values[$k]==1) {
      print "<input type=hidden name=$keys[$k] value=1>\n";
    }
    elsif ($values[$k]==0) {
      print "<input type=hidden name=$keys[$k] value=0>\n";
    }
  }
  print "</form>\n";
}

COMMON:

if ($#commonno>=0 || $#commonyes>=0 || $#commonmaybeyes>=0 || $#commonmaybeno>=0 || $#commonmaybemaybe>=0) {
  print "<center><b>COMMON STRUCTURES (NOT SINGLY DERIVABLE) TO ALL BASIC SOLUTIONS</b></center>\n";
  print "<br>";  
  for ($k=0;$k<=$#commonyes;++$k){
    print "$structs[$commonyes[$k]]  ";
  }  
  if (defined($commonyes[0])) {print "<br>\n"}
  for ($k=0;$k<=$#commonno;++$k){
    print "Not&nbsp;($structs[$commonno[$k]])  ";
  }
  if (defined($commonno[0])) {print "<br>\n"}
  for ($k=0;$k<=$#commonmaybeyes;++$k){
    print "<i>$structs[$commonmaybeyes[$k]]  </i>";
  }
  if (defined($commonmaybeyes[0])) {print "<br>\n"}
  for ($k=0;$k<=$#commonmaybeno;++$k){
    print "<i>Not&nbsp;($structs[$commonmaybeno[$k]])  </i>";
  }
  if (defined($commonmaybeno[0])) {print "<br>\n"}
  for ($k=0;$k<=$#commonmaybemaybe;++$k){
    print "<i>?($structs[$commonmaybemaybe[$k]])  </i>";
  }
  print "\n";
}
elsif ($base[0]>0) {
  print "<center><b>NO COMMON STRUCTURES (NOT SINGLY DERIVABLE) TO ALL BASIC SOLUTIONS!!</b></center>\n";
}
else {
}

print "<br><center><b><font size=+1>
<a href = http://www.umanitoba.ca/cgi-bin/math/bell/structs.cgi>Structure Selection</a>
<a href = http://www.umanitoba.ca/cgi-bin/math/bell/props.cgi>&nbsp;&nbsp;Property Selection</a>
</font></b></center>\n";

print "</body></html>\n";
exit;
