#! /usr/bin/env python

# Author: John Graham
# Date: 07/1/2015

# Description:
# =========================================
# Script to send iPhoto pictures to QNAP869
# =========================================

import sys
import os
import logging
from subprocess import PIPE, Popen

target_nas = 'QNAP869'
fs_mount = '/Volumes/VDIDisks'
rsync_target_directory = '/share/MD0_DATA/Multimedia/Pictures/iPhoto_Library/Originals/'
iphoto_originals = '/Volumes/VDIDisks/iPhoto_Library/Originals/'

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def check_for_process():

    # ==========================================
    # Check for the photoSync.py process running
    # ==========================================

    command = "/bin/ps -ef | /usr/bin/grep rsync | /usr/bin/grep -v grep"

    __sync_process = Popen(command, shell=True,
                           stdout=PIPE,
                           stderr=PIPE)

    __sync_process.wait()

    if __sync_process.returncode == 0:
        logger.info('Sync process is currently running')
        return True
    else:
        logger.info('No active sync processes are running, good to go!')
        return False


def sync_photos():

    # ==========================================================
    # Sync up the Originals folder from iPhoto to QNAP NAS filer
    # ==========================================================

    if os.path.ismount(fs_mount):
        if os.path.isdir(iphoto_originals):
            # ===============
            # Start the rsync
            # ===============

            logger.info('Begining rsync operation')

            try:
                proc = Popen(['/usr/bin/rsync',
                              '-avc',
                              '--sparse',
                              '--progress',
                              '--links',
                              '--hard-links',
                              '-e ssh',
                              iphoto_originals,
                              'admin@qnap869:' + rsync_target_directory])

                proc.wait()
            except OSError, (errno, strerror):
                logger.error('OSError (%s) : %s', (errno, strerror))
        else:
            logger.fatal('Cannot find iPhoto_Originals directory to sync.')
            sys.exit(1)
    else:
        logger.fatal('iPhoto library is not mounted on %s', fs_mount)
        sys.exit(1)


def check_target_nas():
    pass


if __name__ == '__main__':

    if check_for_process():
        logger.info('Stopping execution of this instance')
        sys.exit(1)
    else:
        sync_photos()
