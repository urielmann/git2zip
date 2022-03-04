#########################################################################
# Copyright 2022 (c), Uri Mann. All rights reserved.                    #
# mailto:abba.mann@gmail.com                                            #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU Affero Public License version 3 as      #
# published by the Free Software Foundation.                            #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# See the GNU Affero Public License for more details.                   #
#                                                                       #              
# You should have received a copy of the GNU Affero Public License      #
# along with this program.  If not, see http://www.gnu.org/licenses.    #
#########################################################################

import os
import git
import click
import zipfile

@click.command()
@click.option('--repository', default='.', help='Repository path')
@click.option('--branch', default='main', help='Branch name')
@click.option('--num-commits', default=1, help='Number of commits to archiive')
@click.option('--archive', default='backup.zip', help='Path to .zip (archive) file')
def main(repository, branch, num_commits, archive):
    repo = git.Repo(path=repository, search_parent_directories=True)
    # get all of the commits on the branch
    commits = list(repo.iter_commits(branch))
    # filter out --num-commits in reverse cronological order
    # so newest files are first
    commits = reversed(list(commits[:num_commits]))
    # list of files to prevent duplicates
    archived = set()
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zip:
        # for each commit get the paths to the commited files
        for commit in commits:
            for file in commit.stats.files.keys():
                # skip duplicates
                if file in archived: continue
                archived.add(file)
                print(file)
                path = os.path.join(repository, file)
                zip.write(path, file)


if __name__ == '__main__':
    main()
