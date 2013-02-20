
($#ARGV >= 0) or die "need one arg: number";

#print "Enter url :";
#$url=<STDIN>;
$count=$ARGV[0];

for($i=1; $i<= $count; $i++)
{
	print "$i\n";
	system("mail agun\@agun.pe.kr -s \"메일 보내지마 !!!! \" < t.txt" );
#	system("mail dahee\@netsgo.com -s \"메일 보내지마 !!!! \" < t.txt" );
}
