# Usage: python3 LocalBooru.py -a|-s [-a] [-c] [-s] [-t] arg1 arg2 ...
# To add an image:
# python3 LocalBooru.py -a path/to/file.png -artist Bob -character susie -rating safe -series generic_show -tags female clothed cute

import atexit
import getopt
import pickle
import shutil
import sys
import uuid

from collections import namedtuple

import logging
logging.basicConfig(level=logging.DEBUG)


# Tags are expected as arguments IFF if the -t flag is given
short_opt = "hA:Sa:c:r:s:t"
long_opt = "help add= search artist= character= rating= series= tags".split(" ")

# Info tuple for each image
Data = namedtuple('Data', 'artist character rating series tags')


def save_obj(name, obj):
    with open(f'data/{name}.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(f'data/{name}.pkl', 'rb') as f:
        return pickle.load(f)

# Load database
try:
    file_index = load_obj('file_index')
    logging.info('Loaded file_index')
    shutil.copy2('data/file_index.pkl', 'data/file_index.pkl.backup')
    logging.info('Backed up file_index')
except FileNotFoundError:
    file_index = {} # No existing index

try:
    tag_list = load_obj('tag_list')
    logging.info('Loaded tag_list')
    shutil.copy2('data/tag_list.pkl', 'data/tag_list.pkl.backup')
    logging.info('Backed up tag_list')
except FileNotFoundError:
    tag_list = set() # No existing tag list

################################################################################

def add(inputfile, tags):
    """Add a file to the database.

    :param inputfile: Path to file to add.
    :param tags: Set of tags for the file.

    :returns: Nothing.
    """
    file_id = str(uuid.uuid4())
    shutil.copy2(inputfile, 'data/' + file_id)

    tags.add(f'fid:{file_id}')
    file_index[file_id] = tags
    for tag in tags:
        tag_list.add(tag)
    logging.info(f'Created file "{file_id}"')

def search(tags):
    """Search the database.

    :param tags: Set of tags to search by.

    :returns: Nothing.
    """
    results = set()
    for tag in tags:
        for image in index:
            if tag in image.tags:
                results.add(image)

    return results

################################################################################

def main(args):
    help_str = 'LocalBooru.py [-A]|[-S [filename]] -a <artist> -c <character> -r <rating> -s <series> <tag1 tag2 ...>'

    try:
        opts, args = getopt.gnu_getopt(args, short_opt, long_opt)
    except getopt.GetoptError:
        print(help_str)
        sys.exit(2)

    # Parse input
    tags = []
    for opt, arg in opts:
        if opt == '-h':
            print(help_str)
            sys.exit()
        elif opt in ("-A", "--add"):
            operation = 'add'
            filename = arg
        elif opt in ("-S", "--search"):
            operation = 'search'
        elif opt in ("-a", "--artist"):
            tags.append(f'artist:{arg}')
        elif opt in ("-c", "--character"):
            tags.append(f'character:{arg}')
        elif opt in ("-r", "--rating"):
            tags.append(f'rating:{arg}')
        elif opt in ("-s", "--series"):
            tags.append(f'series:{arg}')

    # Append all tags (non-specific args; get_opt removes all used options and
    # arguments from the argument list it is passed).
    tags = set(tags + args)

    # Perform DB operation
    if operation == 'add':
        add(filename, tags)
    elif operation == 'search':
        search(tags)


def exit_handler():
    save_obj('file_index', file_index)
    save_obj('tag_list', tag_list)
    logging.info('Saved updated indices')


if __name__ == "__main__":
    atexit.register(exit_handler)
    main(sys.argv[1:])
