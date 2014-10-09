
import ConfigParser
import os
import exceptions

class Project:
    def __init__(self):
        self.__projectname__=""
        
    def __init__(self, projectfile):
        self.__read_projectfile(projectfile)
        
    def __read_projectfile(self, projectfile):
        config = ConfigParser.ConfigParser()
        config.readfp(open(projectfile))
        
        try:
            self.__projectname = config.get("General", "projectname")
            self.__project_creationdate = config.get("General", "created")            
            self.__project_lastmodified = config.get("General", "lastmodified")
            self.__project_author = config.get("General", "author")
        except MissingSectionHeaderError as e:
            print "Corrupt projectfile: {0}".format(projectfile)
            print "Missing Section Header".format(e.errno, e.strerror)
            raise CorruptProjectFileException("Missing Section Header: {0}, {1}".format(projectfile, e.strerror))
        except NoSectionError as e:
            print "Corrupt project file: {0}".format(projectfile)
            print "No section: {0}, {1}".format(e.errno, e.strerror)
            raise CorruptProjectFileException("Invalid section or section not found: {0}, {1}".format(projectfile, e.strerror))
        except NoOptionError as e:
            print "Corrupt project file: {0}".format(projectfile)
            print "No option: {0}, {1}".format(e.errno, e.strerror)
            raise CorruptProjectFileException("Invalid option or option not found: {0}, {1}".format(projectfile, e.strerror))
        except ParsingError as e:
            print "Corrupt project file: {0}".format(projectfile)
            print "No option: {0}, {1}".format(e.errno, e.strerror)
            raise CorruptProjectFileException("Invalid option or option not found: {0}, {1}".format(projectfile, e.strerror))
        
            
        