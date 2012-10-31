
cd /root/handol
#D=`date +"%Y%m%d%H%M"`
D=`date +"%Y%m%d"`
echo $D
fname="snssys."$D".txt"
echo $fname
python /root/handol/check_snssys.py >> $fname
