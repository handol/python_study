@stuff=qw(flying gliding skiing dancing parties racing);	# quote-worded list

@new = grep /ing/, @stuff;	# Creates @new, which contains elements of @stuff 
				# matching with 'ing' in them.

				print join ":",@stuff,"\n";	# first makes one string out of the elements of @stuff, joined
								# with ':' , then prints it, then prints \n

								print join ":",@new,"\n";



@stuff=qw(flying gliding skiing dancing parties racing);

@new = grep { s/ing// if /^[gsp]/ } @stuff;

print join ":",@stuff,"\n";
print join ":",@new,"\n";


