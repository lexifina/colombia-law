# Runs every parser whose part lists fallback articles, one at a time, under fallback/hook.py.
cd "$(dirname "$0")/.."
run() { tag=$1; eng=$2; shift 2; echo "== $tag $(date -u +%H:%M:%S)"; python -X utf8 .tmp-co/lowrun.py python -X utf8 fallback/hook.py $eng fallback/.tmp/rec-$tag.json "$@" > fallback/.tmp/log-$tag.txt 2>&1; echo "exit $?"; }
run 60 phase2 phase2/parse_phase2.py --out-dir fallback/.tmp/60
run 70 cst cst/parse_cst.py --out fallback/.tmp/70/70-cst.json
for p in 80:3 90:4 95:5 97:6 98:7 99:8 99a:9 99b:10 99c:11 99d:12 99e:13 99f:14 99g:15 99h:16 99i:17 99j:18 99k:19 99l:20 99m:21 99n:22 99p:24 99q:25 99s:27 99t:28 99w:31; do
  tag=${p%%:*}; b=${p##*:}; run $tag phase2 batch$b/parse_batch$b.py --out-dir fallback/.tmp/$tag
done
echo ALLDONE
