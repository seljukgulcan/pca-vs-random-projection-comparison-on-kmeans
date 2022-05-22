set -e

REPOPATH=~/ee/

PING=false
PINGBIN=${REPOPATH}ping.py
PINGUSERID=''
PINGTOKEN=''

DATANAME='val2017'

err_report() {
    if [ "$PING" = true ] ; then
        message="Download job error on line $1"
        ${PINGBIN} ${PINGUSERID} ${PINGTOKEN} ${message}
    fi
}

trap 'err_report $LINENO' ERR

eval "$(conda shell.bash hook)"
conda activate eee587

if [ "$PING" = true ] ; then
    message="Download started"
    ${PINGBIN} ${PINGUSERID} ${PINGTOKEN} ${message}
fi

# Job starts here

python download_dataset.py ${DATANAME}

# Job ends here

if [ "$PING" = true ] ; then
    message="Download finished"
    ${PINGBIN} ${PINGUSERID} ${PINGTOKEN} ${message}
fi

