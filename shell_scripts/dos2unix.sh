for i in *.h *.hpp *.cpp; 
do 
echo $i; 
dos2unix $i;
done

