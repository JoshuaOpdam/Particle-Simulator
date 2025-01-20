# Make each particle a class with:     X, Y, CellKey, VelX, VelY
# Make all global vareables regular vareables in loop to save performance


import pygame
import os
import time
import random
from math import *
from sklearn import preprocessing

class mainParticleSimulation :
	def __init__(self):
		# Set Manditory Vareables
		self.simType = "Null"

		pygame.display.init()
		pygame.font.init()
		self.myfont = pygame.font.Font("Crunch Chips.otf", 50)
		self.clock = pygame.time.Clock()
		self.quitMenu = False
		self.particlePosition = []

		self.run = True
		self.Width, self.Height = (800), (800)
		self.Window = pygame.display.set_mode(size=(self.Width, self.Height))
		pygame.mouse.set_visible(True)

		#Buttons
		self.startButton = pygame.Rect( (self.Width/10), (self.Height/1.5), 130, 45 )
		self.simButton = pygame.Rect( (self.Width/2.75), (self.Height/1.5), 260, 95 )
		self.quitButton = pygame.Rect( (self.Width/1.3), (self.Height/1.5), 105, 45 )

		#Colours
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.grey = (100,100,100)
		self.red = (255,25,25)

		#Drivers
		self.changeDir = ""
		self.drawDriver8_1 = False
		self.drawDriver9_1 = False

	#Functions
	def printText (self,string,x,y,size) :
		self.myfont = pygame.font.Font("Crunch Chips.otf", round(size))
		self.var = bytes(str(string), 'utf-8')
		self.Text = self.myfont.render(self.var, False, self.white)
		self.Window.blit(self.Text, (round(x),round(y)))

	def printTextColour (self,string,x,y,size,colour) :
		self.myfont = pygame.font.Font("Crunch Chips.otf", round(size))
		self.var = bytes(str(string), 'utf-8')
		self.Text = self.myfont.render(self.var, False, colour)
		self.Window.blit(self.Text, (round(x),round(y)))

	def slider (self, x, y, w, h, mousePos, value) :
		pygame.draw.rect(self.Window, self.white, (x, y, w, h))
		self.pos = x + (w * (value / 100))
		pygame.draw.rect(self.Window, self.grey, (self.pos, y - 5, 10, h + 10))

	def MenuScreen (self) :
		pygame.mouse.set_visible(True)	
		self.mouse = pygame.mouse.get_pos()

		self.Window.fill( self.black )

		self.printText ("Particle Simulation", (self.Width/15), (self.Height/8), 75)

		self.printText ("Start", (self.Width/10), (self.Height/1.5), 50)
		if self.simType == "Null" :
			self.printTextColour ("(select simulation type first)", (15), (self.Height/1.5 + 50), 20, (self.red))

		self.printText ("Simulation", (self.Width/2.75), (self.Height/1.5), 50)
		self.printText ("Type", (self.Width/2.75+60), (self.Height/1.5+50), 50)
		

		self.printText ("Quit",(self.Width/1.3), (self.Height/1.5), 50)
		

		self.printText ( "FPS:" + str(round(self.clock.get_fps())), (10), (10), 30 )

	def distance (self,firstValue,secondValue) :
		firstValue = str(firstValue)
		self.temp1x, self.temp1y = firstValue.strip("()").split(",")
		self.temp1x, self.temp1y = float(self.temp1x), float(self.temp1y)

		secondValue = str(secondValue)
		self.temp2x, self.temp2y = secondValue.strip("()").split(",")
		self.temp2x, self.temp2y = float(self.temp2x), float(self.temp2y)
		
		self.adjacent = self.temp2x - self.temp1x
		self.opposite = self.temp2y - self.temp1y
		self.hypotenuse = sqrt( self.adjacent**2 + self.opposite**2 )

		return self.adjacent, self.opposite, self.hypotenuse

	def fibonacciCircle (self, number, radius) :
		self.phi = (1 + sqrt(5)) / 2 # phi = golden ratio
		self.theta = (2 * pi) / self.phi**2 # theta = golden angle
		self.particlePosition = []

		for i in range(number) :	
			self.radii = radius * sqrt(i / number)
			self.indexTheta = i * self.theta
			self.x = self.radii * cos(self.indexTheta)
			self.y = self.radii * sin(self.indexTheta)
			self.particlePosition.append( (self.x + (self.Width/2),self.y + (self.Height/2)) )

		return self.particlePosition

	def saveFunction (self) : 
		# Opening a text file for saving particle aliases and ensuring data gets overwritten when the program closes ("w+")
		self.saveFile = open("simulationSaveFile.txt", "w+")

		# (@ # $ %) are lookup keys so that it can be searched for
		self.saveFile.write("@" + str(self.particlePosition))
		self.saveFile.write("#" + str(self.velocities))
		self.saveFile.write("$" + str(self.Density)) 
		self.saveFile.write("%" + str(self.Gravity))
		self.saveFile.write("^" + str(self.Magnitude))
		self.saveFile.write("&" + str(self.Speed))
		self.saveFile.write("*" + str(self.simType) + " ") # Space ensuring the [-1] index doesn't cut off density value
		self.saveFile.close()

	def loadFunction (self) :
		# Opening a text file for saving particle aliases and ensuring data gets overwritten when the program closes ("w+")
		self.saveFile = open("simulationSaveFile.txt", "r")
		if self.changeDir == "2_1":
			print("2_1")
			self.saveFile = open(self.driver_2_1(), "r")
		if self.changeDir == "2_2":
			print("2_2")
			self.saveFile = open(self.driver_2_2(), "r")
		if self.changeDir == "3_1":
			print("3_1")
			self.saveFile = open(self.driver_3_1(), "r")
		if self.changeDir == "4_1":
			print("4_1")
			self.saveFile = open(self.driver_4_1(), "r")
		if self.changeDir == "4_2":
			print("4_2")
			self.saveFile = open(self.driver_4_2(), "r")

		self.readText = self.saveFile.read()
		self.indexAt = self.readText.find("@") # particlePosition
		self.indexHash = self.readText.find("#") # velocities
		self.indexDollar = self.readText.find("$") # Density
		self.indexPercent = self.readText.find("%") # Gravity
		self.indexCarrot = self.readText.find("^") # Magnitude
		self.indexAnd = self.readText.find("&") # Speed
		self.indexStar = self.readText.find("*") # simType

		self.particlePosition = list(eval(self.readText[self.indexAt+1:self.indexHash]))
		self.velocities = list(eval(self.readText[self.indexHash+1:self.indexDollar]))
		self.Density = int(self.readText[self.indexDollar+1:self.indexPercent])
		self.particleNumb = self.Density
		self.Gravity = int(self.readText[self.indexPercent+1:self.indexCarrot])
		self.Magnitude = int(self.readText[self.indexCarrot+1:self.indexAnd])
		self.Speed = int(self.readText[self.indexAnd+1:self.indexStar])
		self.simType = str(self.readText[self.indexStar+1:-1])
		self.saveFile.close()

	def initialStartFrame (self) : 
		self.startMenu = True
		self.spacing = 20
		self.particlePosition = []
		self.particleNumb = 25
		self.particlePos = 0
		self.Speed = 10
		self.Gravity = 0
		self.Magnitude = 10
		self.Density = 25

		self.velocity = 1
		self.initialAngle = []
		self.velocities = []
		for i in range( self.particleNumb ) :
			self.initialAngle.append(random.uniform(0, 2*pi))
			self.velocities.append((cos(self.initialAngle[i]) * self.velocity, sin(self.initialAngle[i]) * self.velocity))

		self.particlePosition = self.fibonacciCircle ( self.Density, 300 )

	def startScreenPrint (self):
		self.Window.fill( self.black )
		self.printText ( "Back", (25), (50), 50 )
		self.backButton = pygame.Rect((25), (50), 110, 45)
		self.printText ( "Reset", (360), (750), 50 )
		self.resetButton = pygame.Rect((360), (750), 130, 45)
		self.printText ( "Save", (25), (700), 50 )
		self.saveButton = pygame.Rect((25), (700), 115, 45)
		self.printText ( "Load", (25), (750), 50 )
		self.loadButton = pygame.Rect((25), (750), 115, 45)
		self.printText ( "FPS:" + str(round(self.clock.get_fps())), (10), (10), 30 )
		self.printText ( self.simType, (350), (50), 50 )

	def mouseKeyboardUpdate (self) :
		self.keys = pygame.key.get_pressed()
		self.mouse = pygame.mouse.get_pos()

	def resetFunction (self) : 
		self.particlePosition = []
		self.particleNumb = self.Density
		self.velocity = self.Speed
		self.initialAngle = []
		for i in range( self.particleNumb ) :
			self.initialAngle.append(random.uniform(0, 2*pi))

		self.velocities = []
		for i in range( len(self.initialAngle) ) :
			self.velocities.append((cos(self.initialAngle[i]) * self.velocity, sin(self.initialAngle[i]) * self.velocity))

		self.particlePosition = self.fibonacciCircle ( self.Density, 300 )

	def sliderValueGravity (self,y) : 
		self.x = self.Width - 135
		self.w = 100
		self.h = 10
		
		if self.x <= self.mouse[0] <= (self.x + self.w) and y <= self.mouse[1] <= (y + self.h) :
			
			self.Gravity = min(100, max(0, (self.mouse[0] - self.x) / self.w * 100))
			self.Gravity = round(self.Gravity)

	def sliderValueMagnitude (self,y) : 
		self.x = self.Width - 135
		self.w = 100
		self.h = 10
		
		if self.x <= self.mouse[0] <= (self.x + self.w) and y <= self.mouse[1] <= (y + self.h) :
			
			self.Magnitude = min(100, max(1, (self.mouse[0] - self.x) / self.w * 100))
			self.Magnitude = round(self.Magnitude)

	def sliderValueDensity (self,y) : 
		self.x = self.Width - 135
		self.w = 100
		self.h = 10
		
		if self.x <= self.mouse[0] <= (self.x + self.w) and y <= self.mouse[1] <= (y + self.h) :
			
			self.Density = min(100, max(1, (self.mouse[0] - self.x) / self.w * 100))
			self.Density = round(self.Density)

			if self.Density != self.particleNumb :
				#particlePosition = []
				self.velocities = []
				self.initialAngle = []
				for i in range( self.Density ) :
					self.particleNumb = self.Density
					self.initialAngle.append(random.uniform(0, 2*pi))
					self.velocities.append( (0, 0) )

				self.particlePosition = self.fibonacciCircle ( self.Density, 300 )
				self.particleNumb = len(self.particlePosition)

	def sliderValueSpeed (self,y) :
		self.x = self.Width - 135
		self.w = 100
		self.h = 10
		
		if self.x <= self.mouse[0] <= (self.x + self.w) and y <= self.mouse[1] <= (y + self.h) :
			
			self.Speed = min(100, max(0, (self.mouse[0] - self.x) / self.w * 100))
			self.Speed = round(self.Speed)
			self.velocities = []
			for i in range( len(self.initialAngle) ) :
				self.velocities.append((cos(self.initialAngle[i]) * self.Speed, sin(self.initialAngle[i]) * self.Speed))

	def particleCalculateGravity (self) :
		for i in range( self.particleNumb ) :
			self.part = str(self.particlePosition[i])
			self.partX, self.partY = self.part.strip("()").split(",")
			self.partX, self.partY = float(self.partX), float(self.partY)

			self.vel = str(self.velocities[i])
			self.velX, self.velY = self.vel.strip("()").split(",")
			self.velX, self.velY = float(self.velX), float(self.velY)

			#print(partX, partY)

			if self.partX - self.Magnitude < 0 or self.partX + self.Magnitude > 800:
				self.velX *= -1  
				self.partX = max(0, min(self.partX, 800))  
			if self.partY - self.Magnitude < 0 or self.partY + self.Magnitude > 800:
				self.velY *= -1  
				self.partY = max(0, min(self.partY, 800))  

			self.partX, self.partY = int(round(float(self.partX) + float(self.velX))), int(round(float(self.partY) + float(self.velY)))
			self.velocities[i] = (self.velX, self.velY)
			self.particlePosition[i] = ((self.partX, self.partY))
			
			for c in range( self.particleNumb ) :

				self.vel1 = str(self.velocities[c])
				self.vel1X, self.vel1Y = self.vel1.strip("()").split(",")
				self.vel1X, self.vel1Y = float(self.vel1X), float(self.vel1Y)

				self.adjacent, self.opposite, self.hypotenuse = self.distance(self.particlePosition[i], self.particlePosition[c])

				if self.hypotenuse != 0:
					
					self.velX = self.velX + (( (self.Magnitude/100)/ self.hypotenuse * self.adjacent) / max(0.0001,min(1000,self.hypotenuse**0.1)) /10)
					self.velY = self.velY + (( (self.Magnitude/100)/ self.hypotenuse * self.opposite) / max(0.0001,min(1000,self.hypotenuse**0.1)) /10)
					pass

			self.partX, self.partY = int(round(float(self.partX) + float(self.velX))), int(round(float(self.partY) + float(self.velY)))
			self.velocities[i] = (self.velX, self.velY)
			self.particlePosition[i] = ((self.partX, self.partY))

		if self.changeDir == "2_1" or "2_2":
			average = [sum(x)/len(x) for x in zip(*self.particlePosition)]
			print(average)

	def particleCalculateLiquid (self) :
		
		self.velX = 0
		self.velY = 0	
		for i in range( self.particleNumb ) :
			self.gravityAddX = 0
			self.gravityAddY = 0
			self.part = str(self.particlePosition[i])
			self.partX, self.partY = self.part.strip("()").split(",")
			self.partX, self.partY = float(self.partX), float(self.partY)

			self.vel = str(self.velocities[i])
			self.velX, self.velY = self.vel.strip("()").split(",")
			self.velX, self.velY = float(self.velX), float(self.velY)
			self.velX *= 0.99
			self.velY *= 0.99

			self.partX, self.partY = int(round(float(self.partX) + float(self.velX))), int(round(float(self.partY) + float(self.velY)))
			self.velocities[i] = (self.velX, self.velY)
			self.particlePosition[i] = ((self.partX, self.partY))
			
			for c in range( self.particleNumb ) :

				self.part1 = str(self.particlePosition[i])
				self.part1X, self.part1Y = self.part.strip("()").split(",")
				self.part1X, self.part1Y = float(self.part1X), float(self.part1Y)

				self.vel1 = str(self.velocities[c])
				self.vel1X, self.vel1Y = self.vel1.strip("()").split(",")
				self.vel1X, self.vel1Y = float(self.vel1X), float(self.vel1Y)

				self.velY = self.velY + self.Gravity/100

				self.adjacent, self.opposite, self.hypotenuse = self.distance(self.particlePosition[i], self.particlePosition[c])
				
				# Repulsion force 
				if self.hypotenuse > 0:
					
					self.velX = self.velX + (( (-self.Magnitude/100)/ self.hypotenuse * self.adjacent) / max(0.0001,min(1000,self.hypotenuse**0.1)) /10)
					self.velY = self.velY + (( (-self.Magnitude/100)/ self.hypotenuse * self.opposite) / max(0.0001,min(1000,self.hypotenuse**0.1)) /10)


				if self.partX - self.Magnitude < 0 or self.partX + self.Magnitude > 800:
					self.velX *= 0  
					self.partX = max(0, min(self.partX, 800))  
				if self.partY - self.Magnitude < 0 or self.partY + self.Magnitude > 800:
					self.velY *= 0  
					self.partY = max(0, min(self.partY, 800))  


				self.partX, self.partY = ( round(float(self.partX) + float(self.velX), 4)), (round(float(self.partY) + float(self.velY), 4) )

				self.velocities[i] = (self.velX, self.velY)
				self.particlePosition[i] = (self.partX, self.partY)

	def particleCalculateGas (self) :
		for i in range( self.particleNumb ) :
			self.part = str(self.particlePosition[i])
			self.partX, self.partY = self.part.strip("()").split(",")
			self.partX, self.partY = float(self.partX), float(self.partY)

			self.vel = str(self.velocities[i])
			self.velX, self.velY = self.vel.strip("()").split(",")
			self.velX, self.velY = float(self.velX), float(self.velY)

			if self.partX < 0 or self.partX > 800:
				self.velX *= -1  
				self.partX = max(0, min(self.partX, 800))  
			if self.partY < 0 or self.partY > 800:
				self.velY *= -1  
				self.partY = max(0, min(self.partY, 800))  

			self.partX, self.partY = int(round(float(self.partX) + float(self.velX))), int(round(float(self.partY) + float(self.velY)))
			self.velocities[i] = (self.velX, self.velY)
			self.particlePosition[i] = ((self.partX, self.partY))

			for c in range( self.particleNumb ) :

				self.vel1 = str(self.velocities[c])
				self.vel1X, self.vel1Y = self.vel1.strip("()").split(",")
				self.vel1X, self.vel1Y = float(self.vel1X), float(self.vel1Y)

				self.adjacent, self.opposite, self.hypotenuse = self.distance(self.particlePosition[i], self.particlePosition[c])

				if self.hypotenuse <= self.Magnitude*2:

					self.tempX, self.tempY = self.velX, self.velY
					self.velX, self.velY = self.vel1X, self.vel1Y
					self.vel1X, self.vel1Y = self.tempX, self.tempY

					self.velocities[i] = (self.velX, self.velY)
					self.velocities[c] = (self.vel1X, self.vel1Y)

	def renderGravity (self) :
		if self.simType == "Gravity" :
			for i in range( len(self.particlePosition) ) :
				self.vel = str(self.velocities[i])
				self.velX, self.velY = self.vel.strip("()").split(",")
				self.velX, self.velY = float(self.velX), float(self.velY)

				pygame.draw.circle( self.Window, self.white, (self.particlePosition[i]) , ( max(1, (abs(self.velX) + abs(self.velY))) / min(1, self.Density*self.Magnitude) ) )

			average = [sum(x)/len(x) for x in zip(*self.particlePosition)]
			pygame.draw.circle( self.Window, self.red, (average) , 5 )
							

	def renderLiquid (self) :
		if self.simType == "Liquid":
			for i in range( len(self.particlePosition) ) :
				pygame.draw.circle( self.Window, self.white, (self.particlePosition[i]) , self.Magnitude)

	def renderGas (self) :
		if self.simType == "Gas" :
			for i in range( len(self.particlePosition) ) :
				pygame.draw.circle( self.Window, self.white, (self.particlePosition[i]) , self.Magnitude)

	def renderTooltip (self) :
		self.sliderRect = pygame.Rect( (self.Width-255), (43), 255, 75)
		pygame.draw.rect( self.Window, self.red, self.sliderRect, width=2 )
		self.printTextColour ("hover over sliders to change", (self.Width-290), (23), 20, (self.red) )
		pygame.draw.rect( self.Window, self.red, self.backButton, width=2 )
		self.printTextColour ("return to menu screen", (15), (100), 20, (self.red) )
		pygame.draw.rect( self.Window, self.red, self.resetButton, width=2 )
		self.printTextColour ("reset particle positions", (300), (730), 20, (self.red) )	
		self.snapshotRect = pygame.Rect( (25), (700), 115, 100)
		pygame.draw.rect( self.Window, self.red, self.snapshotRect, width=2 )
		self.printTextColour ("capture a simlation snapshot", (5), (680), 20, (self.red) )

	def renderSimulationMenu (self) :
		self.Window.fill( self.black )

		self.keys = pygame.key.get_pressed()
		self.mouse = pygame.mouse.get_pos()

		self.printText ( "Back", (50), (50), 50 )
		self.backButton = pygame.Rect((50), (50), 105, 45)

		self.printText ( "Simulation Type", (self.Width/8), (self.Height/8), 75 )

		self.printText ( "Liquid", (100), (400), 75 )
		self.liquidButton = pygame.Rect((100), (400), 220, 75)
		pygame.draw.rect(self.Window, self.black, self.liquidButton, 2)

		self.printText ( "Gas", (300), (500), 75 )
		self.gasButton = pygame.Rect((300), (500), 140, 75)
		pygame.draw.rect(self.Window, self.black, self.gasButton, 2)

		self.printText ( "Gravity", (430), (400), 75 )
		self.gravityButton = pygame.Rect((430), (400), 275, 75)
		pygame.draw.rect(self.Window, self.black, self.gravityButton, 2)

		self.printText ( "FPS:" + str(round(self.clock.get_fps())), (10), (10), 30 )

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:

					if self.backButton.collidepoint(self.mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) :
						self.simMenu = False

					if self.liquidButton.collidepoint(self.mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) :
						self.simType = "Liquid"
						self.simMenu = False

					if self.gasButton.collidepoint(self.mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) :
						self.simType = "Gas"
						self.simMenu = False

					if self.gravityButton.collidepoint(self.mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) :
						self.simType = "Gravity"
						self.simMenu = False

	def renderQuitMenu (self) :

		self.Window.fill( self.black )

		self.keys = pygame.key.get_pressed()
		self.mouse = pygame.mouse.get_pos()

		self.printText ( "Are you sure you", (self.Width/8), (self.Height/8), 75 )
		self.printText ( "want to quit?", (self.Width/8)+35, (self.Height/8)+75, 75 )

		self.printText ( "Yes", (self.Width/10), (self.Height/1.5), 75 )
		self.yesButton = pygame.Rect((self.Width/10), (self.Height/1.5), 125, 60)
		
		self.printText ( "No", (self.Width/1.3), (self.Height/1.5), 75 )
		self.noButton = pygame.Rect((self.Width/1.3), (self.Height/1.5), 100, 60)
		
		self.printText ( "FPS:" + str(round(self.clock.get_fps())), (10), (10), 30 )

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				self.running = False

			elif event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:
					if self.yesButton.collidepoint(self.mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) :
						pygame.quit()

					elif self.noButton.collidepoint(self.mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) :
						self.quitMenu = False

	def refreshScreen (self) :
		pygame.display.update()
		self.clock.tick (60)


	# *** DRIVERS ***
	def driver_1_1 (self):
		print(self.fibonacciCircle (2,100))

	def driver_2_1 (self):
		self.changeDir = "2_1"
		self.simType = "Gravity"
		return "driver_2_1.txt"

	def driver_2_2 (self):
		self.changeDir = "2_2"
		self.simType = "Gravity"
		return "driver_2_2.txt"

	def driver_3_1 (self):
		self.changeDir = "3_1"
		self.simType = "Liquid"
		return "driver_3_1.txt"

	def driver_4_1 (self):
		self.changeDir = "4_1"
		self.simType = "Gas"
		return "driver_4_1.txt"

	def driver_4_2 (self):
		self.changeDir = "4_2"
		self.simType = "Gas"
		return "driver_4_2.txt"

	def driver_5_1 (self):
		self.particlePosition = [ (123,456), (654,321) ]

		self.adjacent, self.opposite, self.hypotenuse = self.distance(self.particlePosition[0], self.particlePosition[1])

		print(f"ADJACENT: {self.adjacent}")
		print(f"OPPOSITE: {self.opposite}")
		print(f"HYPOTENUSE: {self.hypotenuse}")

	def driver_8_1 (self):
		self.drawDriver8_1 = True
		self.Window.fill( self.black )
		self.printText ("hello world",400,400,50)
		self.refreshScreen()

	def driver_9_1 (self):
		self.drawDriver9_1 = True
		self.Window.fill( self.black )
		self.printTextColour ("hello world",400,400,50,self.red)
		self.refreshScreen()

	"""			!!!		MAIN LOOP		!!!			"""
	def main (self) :

		while self.run == True:
			# Updates necessary vareables for clicking
			self.mouseKeyboardUpdate ()
			self.MenuScreen ()
			# Driver 8_1
			if self.drawDriver8_1 == True:
				self.driver_8_1()
			if self.drawDriver9_1 == True:
				self.driver_9_1()

			for event in pygame.event.get():

				if self.startButton.collidepoint(self.mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) and self.simType != "Null":

					self.rawTime = 0
					# The initial starting values so that the program can run appropriatly
					self.initialStartFrame ()
					if self.changeDir != "":
						self.loadFunction ()

					while self.startMenu :

						# Updates necessary vareables for clicking
						self.mouseKeyboardUpdate ()
						self.startScreenPrint ()
						
						for event in pygame.event.get ():
							if event.type == pygame.QUIT:
								self.running = False
							elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
								if self.backButton.collidepoint (self.mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) :
									self.startMenu = False

								# If the SAVE button is pressed then save all necessary values into simulationSaveFile
								if self.saveButton.collidepoint(self.mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) :
									self.saveFunction ()

								# If the LOAD button is pressed then assign all values from simulationSaveFile
								if self.loadButton.collidepoint(self.mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) :
									self.loadFunction () 
								
								# Draw all particles in the fibonacci circle
								if self.resetButton.collidepoint(self.mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) :
									self.resetFunction ()
										
						# Restructure all particle postions to a rounded-map-tuple
						for i in range( self.particleNumb ) :
							self.particlePosition[i] = tuple(map(int, map(round, (self.particlePosition[i]))))

						# Main loop for Liquid simiulation graphics and math
						if self.simType == "Liquid" :

							# Draws and witholds every slider value to it's respective vareable
							self.sliderValueGravity (50)
							self.sliderValueMagnitude (75)
							self.sliderValueDensity (100)

							self.slider (self.Width - 135, 50, 100, 10, self.mouse, self.Gravity )
							self.printText ("Gravity", (self.Width - 220), (45), 20 )
							self.printText (str(self.Gravity), (self.Width - 25), (45), 20 )

							self.slider (self.Width - 135, 75, 100, 10, self.mouse, self.Magnitude )
							self.printText ( "Magnitude", (self.Width - 250), (70), 20 )
							self.printText (str(self.Magnitude), (self.Width - 25), (70), 20 )

							self.slider (self.Width - 135, 100, 100, 10, self.mouse, self.Density )
							self.printText ( "Density", (self.Width - 220), (95), 20 )
							self.printText (str(self.Density), (self.Width - 25), (95), 20 )

							# Handles all Liquid collision and values
							self.particleCalculateLiquid ()

						# Main loop for Gravity simiulation graphics and math
						if self.simType == "Gravity" :

							# Draws and witholds every slider value
							self.sliderValueMagnitude (50)
							self.sliderValueDensity (75)

							self.slider (self.Width - 135, 50, 100, 10, self.mouse, self.Magnitude )
							self.printText ( "Magnitude", (self.Width - 250), (45), 20 )
							self.printText (str(self.Magnitude), (self.Width - 25), (45), 20 )

							self.slider (self.Width - 135, 75, 100, 10, self.mouse, self.Density )
							self.printText ( "Density", (self.Width - 220), (70), 20 )
							self.printText (str(self.Density), (self.Width - 25), (70), 20 )

							# Handles all Gravity collision and values
							self.particleCalculateGravity ()

						# Main loop for Gas simiulation graphics and math
						if self.simType == "Gas" :
							
							# Draws and witholds every slider value
							self.sliderValueSpeed (50)
							self.sliderValueMagnitude (75)
							self.sliderValueDensity (100)

							self.slider(self.Width - 135, 50, 100, 10, self.mouse, self.Speed )
							self.printText ("Speed", (self.Width - 205), (45), 20 )
							self.printText (str(self.Speed), (self.Width - 25), (45), 20 )

							self.slider(self.Width - 135, 75, 100, 10, self.mouse, self.Magnitude )
							self.printText ( "Magnitude", (self.Width - 250), (70), 20 )
							self.printText (str(self.Magnitude), (self.Width - 25), (70), 20 )

							self.slider(self.Width - 135, 100, 100, 10, self.mouse, self.Density )
							self.printText ( "Density", (self.Width - 220), (95), 20 )
							self.printText (str(self.Density), (self.Width - 25), (95), 20 )

							# Handles all Gas collision and values
							self.particleCalculateGas ()
						
						# Render and draw particles
						self.renderGravity ()					
						self.renderGas ()					
						self.renderLiquid ()

						# Count up to 10,000 ms between frames for tooltips to go away
						self.rawTime += self.clock.get_rawtime()
						if self.rawTime < 10000 :
							# In program tutorial ToolTip
							self.renderTooltip ()

						# Update the screen and cap loops to 60 fps
						self.refreshScreen ()

				# Draws and handles collision for selecting a simuation type
				if self.simButton.collidepoint(self.mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) :
					self.simMenu = True
					while self.simMenu :

						self.renderSimulationMenu ()
						# Update the screen and cap loops to 60 fps
						self.refreshScreen ()

				# Draws and handles collision for quitting the program
				if self.quitButton.collidepoint(self.mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) :
					self.quitMenu = True

				# Draws and handles collision for quitting the program
				while self.quitMenu :
					
					self.renderQuitMenu ()
					self.refreshScreen ()

				if event.type == pygame.QUIT:
					run = False

			self.refreshScreen ()


# Clear and uncluttered mainLine !!!
if __name__ == "__main__":
	simulation = mainParticleSimulation()
	
	# DRIVERS can be ran alongside the main()
	#simulation.driver_1_1()
	#simulation.driver_2_1()
	#simulation.driver_2_2()
	#simulation.driver_3_1()
	#simulation.driver_4_1()
	#simulation.driver_4_2()
	#simulation.driver_5_1()
	#simulation.driver_8_1()
	#simulation.driver_9_1()

	# MAIN
	simulation.main()
