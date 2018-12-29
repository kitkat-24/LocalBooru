# Usage: python3 LocalBooru.py -a|-s [-a] [-c] [-s] [-t] arg1 arg2 ...
# To add an image:
# python3 LocalBooru.py -a path/to/file.png -artist Bob -character susie -rating safe -series generic_show -tags female clothed cute

import getopt, shutil, sys, uuid, sqlite3

conn = sqlite3.connect('localbooru.db')

# Tags are expected as arguments IFF if the -t flag is given
short_opt = "hA:Sa:c:r:s:t"
long_opt = "help add= search artist= character= rating= series= tag".split(" ")

def add(inputfile, opts, tags):
    """Add a file to the database.

    :param inputfile: Path to file to add.
    :param opts: File fields to add.
    :param tags: Tags to add.

    :returns: Nothing.
    """
    outputfile = str(uuid.uuid4())
    shutil.copy2(inputfile, 'data/' + outputfile)



def search(opts, tags):
    """Search the database.

    :param opts: File fields to search by.
    :param tags: Tags to search by.

    :returns: Nothing.
    """


def main(argv):
    try:
        opts, args = getopt.getopt(argv, short_opt, long_opt)
    except getopt.GetoptError:
        print 'LocalBooru.py -A|-S [filename] -a <artist> -c <character> -r <rating> -s <series> -t <tag1,tag2,...>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'LocalBooru.py -A|-S [filename] -a <artist> -c <character> -r <rating> -s <series> -t <tag1,tag2,...>'
            sys.exit()
        elif opt in ("-A", "--add"):
            add(arg, opts[1:], args)
        elif opt in ("-S", "--search"):
            search(argv[1:])

    print 'Input file is "', inputfile
    print 'Output file is "', outputfile

if __name__ == "__main__":
    main(sys.argv[1:])
