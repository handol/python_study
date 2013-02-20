$dir= shift || '.';

opendir DIR, $dir or die "Can't open directory $dir: $!\n";

while ($file= readdir DIR) {
	next if $file=~/^\./ ;
	print "$1 \n" if $file =~ /([0-9]+)/ ;
 #	print "Found a file: $dir/$file\n" if -T "$dir/$file" ;
}

$now_string = localtime;  # e.g., "Thu Oct 13 04:54:34 1994"
print "$now_string \n";

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) =
                                                localtime(time);

print "$sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst \n";

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) =
                                            gmtime(time);
print "$sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst \n";

