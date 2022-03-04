import os
import git
import click
import zipfile

@click.command()
@click.option('--repository', default='D:/CrowdStrike/private/main', help='Repository path')
@click.option('--branch', default='main', help='Branch name')
@click.option('--num-commits', default=1, help='Number of commits to zip')
@click.option('--archive', default='backup.zip', help='Path to zip')
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
            # print(i, len(commit.stats.files),
            #          commit.message,
            #          commit.stats.files.keys())
            for file in commit.stats.files.keys():
                if file in archived: continue
                archived.add(file)
                print(file)
                path = os.path.join(repository, file)
                zip.write(path, file)


if __name__ == '__main__':
    main()
