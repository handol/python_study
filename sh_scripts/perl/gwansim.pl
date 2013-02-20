
if ($ARGV[0] eq "") {
	print "need a file name\n";
	die "need a file name\n";
	exit;
}

open FILE, $ARGV[0] or die "file read error: \" . $ARGV[0] . \"";
$out="";
while (<FILE>) {
	if (/^\d/) {
		#print "$_";
		/^\d+=\d(\d+)/;
		$code=$1;
		print "$code\n";

		#$code =~ s/^\d+=\d//;
		#($code = $_) =~ s/^\d+=\d//;
		#@arr = $code;
		#print "$code\n";
		#print "$arr[0]\n";

		#$oneline = `/home/terminal/work/new/stockplus N $code`;
		##print $oneline;
		#$out .= $oneline;
	}
}
print $out;
