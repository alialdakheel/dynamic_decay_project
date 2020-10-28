################
#Prerpare zip file of benchmarks to upload to StarExec
#Assumes filtered_cnf_list and sr2019benchmarks dir available in top level dir.
################

for f in $(cat filtered_cnf_list)
do
  find ./sr2019benchmarks -name "*.cnf*" | grep $f*
done > benchmarks_paths

rm -r exp_benchmarks
mkdir exp_benchmarks
for f in $(cat benchmarks_paths)
do
  cp -v $f exp_benchmarks/
done

zip exp_benchmarks.zip exp_benchmarks/*
