my ($d,$m,$y)=(localtime)[3..5];

print $y+1900,"-",$m+1,"-",$d,"\n";
