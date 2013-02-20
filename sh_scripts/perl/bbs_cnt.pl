
($#ARGV >= 0) or die "need one arg: number";

print "Enter url :";
$url=<STDIN>;
$count=$ARGV[0];

$_ = $url;
s/\&/\\\&/g;
s/\?/\\\?/g;
$url = $_;
print "$url\n";

for($i=1; $i<= $count; $i++)
{
	print "$i\n";
	system("geturl -d -h $url");
}
