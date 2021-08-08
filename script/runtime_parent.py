import os
import logging
import sys
import json
import fnmatch
from pathlib import Path


class RuntimeParent(object):
    def __init__(self, logname=__file__, workspace=None):
        """ 
        Provides easy access to the directory space inside docker
        container for a runtime task. This is an abstract parent class
        to be derived for new runtime tasks

        runtime jobs can use inherent variables, logger,
        and upload config builder to simplify tasks

        locally - should have /home/user/workspace directory
        pointed to by run.sh script

        Expected Structure:

        /workspace
        |-- attachments
        |   `-- ...
        |-- files
        |   `-- ...
        |-- cache
        |   `-- ...
        |-- metadata
        |   `-- ...
        |-- secrets
        |   `-- ...
        |-- tmp
        `-- out
        """

        if not workspace:
            workspace = '/workspace'

        self.workspace = Path(workspace).absolute()		# base directory must exist
        self.out = self.workspace / 'out'     		        # results directory - consider this the output write space - do we put a log here too?
        self.files = self.workspace / 'files'      		# files to work with - consider this read only
        self.attachments = self.workspace / 'attachments'       # consider this read only
        self.cache = self.workspace / 'cache'                   # consider this read only
        self.metadata = self.workspace / 'metadata'             # consider this read only - available if iterating over collection - then contains [recording_id.txt, recording.json] files for use
        self.tmp = self.workspace / 'tmp'                       # shared data between images in a multi-image workflow. Contents will not be preserved after task completes.
        self.secrets = self.workspace / 'secrets'               # consider this read only

        self.logger = self.setup_logger(logname)
        self.verifyPaths()
        self.upload = {'upload': [], 'delete': [], 'move': []}

    def add_upload(self, srcpath, target):
        """ srcpath = path to item being uploaded locally.
            target = location on datasets, ex files = files://
        """
        # TODO: make sure to support all types
        assert 'attachments://' in target or 'files://' in target, "Malformed targetpath,"\
            " try something like 'files://' "
        p = Path(srcpath)
        item = {'source': str(p.absolute()), 'target': target}
        self.upload['upload'].append(item)

    def add_delete(self, target):
        assert 'attachments://' in target or 'files://' in target, "Malformed targetpath,"\
            " try something like 'files://' "
        self.upload['delete'].append({'target': target})

    def add_move(self, srcpath, target):
        assert 'attachments://' in target or 'files://' in target, "Malformed targetpath,"\
            " try something like 'files://' "
        p = Path(srcpath)
        item = {'source': str(p.absolute()), 'target': target}
        self.upload['move'].append(item)


    def create_upload_config(self, name='out'):
        """ 
        Creates the upload JSON config file with necessary rules...
        """
        with open(str(self.out / '{}.content.runtime'.format(name)), 'w') as f:
            f.write(json.dumps(self.upload))
        self.logger.info("Content of upload config file:\n{}".format(self.upload))

    def __get__(self, datadir):
        """ 
        Generic path fetcher, to be used for each of the expected directories
        see the 5x get_<DIRECTORY> functions below.
        """
        data = [str(x) for x in datadir.glob("*")]
        for itr, i in enumerate(data):
            p = Path(i)
            if p.is_dir():
                data[itr] = [str(x) for x in p.absolute().glob("*")]
        return data

    def get_attachments(self):
        return self.__get__(self.attachments)

    def get_files(self):
        return self.__get__(self.files)

    def get_cache(self):
        return self.__get__(self.cache)

    def get_metadata(self):
        return self.__get__(self.metadata)

    def get_secrets(self):
        return self.__get__(self.secrets)

    def search(self, searchdir, pattern):
        files = Path(searchdir).glob('**/{}'.format(pattern))
        return [str(f.absolute()) for f in files]

    def setup_logger(self, name=__file__):
        """ 
        Prepares a logger for the child-runtimejob to use throughout the process.
        invoke with self.logger.info("logtext") or replace info with debug/warning/etc
        see logger api for full list of options.
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.propagate = 0
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s: %(name)s: %(message)s')
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        screen_handler.setLevel(logging.DEBUG)
        logger.addHandler(screen_handler)
        return logger

    def verifyPaths(self):
        """ 
        This function verifies the existance of each path
        or reports missing environment expectations
        this environment should have be prepared by the packets run.sh script.
        """
        errs = 0
        check_paths = [self.tmp]
        base_err = 'directory is missing in workspace, expected in:'
        for pathy in check_paths:
            if not pathy.exists():
                warn_msg = "{} {} {}".format(str(pathy.name), base_err, str(pathy))
                self.logger.warning(warn_msg)
                errs += 1
        if errs > 0:
            self.logger.info("{} missing items".format(str(errs)))
            self.logger.info([x for x in self.workspace.glob("*")])
            peak = [x for x in Path('/').glob("*")]
            self.logger.info("{}, {}".format(peak, len(peak)))
        return errs  # returns how many files are missing - incase verification is needed
