#########################

#need to have some stuff
gene=''

#nucleotide genes directory, where to find annoted nucleotide fasta sequence for the group
gene_database=''

#single gene protein directory
gene_prot_path=''

#list of code of mitogenomes that need to be annoted
list_code=''

######################

#set working directory
working_directory=$PWD

#settings
line_output_value=1230

#build hmm profile of alignment, nucleotide one
#mafft --auto $gene_database > $gene'.nucl.align.fasta'
for i in $gene_database/*
do name_s=$(echo $i | awk -F "/" '{print $NF}')
cat $i > $name_s
hmmbuild ${name_s%.fasta}.hmm $name_s
cat ${name_s%.fasta}.hmm >> $gene'.nucl.hmm'
rm ${name_s%.fasta}.hmm $name_s
done

echo -e "missing\treference\tstart_ref\tend_ref\tstart_missing\tend_missing\taccuracy" > $gene'_missing_annotation_results.txt'

#retrieve every fasta genome from ncbi
#downloading every species from the list
for species in $(cat $list_code)
    do mkdir $species
    esearch -db nuccore -query $species | efetch -format fasta > $species/$species'.fasta'
    esearch -db nuccore -query $species | efetch -format gff3 > $species/$species'.gff3'
    done

#hmmscan every fasta genome whose missing the gene
echo 'hmmscanning every downloaded genome, looking fot whats missing'
for species in $(cat $list_code)
    do hmmsearch -o $species/$species'.out' --incE 0.5 $gene'.nucl.hmm' $species/$species'.fasta' 
    python /home/PERSONALE/diego.carli2/app/gene_missing_annotation/split.hmm.files.py --input_file $species/$species'.out'
    cd $species/$species'.output_files'
    for outfile in $(python /home/PERSONALE/diego.carli2/app/gene_missing_annotation/find_files_unusual_size.py $PWD | awk -F ":" '{print $1}')
        do python /home/PERSONALE/diego.carli2/app/gene_missing_annotation/read.hmm.output.py $species $PWD/$outfile >> $species'.'$outfile'.'missing.txt'
        cat $species'.'$outfile'.'missing.txt' >> ../../$gene'_missing_annotation_results.txt'
        done
    #python /home/PERSONALE/diego.carli2/app/my_alias/extract_nc_regions.py $species'.fasta' $species'.gff3' $species'.nc.fasta'
    cd $working_directory
    done
