#Created by Timothy Gamble
#tjgambs@gmail.com

from fabric.api import local, cd

def commit_push(message):
	with cd('../'):
		#Commits to gh-pages
		local('git checkout gh-pages')
		local('git add .')
		local('git commit -a -m "%s"' % message)
		local('git push')

		#Commits to master
		local('git checkout master')
		local('git rebase gh-pages')
		local('git push origin master')
		local('git checkout gh-pages')
