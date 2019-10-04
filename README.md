LocalBooru
==========
An application to organize local media files similarly to an image booru.

Currently is in very early alpha and only works as a clunky CLI program. A GUI
and functionality to make it easier for users to install and run is planned.



Changelog
=========

v0.1.0 (Oct. 3rd, 2019)
-----------------------
First vaguely functional build. Implemented simple homebrew database that works
through a dictionary of the form {file\_id: [list of tags]} and a reverse
dictionary of the form {tag: [list of file\_ids]}.

### Functions:

- add: can add a file through the commandline with tags given
- list: lists all tags in the database
- remove: removes a file by UUID (and wipes any singleton tags)
- search: searches for an intersection of tags and returns file UUIDs; returns all files if no tags are given

### Immediate goals:

- Add updating of the tags of a file
- More full-featured search
- Preliminary display of images on search
