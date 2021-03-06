import numpy as np
from matplotlib import pyplot as plt

# different colours as shortcuts

wt = [255,255,255]
bl = [0,0,0]
gr = [128, 128, 128]

fi = [0,0,255]     # format information
vi = [0,255,255]   # version information

def draw_qr(v,n,out):

	img = np.zeros((n,n,3), np.uint8)
	img[:,:] = gr
	
	''' Format Information Area reservation '''
	for i in range(8):
		img[i,8] = img[8,i] = img[8,8] = fi  # top-left
		img[8,n-i-1] = fi  # top-right
		img[n-i-1,8] = fi  # bottom-left

	''' Version Information Area reservation '''
	if v>=7:
		img[n-11:n-8,0:6] = vi
		img[0:6,n-11:n-8] = vi

	''' Timing Patterns '''
	# always start and end with a dark module

	for i in range(n):
		if(i%2 == 0):
			img[6,i] = img[i,6] = bl
		else:
			img[6,i] = img[i,6] = wt
			
	''' Finder Patterns '''
	# building the basic structure
	fp = np.zeros((9,9,3), np.uint8)
	fp[0:9,0:9] = wt # separator
	fp[1:8,1:8] = bl
	fp[2:7,2:7] = wt
	fp[3:6,3:6] = bl

	# placing finders onto the image
	img[0:8,0:8] = fp[1:,1:] # top-left
	img[0:8,n-8:n] = fp[1:,:8] # top-right
	img[n-8:n,0:8] = fp[:8,1:] # bottom-left

	''' Alignment Patterns '''
	# qr-codes having version > 2 need to have
	# certain fixed sizes as in the reference
	# array below
	apr = [[],[],[6,18],[6,22],[6,26],[6,30],[6,34],[6,22,38],[6,24,42],[6,26,46]] # and so on ...

	# building the basic structure
	ap = np.zeros((5,5,3), np.uint8)
	ap[0:5,0:5] = bl
	ap[1:4,1:4] = wt
	ap[2,2] = bl

	# computing viable options
	for i in range(len(apr[v])):
		for j in range(len(apr[v])):
		
			x = apr[v][i]
			y = apr[v][j]
		
			r = range(0,8)
			s = range(n-8,n)
			
			# check if in range, if not, place it
			print('placing finders on grid:')
			if(x in r and y in r or x in r and y in s or x in s and y in r):
				print(x,y,': not viable')
			else:
				print(x,y,': viable, inserting...')
				img[x-2:x+3,y-2:y+3] = ap

	''' Dark Module '''
	img[[(4 * v) + 9], 8] = bl

	''' Place the Data Bits '''
	
	x=n-1
	y=n-1
	
	column_height = ((n-1)-8)*2

	for i in range(column_height):
	
		#if img[y,x].tolist() == gr:
		if out[i] == '1':
			img[y,x] = bl
		else:
			img[y,x] = wt
	
		if i%4 == 0:
			x = x-1
		elif (i-1)%4 == 0:
			x = x+1
			y = y-1
		elif (i-2)%4 == 0:
			x = x-1
		elif (i-3)%4 == 0:
			x = x+1
			y = y-1

	x = x-2
	y = y+1
	
	for i in range(column_height, column_height*2):
		# if img[y,x].tolist() == gr:
		if out[i] == '1':
			img[y,x] = bl
		else:
			img[y,x] = wt
			
		if i%4 == 0:
			x = x-1
		elif (i-1)%4 == 0:
			x = x+1
			y = y+1
		elif (i-2)%4 == 0:
			x = x-1
		elif (i-3)%4 == 0:
			x = x+1
			y = y+1
			
	x = x-2
	y = y-1
	
	for i in range(column_height*2,column_height*3-1):
	
		# if img[y,x].tolist() == gr:
		if out[i] == '1':
			img[y,x] = bl
		else:
			img[y,x] = wt
	
		if i%4 == 0:
			x = x-1
		elif (i-1)%4 == 0:
			x = x+1
			y = y-1
		elif (i-2)%4 == 0:
			x = x-1
		elif (i-3)%4 == 0:
			x = x+1
			y = y-1
	
	''' Data Masking 
	# toggle the color of the module if it is masked
	# specification defines eight mask patterns that can be applied
	# must ONLY be applied to data modules and error correction modules
	# entire matrix is evaluated based on four evaluation conditions
	
	Four Rules:-
	1. five or more same coloured modules
	2. 2x2 area of same coloured modules
	3. patterns simliar to finder patterns
	4. more than half modules are dark or light
	
	'''
	
	'''
	Format and Version info
	
	
	
	'''
	
	''' Show the image '''

	plt.imshow(img)
	plt.show()
