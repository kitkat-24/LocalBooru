LocalBooru
==========
An application to organize local media files similarly to an
[image booru.](https://tvtropes.org/pmwiki/pmwiki.php/Main/ImageBooru)

Currently is in early alpha; only half the functionality is implemented in the
GUI, and the underlying structure will certainly evolve as the project develops.
Expect the CLI to not keep up with addition of new features to the GUI, and
possibly be entirely removed in the future.


GUI Manual
==========
Search
------
Searching is performed through the searchbar at the top with tags separated by
spaces. Currently search only displays images matching all tags entered. Meta
tags (such as artist or character can be entered directly (e.g.
"artist:Picasso") or in the format used on the commandline (e.g. "-a Picasso").

Adding Files
------------
Files are added through the plus button in the top left, which will open the
native file browser as a dialog to select (currently only) one file at a time.
Once opened, a dialog will open to allow the user to enter tags. If none are
given, the program will not add the file because we don't want un-tagged files
disappearing in the database but taking up space.

Editing Tags
------------
Press the edit tag button in the bottom left while an image is enlarged. Tags
must be separated by whitespace and/or a semicolon.


Changelog
=========
v0.2.2 (July 11th, 2020)
------------------------
Implemented adding images through the GUI.

v0.2.1 (January 1st, 2020)
--------------------------
Implemented search, display of image tags when focused on (click-to-enlarge
mode), and ability to click on a tag to search for all images with said tag.

v0.2.0 (December 31st, 2019)
----------------------------
Transitioned over to PyQt5. Can theoretically display up to 16 images from the
database with click-to-enlarge and zoom functions. GUI layout v1 is mapped out
but otherwise non-functional.

v0.1.0 (Oct. 3rd, 2019)
-----------------------
First vaguely functional build. Implemented simple homebrew database that works
through a dictionary of the form {file\_id: [list of tags]} and a reverse
dictionary of the form {tag: [list of file\_ids]}.

Acknowledgements
================
Big thank you to [acbetter](https://gist.github.com/acbetter) for their
[PyQt5 Image Viewer demo!](https://gist.github.com/acbetter/32c575803ec361c3e82064e60db4e3e0)

### Functions:

- add: can add a file through the commandline with tags given
- list: lists all tags in the database
- remove: removes a file by UUID (and wipes any singleton tags)
- search: searches for an intersection of tags and returns file UUIDs; returns all files if no tags are given

### Immediate goals:

- Add images thru GUI
- Export images thru GUI
- Delete images thru GUI
- More full-featured search
- Export tags/metadata/archive thru GUI
- Add updating of the tags of a file
