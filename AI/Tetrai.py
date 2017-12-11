from queue import Queue
import pygame

BLACK = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple=(120,0,120)
WHITE=(255,255,255)
yellow=(255,255,0)
cyan=(0, 255, 255)
grey=(128, 128, 128)
orange=(255, 127, 0)

cyanBlock=[[-1,0],[1,0],[2,0],cyan]

class tetrai:

	def __init__(self,aggConst,lineConst,holesConst,bumpConst,multiLineWeight,columnWidth,rowHeight):
		print("Initializing Tetrai", end=' ')
		self.aggConst = aggConst
		self.lineConst = lineConst
		self.holesConst = holesConst
		self.bumpConst =  bumpConst
		self.multiLineWeight = multiLineWeight
		self.normalizeConstants()
		self.columnWidth = columnWidth
		self.rowHeight = rowHeight
		self.score = 0
		print("with a={}, l={}, h={}, b={}, m={}".format(aggConst,lineConst,holesConst,bumpConst,multiLineWeight))

	def normalizeConstants(self):
		magnitude = abs(self.aggConst)+abs(self.lineConst)+abs(self.holesConst)+abs(self.bumpConst)+abs(self.multiLineWeight)
		self.aggConst /= magnitude
		self.lineConst /= magnitude
		self.holesConst /= magnitude
		self.bumpConst /= magnitude
		self.multiLineWeight /= magnitude

	def setScore(self, points):
		self.score=points

	def calculateNewMove(self,board,currentPiece,nextPiece):
		maxH = -99999999
		maxLoc = -1
		maxRot = -1
		moveLoc=-1

		for rot in range (self.getUniqueRot(currentPiece)):
			for column in range(10):
				self.setShapeToColumn(currentPiece,column)
				self.moveShapeToBottom(currentPiece,board)
				if (self.shapeOutOfBounds(currentPiece)):
					continue
				h = self.calculateHeuristic(self.getReasonableBoard(board,currentPiece))#self.predictNextPiece(board,nextPiece)
				if (h>maxH):
					maxH=h
					maxRot=rot
					maxLoc=column
			self.setShapeToColumn(currentPiece,4)
			self.rotate(currentPiece)

		moveQueue = Queue()
		for i in range(maxRot):
			self.rotate(currentPiece)

		moveLoc=self.getShapeColumn(currentPiece)
		while moveLoc!=maxLoc:
			if (moveLoc<maxLoc):
				moveQueue.put(pygame.K_RIGHT)
				moveLoc+=1
			else:
				moveQueue.put(pygame.K_LEFT)
				moveLoc-=1
		

		moveQueue.put(pygame.K_SPACE)
		return moveQueue

	def predictNextPiece(self,board,currentPiece):
		maxH = -99999999

		for rot in range (self.getUniqueRot(currentPiece)):
			for column in range(10):
				self.setShapeToColumn(currentPiece,column)
				self.moveShapeToBottom(currentPiece,board)
				if (self.shapeOutOfBounds(currentPiece)):
					continue
				h = self.calculateHeuristic(self.getReasonableBoard(board,currentPiece))
				if (h>maxH):
					maxH=h
			self.setShapeToColumn(currentPiece,4)
			self.rotate(currentPiece)

		return maxH



	def getShapeColumn(self,shape):
		lowestX = 9999999
		lowestY = 9999999

		for i in range(4):
			if shape[i].left<lowestX:
				lowestX = shape[i].left

		return lowestX//self.columnWidth

	def shapeOutOfBounds(self, shape):
		for i in range (len(shape)-1):
			if shape[i].top>=self.rowHeight*20 or shape[i].left<0 or shape[i].left>=self.columnWidth*10:
				return True
		return False

	def getReasonableBoard(self, board,curBlock):
		newBoard = list()
		for i in range (10):
			newBoard.append(list())
			for j in range(20):
				newBoard[i].append(0)
		for block in board:
			for i in range (len(block)-1):
				if (block[i].top>=0 and block[i].left<=self.columnWidth*9 and  block[i].left>=0 ):
					newBoard[block[i].left//self.columnWidth][19-block[i].top//self.rowHeight]=1
		for i in range (len(curBlock)-1):
			if (curBlock[i].top>=0 and curBlock[i].left<=self.columnWidth*9 and  curBlock[i].left>=0 ):
					newBoard[curBlock[i].left//self.columnWidth][19-curBlock[i].top//self.rowHeight]=1
		return newBoard

	def calculateHeuristic(self, board):
		aggregateHeight =0
		bumpiness=0
		numHoles=0
		lineClears=0
		prevHeight=-1
		for x in range(10):
			foundBlock=False
			for y in reversed(range (20)):
				if ((not foundBlock) and board[x][y]==1):
					foundBlock=True
					aggregateHeight+=y;
					if (prevHeight!=-1):
						bumpiness+=abs(y-prevHeight)
					prevHeight=y
				elif foundBlock and board[x][y]==0:
					numHoles+=1

		for y in range(20):
			clear=True
			for x in range(10):
				if board[x][y]==0:
					clear=False
			if clear:
				lineClears+=1

		return self.aggConst*aggregateHeight+self.lineConst*lineClears+self.holesConst*numHoles+self.bumpConst*bumpiness


	def getUniqueRot(self, shape):
		if (shape[4]==cyan or shape[4]==red or shape[4]==green):
			return 2
		elif (shape[4]==yellow):
			return 1
		else:
			return 4

	def setShapeToColumn(self, shape,column):
		lowestX = 9999999
		lowestY = 9999999

		for i in range(4):
			if shape[i].left<lowestX:
				lowestX = shape[i].left
			if shape[i].top < lowestY:
				lowestY=shape[i].top

		offsetX = column*self.columnWidth - lowestX
		offsetY = -self.rowHeight - lowestY

		for i in range(4):
			shape[i].left=shape[i].left+offsetX
			shape[i].top=shape[i].top+offsetY

	def moveShapeToBottom(self,currentPiece,board):
		fix=0
		while True:
			for i in range(4):
				currentPiece[i].top+=(self.rowHeight)
				if currentPiece[i].top==self.rowHeight*20:
					fix=1
				if self.overlap(currentPiece[i],board,currentPiece):
					fix=1
			if fix:
				for i in range(4):
					currentPiece[i].top-=(self.rowHeight)
					fix=0
				break

		if currentPiece[i].top>=self.rowHeight*20:
			pygame.quit()

	def overlap(self,one,two,three):
		for bk in two:
			if bk!=three:
				for b in range(len(bk)-1):
					if one==bk[b]:
						return True
		return False

	def rotate(self,curr):
		if curr[4]==yellow:
			self.rotateo(curr)
		if curr[4]==cyan:
			self.rotatei(curr)
		else:
			self.rotatea(curr)

	def rotatei(self,curr):
		bla=1
		if curr[2].centerx>curr[0].centerx and curr[3].centerx>curr[0].centerx:
			horiz=True
			curr[0].centerx+=self.columnWidth
			bla=1
		elif curr[2].centerx<curr[0].centerx and curr[3].centerx<curr[0].centerx:
			horiz=True
			curr[0].centerx-=self.columnWidth
			bla=-1
		elif curr[2].centery>curr[0].centery and curr[3].centery>curr[0].centery:
			horiz=False
			curr[0].centery+=self.rowHeight
			bla=-1
		elif curr[2].centery<curr[0].centery and curr[3].centery<curr[0].centery:
			horiz=False
			curr[0].centery-=self.rowHeight
			bla=1
		for f in range (1,4):
			if horiz:
				curr[f].left=curr[0].left
				curr[f].top=curr[0].top+(cyanBlock[f-1][0]*self.rowHeight*bla)
			else:
				curr[f].top=curr[0].top
				curr[f].right=curr[0].right+(cyanBlock[f-1][0]*self.columnWidth*bla)

	def rotateo(self,curr):
		pass

	def rotatea(self,curr):
		middlex=curr[0].centerx
		middley=curr[0].centery
		for r in range(1,4):
			if curr[r].centery==middley and curr[r].centerx>middlex:
				curr[r].centery+=self.rowHeight
				curr[r].centerx-=self.columnWidth
			elif curr[r].centery==middley and curr[r].centerx<middlex:
				curr[r].centery-=self.rowHeight
				curr[r].centerx+=self.columnWidth
			elif curr[r].centerx==middlex and curr[r].centery>middley:
				curr[r].centery-=self.rowHeight
				curr[r].centerx-=self.columnWidth			
			elif curr[r].centerx==middlex and curr[r].centery<middley:
				curr[r].centery+=self.rowHeight
				curr[r].centerx+=self.columnWidth			
			elif curr[r].centerx>middlex and curr[r].centery>middley:
				curr[r].centerx-=(2*self.columnWidth)
			elif curr[r].centery>middley and curr[r].centerx<middlex:
				curr[r].centery-=(2*self.rowHeight)
			elif curr[r].centerx<middlex and curr[r].centery<middley:
				curr[r].centerx+=(2*self.columnWidth)
			elif curr[r].centerx>middlex and curr[r].centery<middley:
				curr[r].centery+=(2*self.rowHeight)