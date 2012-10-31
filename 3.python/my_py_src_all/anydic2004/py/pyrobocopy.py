""" pyrobocopy.py -

    Version: 0.1
    
    Report the difference in content
    of two directories, synchronize or
    update a directory from another, taking
    into account time-stamps of files etc.

    By Anand B Pillai 

    (This program is inspired by the windows
    'Robocopy' program.)
        
"""

import os, stat
import shutil

def usage():
    return """
Pyrobocopy: Advanced directory synchronization tool

Usage: pyrobocopy.py <sourcedir> <targetdir> Options

Main Options:\n
\t -d --diff        - Only report difference between sourcedir and targetdir
\t-s, --synchronize - Synchronize content between sourcedir and targetdir
\t-u, --update      - Update existing content between sourcedir and targetdir

Additional Options:\n
\t-p, --purge       - Purge files when synchronizing (does not purge by default).
\t-f, --force       - Force copying of files, by trying to change file permissions.
\t-n, --nodirection - Update files in source directory from target
\t                    directory (only updates target from source by default).
"""                   



class PyRobocopier:
    """ An advanced directory synchornization, updation
    and file copying class """
    
    def __init__(self):

        self.__dir1 = ''
        self.__dir2 = ''
        self.__copyfiles = True
        self.__forcecopy = False
        self.__copydirection = 0
        self.__updatefiles = True
        self.__creatdirs = True
        self.__purge=False
        self.__count = 0
        self.__mainfunc = None

        self.__numdirs=0
        self.__numfiles=0
        self.__numdelfiles=0
        self.__numdeldirs=0     
        self.__numnewdirs=0
        self.__numupdates=0
        

    def parse_args(self, arguments):
        """ Parse arguments """
        
        import getopt
        
        optlist, args = getopt.getopt( arguments, 'supn', ["synchronize=", "update=", "purge=", "nodirection="])

        if len(optlist):
            self.__setargs([x[0] for x in optlist])
        else:
            self.__setargs(args)
            
    def __setargs(self, argslist):
        """ Sets internal variables using arguments """
        
        for option in argslist:
            if option.lower() in ('-s', '--synchronize'):
                self.__mainfunc = self.synchronize
            elif option.lower() in ('-u', '--update'):
                self.__mainfunc = self.update
            elif option.lower() in ('-d', '--diff'):
                self.__mainfunc = self.dirdiff
            elif option.lower() in ('-p', '--purge'):
                self.__purge = True
            elif option.lower() in ('-n', '--nodirection'):
                self.__copydirection = 2
            elif option.lower() in ('-f', '--force'):
                self.__forcecopy = True
                
            else:
                if self.__dir1=='':
                    self.__dir1 = option
                elif self.__dir2=='':
                    self.__dir2 = option
                
        if self.__dir1=='' or self.__dir2=='':
            sys.exit("Error, directory arguments not given!")
        if not os.path.exists(self.__dir1) or not os.path.exists(self.__dir2):
            sys.exit("Error, directories does not exist!")          
        if self.__mainfunc is None:
            sys.exit("Error, specify an action (diff, synchronize, update) ")

    def do_work(self):
        """ Do work """
        
        self.__mainfunc()
        
    def __dowork(self, dir1, dir2, copyfunc = None, updatefunc = None):
        """ Private attribute for doing work """
        
        list1 = os.listdir(dir1)
        list2 = os.listdir(dir2)

        print 'Source directory: ', dir1, ':'

        self.__numdirs += 1
        
        # Do any purging if needed
        if self.__purge:
            for f2 in list2:
                fullf2 = os.path.join(dir2, f2)

                # See if this exists on dir1
                if not os.path.exists(os.path.join(dir1, f2)):
                    print 'Purging ', fullf2
                    try:
                        if os.path.isfile(fullf2):
                            os.remove(fullf2)
                            self.__numdelfiles += 1
                            
                        elif os.path.isdir(fullf2):
                            os.removedirs(fullf2)
                            self.__numdeldirs += 1
                            
                    except Exception, e:
                        print e
                        continue


        for f1 in list1:
            try:
                st = os.lstat(os.path.join(dir1, f1))
            except os.error:
                continue

            if stat.S_ISREG(st.st_mode):
                try:
                    list2.index(f1)
                    if updatefunc: updatefunc(f1, dir1, dir2)
                except ValueError:
                    if copyfunc: copyfunc(f1, dir1, dir2)
                    print '>>', f1
                    self.__count += 1

            elif stat.S_ISDIR(st.st_mode):
                # Locate the same directory from dir2
                fulld1 = os.path.join(dir1, f1)
                fulld2 = os.path.join(dir2, f1)

                if not os.path.exists(fulld2):
                    if self.__creatdirs:
                        try:
                            print 'Making directory ', fulld2
                            os.makedirs(fulld2)
                            self.__numnewdirs += 1
                        except:
                            continue

                # Call tail recursive
                if os.path.exists(fulld2):
                    self.__dowork(fulld1, fulld2, copyfunc, updatefunc)

    def __copy(self, filename, dir1, dir2):
        """ Private function for copying a file """

        # NOTE: dir1 is source & dir2 is target
        if self.__copyfiles:

            print 'Copying file', filename, dir1, dir2
            try:
                if self.__copydirection== 0 or self.__copydirection == 2:  # source to target
                    # print 'COPY DIRECTION IS ', self.__copydirection
                    
                    if not os.path.exists(dir2):
                        if self.__forcecopy:
                            os.chmod(os.path.dirname(dir2), 0777)
                        os.makedirs(dir1)
                        
                    if self.__forcecopy:
                        os.chmod(dir2, 0777)

                    sourcefile = os.path.join(dir1, filename)
                    shutil.copy(sourcefile, dir2)
                    self.__numfiles += 1
                    
                elif self.__copydirection==1 or self.__copydirection == 2: # target to source 

                    if not os.path.exists(dir1):
                        if self.__forcecopy:
                            os.chmod(os.path.dirname(dir1), 0777)
                            
                        os.makedirs(dir1)

                    targetfile = os.path.abspath(os.path.join(dir1, filename))
                    if self.__forcecopy:
                        os.chmod(dir1, 0777)

                    sourcefile = os.path.join(dir2, filename)
                    shutil.copy(sourcefile, dir1)
                    self.__numfiles += 1
                    
            except Exception, e:
                print 'Error copying  file', filename, e

    def __update(self, filename, dir1, dir2):
        """ Private function for updating a file based on
        last time stamp of modification """

        print 'Updating file', filename
        
        # NOTE: dir1 is source & dir2 is target        
        if self.__updatefiles:

            file1 = os.path.join(dir1, filename)
            file2 = os.path.join(dir2, filename)

            try:
                st1 = os.lstat(file1)
                st2 = os.lstat(file2)
            except os.error:
                return -1

            # Update will update in both directions depending
            # on the timestamp of the file & copy-direction.

            if self.__copydirection==0 or self.__copydirection == 2:
                if st1.st_mtime > st2.st_mtime:
                    print 'Updating file ', file2 # source to target
                    try:
                        if self.__forcecopy:
                            os.chmod(file2, 0666)

                        shutil.copy(file1, file2)
                        self.__numupdates += 1                      
                        return 0                    
                    except Exception, e:
                        print e
                        return -1

            elif self.__copydirection==1 or self.__copydirection == 2:
                if st2.st_mtime > st1.st_mtime:
                    print 'Updating file ', file1 # target to source
                    try:
                        if self.__forcecopy:
                            os.chmod(file1, 0666)

                        shutil.copy(file2, file1)
                        self.__numupdates += 1                                              
                        return 0
                    except Exception, e:
                        print e
                        return -1

        return -1

    def __dirdiffandcopy(self, dir1, dir2):
        """ Private function which does directory diff & copy """
        self.__dowork(dir1, dir2, self.__copy)

    def __dirdiffandupdate(self, dir1, dir2):
        """ Private function which does directory diff & update  """        
        self.__dowork(dir1, dir2, None, self.__update)

    def __dirdiffcopyandupdate(self, dir1, dir2):
        """ Private function which does directory diff, copy and update (synchro) """               
        self.__dowork(dir1, dir2, self.__copy, self.__update)

    def __dirdiff(self, dir1, dir2):
        """ Private function which only does directory diff """
        self.__dowork(dir1, dir2)

    def synchronize(self):
        """ Synchronize will try to synchronize two directories w.r.t
        each other's contents, copying files if necessary from source
        to target, and creating directories if necessary. If the optional
        argument purge is True, directories in target (dir2) that are
        not present in the source (dir1) will be deleted . Synchronization
        is done in the direction of source to target """

        self.__copyfiles = True
        self.__updatefiles = True
        self.__creatdirs = True
        self.__copydirection = 0
        
        print 'Synchronizing directory', self.__dir2, 'with', self.__dir1 ,'\n'
        self.__dirdiffcopyandupdate(self.__dir1, self.__dir2)

    def update(self):
        """ Update will try to update the target directory
        w.r.t source directory. Only files that are common
        to both directories will be updated, no new files
        or directories are created """

        self.__copyfiles = False
        self.__updatefiles = True
        self.__purge = False
        self.__creatdirs = False

        print 'Updating directory', self.__dir2, 'from', self.__dir1 , '\n'
        self.__dirdiffandupdate(self.__dir1, self.__dir2)

    def dirdiff(self):
        """ Only report difference in content between two
        directories """

        self.__copyfiles = False
        self.__updatefiles = True
        self.__purge = False
        self.__creatdirs = False
        self.__updatefiles = False
        
        print 'Difference of directory ', self.__dir2, 'from', self.__dir1 , '\n'
        self.__dirdiff(self.__dir1, self.__dir2)
        
    def report(self):
        """ Print report of work at the end """

        print '\nPython robocopier finished.'
        print self.__numdirs, 'directories parsed'
        print self.__numfiles, 'files copied'
        if self.__purge:
            print self.__numdelfiles, 'files purged'
        if self.__creatdirs:
            print self.__numnewdirs, 'directories created'
        if self.__updatefiles:
            print self.__numupdates, 'files updated by timestamp'
        
if __name__=="__main__":
    import sys

    if len(sys.argv)<2:
        sys.exit(usage())

    copier = PyRobocopier()
    copier.parse_args(sys.argv[1:])
    copier.do_work()

    # print report at the end
    copier.report()
