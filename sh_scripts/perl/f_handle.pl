($size, $mtime, $tt) = (stat($ARGV[0])) [7,9];
print "$tt\n";
$t = time;
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time) ;
print $t."\n";
$year += 1900;
$mon++;
print "$year/$mon/$mday $hour:$min:$sec $wday\n";
print "$size, $mtime\n";
#utime($mtime, $mtime, "dahee");
