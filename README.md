Getting Started
===============

Tool to print boards from trello

To run this tool, please get py-trello from

  https://github.com/sarumont/py-trello

and install it using pip.

Then generate a developer key using

  https://trello.com/1/appKey/generate

take that key and create an application secret at

  https://trello.com/1/authorize?key=substitutewithyourapplicationkey&name=My+Application&expiration=never&response_type=token

You can now use the developer key as -u and the application secret as -p parameters.

First Steps
===========

The first thing you probably want to do is list all repos:

  $ ./trello.py -u <devkey> -p <secret> -L
    Foo Board
    Bar Board
    Really awesome list

Then you can take one of those boards and check out its contents:

  $ ./trello.py -u <devkey> -p <secret> -b "Foo Board"
    [Todo]
      - Talk about trello-print
    [Done]
      - Write documentation

Congratulations, you can now play with trello-print!
