lst - manage lists in files
===========================

I keep lot of lists, usually I edit them with vim, this will end... today.

lst is a small program that provides functionality to manipulate lists of
things.

general help
------------

::

	usage: lst [-h] {add,remove,purge,slice,head,tail,filter,export} ...

	positional arguments:
	  {add,remove,purge,slice,head,tail,filter,export}
	    add                 add an element to a list
	    remove              remove element from list
	    purge               purge removed items from the file
	    slice               show a slice of the list
	    head                show the first N elements of the list
	    tail                show the last N elements of the list
	    filter              show elements that match the filter

	optional arguments:
	  -h, --help            show this help message and exit

add command
-----------

::

	usage: lst add [-h] [-a | -i INDEX] [-t TAG [TAG ...]] LIST MSG [MSG ...]

	positional arguments:
	  LIST
	  MSG

	optional arguments:
	  -h, --help            show this help message and exit
	  -t TAG [TAG ...], --tags TAG [TAG ...]
				tag message with specified tag

examples
::::::::

::

        # add item with tags

        ➜  ~  lst add todos do something interesting -t tag1 tag2 tag3
        * Tue Jul 10 17:55:46 2012 do something interesting # tag1 tag2 tag3

        # add item without tags

        ➜  ~  lst add todos do something else
        * Tue Jul 10 17:55:55 2012 do something else


remove command
--------------

::

	usage: lst remove [-h] [-a | -i INDEX [INDEX ...]] [-f] LIST

	positional arguments:
	  LIST

	optional arguments:
	  -h, --help            show this help message and exit
	  -a, --all             remove all elements from list
	  -i INDEX [INDEX ...], --index INDEX [INDEX ...]
				remove elements at index
	  -f, --force           don't ask for confirmation

examples
::::::::

::

        # example items from a list

        0 * Tue Jul 10 17:55:46 2012 do something interesting # tag1 tag2 tag3
        1 * Tue Jul 10 17:55:55 2012 do something else
        2 * Tue Jul 10 17:59:20 2012 conquer the world
        3 * Tue Jul 10 17:59:28 2012 do this demo # recursive

        # remove the item at index 1

        ➜  ~  lst remove todos -i 1

        # result

        0 * Tue Jul 10 17:55:46 2012 do something interesting # tag1 tag2 tag3
        1 x Tue Jul 10 17:55:55 2012 do something else
        2 * Tue Jul 10 17:59:20 2012 conquer the world
        3 * Tue Jul 10 17:59:28 2012 do this demo # recursive

        # remove items at index 0 and 3
        ➜  ~  lst remove todos -i 0 3

        # result

        0 x Tue Jul 10 17:55:46 2012 do something interesting # tag1 tag2 tag3
        1 x Tue Jul 10 17:55:55 2012 do something else
        2 * Tue Jul 10 17:59:20 2012 conquer the world
        3 x Tue Jul 10 17:59:28 2012 do this demo # recursive


purge command
-------------

::

	usage: lst purge [-h] [-f] LIST

	positional arguments:
	  LIST

	optional arguments:
	  -h, --help   show this help message and exit
	  -f, --force  don't ask for confirmation

examples
::::::::

::

        # example items from a list

        0 x Tue Jul 10 17:55:46 2012 do something interesting # tag1 tag2 tag3
        1 x Tue Jul 10 17:55:55 2012 do something else
        2 * Tue Jul 10 17:59:20 2012 conquer the world
        3 x Tue Jul 10 17:59:28 2012 do this demo # recursive

        ➜  ~  lst purge todos
        are you sure you want to purge the list? [yes/no] yes

        # result (removed items are completely removed from the list)

        0 * Tue Jul 10 17:59:20 2012 conquer the world

slice command
-------------

::

	usage: lst slice [-h] [-a] [-i] LIST BEGIN END STEP

	positional arguments:
	  LIST
	  BEGIN
	  END
	  STEP

	optional arguments:
	  -h, --help        show this help message and exit
	  -a, --show-all    show removed elements too
	  -i, --show-index  show the absolute index of the item

examples
::::::::

