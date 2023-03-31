#!/usr/local/bin/perl -w

$cmd='/usr/lib/sendmail';
$q='0=1';
#read (STDIN, $q, $ENV{'CONTENT_LENGTH'});
@pairs = split(/&/, $q);
foreach $k (@pairs) {
  ($a, $b) = split(/=/, $k);
  $hash{$a}=$b;
}

@keys=keys(%hash);
@values=values(%hash);

$file = 'hr.dat';
open (FILE, "<$file") || die "Can't open $file!";
$hr = <FILE>;
chop($hr);

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

$file = 'bopbits.dat';
open (FILE, "<$file") || die "Can't open $file!";
@opbits = <FILE>;

$file = 'dssbits.dat';
open (FILE, "<$file") || die "Can't open $file!";
@dssbits = <FILE>;

close FILE;
&send_mail;

PREPARSE:

$k=$ret=0;
if ($#keys==-1) {
  $soln=$realsoln=1;
  for ($k=0;$k<=$#spaces;++$k) {$solns[$k]=1}
  goto HTML;
}
while ($k<=$#keys && $ret==0) {
  $a=$values[$k];$b=$props[$keys[$k]];
  $j=$k+1;
  while ($j<=$#keys && $ret==0) {
    $c=$values[$j];$d=$props[$keys[$j]];
    $x=ord(substr($dssbits[$keys[$k]],$keys[$j],1))-48;
    if ($a==1 && $c==1 && $x==2) {
      $ret=1;
      $comment="Contradiction!<br> $b implies
      NOT($d).\n";
    }
    elsif ($a==1 && $c==1 && ($x==3 || $x==15)) {
      $ret=1;
      $comment="Redundancy!<br> $b implies $d.\n";
    }
    elsif ($a==1 && $c==1 && ($x==4 || $x==14)) {
      $ret=1;
      $comment="Redundancy!<br> $d implies $b.\n";
    }
    if ($a==0 && $c==0 && $x==5) {
      $ret=1;
      $comment="Contradiction!<br> NOT($b) implies
      $d.\n";
    }
    elsif ($a==0 && $c==0 && ($x==4 || $x==14)) {
      $ret=1;
      $comment="Redundancy!<br> NOT($b) implies
      NOT($d).\n";
    }
    elsif ($a==0 && $c==0 && ($x==3 || $x==15)) {
      $ret=1;
      $comment="Redundancy!<br> NOT($d) implies
      NOT($b).\n";
    }
    if ($a==0 && $c==1 && ($x==4 || $x==14)) {
      $ret=1;
      $comment="Contradiction!<br> $d implies $b.\n";
    }
    elsif ($a==0 && $c==1 && $x==2) {
      $ret=1;
      $comment="Redundancy!<br> $d implies
      NOT($b).\n";
    }
    elsif ($a==0 && $c==1 && $x==5) {
      $ret=1;
      $comment="Redundancy!<br> NOT($b) implies $d.\n";
    }
    if ($a==1 && $c==0 && ($x==3 || $x==15)) {
      $ret=1;
      $comment="Contradiction!<br> $b implies $d.\n";
    }
    elsif ($a==1 && $c==0 && $x==2) {
      $ret=1;
      $comment="Redundancy!<br> $b implies
      NOT($d).\n";
    }
    elsif ($a==1 && $c==0 && $x==5) {
      $ret=1;
      $comment="Redundancy!<br> NOT($d) implies $b.\n";
    }
    ++$j;
  }
  ++$k;
}

if ($ret==1) {goto HTML}

$k=0;$succmul=1;
while ($k<=$#keys && $succmul==1) {
  $a=ord(substr($opbits[23],$keys[$k],1))-48;
  $b=ord(substr($opbits[49],$keys[$k],1))-48;
  $v=$values[$k];
  if ($v==1 && $a==6) {++$k;next}
  if ($v==1) {
    if ($a==4) {
      push(@kemul,$keys[$k]);
      push(@vamul,$v);
    }
    else {
      $succmul=0;
    }
  }
  if ($v==0 && $a==7) {++$k;next}
  if ($v==0) {
    if ($b==4) {
      push(@kemul,$keys[$k]);
      push(@vamul,$v);
    }
    else {
      $succmul=0;
    }
  }
  ++$k;
}

$k=0;$succadd=1;
while ($k<=$#keys && $succadd==1) {
  $a=ord(substr($opbits[24],$keys[$k],1))-48;
  $b=ord(substr($opbits[50],$keys[$k],1))-48;
  $v=$values[$k];
  if ($v==1 && $a==6) {++$k;next}
  if ($v==1) {
    if ($a==4) {
      push(@keadd,$keys[$k]);
      push(@vaadd,$v);
    }
    else {
      $succadd=0;
    }
  }
  if ($v==0 && $a==7) {++$k;next}
  if ($v==0) {
    if ($b==4) {
      push(@keadd,$keys[$k]);
      push(@vaadd,$v);
    }
    else {
      $succadd=0;
    }
  }
  ++$k
}

@xkeys=@keys;@xvalues=@values;
$flagmul=$flagadd=$solnmul=$solnadd=0;
$soln=$realsoln=$maybesoln=$extsolns=0;

SOLNS:

for ($k=0;$k<=$#spaces;++$k) {
  if (defined($solns[$k]) && $solns[$k] != 2 && $solns[$k] != 0) {next}
  $maybe=$stop=$j=0;
  $w=$gw=$lec=$gc=$gec=$lc=0;
  while ($j<=$#xkeys && $stop==0) {
    $v=ord(substr($psbits[$xkeys[$j]],$k,1))-48;
    if ($v<4) {$maybe=1}
    if ($v==4 && $xvalues[$j]==0) {$solns[$k]=0;$stop=1}
    if ($v==5 && $xvalues[$j]==1) {$solns[$k]=0;$stop=1}
    if ($v>6) {
      if ($v==7) {if ($xvalues[$j]==1) {$w=1} else {$gw=1}}
      if ($v==8) {if ($xvalues[$j]==1) {$lec=1} else {$gc=1}}
      if ($v==9 || $v==16) {if ($xvalues[$j]==1) {$gec=1} else {$lc=1}}
      if ($v==10) {if ($xvalues[$j]==1) {$w=1} else {$gc=1}}
      if ($v==11 || $v==15) {if ($xvalues[$j]==1) {$lc=1} else {$gec=1}}
      if ($v==12) {if ($xvalues[$j]==1) {$gc=1} else {$lec=1}}
      if ($v==13) {if ($xvalues[$j]==1) {$gc=1} else {$w=1}}
      if ($v==14) {if ($xvalues[$j]==1) {$gw=1} else {$w=1}}
      if ($w*($gw+$gc)>0) {$solns[$k]=0;$stop=1}
      if ($lc*$gec>0) {$solns[$k]=0;$stop=1}
      if ($gc*($lec+$lc)>0) {$solns[$k]=0;$stop=1}
      if ($lc>0) {$maybe=1}
      if ($w*$gec>0) {$maybe=1}
      if ($gw*$lec>0) {$maybe=1}
    }
    ++$j;
  }
  if ($stop==0) {
    if ($maybe==1 && $flagmul==0 && $flagadd==0) {$solns[$k]=2; $maybesoln=1}
    elsif ($maybe==0) {
      $tag[$k]=0;
      if ($flagmul==0 && $flagadd==0) {
        $solns[$k]=1;
        $soln=1;
        if ($k<$hr+1) {$realsoln=1}
      }
      elsif ($flagmul==1 && $flagadd==0) {
        if ($solns[$k]==2) {$solns[$k]=5}
        elsif ($solns[$k]==0) {$solns[$k]=7}
        else {$solns[$k]=3}
        $solnmul=1;
      }
      elsif ($flagadd==1) {
        if ($solns[$k]==2) {$solns[$k]=6}
        elsif ($solns[$k]==0) {$solns[$k]=8}
        else {$solns[$k]=4}
        $solnadd=1;
      }
      if ($w>0) {$tag[$k]=1}
      elsif ($gc>0) {$tag[$k]=6}
      elsif ($lec*$gec>0) {$tag[$k]=3}
      elsif ($gw*$gec>0) {$tag[$k]=6}
      elsif ($gw>0) {$tag[$k]=5}
      elsif ($lec>0) {$tag[$k]=2}
      elsif ($gec>0) {$tag[$k]=4}
    }
  }
}

if ($succmul==1 && $flagmul==0 && $soln==0 && $#kemul<$#keys) {
  @xkeys=@kemul;@xvalues=@vamul;$flagmul=1;
  goto SOLNS;
}
if ($succadd==1 && $flagadd==0 && $soln==0 && $solnmul==0 && $#keadd<$#keys) {
  @xkeys=@keadd;@xvalues=@vaadd;$flagadd=1;
  goto SOLNS;
}

COMMONPROPS:

if ($soln==1) {
  for ($k=0;$k<=$#props;++$k) {
    if ($props[$k] eq "            ") {next}
    $stop=0;
    for ($j=0;$j<=$#keys;++$j) {
      $v=ord(substr($dssbits[$keys[$j]],$k,1))-48;
      if ($values[$j]==1 && ($v==2 || $v==3 || $v==6 || $v==15)) {$stop=1;last}
      if ($values[$j]==0 && ($v==4 || $v==5 || $v==6 || $v==14)) {$stop=1;last}
    }
    if ($stop==1) {next}

    $n=$y=$m=$o=0;
    $i=0;
    while ($i<=$#spaces && $stop==0) {
      if ($solns[$i]==1) {
        $v=ord(substr($psbits[$k],$i,1))-48;
        if ($v==0) {$m=1}
        elsif ($v==4) {$y=1}
        elsif ($v==5) {$n=1}
        elsif ($v==7) {
          if ($tag[$i]==1) {$y=1}
          elsif ($tag[$i]>4) {$n=1}
          else {$stop=1}
        }
        elsif ($v==8) {
          if ($tag[$i]>0 && $tag[$i]<4) {$y=1}
          elsif ($tag[$i]==6) {$n=1}
          else {$stop=1}
        }
        elsif ($v==9 || $v==16) {
          if ($tag[$i]>2 && $tag[$i] != 5) {$y=1}
          else {$stop=1}
        }
        elsif ($v==10) {
          if ($tag[$i]==1) {$y=1}
          elsif ($tag[$i]==6) {$n=1}
          else {$stop=1}
        }
        elsif ($v==11 || $v==15) {
          if ($tag[$i]>2 && $tag[$i] != 5) {$n=1}
          else {$stop=1}
        }
        elsif ($v==12) {
          if ($tag[$i]==6) {$y=1}
          elsif ($tag[$i]>0 && $tag[$i]<4) {$n=1}
          else {$stop=1}
        }
        elsif ($v==13) {
          if ($tag[$i]==6) {$y=1}
          elsif ($tag[$i]==1) {$n=1}
          else {$stop=1}
        }
        elsif ($v==14) {
          if ($tag[$i]>4) {$y=1}
          elsif ($tag[$i]==1) {$n=1}
          else {$stop=1}
        }
        else {$o=1}
      }
      if ($n==1 && $y==1) {$stop=1}
      ++$i;
    }

COMMONPROPSREDUCTION:

    if ($stop==0) {
      if ($n==1 && $m==1 && $o==0) {
        $ignore=$i=0;
        while ($ignore==0 && $i<=$#commonmaybeno) {
          $x=ord(substr($dssbits[$commonmaybeno[$i]],$k,1))-48;
          if ($x==4 || $x==14) {$ignore=1}
          if ($x==3 || $x==15) {splice(@commonmaybeno,$i,1);redo if
          defined($commonmaybeno[$i])}
          ++$i;
        }
        $i=0;
        while ($ignore==0 && $i<=$#commonmaybeyes) {
          $x=ord(substr($dssbits[$commonmaybeyes[$i]],$k,1))-48;
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
          $x=ord(substr($dssbits[$commonmaybeno[$i]],$k,1))-48;
          if ($x==5) {$ignore=1}
          if ($x==2) {splice(@commonmaybeno,$i,1);redo if
          defined($commonmaybeno[$i])}
          ++$i;
        }
        $i=0;
        while ($ignore==0 && $i<=$#commonmaybeyes) {
          $x=ord(substr($dssbits[$commonmaybeyes[$i]],$k,1))-48;
          if ($x==3 || $x==15) {$ignore=1}
          if ($x==4 || $x==14) {splice(@commonmaybeyes,$i,1);redo if
          defined($commonmaybeyes[$i])}
          ++$i;
        }
        if ($ignore==0) {push(@commonmaybeyes,$k)}
      }
      if ($n+$y+$o==0) {push(@commonmaybemaybe, $k)}
      if ($y+$m+$o==0 && $n==1) {
        $ignore=$i=0;
        while ($ignore==0 && $i<=$#commonno) {
          $x=ord(substr($dssbits[$commonno[$i]],$k,1))-48;
          if ($x==4 || $x==14) {$ignore=1}
          if ($x==3 || $x==15) {splice(@commonno,$i,1);redo if defined($commonno[$i])}
          ++$i;
        }
        $i=0;
        while ($ignore==0 && $i<=$#commonyes) {
          $x=ord(substr($dssbits[$commonyes[$i]],$k,1))-48;
          if ($x==2) {$ignore=1}
          if ($x==5) {splice(@commonyes,$i,1);redo if defined($commonyes[$i])}
          ++$i;
        }
        if ($ignore==0) {push(@commonno,$k)}
      }
      if ($n+$m+$o==0 && $y==1) {
        $ignore=$i=0;
        while ($ignore==0 && $i<=$#commonno) {
          $x=ord(substr($dssbits[$commonno[$i]],$k,1))-48;
          if ($x==5) {$ignore=1}
          if ($x==2) {splice(@commonno,$i,1);redo if defined($commonno[$i])}
          ++$i;
        }
        $i=0;
        while ($ignore==0 && $i<=$#commonyes) {
          $x=ord(substr($dssbits[$commonyes[$i]],$k,1))-48;
          if ($x==3 || $x==15) {$ignore=1}
          if ($x==4 || $x==14) {splice(@commonyes,$i,1);redo if defined($commonyes[$i])}
          ++$i;
        }
        if ($ignore==0) {push(@commonyes,$k)}
      }
    }
  }
  if ($succmul==1) {
    $i=0;
    while ($i<=$#commonyes) {
      if (ord(substr($opbits[23],$commonyes[$i],1))==55) {
      splice(@commonyes,$i,1);redo if defined($commonyes[$i])}
      ++$i;
    }
    $i=0;
    while ($i<=$#commonmaybeyes) {
      if (ord(substr($opbits[23],$commonmaybeyes[$i],1))==55) {
      splice(@commonmaybeyes,$i,1);redo if defined($commonmaybeyes[$i])}
      ++$i;
    }
    $i=0;
    while ($i<=$#commonno) {
      if (ord(substr($opbits[23],$commonno[$i],1))==54) {
      splice(@commonno,$i,1);redo if defined($commonno[$i])}
      ++$i;
    }
    $i=0;
    while ($i<=$#commonmaybeno) {
      if (ord(substr($opbits[23],$commonmaybeno[$i],1))==54) {
      splice(@commonmaybeno,$i,1);redo if defined($commonmaybeno[$i])}
      ++$i;
    }
    $i=0;
    while ($i<=$#commonmaybemaybe) {
      if (ord(substr($opbits[23],$commonmaybemaybe[$i],1))==55) {
        push(@commonmaybeno,$commonmaybemaybe[$i]);
        splice(@commonmaybemaybe,$i,1);
        redo if defined($commonmaybemaybe[$i]);
      }
      ++$i;
    }
    $i=0;
    while ($i<=$#commonmaybemaybe) {
      if (ord(substr($opbits[23],$commonmaybemaybe[$i],1))==54) {
        push(@commonmaybeyes,$commonmaybemaybe[$i]);
        splice(@commonmaybemaybe,$i,1);
        redo if defined($commonmaybemaybe[$i]);
      }
      ++$i;
    }
  }
  if ($succadd==1) {
    $i=0;
    while ($i<=$#commonyes) {
      if (ord(substr($opbits[24],$commonyes[$i],1))==55) {
      splice(@commonyes,$i,1);redo if defined($commonyes[$i])}
      ++$i;
    }
    $i=0;
    while ($i<=$#commonmaybeyes) {
      if (ord(substr($opbits[24],$commonmaybeyes[$i],1))==55) {
      splice(@commonmaybeyes,$i,1);redo if defined($commonmaybeyes[$i])}
      ++$i;
    }
    $i=0;
    while ($i<=$#commonno) {
      if (ord(substr($opbits[24],$commonno[$i],1))==54) {
      splice(@commonno,$i,1);redo if defined($commonno[$i])}
      ++$i;
    }
    $i=0;
    while ($i<=$#commonmaybeno) {
      if (ord(substr($opbits[24],$commonmaybeno[$i],1))==54) {
      splice(@commonmaybeno,$i,1);redo if defined($commonmaybeno[$i])}
      ++$i;
    }
    $i=0;
    while ($i<=$#commonmaybemaybe) {
      if (ord(substr($opbits[24],$commonmaybemaybe[$i],1))==55) {
        push(@commonmaybeno,$commonmaybemaybe[$i]);
        splice(@commonmaybemaybe,$i,1);
        redo if defined($commonmaybemaybe[$i]);
      }
      ++$i;
    }
    $i=0;
    while ($i<=$#commonmaybemaybe) {
      if (ord(substr($opbits[24],$commonmaybemaybe[$i],1))==54) {
        push(@commonmaybeyes,$commonmaybemaybe[$i]);
        splice(@commonmaybemaybe,$i,1);
        redo if defined($commonmaybemaybe[$i]);
      }
      ++$i;
    }
  }
}

HTML:

print "Content-type: text/html\n\n";
print "<html><head><title>Solution Spaces</title></head><body>\n";

print "<center><b><font size=+1>
<a href = http://www.umanitoba.ca/cgi-bin/math/bell/props.cgi>Property Selection</a>
<a href = http://www.umanitoba.ca/cgi-bin/math/bell/structs.cgi>&nbsp;&nbsp;Structure Selection</a>
</font></b></center>\n";

print "<b>\n";
for ($k=0; $k<=$#keys; ++$k) {
  if ($values[$k]==1) {$x=$props[$keys[$k]];print "$x ";}
}
print "<br>\n";
for ($k=0; $k<=$#keys; ++$k) {
  if ($values[$k]==0) {$x=$props[$keys[$k]];print "Not&nbsp;($x) ";}
}
print "</b><hr>\n";

if ($ret==1) {
  print "<center><h2>$comment";
  print "<br>Try Again!!</h2></center>\n";
  print "<center><b><font size=+1>
  <a href = http://www.umanitoba.ca/cgi-bin/math/bell/props.cgi>Property Selection</a>
  </font></b></center>\n";
  print "</body></html>\n";
  exit;
}

if ($soln==0 && $maybesoln==0) {
  print "<center><b>NO BASIC SOLUTIONS IN THE DATABASE!</b></center>";
}
else {
  print "<form action=http://www.umanitoba.ca/cgi-bin/math/bell/propsreveal.cgi method=post>\n";
  print "<br><table align=center border=1 cellspacing=1>\n";

#  $cnt=0;
#  for ($i=0; $i<144; ++$i) {
#    if ($i<=$#spaces && ($solns[$i]==1 || $solns[$i]==2)) {
#      if ($cnt%5==0) {print "<tr>"}
#      if ($solns[$i]==1) {$x="<b>$spaces[$i]</b>"}
#      if ($solns[$i]==2) {$x="<i>$spaces[$i]</i>"}
#      if ($i<10) {$y='00'.$i} elsif ($i<100) {$y='0'.$i} else {$y=$i}
#      print "<td><input type=submit name=space value=$y></td><td bgcolor=beige>$x</td>";
#      ++$cnt;
#      if ($cnt%5==0) {print "</tr>\n"}
#    }
#  }
#  if ($cnt%5!=0) {print "</tr>\n"}

  for ($k=0; $k<=25; ++$k) {
    print "<tr>\n";  
    for ($j=0; $j<=4; ++$j) {
      $i=$k+26*$j;
      if ($i<=$#spaces) {
        if ($solns[$i]==1) {
          $x="<b>$spaces[$i]</b>";
        }
        elsif ($solns[$i]==2) {
          $x="<i>$spaces[$i]</i>";
        }
        else {
          $x='';
        }
        if ($i<10) {
          $y='00'.$i;
        }
        elsif ($i<100) {
          $y='0'.$i;
        }  
        else {
          $y=$i;
        }             
        if ($x ne '') {
          print "<td><input type=submit name=space value=$y></td><td bgcolor=beige>$x</td>";
        }
        elsif ($solns[$i]==3) {
          print "<td>&nbsp;</td><td>&nbsp;</td>";          
        }  
        else {
          print "<td><input type=submit name=space value=$y></td><td>&nbsp;</td>";
        }
      }  
    }
    print "</tr>\n";
  }
  
  print "</table>";

  for ($k=0; $k<=$#keys; ++$k) {
    if ($values[$k]==1) {
      print "<input type=hidden name=$keys[$k] value=1>\n";
    }
    elsif ($values[$k]==0) {
      print "<input type=hidden name=$keys[$k] value=0>\n";
    }
  }
  print "</form>\n";

  if ($soln==0) {
    print "<center><b>NOT CLEAR WHETHER THESE ARE SOLUTIONS!</b></center>\n";
  }
  else {
    if ($realsoln==0) {
      print "<center><b>NO ZFC BASIC SOLUTIONS IN THE DATABASE!</b></center>\n";
    }
  }
}

SOLNSMULADD:

if ($soln==0 && $solnmul==1) {
  $halt=0;$k=0;
  while ($k<=$#spaces && $halt==0) {
    if ($solns[$k]==3 || $solns[$k]==5 ||$solns[$k]==7) {$halt=1;$it=$k}
    ++$k
  }
  print "<center>Here's a Solution!</center>\n";
  print "<center><b>$spaces[$it] x 2^W</b></center>\n";
}
if ($soln==0 && $solnmul==0 && $solnadd==1) {
  $halt=0;$k=0;
  while ($k<=$#spaces && $halt==0) {
    if ($solns[$k]==4 || $solns[$k]==6 ||$solns[$k]==8)  {$halt=1;$it=$k}
    ++$k
  }
  print "<center>Here's a Solution!</center>\n";
  print "<center><b>$spaces[$it] + 1</b></center>\n";
}

EXTPARSE:

if ($soln==1 || ($solnmul==0 && $solnadd==0)) {
  $k=$killsum=$killprod=0;
  while ($k<=$#keys && ($killsum * $killprod == 0)) {
    if ($values[$k]==1) {
      $x=substr($opbits[20],$keys[$k],1);
      $y=substr($opbits[29],$keys[$k],1);
      $a=substr($opbits[15],$keys[$k],1);
      $b=substr($opbits[11],$keys[$k],1);
      if ($x!=4) {$killsum=1}
      elsif ($y==4) {push(@yessum2,$keys[$k])}
      else {push(@yessum1,$keys[$k])}
      if ($a!=4) {$killprod=1}
      elsif ($b==4) {push(@yesprod2,$keys[$k])}
      else {push(@yesprod1,$keys[$k])}
    }
    elsif ($values[$k]==0) {
      $x=substr($opbits[46],$keys[$k],1);
      $y=substr($opbits[3],$keys[$k],1);
      $a=substr($opbits[41],$keys[$k],1);
      $b=substr($opbits[37],$keys[$k],1);
      if ($x!=4) {$killsum=1}
      elsif ($y==4) {push(@nosum2,$keys[$k])}
      else {push(@nosum1,$keys[$k])}
      if ($a!=4) {$killprod=1}
      elsif ($b==4) {push(@noprod2,$keys[$k])}
      else {push(@noprod1,$keys[$k])}
    }
    ++$k;
  }
}
else {
  goto FINITO
}

if ($#yessum2 + $#nosum2 < -1) {$killsum=1}
if ($#yesprod2 + $#noprod2 < -1) {$killprod=1}

EXTSOLNS:

$extsolns=0;
for ($ext=0;$ext<=1;++$ext) {
  $killflag=0;$unreal=0;$unrealid=-1;
  if ($ext==0) {
    if ($killsum==1) {next}
    @yes1=@yessum1;
    @yes2=@yessum2;
    @no1=@nosum1;
    @no2=@nosum2;
    $add=29;$sum=20;$onesum=46;$twosum=3;
    $insert="SUM";$conn="&nbsp;&nbsp;+&nbsp;&nbsp;";
  }
  else {
    if ($killprod==1) {last}
    @yes1=@yesprod1;
    @yes2=@yesprod2;
    @no1=@noprod1;
    @no2=@noprod2;
    $add=11;$sum=15;$onesum=41;$twosum=37;
    $insert="PRODUCT";$conn="&nbsp;&nbsp;x&nbsp;&nbsp;";
  }

  @solns=();
  @yessolns=();
  @nosolns=();
  $core=$solns[0]=0;
  for ($k=0;$k<=$#spaces;++$k) {
    $stop=$j=0;
    $w=$gw=$lec=$gc=$gec=$lc=0;
    while ($j<=$#yes1 && $stop==0) {
      $v=ord(substr($psbits[$yes1[$j]],$k,1))-48;
      if ($v<4 || $v==5) {$stop=1}
      if ($v>6) {
        if ($v==7) {$w=1}
        if ($v==8) {$lec=1}
        if ($v==9) {$gec=1}
        if ($v==10) {$w=1}
        if ($v==11) {$lc=1}
        if ($v==12) {$gc=1}
        if ($v==13) {$gc=1}
        if ($v==14) {$gw=1}
        if ($v==15) {$lc=1}
        if ($v==16) {$gec=1}
        if ($lc>0) {$stop=1}
        if ($w*($gw+$gc+$gec)>0) {$stop=1}
        if ($lec*($gw+$gc)>0) {$stop=1}
      }
      ++$j;
    }
    if ($stop==0) {
      $j=0;
      while ($j<=$#no1 && $stop==0) {
        $v=ord(substr($psbits[$no1[$j]],$k,1))-48;
        if ($v<5) {$stop=1}
        if ($v>6) {
          if ($v==7) {$gw=1}
          if ($v==8) {$gc=1}
          if ($v==9) {$lc=1}
          if ($v==10) {$gc=1}
          if ($v==11) {$gec=1}
          if ($v==12) {$lec=1}
          if ($v==13) {$w=1}
          if ($v==14) {$w=1}
          if ($v==15) {$gec=1}
          if ($v==16) {$lc=1}
          if ($lc>0) {$stop=1}
          if ($w*($gw+$gc+$gec)>0) {$stop=1}
          if ($lec*($gc+$gw)>0) {$stop=1}
        }
        ++$j;
      }
    }
    if ($stop==0) {
      $solns[$core]=$k;
      $tag[$core]=0;
      if ($w>0) {$tag[$core]=1}
      elsif ($gc>0) {$tag[$core]=6}
      elsif ($lec*$gec>0) {$tag[$core]=3}
      elsif ($gw*$gec>0) {$tag[$core]=6}
      elsif ($gw>0) {$tag[$core]=5}
      elsif ($lec>0) {$tag[$core]=2}
      elsif ($gec>0) {$tag[$core]=4}
      ++$core;
    }
  }
  if ($core==0) {$killflag=1;goto FINI}

  $k=0;
  while ($killflag==0 && $k <= $#yes2) {
    @dummy = ();
    for ($j=0;$j<=$core-1;++$j) {
      $v=ord(substr($psbits[$yes2[$k]],$solns[$j],1))-48;
      if ($v==4) {push(@dummy,$j)}
      if ($v > 6) {
        if ($v!=11 && $v!=15 && $tag[$j]==0) {push(@dummy,$j)}
        if ($v==7 && $tag[$j]>0 && $tag[$j]<3) {push(@dummy,$j)}
        if ($v==8 && $tag[$j]>0 && $tag[$j]<5) {push(@dummy,$j)}
        if ($v==9 && $tag[$j]>1) {push(@dummy,$j)}
        if ($v==10 && $tag[$j]>0 && $tag[$j]<3) {push(@dummy,$j)}
        if ($v==12 && $tag[$j]>3) {push(@dummy,$j)}
        if ($v==13 && $tag[$j]>3) {push(@dummy,$j)}
        if ($v==14 && $tag[$j]>3) {push(@dummy,$j)}
        if ($v==16 && $tag[$j]>1) {push(@dummy,$j)}
      }
    }
    if (defined($dummy[0])) {
      $yessolns[$k] = [ @dummy ];
      if ($solns[$dummy[0]]>$hr && $unrealid!=$solns[$dummy[0]]) {
        $unreal=$unreal+1;
        $unrealid=$solns[$dummy[0]];
        if ($unreal>1) {$killflag=1}
      }
    }
    else {
      $killflag=1;
    }
    ++$k;
  }
  if ($killflag==1) {goto FINI}

  $k=0;
  while ($killflag==0 && $k <= $#no2) {
    @dummy = ();
    for ($j=0;$j<=$core-1;++$j) {
      $v=ord(substr($psbits[$no2[$k]],$solns[$j],1))-48;
      if ($v==5) {push(@dummy,$j)}
      if ($v > 6) {
        if ($v!=9 && $v!=16 && $tag[$j]==0) {push(@dummy,$j)}
        if ($v==7 && $tag[$j]>3) {push(@dummy,$j)}
        if ($v==8 && $tag[$j]>3) {push(@dummy,$j)}
        if ($v==10 && $tag[$j]>3) {push(@dummy,$j)}
        if ($v==11 && $tag[$j]>1) {push(@dummy,$j)}
        if ($v==12 && $tag[$j]>0 && $tag[$j]<5) {push(@dummy,$j)}
        if ($v==13 && $tag[$j]>0 && $tag[$j]<3) {push(@dummy,$j)}
        if ($v==14 && $tag[$j]>0 && $tag[$j]<3) {push(@dummy,$j)}
        if ($v==15 && $tag[$j]>1) {push(@dummy,$j)}
      }
    }
    if (defined($dummy[0])) {
      $nosolns[$k] = [ @dummy ];
      if ($solns[$dummy[0]]>$hr && $unrealid!=$solns[$dummy[0]]) {
        $unreal=$unreal+1;
        $unrealid=$solns[$dummy[0]];
        if ($unreal>1) {$killflag=1}
      }
    }
    else {
      $killflag=1;
    }
    ++$k;
  }
  if ($killflag==1) {goto FINI}
  $extsolns=1;

EXTCOMMONPROPS:

  for ($h=0;$h<=1;++$h) {
    if ($h==0) {@dummy=@commonmaybeyes} else {@dummy=@commonyes}
    $k=0;
    while ($k<=$#dummy) {
      $killit = 0;
      $x=substr($opbits[$onesum],$dummy[$k],1);
      if ($x==4) {
        $y=substr($opbits[$twosum],$dummy[$k],1);
        if ($y==4) {
          for ($j=0;$j<=$core-1;++$j) {
            $v=ord(substr($psbits[$dummy[$k]],$solns[$j],1))-48;
            if ($v==5) {$killit=1; last}
            if ($v > 6) {
              if ($v!=9 && $v!=16 && $tag[$j]==0) {$killit=1; last}
              if ($v==7 && $tag[$j]>3) {$killit=1; last}
              if ($v==8 && $tag[$j]>3) {$killit=1; last}
              if ($v==10 && $tag[$j]>3) {$killit=1; last}
              if ($v==11 && $tag[$j]>1) {$killit=1; last}
              if ($v==12 && $tag[$j]>0 && $tag[$j]<5) {$killit=1; last}
              if ($v==13 && $tag[$j]<3) {$killit=1; last}
              if ($v==14 && $tag[$j]<3) {$killit=1; last}
              if ($v==15 && $tag[$j]>1) {$killit=1; last}
            }
          }
        }
        else {
          $found=1;
          foreach $i (@yessolns) {
            $l=0; $found=0;
            while ($found==0 & $l<=$#$i) {
              $v=ord(substr($psbits[$dummy[$k]],$solns[$$i[$l]],1))-48;
              if ($v==5) {$found=1}
              if ($v > 6) {
                if ($v!=9 && $v!=16 && $tag[$$i[$l]]==0) {$found=1}
                if ($v==7 && $tag[$$i[$l]]>3) {$found=1}
                if ($v==8 && $tag[$$i[$l]]>3) {$found=1}
                if ($v==10 && $tag[$$i[$l]]>3) {$found=1}
                if ($v==11 && $tag[$$i[$l]]>1) {$found=1}
                if ($v==12 && $tag[$$i[$l]]>0 && $tag[$$i[$l]]<5) {$found=1}
                if ($v==13 && $tag[$$i[$l]]<3) {$found=1}
                if ($v==14 && $tag[$$i[$l]]<3) {$found=1}
                if ($v==15 && $tag[$$i[$l]]>1) {$found=1}
              }
              ++$l;
            }
            if ($found==0) {last}
          }
          if ($found==1) {
            foreach $i (@nosolns) {
              $l=0; $found=0;
              while ($found==0 & $l<=$#$i) {
                $v=ord(substr($psbits[$dummy[$k]],$solns[$$i[$l]],1))-48;
                if ($v==5) {$found=1}
                if ($v > 6) {
                  if ($v!=9 && $v!=16 && $tag[$$i[$l]]==0) {$found=1}
                  if ($v==7 && $tag[$$i[$l]]>3) {$found=1}
                  if ($v==8 && $tag[$$i[$l]]>3) {$found=1}
                  if ($v==10 && $tag[$$i[$l]]>3) {$found=1}
                  if ($v==11 && $tag[$$i[$l]]>1) {$found=1}
                  if ($v==12 && $tag[$$i[$l]]>0 && $tag[$$i[$l]]<5) {$found=1}
                  if ($v==13 && $tag[$$i[$l]]<3) {$found=1}
                  if ($v==14 && $tag[$$i[$l]]<3) {$found=1}
                  if ($v==15 && $tag[$$i[$l]]>1) {$found=1}
                }
                ++$l;
              }
              if ($found==0) {last}
            }
          }
          if ($found==1) {$killit=1}
        }
      }
      if ($killit==1) {splice(@dummy,$k,1);redo if defined($dummy[$k])}
      ++$k;
    }
    if ($h==0) {@commonmaybeyes=@dummy} else {@commonyes=@dummy}
  }

  for ($h=0;$h<=1;++$h) {
    if ($h==0) {@dummy=@commonmaybeno} else {@dummy=@commonno}
    $k=0;
    while ($k<=$#dummy) {
      $killit = 0;
      $x=substr($opbits[$sum],$dummy[$k],1);
      if ($x==4) {
        $y=substr($opbits[$add],$dummy[$k],1);
        if ($y==4) {
          for ($j=0;$j<=$core-1;++$j) {
            $v=ord(substr($psbits[$dummy[$k]],$solns[$j],1))-48;
            if ($v==4) {$killit=1; last}
            if ($v > 6) {
              if ($v!=11 && $v!=15 && $tag[$j]==0) {$killit=1; last}
              if ($v==7 && $tag[$j]>0 && $tag[$j]<3) {$killit=1; last}
              if ($v==8 && $tag[$j]>0 && $tag[$j]<5) {$killit=1; last}
              if ($v==9 && $tag[$j]>1) {$killit=1; last}
              if ($v==10 && $tag[$j]>0 && $tag[$j]<3) {$killit=1; last}
              if ($v==12 && $tag[$j]>3) {$killit=1; last}
              if ($v==13 && $tag[$j]>3) {$killit=1; last}
              if ($v==14 && $tag[$j]>3) {$killit=1; last}
              if ($v==16 && $tag[$j]>1) {$killit=1; last}
            }
          }
        }
        else {
          $found=1;
          foreach $i (@yessolns) {
            $l=0; $found=0;
            while ($found==0 & $l<=$#$i) {
              $v=ord(substr($psbits[$dummy[$k]],$solns[$$i[$l]],1))-48;
              if ($v==4) {$found=1}
              if ($v > 6) {
                if ($v!=11 && $v!=15 && $tag[$$i[$l]]==0) {$found=1}
                if ($v==7 && $tag[$$i[$l]]>0 && $tag[$$i[$l]]<3) {$found=1}
                if ($v==8 && $tag[$$i[$l]]>0 && $tag[$$i[$l]]<5) {$found=1}
                if ($v==9 && $tag[$$i[$l]]>1) {$found=1}
                if ($v==10 && $tag[$$i[$l]]>0 && $tag[$$i[$l]]<3) {$found=1}
                if ($v==12 && $tag[$$i[$l]]>3) {$found=1}
                if ($v==13 && $tag[$$i[$l]]>3) {$found=1}
                if ($v==14 && $tag[$$i[$l]]>3) {$found=1}
                if ($v==16 && $tag[$$i[$l]]>1) {$found=1}
              }
              ++$l;
            }
            if ($found==0) {last}
          }
          if ($found==1) {
            foreach $i (@nosolns) {
              $l=0; $found=0;
              while ($found==0 & $l<=$#$i) {
                $v=ord(substr($psbits[$dummy[$k]],$solns[$$i[$l]],1))-48;
                if ($v==4) {$found=1}
                if ($v > 6) {
                  if ($v!=11 && $v!=15 && $tag[$$i[$l]]==0) {$found=1}
                  if ($v==7 && $tag[$$i[$l]]>0 && $tag[$$i[$l]]<3) {$found=1}
                  if ($v==8 && $tag[$$i[$l]]>0 && $tag[$$i[$l]]<5) {$found=1}
                  if ($v==9 && $tag[$$i[$l]]>1) {$found=1}
                  if ($v==10 && $tag[$$i[$l]]>0 && $tag[$$i[$l]]<3) {$found=1}
                  if ($v==12 && $tag[$$i[$l]]>3) {$found=1}
                  if ($v==13 && $tag[$$i[$l]]>3) {$found=1}
                  if ($v==14 && $tag[$$i[$l]]>3) {$found=1}
                  if ($v==16 && $tag[$$i[$l]]>1) {$found=1}
                }
                ++$l;
              }
              if ($found==0) {last}
            }
          }
          if ($found==1) {$killit=1}
        }
      }
      if ($killit==1) {splice(@dummy,$k,1);redo if defined($dummy[$k])}
      ++$k;
    }
    if ($h==0) {@commonmaybeno=@dummy} else {@commonno=@dummy}
  }

FINI:

  if ($killflag==1 || $soln==1) {}
  else {
    print "<center>AN EXTENDED FINITE $insert SOLUTION</center>\n";
    print "<center><b>\n";

    foreach $k (@yessolns) {
      push(@extended,$solns[$$k[0]]);
    }
    foreach $k (@nosolns) {
      push(@extended,$solns[$$k[0]]);
    }
    for ($k=0;$k<=$#extended;++$k) {
      $j=0;$stop=0;
      while ($j<$k && $stop==0) {
        if ($extended[$k]==$extended[$j]) {$stop=1}
        ++$j;
      }
      if ($stop==0 && $k==0) {print " $spaces[$extended[$k]] "}
      if ($stop==0 && $k>0) {print " $conn $spaces[$extended[$k]] "}
    }
    print "</b></center>\n";
  }
}

if ($extsolns==0 && $soln==0) {
  print "<center><b>NO EXTENDED SOLUTIONS IN THE DATABASE!</b></center>\n";
}

COMMON:

if ($#commonno>=0 || $#commonyes>=0 || $#commonmaybeyes>=0 || $#commonmaybeno>=0 || $#commonmaybemaybe>=0) {
  print "<center><b>COMMON PROPERTIES (NOT SINGLY DERIVABLE) TO <i>ALL</i> SOLUTIONS</b></center>\n";
  print "<br>";
  for ($k=0;$k<=$#commonyes;++$k){
    print "$props[$commonyes[$k]]  ";
  }
  if (defined($commonyes[0])) {print "<br>\n"}
  for ($k=0;$k<=$#commonno;++$k){
    print "Not&nbsp;($props[$commonno[$k]])  ";
  }
  if (defined($commonno[0])) {print "<br>\n"}
  for ($k=0;$k<=$#commonmaybeyes;++$k){
    print "<i>$props[$commonmaybeyes[$k]]  </i>";
  }
  if (defined($commonmaybeyes[0])) {print "<br>\n"}
  for ($k=0;$k<=$#commonmaybeno;++$k){
    print "<i>Not&nbsp;($props[$commonmaybeno[$k]])  </i>";
  }
  if (defined($commonmaybeno[0])) {print "<br>\n"}
  for ($k=0;$k<=$#commonmaybemaybe;++$k){
    print "<i>?($props[$commonmaybemaybe[$k]])  </i>";
  }
  print "\n";
}
elsif ($soln==1 || $extsolns==1) {
  print "<center><b>NO COMMON PROPERTIES (NOT SINGLY DERIVABLE) TO <i>ALL</i> SOLUTIONS!<b></center>\n";
}

FINITO:

print "<br><center><b><font size=+1>
<a href = http://www.umanitoba.ca/cgi-bin/math/bell/props.cgi>Property Selection</a>
<a href = http://www.umanitoba.ca/cgi-bin/math/bell/structs.cgi>&nbsp;&nbsp;Structure Selection</a>
</font></b></center>\n";

print "</body></html>\n";
exit;

sub send_mail {
  open(MAIL,"|$cmd -t");
  print MAIL "To: mbell\@cc.umanitoba.ca \n";
  print MAIL "From: Machine \n";
  print MAIL "Subject: Property Choice \n\n";
  
  print MAIL "REMOTE_HOST :     $ENV{'REMOTE_HOST'}\n";
  print MAIL "REMOTE_ADDRESS :  $ENV{'REMOTE_ADDR'}\n";
  print MAIL "HTTP_USER_AGENT : $ENV{'HTTP_USER_AGENT'}\n";
  print MAIL "************************************** \n"; 
  $k=0;
  while ($k<=$#keys) {
    $a=$values[$k];$b=$props[$keys[$k]];
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
