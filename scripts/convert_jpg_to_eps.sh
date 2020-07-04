for i in abcs/*.jpg; do # Whitespace-safe but not recursive.
    export JPG_FILENAME=$(echo $i | cut -f 1 -d '.')
    convert ${JPG_FILENAME}.jpg ${JPG_FILENAME}.eps 
done
