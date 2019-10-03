# Usage: python3 LocalBooru.py -a|-s [-a] [-c] [-s] [-t] arg1 arg2 ...
# To add an image:
# python3 LocalBooru.py -a path/to/file.png -artist Bob -character susie -rating safe -series generic_show -tags female clothed cute

import getopt
import pickle
import shutil
import sys
import uuid

from collections import namedtuple


# Tags are expected as arguments IFF if the -t flag is given
short_opt = "hA:Sa:c:r:s:t"
long_opt = "help add= search artist= character= rating= series= tags".split(" ")

# Info tuple for each image
Data = namedtuple('Data', 'artist character rating series tags')


def save_index(obj):
    with open('data/index.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_index():
    with open('data/index.pkl', 'rb') as f:
        return pickle.load(f)

try:
    index = load_index()
except FileNotFoundError:
    index = {} # No existing index

################################################################################

def add(inputfile, opts, tags):
    """Add a file to the database.

    :param inputfile: Path to file to add.
    :param opts: File fields to add.
    :param tags: Tags to add.

    :returns: Nothing.
    """
    outputfile = str(uuid.uuid4())
    shutil.copy2(inputfile, 'data/' + outputfile)

    obj_data = Data(
        artist='',
        character='',
        rating='',
        series='',
        tags=set()
    )

def search(opts, tags):
    """Search the database.

    :param opts: File fields to search by.
    :param tags: Tags to search by.

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
    print(opts)
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
    tags = tags + args
    print(tags)


if __name__ == "__main__":
    main(sys.argv[1:])
