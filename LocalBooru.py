# Usage: python3 LocalBooru.py -a|-s [-a] [-c] [-s] [-t] arg1 arg2 ...
# To add an image:
# python3 LocalBooru.py -a path/to/file.png -artist Bob -character susie -rating safe -series generic_show -tags female clothed cute

import atexit
import getopt
import pickle
import os
import shutil
import sys
import uuid

from collections import namedtuple

import logging
logging.basicConfig(level=logging.DEBUG)

import pprint
pp = pprint.PrettyPrinter(indent=4)


# Tags are expected as arguments IFF if the -t flag is given
short_opt = "hA:LR:Sa:c:r:s:"
long_opt = "help add= list remove= search artist= character= rating= series=".split(" ")


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
    file_index = dict() # No existing index
    logging.info('file_index not found. Created new one.')

try:
    tag_list = load_obj('tag_list')
    logging.info('Loaded tag_list')
    shutil.copy2('data/tag_list.pkl', 'data/tag_list.pkl.backup')
    logging.info('Backed up tag_list')
except FileNotFoundError:
    tag_list = dict() # No existing tag list
    logging.info('tag_list not found. Created new one.')

################################################################################
# Helper Methods                                                               #
################################################################################

# TODO why is tag_list a dict(tag:list) instead of dict(tag:set)? O(n) searches
# could get bad to remove popular tags
def add_tags_to_file(fid, tags):
    """Add a set of tags to a file. The tags are assumed to be unique to the
    file."""
    for tag in tags:
        if tag in tag_list:
            tag_list[tag].append(fid)
        else:
            tag_list[tag] = [fid]

def remove_tags_from_file(fid, tags):
    """Remove a set of tags from a file. The tags are assumed to be actually
    present for the given file."""
    for tag in tags:
        tag_list[tag].remove(fid)
        # If the image was the last one with the given tag, purge the tag
        # from the database.
        if not tag_list[tag]:
            del tag_list[tag]

################################################################################
# Core Methods                                                                 #
################################################################################

def add_file(inputfile, tags):
    """Add a file to the database.

    :param inputfile: Path to file to add.
    :param tags: Set of tags for the file.

    :returns: Nothing.
    """
    file_id = str(uuid.uuid4())
    shutil.copy2(inputfile, 'data/' + file_id)

    tags.add(f'fid:{file_id}')
    file_index[file_id] = tags
    add_tags_to_file(file_id, tags)

    logging.info(f'Created file "{file_id}"')

def get_tags(fids):
    """Return a set of all tags the given file_ids have. If no file_ids are
    given, returns all tags in the database.

    :param fids: Collection of file_ids.

    :returns: A set of tags.
    """
    file_id_list = fids if fids else file_index.keys()
    tags = set()
    for fid in file_id_list:
        tags = tags | file_index[fid] # Perform set union

    # Remove fid tags from display
    return {tag for tag in tags if not "fid:" in tag}

def update_tags(fid, new_tags):
    """For the given file, update its tags and the database as a whole.

    :param fid: File_id of the file to update.
    :param new_tags: A set of tags.
    """
    # We use the set difference operation to handle this cleanly
    old_tags = get_tags([fid])
    add_tags_to_file(fid, new_tags - old_tags)
    remove_tags_from_file(fid, old_tags - new_tags)
    file_index[fid] = new_tags

    logging.info(f'Updated tags of file "{fid}"')

def list_tags():
    """List all tags in the database by printing to stdout.

    :returns: Nothing.
    """
    for tag in sorted(tag_list.keys()):
        # Don't print out every unique file id
        if not 'fid:' in tag:
            print('{}: {}'.format(tag, len(tag_list[tag])))

def remove(fid):
    """Remove an image from the database. If the file is not in the database,
    the method does nothing.

    :param fid: The uuid of the file to remove.

    :returns: Nothing.
    """
    # Returns file_index[fid] or None if fid is not in file_index.
    rm_tags = file_index.pop(fid, None)
    if rm_tags:
        logging.info('Removing file "{}".'.format(fid))
        os.remove(f'data/{fid}')
        remove_tags_from_file(fid, rm_tags)
    else:
        logging.info('File "{}" not found.'.format(fid))

def search(tags):
    """Search the database.

    :param tags: Set of tags to search by.

    :returns: Set of file_ids of files that have all listed tags.
    """
    results = set()
    # If given no tags, just return all files
    if not tags:
        results = set(file_index.keys())
    # Otherwise, perform search
    else:
        for tag in tags:
            if tag in tag_list:
                if results:
                    results &= set(tag_list[tag])
                else:
                    results = set(tag_list[tag])

    if results:
        return results
    else:
        logging.info('No files tagged with "{}" found.'.format(" ".join(sorted(tags))))
        return None

#-------------------------------------------------------------------------------

def parse_args(args):
    """
    Parses input arguments.

    :param args: List of commandline arguments.

    :returns: Tuple (operation, tags)
        operation: string denoting the operation
        tags: set of tags
    """
    help_str = 'LocalBooru.py [-A filename] | [-L] | [-R uuid] | [-S]  -a <artist> -c <character> -r <rating> -s <series> <tag1 tag2 ...>'

    try:
        opts, args = getopt.gnu_getopt(args, short_opt, long_opt)
    except getopt.GetoptError:
        print(help_str)
        sys.exit(2)

    operation = None
    tags = []
    filename = ''
    fid = ''
    for opt, arg in opts:
        if opt == '-h':
            print(help_str)
            sys.exit()
        elif opt in ("-A", "--add"):
            operation = 'add'
            filename = arg
        elif opt in ("-L", "--list"):
            operation = 'list'
        elif opt in ("-R", "--remove"):
            operation = 'remove'
            fid = arg
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

    # Append all tags (non-specific args; get_opt removes all used options
    # and arguments from the argument list it is passed).
    tags = set(tags + args)

    return operation, tags, filename, fid

def call_operation(operation, tags, filename='', fid=''):
    """
    Calls the appropriate operation.

    :param operation: A string with the name of the operation.
    :param tags: A set of the tags for the operation.

    :returns: The result of the operation.
    """
    if operation == 'add':
        if filename:
            return add(filename, tags)
        else:
            print('Invalid filename specified.')
            sys.exit(2)
    elif operation == 'list':
        return list_tags()
    elif operation == 'remove':
        return remove(fid)
    elif operation == 'search':
        return search(tags)



def main(args):
    operation, tags, filename, fid = parse_args(args)
    return call_operation(operation, tags, filename, fid)



def exit_handler():
    save_obj('file_index', file_index)
    save_obj('tag_list', tag_list)
    logging.info('Saved updated indices')

atexit.register(exit_handler)

if __name__ == "__main__":
    main(sys.argv[1:])
