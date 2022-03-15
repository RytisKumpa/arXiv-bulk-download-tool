import boto3
import os
from argparse import ArgumentParser
import xml.etree.ElementTree as ET
import time

def main(**kwargs):
    manifest_file = kwargs['old_manifest']
    type = kwargs['type']
    log_file_path = kwargs['log_file']
    year = kwargs['spec_year']
    s3 = boto3.client('s3')
    if manifest_file == None:
        with open(os.path.join(type, 'manifest.xml'), 'wb') as file:
            s3.download_fileobj('arxiv', '{}/arXiv_{}_manifest.xml'.format(type, type), file,
                                {'RequestPayer': 'requester'})
        print('Manifest downloaded.')

    log_file = open(log_file_path, 'w')
    tree = ET.parse('{}/manifest.xml'.format(type))
    root = tree.getroot()
    start_time = time.time()
    for file in root.findall('file'):
        filename = file.find('filename').text
        current_year = file.find('yymm').text[:2]
        if current_year == year[2:]:
            if os.path.isfile(filename) is False or os.path.getsize(filename) == 0:
                print('Downloading: {}'.format(filename))
                with open(filename, 'wb') as file:
                    s3.download_fileobj('arxiv', filename, file,
                                    {'RequestPayer': 'requester'})
                elapsed_time = time.time() - start_time
                elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                print('{} downloaded. Time spent: {}'.format(filename, elapsed_time))
                log_file.write(filename + '\n')

    log_file.close()
    print('Download finished.')

if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('--old_manifest', '-m', type=str, default=None, help='Type the location of the manifest file. Do not provide this argument if you fish for the new manifest file to be dowloaded.')
    ap.add_argument('--type', type=str, default='src', choices=set(('pdf', 'src')),
                  help='File type can only be "pdf" or "src".')
    ap.add_argument('--log_file', default='processed.txt', help='A file that logs the downloaded files.')
    ap.add_argument('--spec_year', type=str, default='2018', help='Specify the year of which to download the files. 2018 by default.')
    kwargs = ap.parse_args()
    main(**vars(kwargs))