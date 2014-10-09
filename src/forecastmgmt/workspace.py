__author__="vvladych"
__date__ ="$21.09.2014 23:57:13$"

import os


class WorkspaceConst:
    ProjectFilename=".fcproject"

class Workspace:
    def __init__(self):
        self.__working_directory="./"
        self.__project_list=[]
        self.__current_project=None
        
    def set_working_directory(self, working_directory):
        self.__working_directory=working_directory
        
    def get_working_directory(self):
        return self.__working_directory
    
    # from http://stackoverflow.com/questions/16953842/using-os-walk-to-recursively-traverse-directories-in-python
    def __traverse_working_directory(self):
        for root, dirs, files in os.walk(self.__working_directory):
            path = root.split("/")
            for file in files:
                if file == WorkspaceConst.ProjectFilename:
                    print "create a project from the filename "+file
                    
    def get_current_project(self):
        return __current_project;
                        