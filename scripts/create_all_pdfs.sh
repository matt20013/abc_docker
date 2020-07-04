#find . -maxdepth 1 -type f -name "*.txt"

#shopt -s globstar
#for i in **/*.abc; do # Whitespace-safe and recursive
#    ABC_FILENAME=$(echo $i | cut -f 1 -d '.')
#    echo $ABC_FILENAME
#done

for i in *.abc; do # Whitespace-safe but not recursive.
    export ABC_FILENAME=$(echo $i | cut -f 1 -d '.')
    echo $ABC_FILENAME
    ./create_pdf.sh
done
