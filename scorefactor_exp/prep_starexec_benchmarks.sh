################
#Prerpare zip file of benchmarks to upload to StarExec
#Assumes filtered_cnf_list and sr2019benchmarks dir available in top level dir.
################

for f in $(cat unfiltered_cnf_list)
do
  find ./sr2019benchmarks -name "*.cnf*" | grep $f*
done > unfiltered_benchmarks_paths

rm -r unfiltered_exp_benchmarks
mkdir unfiltered_exp_benchmarks
for f in $(cat unfiltered_benchmarks_paths)
do
  cp -v $f unfiltered_exp_benchmarks/
done

zip exp_benchmarks_unfiltered.zip unfiltered_exp_benchmarks/*
