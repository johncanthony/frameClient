import os
from DataHandler import ImgManifest 
from uuid import uuid4
import json
import requests

class ClientManifest(ImgManifest):

    _CLIENT_MANIFEST_FILE = './client_manifest.json'
    

    '''
    Params :
        data: string from json.dumps()
    '''
    def write_client_manifest(self,data):

        client_manifest_filename = None
        try:
            with open(self._CLIENT_MANIFEST_FILE, 'w') as client_manifest:
                output_string = "data='{}'".format(data)
                client_manifest.write(output_string)
            client_manifest_filename = self._CLIENT_MANIFEST_FILE
        except EnvironmentError, err:
            pass

        return client_manifest_filename


    def _is_new_manifest(self,new_manifest):
        '''
        new_manifest needs to be a json.load[s]() object
            compare old checksum to the new checksum
            return bool
        '''

        pass

    def _diff_manifests(self, new_manifest):
        '''
        new_manifest needs to be in a json.load[s]() object
            check for file discrepancies between the two 
            for each in new_manifest.data:
                if self.manifest.get(each, None) == None:
                    add removable image to return list
        '''
        pass


class FrameClient(object):

    _HOSTID_FILE = './hostID'

    def __init__(self):

        if not self._file_exists(self._HOSTID_FILE):
            self._create_hostID()

        self.frameID = self._get_HostID()
        self.images = []

    def _file_exists(self,filename):
        return os.path.isfile(filename)

    def _create_hostID(self):
        id_file = "/etc/machine-id"
        self._HOSTID_FILE
        id_str = None

        try:

            with open(id_file,'r') as idFile:
                id_str = idFile.read()

        except EnvironmentError, err:
            pass

        if id_str != None:
            try:
                with open(self._HOSTID_FILE,'w') as hostIdFile:
                    hostIdFile.write(id_str.strip())
            except EnvironmentError, err:
                pass

        return id_str


    def _get_HostID(self):

        host_id = None

        try:
            with open(self._HOSTID_FILE) as hostIdFile:
                host_id = hostIdFile.read()

        except EnvironmentError, err:
            pass

        return host_id.strip()


class FrameRequestHandler:
    _URL_ROOT = 'http://frame.mroots.io/frame'
    _IMG_ROOT = './IMG'

    def __init__(self,frameID=None):
        self._frame_id = frameID

    def _is_server_healthy(self):
        r = requests.get("{}/{}".format(self._URL_ROOT,'healthcheck'))

        if r.status_code is 200:
            return True

        return False

    def download_image(self, img_filename):
        data = None

        request_string ="{}/{}/img/{}".format(self_URL_ROOT,self._frame_id,img_filename)
        r = requests.get(request_string)

        if r.status_code is 200:
            data = r.content

        return data

    def save_image(self, img_filename, data):
        saved = False
        img_filepath = '{}/{}'.format(self._URL_ROOT,img_filename)

        try:
            with open(img_filepath,'wb') as imgFile:
                imgFile.write(data)
            saved = True
        except EnvironmentError, err:
            pass

        return saved


    def dl_manifest(self):
        manifest_text = None

        r = requests.get("{}/{}".format(self._URL_ROOT,self._frame_id))
        if r.status_code == 200:
            manifest_text = r.text

        return manifest_text


if __name__ == "__main__":

    frame = FrameClient()
    print(frame.frameID)

    manifest = ClientManifest(frame.frameID)
    
