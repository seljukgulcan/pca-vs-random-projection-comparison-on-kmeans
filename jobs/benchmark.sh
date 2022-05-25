set -e

REPOPATH=~/ee/

PING=false
PINGBIN=${REPOPATH}ping.py
PINGUSERID=''
PINGTOKEN=''

DATANAME='val2017'
DIMENSION=64
D_PCA=100
K=20

err_report() {
    if [ "$PING" = true ] ; then
        message="Benchmark job ${DATANAME} ${DIMENSION} error on line $1"
        python ${PINGBIN} ${PINGUSERID} ${PINGTOKEN} "${message}"
    fi
}

trap 'err_report $LINENO' ERR

eval "$(conda shell.bash hook)"
conda activate eee587

if [ "$PING" = true ] ; then
    message="Benchmark job ${DATANAME} ${DIMENSION} started"
    python ${PINGBIN} ${PINGUSERID} ${PINGTOKEN} "${message}"
fi

# Job starts here

cd ${REPOPATH}
python benchmark.py ${DATANAME} ${DIMENSION} {D_PCA} {K}

# Job ends here

if [ "$PING" = true ] ; then
    message="Benchmark job ${DATANAME} ${DIMENSION} finished"
    python ${PINGBIN} ${PINGUSERID} ${PINGTOKEN} "${message}"
fi

