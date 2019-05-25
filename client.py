import os
from DataHandler import ImgManifest 
from uuid import uuid4
import json

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
            self.creat_hostID()

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
                with open(if_file,'w') as hostIdFile:
                    hostIdFile.write(id_str.strip())
            except EnvironmentError, err:
                pass

        return id_str


    def _get_HostID(self):

        host_id = None

        try:
            with open(self._HOSTID_FILE) as hostIdFile:
                hostIdFile.read()

        except EnvironmentError, err:
            pass

        return host_id


class FrameRequestHandler:
    URL_ROOT = 'http://frame.mroots.io'

    def __init__(self,frameID=None):
        self.frame_id = frameID


    def download_image(self, img_filename):
        pass

    def save_image(self, img_filename, data):
        pass

    def dl_manifest(self):
        pass


