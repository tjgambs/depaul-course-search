#Created by Timothy Gamble
#tjgambs@gmail.com

import update_data as one
import make_course_pages as two
import make_teacher_pages as three

import fabfile as four

def main():
	#one.main()
	print 'Finished Step One!'
	#two.main()
	print 'Finished Step Two!'
	#three.main()
	print 'Finished Step Three!'
	print 'Running fabric to commit to gh-pages and master'
	four.commit_push()
	print 'Finished!'
	


if __name__ == '__main__':
	main()