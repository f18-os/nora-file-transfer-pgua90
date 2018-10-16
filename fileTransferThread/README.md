# nets-tcp-framed-race

This lab enables the student to create a file transfer between a client and a server, whilst sending this file through 100 bytes at a time, yet instead of the use of 'forking', the file transfer will be transferred via threads, of which the assignment also required that the student was to use mutex in order to prevent race conditions, in the scenario that the same file is sent at the same time .In order to implement this idea, I used the professor's code in order that from there I would attempt to implement the requirements of the assignment, whilst using the code as resource and reference.

RESOURCES USE:
The following resources were used in order to obtain more knowledge in order to attempt and create this.

* Dr. Freudenthal's code.
* The following sites were used:
   * https://www.youtube.com/watch?v=ZwxTGGEx-1w&feature=youtu.be - Video that provides information on how to create a multithreaded server and the use of multiple clients.
   * https://www.tutorialspoint.com/python3/python_networking.htm - Site used as refernce towards sockets and manipulating sockets with Python.
   * https://docs.python.org/3/library/threading.html#module-threading - Site was used in order obtian a deeper knowledge towards thread objects and how to implement them with the use of Python.
   
