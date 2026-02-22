for i in ../abcs/*.jpg; do # Whitespace-safe but not recursive.
    echo "$i"
    export JPG_FILENAME="${i%.*}"
    convert "${JPG_FILENAME}.jpg" "${JPG_FILENAME}.eps"
done
