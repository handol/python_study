if ($#ARGV < 1) {
die "usage: dir1 dir2\n";
}
$dir1 = $ARGV[0];
$dir2 = $ARGV[1];
#print "$dir1 $dir2\n";

#@f1 = <$dir1/*>;
#@f2 = <$dir2/*>;
open (F1, $dir1) || die "read fail $dir1\n";
@f1 = <F1>;
close F1;
open (F2, $dir2) || die "read fail $dir2\n";
@f2 = <F2>;
close F2;

@f1 = sort @f1;
@f2 = sort @f2;

$n1 = $#f1+1;
$n2 = $#f2+1;

@only1=();
@only2=();
@share=();

#print "A:@f1\n";
#print "B:@f2\n";

for($i=0, $j=0; $i < $n1 && $j < $n2; ) 
{
  if ($i < $n1 && $j < $n2 && $f1[$i] eq $f2[$j]) {
	push(@share, $f1[$i]);
	$i++;
	$j++;
  }
  while ( ($i==$n1 || $f1[$i] gt $f2[$j])  && $j < $n2 ) {
	push(@only2, $f2[$j]);
	$j++;
  }
  while ( ($j==$n2 || $f1[$i] lt $f2[$j]) && $i < $n1 )  {
	push(@only1, $f1[$i]);
	$i++;
  }
}

$tmp = join(" ", @share);
print "share: $tmp\n";
$tmp = join(" ", @only1);
print "only1: $tmp\n";
$tmp = join(" ", @only2);
print "only2: $tmp\n";
