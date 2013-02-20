#!/usr/bin/perl
use Time::Local; 
sub prn_time 
{
   my @dayofweek = (qw(Sunday Monday Tuesday Wednesday Thursday Friday Saturday)); 
   my @monthnames = (qw(Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec)); 
   my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday); 
   #$ENV{TZ} = ':/usr/share/zoneinfo/Europe/Paris'; 
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday) = localtime($TimeInSeconds); 
   $year += 1900; 
   #print "This date is $dayofweek[$wday], $monthnames[$mon] $mday, $year\n"; 
   #print "This time is $hour:$min:$sec\n"; 
   print "$hour:$min:$sec\n"; 
}

$kosdaq = "/cygdrive/c/FN/KiwoomHero/Data/KMaster.dat";
$kospi = "/cygdrive/c/FN/KiwoomHero/Data/JMaster.dat";

my %company_list=();
sub read_company_code
{
	local $code;
	open FILE, $_[0] or die "file read error: $_[0]\n";
	while (<FILE>) {
			@line = split " ", $_;			
    	#print "$line[0], $line[1]\n";
    	$_ = $line[1];
    	/^(\d{5})/;
			$code = $1;
			
			#print "$line[0], $code\n";
			$company_list{$code} = $line[0];
  }
}




my $sm_gwansim_f="/cygdrive/d/cygwin/home/anydict/work/data/real_gwansim.usr";

my $all_gwansim_f="/cygdrive/d/cygwin/home/anydict/work/data/GwanList_dahee00.usr";
my $my_gwansim;

my @codelist=();

sub read_org_code_file
{

	$my_gwansim = $_[0];
	print "Gwansim: $_[0]\n";
    open FILE, $_[0] or die "file read error: $_[0]\n";
    @codelist=();
    while (<FILE>) {
    	if (/^\d/) {
    		#print "$_";
    		/^\d+=\d(\d+)/;
    		$code=$1;
    		push(@codelist, $code);     
    	}
    }
	close FILE;    
	print "$#codelist+1 codes\n";
}


sub read_code_file
{
	local $codefile="/cygdrive/d/cygwin/home/anydict/work/data/gwansim.dat";

	$my_gwansim = $codefile;
    open FILE, $codefile or die "file read error: \" . $codefile . \"\n";

    print "Gwansim: $codefile\n";
    @codelist=();
    while (<FILE>) {
    	chop;
    	if (!/^\s/) {
	    	push(@codelist, $_);
	    }
	    else {
	    	#prinf("empty\n");
	    }
    }
    close FILE;
    print "$#codelist+1 codes\n";
}

sub prn_code_list
{
	for $code (@codelist) {
		print "$code\n";
	}
}
	
sub read_val
{
	local ($i);
	open FILE, $_[0] or die "file read error: \" . $_[0] . \"";
	@res_txt=();
	while (<FILE>) {
		push (@res_txt,$_);
	}
	
	close FILE;
	
	$i=0;
	foreach $line (@res_txt) {
		if ($line =~ /전일비/) ## =~ match, !~ no match
			{
				#print "$line";
				#print $res_txt[$i+1];
				$_ = $res_txt[$i+1];
				~/\s+(\d+\.\d+)/;
				#print "$1\n"	;  # 전일비 거래량 %
				return $1;		
			}
		$i++;
	}
	return "0";
	
}

my %code_score;
my $agent="User-Agent: Mozilla/4.0";
sub do_kiwoom {
	local ($i);
	%code_score=();
    $tmp_file="tmp.html";
    $tmp_text="tmp.txt";
    $i=0;
    for $code (@codelist) {
    	$url="www.kiwoom.com/cgi-bin/trading/stai0101/stai0101-2.cgi?shcode=$code";
    	#print $url;
    	#print "web2txt $url $tmp_file\n"
    	system("wget -q -O $tmp_file -T 3 -U \"$agent\" $url");
    	system("html2txt $tmp_file");
    	$vol = read_val("$tmp_text");
    	$i++;
    	print "$i\t$code\t $vol\%\t $company_list{$code}\n";
    	$code_score{$vol} = $code;
    }
}

my @sorted=();

sub prn_score
{
	local $code;
	@sorted = reverse sort {$a <=> $b} keys %code_score;
	foreach (@sorted) {
		$code = $code_score{$_};
   		print "$_\%\t $code\t $company_list{$code}\n";
	}
}

sub write_score
{
  local $code;
  $out=$_[0];
  
  open OUT, ">$out" or die "Cannot open $out for write :$!";

  $t = `date`;
  print OUT "$t";
  print OUT "Gwansim: $my_gwansim\n\n";
  foreach (@sorted) {
  	$code = $code_score{$_};
	print OUT "$_\%\t $code\t $company_list{$code}\n";
  }
}

sub fetch_all_code
{
	&do_kiwoom();

	system("date");

	&prn_score();

	&write_score("kw_score.txt");

}
#-------------Main---------------
#-----------------------
#prn_time();
system("date");
#print "Result: $?\n";

&read_company_code($kosdaq);
&read_company_code($kospi);

if ($ARGV[0] eq "") {
	&read_org_code_file($sm_gwansim_f);
}
else {
	&read_org_code_file($all_gwansim_f);
}

#prn_code_list();


#@codelist=("16360", "17670", "32380"); 	

&fetch_all_code();
