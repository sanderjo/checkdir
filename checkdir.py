#!/usr/bin/env python

# Functions to do checking on a directory:
# is directory on a FAT filesystem? 

import sys, os, subprocess

debug = False

def isFAT(dir):

# Check if "dir" is on FAT. FAT considered harmful (for big files)
# Works for Linux, Windows
# NB: On Windows, full path with drive letter is needed!

	FAT = False	# default: not FAT
	if 'linux' in sys.platform:
		# On Linux:
		# df -T /home/sander/weg

		'''
		Example output of a 500GB external USB drive formatted with FAT:
		$ df -T /media/sander/INTENSO
		Filesystem     Type 1K-blocks      Used Available Use% Mounted on
		/dev/sda1      vfat 488263616 163545248 324718368  34% /media/sander/INTENSO
		'''

		cmd = "df -T " + dir
		for thisline in os.popen(cmd).readlines():
			#print thisline
			if thisline.find('/')==0:
				# Starts with /, so a real, local device
				fstype = thisline.split()[1]
				if debug: print "File system type:", fstype
				if fstype.lower().find('fat') >= 0:
					FAT = True
					if debug: print "FAT found"
					break
	elif 'win' in sys.platform:
		# On Windows:
		'''
		C:\>wmic logicaldisk get name,filesystem
		FileSystem  Name
		NTFS        C:
			    D:
		FAT         E:
		FAT         F:
		NTFS        G:
		NTFS        H:
		NTFS        M:
		NTFS        Q:
		NTFS        X:

		We now can see dir "E:\other\dir\something" is on FAT (just like F:\bla), 
		and "Q:\dome\dir\bla" is not on FAT.
		'''
		windowscmd = "wmic logicaldisk get name,filesystem".split()
		CREATE_NO_WINDOW = 0x08000000
		for line in subprocess.check_output(windowscmd,creationflags=CREATE_NO_WINDOW).replace('\r','').split('\n'):
			if 'FAT' in line:
				# I'm quite sure if 'FAT' is there, there is always a space before the drive letter, 
				# thus a split() is possible, but to be sure put it in a try/except:
				try:
					driveletter = line.split()[1]
					# We have found a drive letter which is FAT
					# Now check if that drive letter is in the dir to be checked (somewhere in the beginning of the path)
					# ... because can be '\\?\C:\Media\...'
					if dir.find(driveletter) >=0 and dir.find(driveletter) <= 5 :
						FAT = true
						break	# we're done
				except:
					continue


	return FAT



if __name__ == "__main__":
	if debug: print sys.platform
	try:
		dir = sys.argv[1]
	except:
		print "Specify dir on the command line"
		sys.exit(0)
	print  "Is", dir, "on FAT? Answer:", isFAT(dir)




