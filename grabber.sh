#!/bin/bash


##Helper function to create hostID file
if [ "$#" -gt 1 ] && [ $1 == '-h' ]
then
    echo $2 > hostID 
    exit 0
fi

##Check to see if end server is alive


FRAME_SERVER="127.0.0.1:1225/frame"
HEALTHCHECK=$(curl -s $FRAME_SERVER/healthcheck)

if [ $HEALTHCHECK != "GOOD" ]
then
  exit 1
fi

MANIFEST_FILE="manifest.json"
MANIFEST_CLIENT="client_manifest.json"
HOSTID=$(cat hostID)
FIRST_RUN=0

GET_MANIFEST=$(curl -s $FRAME_SERVER/$HOSTID)

GET_MANIFEST_FILE(){
    echo $GET_MANIFEST > $MANIFEST_FILE
    echo "data='$(cat $MANIFEST_FILE)'" > $MANIFEST_CLIENT 
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

