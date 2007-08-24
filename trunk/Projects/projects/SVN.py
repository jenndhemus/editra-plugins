#!/usr/bin/env python

import re, os
from SourceControl import SourceControl

class SVN(SourceControl):

    command = 'svn'
    
    def isControlled(self, path):
        """ Is the path controlled by CVS? """
        if os.path.isdir(path):
            if os.path.isfile(os.path.join(path,'.svn','all-wcprops')):
                return True
        path, basename = os.path.split(path)
        svndir = os.path.join(path,'.svn')
        if os.path.isdir(svndir):
            try:
                for line in open(os.path.join(svndir,'all-wcprops')):
                    if line.startswith('/'):
                        filename = line.split('/')[-1].strip()
                        if filename == basename:
                            return True
            except (IOError, OSError):
                pass
        return False
        
    def add(self, paths):
        """ Add paths to the repository """
        for path in paths:
            root, files = self.splitFiles(path)
            out = self.run(root, ['add'] + files)
            self.logOutput(out)
        
    def checkout(self, paths):
        for path in paths:
            root, files = self.splitFiles(path)
            out = self.run(root, ['checkout'] + files)
            self.logOutput(out)
        
    def commit(self, paths, message=''):
        """ Commit paths to the repository """
        for path in paths:
            root, files = self.splitFiles(path)
            out = self.run(root, ['commit', '-m', message] + files)
            self.logOutput(out)
                                   
    def diff(self, paths):
        for path in paths:
            root, files = self.splitFiles(path)
            out = self.run(root, ['diff'] + files)
            self.closeProcess(out)
        
    def history(self, paths, history=[]):
        for path in paths:
            root, files = self.splitFiles(path)
            for file in files:
                out = self.run(root, ['log', file])
                if out:
                    for line in out.stdout:
                        self.log(line)
                        if line.strip().startswith('-----------'):
                            current = {'path':file}
                            history.append(current)
                            for data in out.stdout:
                                self.log(data)
                                rev, author, date, lines = data.split(' | ')
                                current['revision'] = rev
                                current['author'] = author
                                current['date'] = date
                                current['log'] = ''
                                self.log(out.stdout.next())
                                break
                        else:
                            current['log'] += line
                self.logOutput(out)
                history.pop()
        return history
        
    def remove(self, paths):
        """ Recursively remove paths from repository """
        for path in paths:
            root, files = self.splitFiles(path)
            out = self.run(root, ['remove'] + files)
            self.logOutput(out)
        
    def status(self, paths, recursive=False, status={}):
        """ Get SVN status information from given file/directory """
        codes = {' ':'uptodate', 'A':'added', 'C':'conflict', 'D':'deleted',
                 'M':'modified'}
        options = ['status', '-v']
        if not recursive:
            options.append('-N')
        for path in paths:
            root, files = self.splitFiles(path)
            out = self.run(root, options + files)
            if out:
                for line in out.stdout:
                    self.log(line)
                    name = line.strip().split()[-1]
                    try: status[name] = {'status':codes[line[0]]}
                    except KeyError: pass
                self.logOutput(out)
        return status

    def update(self, paths):
        """ Recursively update paths """
        for path in paths:
            root, files = self.splitFiles(path)
            out = self.run(root, ['update'] + files)
            self.logOutput(out)
            
    def revert(self, paths):
        """ Recursively revert paths to repository version """
        for path in paths:
            root, files = self.splitFiles(path)
            if not files:
                files = ['.']
            out = self.run(root, ['revert','-R'] + files)
            self.logOutput(out)
            
    def fetch(self, paths):
        """ Fetch a copy of the paths' contents """
        output = []
        for path in paths:
            if os.path.isdir(path):
                continue
            root, files = self.splitFiles(path)
            out = self.run(root, ['cat'] + files)
            if out:
                output.append(out.stdout.read())
                self.logOutput(out)
            else:
                output.append(None)
        return output
               
if __name__ == '__main__':
    svn = SVN()
    svn.add(['/Users/kesmit/pp/editra-plugins/Projects/projects/Icons'])