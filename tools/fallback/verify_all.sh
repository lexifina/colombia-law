# Runs each touched part's verifier against the patched copies in the folder given (default fallback/.tmp/cdall).
cd "$(dirname "$0")/.."
D=${1:-fallback/.tmp/cdall}
v() { echo "== $1"; python -X utf8 .tmp-co/lowrun.py python -X utf8 $2 $D/$1 2>&1 | grep -E "differ|TOTAL|FAILED|Error|rror:" | grep -vE ": 0 differ|, 0 differ" ; }
v 50-codes.json codes/verify_today.py
v 60-phase2.json phase2/verify_phase2.py
v 70-cst.json cst/verify_cst.py
for p in 80-batch3:3 90-batch4:4 95-batch5:5 97-batch6:6 98-batch7:7 99-batch8:8 99a-batch9:9 99b-batch10:10 99c-batch11:11 99d-batch12:12 99e-batch13:13 99f-batch14:14 99g-batch15:15 99h-batch16:16 99i-batch17:17 99j-batch18:18 99k-batch19:19 99l-batch20:20 99p-batch24:24 99q-batch25:25 99s-batch27:27 99t-batch28:28; do
  v ${p%%:*}.json batch${p##*:}/verify_batch${p##*:}.py
done
echo VERIFY_DONE