::

        # slice from 0 to 2 with step 1

        ➜  ~  lst slice todos 0 2 1
        * Tue Jul 10 17:59:20 2012 conquer the world
        * Tue Jul 10 18:02:16 2012 do thing 1

        # same as before but displaying index

        ➜  ~  lst slice todos 0 2 1 -i
        0 * Tue Jul 10 17:59:20 2012 conquer the world
        1 * Tue Jul 10 18:02:16 2012 do thing 1

        # slice from 0 to 4 with step 2 showing index

        ➜  ~  lst slice todos 0 4 2 -i
        0 * Tue Jul 10 17:59:20 2012 conquer the world
        2 * Tue Jul 10 18:02:16 2012 do thing 1

        # slice from 0 to 4 with step 1 showing index

        ➜  ~  lst slice todos 0 4 1 -i
        0 * Tue Jul 10 17:59:20 2012 conquer the world
        1 * Tue Jul 10 18:02:16 2012 do thing 1
        3 * Tue Jul 10 18:02:28 2012 do thing 3 # tag task3

        # slice from 0 to 4 with step 1 showing index and removed items

        ➜  ~  lst slice todos 0 4 1 -i -a
        0 * Tue Jul 10 17:59:20 2012 conquer the world
        1 * Tue Jul 10 18:02:16 2012 do thing 1
        2 x Tue Jul 10 18:02:19 2012 do thing 2 # tag
        3 * Tue Jul 10 18:02:28 2012 do thing 3 # tag task3

head command
------------

::

	usage: lst head [-h] [-a] [-i] [-c COUNT] LIST

	positional arguments:
	  LIST

	optional arguments:
	  -h, --help            show this help message and exit
	  -a, --show-all        show removed elements too
	  -i, --show-index      show the absolute index of the item
	  -c COUNT, --count COUNT

examples
::::::::

::

        # list first items with default count (10)

        ➜  ~  lst head todos 
        * Tue Jul 10 17:59:20 2012 conquer the world
        * Tue Jul 10 18:02:16 2012 do thing 1
        * Tue Jul 10 18:02:19 2012 do thing 2 # tag
        * Tue Jul 10 18:02:28 2012 do thing 3 # tag task3
        * Tue Jul 10 18:02:35 2012 do thing 4 # task task4
        * Tue Jul 10 18:02:43 2012 do thing 5 # task

        # list first two

        ➜  ~  lst head todos -c 2
        * Tue Jul 10 17:59:20 2012 conquer the world
        * Tue Jul 10 18:02:16 2012 do thing 1

        # list first 4 with index

        ➜  ~  lst head todos -c 4 -i
        0 * Tue Jul 10 17:59:20 2012 conquer the world
        1 * Tue Jul 10 18:02:16 2012 do thing 1
        2 * Tue Jul 10 18:02:19 2012 do thing 2 # tag
        3 * Tue Jul 10 18:02:28 2012 do thing 3 # tag task3

        # remove one

        ➜  ~  lst remove todos -i 2

        # list again (see that item at index 2 is missing)

        ➜  ~  lst head todos -i     
        0 * Tue Jul 10 17:59:20 2012 conquer the world
        1 * Tue Jul 10 18:02:16 2012 do thing 1
        3 * Tue Jul 10 18:02:28 2012 do thing 3 # tag task3
        4 * Tue Jul 10 18:02:35 2012 do thing 4 # task task4
        5 * Tue Jul 10 18:02:43 2012 do thing 5 # task

        # list all (see that item at index 2 is marked as removed)

        ➜  ~  lst head todos -i -a
        0 * Tue Jul 10 17:59:20 2012 conquer the world
        1 * Tue Jul 10 18:02:16 2012 do thing 1
        2 x Tue Jul 10 18:02:19 2012 do thing 2 # tag
        3 * Tue Jul 10 18:02:28 2012 do thing 3 # tag task3
        4 * Tue Jul 10 18:02:35 2012 do thing 4 # task task4
        5 * Tue Jul 10 18:02:43 2012 do thing 5 # task


tail command
------------

::

	usage: lst tail [-h] [-a] [-i] [-c COUNT] LIST

	positional arguments:
	  LIST

	optional arguments:
	  -h, --help            show this help message and exit
	  -a, --show-all        show removed elements too
	  -i, --show-index      show the absolute index of the item
	  -c COUNT, --count COUNT

examples
::::::::

::

        # list last items with default count (10)

        ➜  ~  lst tail todos
        * Tue Jul 10 17:59:20 2012 conquer the world
        * Tue Jul 10 18:02:16 2012 do thing 1
        * Tue Jul 10 18:02:28 2012 do thing 3 # tag task3
        * Tue Jul 10 18:02:35 2012 do thing 4 # task task4
        * Tue Jul 10 18:02:43 2012 do thing 5 # task

        # list last two

        ➜  ~  lst tail todos -c 2
        * Tue Jul 10 18:02:35 2012 do thing 4 # task task4
        * Tue Jul 10 18:02:43 2012 do thing 5 # task

        # list last 4 with index

        ➜  ~  lst tail todos -c 4 -i
        1 * Tue Jul 10 18:02:16 2012 do thing 1
        3 * Tue Jul 10 18:02:28 2012 do thing 3 # tag task3
        4 * Tue Jul 10 18:02:35 2012 do thing 4 # task task4
        5 * Tue Jul 10 18:02:43 2012 do thing 5 # task

        # list all (see that item at index 2 is marked as removed)

        ➜  ~  lst tail todos -c 4 -i -a
        2 x Tue Jul 10 18:02:19 2012 do thing 2 # tag
        3 * Tue Jul 10 18:02:28 2012 do thing 3 # tag task3
        4 * Tue Jul 10 18:02:35 2012 do thing 4 # task task4
        5 * Tue Jul 10 18:02:43 2012 do thing 5 # task


