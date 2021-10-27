#!bin/bash

strategy=$1

coll_path="data/tipster-ap-frac/"
indexfile="output/indexfile_c$strategy"
stopwordfile="data/stopwords.txt"
xml_tags_info="data/xml_tags_info.txt"
queryfile="data/queryfile_1.txt"
resultfile="output/resultfile_c$strategy"

# bash invidx.sh $coll_path $indexfile $stopwordfile $strategy $xml_tags_info

bash boolsearch.sh $queryfile $resultfile "$indexfile.idx" "$indexfile.dict"