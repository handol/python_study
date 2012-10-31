cd /root/handol
#D=`date +"%Y%m%d%H%M"`
D=`date +"%Y%m%d"`
echo $D
fname="chk_processlist."$D".txt"
echo $fname
python /root/handol/chk_processlist.py >> $fname