filter command
--------------

::

	usage: lst filter [-h] [-a] [-i] [-t TAG [TAG ...] | -T TAG [TAG ...]]
			  LIST [QUERY [QUERY ...]]

	positional arguments:
	  LIST
	  QUERY

	optional arguments:
	  -h, --help            show this help message and exit
	  -a, --show-all        show removed elements too
	  -i, --show-index      show the absolute index of the item
	  -t TAG [TAG ...], --tags TAG [TAG ...]
				show elements that have *any* of the tags
	  -T TAG [TAG ...], --all-tags TAG [TAG ...]
				show elements that have *all* of the tags

examples
::::::::

::

        # apply no filter

        ➜  ~  lst filter todos
        * Tue Jul 10 17:59:20 2012 conquer the world
        * Tue Jul 10 18:02:16 2012 do thing 1
        * Tue Jul 10 18:02:28 2012 do thing 3 # tag task3
        * Tue Jul 10 18:02:35 2012 do thing 4 # task task4
        * Tue Jul 10 18:02:43 2012 do thing 5 # task

        # list items that contain the word "thing"

        ➜  ~  lst filter todos thing
        * Tue Jul 10 18:02:16 2012 do thing 1
        * Tue Jul 10 18:02:28 2012 do thing 3 # tag task3
        * Tue Jul 10 18:02:35 2012 do thing 4 # task task4
        * Tue Jul 10 18:02:43 2012 do thing 5 # task

        # list items that contain the word "thing" or the tag "task"

        ➜  ~  lst filter todos thing -t task
        * Tue Jul 10 18:02:16 2012 do thing 1
        * Tue Jul 10 18:02:28 2012 do thing 3 # tag task3
        * Tue Jul 10 18:02:35 2012 do thing 4 # task task4
        * Tue Jul 10 18:02:35 2012 do thing 4 # task task4
        * Tue Jul 10 18:02:43 2012 do thing 5 # task
        * Tue Jul 10 18:02:43 2012 do thing 5 # task

        # list items that contain the tag "task"

        ➜  ~  lst filter todos -t task      
        * Tue Jul 10 18:02:35 2012 do thing 4 # task task4
        * Tue Jul 10 18:02:43 2012 do thing 5 # task

        # list items that contain the tag "task" or "tag"

        ➜  ~  lst filter todos -t task tag
        * Tue Jul 10 18:02:28 2012 do thing 3 # tag task3
        * Tue Jul 10 18:02:35 2012 do thing 4 # task task4
        * Tue Jul 10 18:02:43 2012 do thing 5 # task

        # list items that contain the tag "task" and "tag"

        ➜  ~  lst filter todos -T task tag

        # list items that contain the tag "task" and "task4"

        ➜  ~  lst filter todos -T task task4
        * Tue Jul 10 18:02:35 2012 do thing 4 # task task4

        # list items that contain the tag "task" or "task4"

        ➜  ~  lst filter todos -t task task4
        * Tue Jul 10 18:02:35 2012 do thing 4 # task task4
        * Tue Jul 10 18:02:43 2012 do thing 5 # task

        # list items that contain the word "world"

        ➜  ~  lst filter todos world        
        * Tue Jul 10 17:59:20 2012 conquer the world


configuration
-------------

by default the configuration is looked up in .config/lst

the file contains a JSON object with the configuration of the program with
the following subojects:

lists
.....

the lists object contains as keys the names of the lists that you want to
configure and as values the configuration for those lists, for example:

if the path to a list doesn't exists it's created::

	{
	    "lists": {
		"links": {
		    "format": "src/me/links/%Y/%m.links" // strftime format can be used
		}
	    }
	}


fields
::::::

format
        is the path to the list, you can use *~* to refer to the user's home
        and any format from datetime.strftime

details
-------

license
.......

MIT + optional beer for the author

author
......

marianoguerra

tools
.....

python 3
