#!/bin/bash


if [ "$#" -gt 1 ] && [ $1 == '-h' ]
then
    echo $2 > hostID 
    exit 0
fi

FRAME_SERVER="127.0.0.1:1225/frame"
MANIFEST_FILE="manifest.json"
HOSTID=$(cat hostID)
FIRST_RUN=0

GET_MANIFEST=$(curl -s $FRAME_SERVER/$HOSTID)

GET_MANIFEST_FILE(){
    echo $GET_MANIFEST > $MANIFEST_FILE
}


if [ ! -f $MANIFEST_FILE ]
then
    echo "No Manifest file found. Fetching...."
    GET_MANIFEST_FILE
    FIRST_RUN=1
fi

CURL_CHECKSUM=$(curl -s $FRAME_SERVER/$HOSTID | jq .checksum)
CUR_CHECKSUM=$(cat $MANIFEST_FILE | jq .checksum)




GRAB_PHOTOS() {
    PHOTO_LIST=$(cat $MANIFEST_FILE | jq .data | jq 'keys[]' | tr '"' ' ')

    rm -rf IMG/
    mkdir IMG

    for photo in $PHOTO_LIST
    do
        curl -s $FRAME_SERVER/$HOSTID/img/$photo > IMG/$photo
    done
}



if [ $FIRST_RUN == 1 ]
then
    GRAB_PHOTOS
    exit 0
fi


#####
# Look for checksum change
#####
if [ $CURL_CHECKSUM == $CUR_CHECKSUM ]
then
    exit 0
else
    echo "Change Detected. Fetching Manifest and Photos...."
    GET_MANIFEST_FILE
    GRAB_PHOTOS
fi

