
($#ARGV >= 0) or die "need one arg: number";

#print "Enter url :";
#$url=<STDIN>;
$count=$ARGV[0];

for($i=1; $i<= $count; $i++)
{
	print "$i\n";
	system("mail agun\@agun.pe.kr -s \"���� �������� !!!! \" < t.txt" );
#	system("mail dahee\@netsgo.com -s \"���� �������� !!!! \" < t.txt" );
}
