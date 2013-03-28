for i in *.h *.hpp *.cpp Make*; 
do 
name=${i##Pms}
echo $i $name
sed 's/Abc//g' $i >  tmp
cp tmp $name
done

