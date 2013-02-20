#!/usr/bin/perl
$string="perl";
$num1=20;
$num2=10.75;
print "The string is $string, number 1 is $num1 and number 2 is $num2\n";
print "$num1*$num2;  $num1 ** 2\n";
$str="aabb";
$str++;
print "$str \n";
$var="Perl";
$num=10;
print "Two \$nums are $num * 2 and adding one to \$var makes $var++\n";
print "Two \$nums are ", $num * 2," and adding one to \$var makes ", $var++,"\n";

print "$var \n";

##########

@names=("Muriel","Gavin","Susanne","Sarah");
@cities=("Brussels","Hamburg","London","Breda");

&look;

$last=pop(@names);
unshift (@cities, $last);

&look;

sub look {
        print "Names : @names\n";
        print "Cities: @cities\n";
}


##########
@names=("Muriel","Sarah","Susanne","Gavin");

&look;

@middle=splice (@names, 1, 2);

&look;

sub look {
        print "Names : @names\n";
        print "The Splice Girls are: @middle\n";
}

#######
@names=("Muriel","Gavin","Susanne","Sarah");
@cities=("Brussels","Hamburg","London","Breda");

&look;

splice (@names, 1, 0, @cities[1..3]);

&look;

sub look {
        print "Names : @names\n";
        print "Cities: @cities\n";
}


