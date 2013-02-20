BEGIN { old = 0 } 

/Status:/ { 
	if ($NF !~ /Up-to-date/) { 
		print "========================================================"; 
		print $0; 
		old = old + 1 
	} 
} 

/revision/ { 
	if (old > 0) { 
		print $0; 
		old = old + 1 
	} 

	if (old > 2) { 
		old = 0; 
		print "========================================================"; 
	} 
} 

