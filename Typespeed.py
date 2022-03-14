# TypeSpeed

import Draw
import time
import random

# lanes -  [[word, xPosition], [word, xPosition], [], [word, xPosition] ...]
# initialize 20 lanes, each with an empty string and an x-position of 0
def initializeLanes(): 
	return [["", 0] for i in range(20)]

# define dictionary of 1000 words
def listOfWords():
	# open file with list of words and begin adding to the python 
	# list of words
	fileInput = open("1000words.txt")
	words = [fileInput.readline().strip().upper()]
	
	# loop through the list of words and continue adding them to the 
	# python list
	for i in range(999):
		line = fileInput.readline().strip().upper()
		words += [line]
		
	# close the word file
	fileInput.close()
	
	# return the list of words
	return words
	
# draw the title in bold, at the top center of the screen
def drawTitle(lengthOfBoard):
	# set font size, turn on bold, set color
	Draw.setFontSize(50)
	Draw.setFontBold(True)
	Draw.setBackground(Draw.BLACK)	
	Draw.setColor(Draw.CYAN)
	
	# write "TypeSpeed" at the top of screen
	Draw.string("TypeSpeed", (lengthOfBoard/2) - 150, 30)
	
	# turn font size back to 30, turn off bold
	Draw.setFontSize(30)
	Draw.setFontBold(False)

# draw the instructions
def drawInstructions():
	Draw.setColor(Draw.WHITE)
	Draw.string("- Type the words that appear on the screen", \
		    0, 110)
	Draw.string("- To clear the last letter typed, press DELETE",\
		    0, 170)	
	Draw.string("- To clear the word being typed, press ENTER",\
		    0, 230)	
	Draw.string("- When the word being typed matches the word" + \
		    " on the screen,", 0, 290)
	Draw.string("  the word on the screen will automatically" + \
		    " disappear", 0, 330)
	Draw.string("- You have three lives. When three words fall" + \
		    " off the right", 0, 390)
	Draw.string("  side of the screen, you are out.", 0, 430)
	Draw.string("- Choose a level to begin!", 0, 490)

# build the difficulty buttons
# accept the color of button, x-position of rectangle, name of difficulty 
# level, x-position of name of difficulty level
def drawSingleDifficultyButton(color, xofRect, name, xOfName):
	# set the color of the difficulty button and draw the rectangle
	# with its proper x-coordinate
	Draw.setColor(color)
	Draw.filledRect(xofRect, 485, 140, 50)
	
	# set the font to bold, set the text-color to black, draw the name of
	# the difficulty level in black with it's correct x-position
	Draw.setFontBold(True)
	Draw.setColor(Draw.BLACK)
	Draw.string(name, xOfName, 495)
	
	# turn off the bold font
	Draw.setFontBold(False)
	
# draw the difficulty buttons using the function that builds them
def drawDifficultyButtons():
	# draw the EASY button	
	drawSingleDifficultyButton(Draw.GREEN, 350, "EASY", 381)
	
	# draw the MEDIUM button
	drawSingleDifficultyButton(Draw.YELLOW, 540, "MEDIUM", 550)
	
	# draw the HARD button
	drawSingleDifficultyButton(Draw.RED, 730, "HARD", 759)

# keep looping until user clicks one of the designated areas on the screen 
# (until a difficulty level has been chosen)
def waitUntilUserChoosesDifficulty():	
	# while the user has not clicked any of the 3 difficulty levels
	while not (Draw.mousePressed() \
	           and ((Draw.mouseX() >= 350 and Draw.mouseX() <= 490 \
			 and Draw.mouseY() >= 485 and Draw.mouseY() <= 535) \
		   or (Draw.mouseX() >= 540 and Draw.mouseX() <= 680 \
			and Draw.mouseY() >= 485 and Draw.mouseY() <= 535) \
		   or (Draw.mouseX() >= 730 and Draw.mouseX() <= 870 \
			and Draw.mouseY() >= 485 and Draw.mouseY() <= 535))):
		# keep displayng the instructions page
		pass
		
# allow difficulty level to be chosen, return the chosen difficulty level
def getDifficultyFromUser():
	difficulty = None
	
	# if "EASY" is chosen, set difficulty to easy
	if (Draw.mouseX() >= 350 and Draw.mouseX() <= 490 \
			 and Draw.mouseY() >= 485 and Draw.mouseY() <= 535):
		difficulty = "EASY"
		
	# if "MEDIUM" is chosen, set difficulty to medium
	elif (Draw.mouseX() >= 540 and Draw.mouseX() <= 680 \
			and Draw.mouseY() >= 485 and Draw.mouseY() <= 535):
		difficulty = "MEDIUM"
		
	# if "HARD" is chosen, set difficulty to hard
	elif (Draw.mouseX() >= 730 and Draw.mouseX() <= 870 \
			and Draw.mouseY() >= 485 and Draw.mouseY() <= 535):
		difficulty = "HARD"
		
	return difficulty

# While the user has not chosen a level, keep the instructions
# page open. Once a difficulty level has been chosen, return the difficulty 
# level (and stop displaying the instructions page).
def waitThenGetDifficulty():	
	waitUntilUserChoosesDifficulty()
	
	return getDifficultyFromUser()

# initialize the canvas; call various functions
def initializeCanvas(lengthOfBoard, heightOfBoard):	
	# set canvas size and background color
	Draw.setCanvasSize(lengthOfBoard, heightOfBoard)
	Draw.setBackground(Draw.BLACK)
	
	# call the function that draws "TypeSpeed" at the top of the 
	# instructions page
	drawTitle(lengthOfBoard)
	
	# call the function that draws the instructions
	drawInstructions()
	
	# call the function that draws the "EASY", "MEDIUM", and "HARD" buttons
	drawDifficultyButtons()
	
	# call the function that waits for user to choose a difficulty button
	# and then returns the chosen difficulty level
	return waitThenGetDifficulty()

# draw the bar of information at the bottom of the canvas
def drawInfoBar():
	# set color and font size
	Draw.setColor(Draw.CYAN)
	Draw.setFontSize(20)
	
	# draw a line to separate the infoBar from the rest of the canvas
	Draw.line(0, 555, 900, 555)
	
	# ">>" indicates where the word is being typed
	Draw.string(">> ", 0, 560)
	
	# "score" indicates the score
	Draw.string("Score: ", 350, 560)
	
	# "CpS" indicates the characters per second
	Draw.string("CpS: ", 530, 560)
	
	# "Lives Remaining" starts at 3 and decrements as words fall of the 
	# right side of the screen
	Draw.string("Lives Remaining: ", 680, 560)

# update the lanes' x-positions
def shiftWordsInLanes(lanes, laneShiftPixels):
	# loop through lanes
	for i in range(len(lanes)):
		# increment all x-positions
		lanes[i][1] += laneShiftPixels
			
	return lanes

# decrement livesRemaining after a word exits the screen's right end		
def decrementLives(lanes, livesRemaining, lengthOfBoard):
	# loop through lanes
	for i in range(len(lanes)):	
		# if a non-empty word exists the screen's right end,
		# and if there are lives remaining, decrement 
		# livesRemaining by one
		if lanes[i][0] and lanes[i][1] >= lengthOfBoard \
		   and livesRemaining > 0:
			livesRemaining -= 1
			
	return livesRemaining
			
# empty the lane after a word exits the screen's right end
def emptyLane(lanes, lengthOfBoard):
	# loop through lanes
	for i in range(len(lanes)):
		# if a non-empty word went off the screen's right end,
		# make the lane empty
		if lanes[i][0] and lanes[i][1] >= lengthOfBoard:		
			lanes[i][0] = ""
			
	return lanes

# rate of words being added increases as score increases
def incrementRate(score, difficulty, rateOfAddedWords):
	# while the score is divisible by 5 (at 5 point increments)
	# add a constant number to the rate of whether a word should
	# be added
	if not (score % 5):
		if difficulty == "EASY":
			return rateOfAddedWords + 0.00001
		elif difficulty == "MEDIUM":
			return rateOfAddedWords + 0.00004
		elif difficulty == "HARD":
			return rateOfAddedWords + 0.00007
		
	# when the score is not divisble by 5, return the previous rate
	else:
		return rateOfAddedWords
	
# decide whether a new word is added to the lane
# input score, difficulty, rateOfAddedWords, and return boolean whether 
# to replace word
def decideWhetherWordIsAdded(score, difficulty, rateOfAddedWords):
	return random.random() <= rateOfAddedWords

# draw the updates of the infoBar at the bottom of the canvas
def updateInfoBar(wordTypedSoFar, score, charactersTypedSoFar, startingTime, \
	      LivesRemaining):
	# set color, font size
	Draw.setColor(Draw.WHITE)
	Draw.setFontSize(20)
	
	# draw wordTypedSoFar (initially "")
	# capped at 15 letters in case the user types without clearing
	Draw.string(str(wordTypedSoFar)[:15], 30, 560)
	
	# draw the score (how many words have been typed so far)
	Draw.string(str(score), 430, 560)	
	
	# draw characters per second (CpS) - capped at 5 integers
	Draw.string(str(charactersTypedSoFar / \
			(time.time() - startingTime))[:5], 590, 560)
	
	# draw the number of lives remaining
	Draw.string(str(LivesRemaining), 850, 560)	
	
# alert the user to clear wordTypedSoFar after 15 characters have 
# been typed		
def alertUser(wordTypedSoFar):
	if len(wordTypedSoFar) >= 15:
		# alert appears in red
		Draw.setColor(Draw.RED)	
		# alert appears in the infoBar under the word being typed
		Draw.string("Press ENTER to clear the word", 0, 580)		

# draw each word in its assigned color		
def correctColor(lanes, lengthOfBoard):
	# loop through the lanes
	for i in range(len(lanes)):
		# if word in last quarter of board, turn red
		if lanes[i][1] >= (.75 * lengthOfBoard):
			Draw.setColor(Draw.RED)
		# if word between second half and last quarter of board, 
		# turn yellow
		elif lanes[i][1] >= (.5 * lengthOfBoard):
			Draw.setColor(Draw.YELLOW)
		# if word in first half of board, appears green
		else:
			Draw.setColor(Draw.GREEN)
			
		# draw the words (each in their correct color)	
		Draw.string(lanes[i][0], lanes[i][1], i * 27)	

# highlight the word on the board in white as it's being typed	
def highlightWord(lanes, wordTypedSoFar):
	# loop through the lanes
	for i in range(len(lanes)):
		# if the word being typed matches the start of a word on 
		# the board
		if lanes[i][0].startswith(wordTypedSoFar):
			# highlight the part that's being typed
				Draw.setColor(Draw.WHITE)
				Draw.string(lanes[i][0] \
					    [0:len(wordTypedSoFar)],\
					    lanes[i][1], i * 27)
				
# update the canvas to its correct color, infoBar settings, and highlightings
def gameUpdates(wordTypedSoFar, score, charactersTypedSoFar, \
		startingTime, LivesRemaining, lanes, lengthOfBoard):
	# update the information bar at the bottom of the screen
	updateInfoBar(wordTypedSoFar, score, charactersTypedSoFar, \
		      startingTime, LivesRemaining)
	
	# alert the user to press "return" when 15 characters have been typed
	# (in order to clear wordTypedSoFar)
	alertUser(wordTypedSoFar)
	
	# draw the words in their correct colors
	correctColor(lanes, lengthOfBoard)
	
	# highlight the word as its being typed
	highlightWord(lanes, wordTypedSoFar)

# if wordTypedSoFar matches a word on the screen, increment the score by one,
# empty the lane with that word, make wordTypedSoFar an empty string, and
# change the rate of the words being added if appropriate (the rate 
# changes at 5 point increments)
# return the score, wordTypedSoFar, and the newly incremented rateOfAddedWords
def matchesWordOnScreen(i, wordTypedSoFar, lanes, score, rateOfAddedWords, \
			difficulty):
	# if the word being typed is non-empty and in a lane
	if wordTypedSoFar and wordTypedSoFar == lanes[i][0]:
		# increment the score
		score += 1
		
		# remove the word from the lane
		lanes[i][0] = ""
		
		# re-initialize wordTypedSoFar to ""
		wordTypedSoFar = ""	
		
		# change rateOfAddedWords according to the algorithm in the
		# function incrementRate
		rateOfAddedWords = incrementRate(score, difficulty, \
			rateOfAddedWords)		
	
	return score, wordTypedSoFar, rateOfAddedWords

# add random words according to the algorithm in decideWhetherWordIsAdded
def addWords(lanes, score, difficulty, rateOfAddedWords):	
	# for each lane
	for lane in lanes:
		# if the lane is empty
		if not lane[0]:
			# call function decideWhetherWordIsAdded to
			# see whether to add a word to the empty lane
			if decideWhetherWordIsAdded(score, difficulty, \
					rateOfAddedWords):
				# if a word is being added, add random 
				# word from word-list and set x-position to 0
				lane[0] = random.choice(listOfWords())
				lane[1] = 0
				
# When there are zero lives remaining, print "GAME OVER" in a box
def gameOver(lengthOfBoard, heightOfBoard):
	# draw white box
	Draw.setColor(Draw.WHITE)
	Draw.filledRect((lengthOfBoard/2) - 150, \
			(heightOfBoard/2) - 75, 300, 150)
	
	# draw "Game Over" in red inside the white box
	Draw.setColor(Draw.RED)	
	Draw.string("GAME \nOVER", (lengthOfBoard / 2) - 30, \
		    (heightOfBoard / 2) - 20)
	
	Draw.show()
	
# main:
def main():
	# initialize variables
	# initialize lengthOfBoard
	lengthOfBoard = 900	
	# initialize heightOfBoard
	heightOfBoard = 600
	# initialize canvas and return difficulty
	difficulty = initializeCanvas(lengthOfBoard, heightOfBoard)
	# initialize the lanes list as all empty
	lanes = initializeLanes()
	# initialize x-position increments
	laneShiftPixels = 1
	# initialize charactersTypedSoFar to 0	
	charactersTypedSoFar = 0
	# initialize startingTime to the time the game started	
	startingTime = time.time()
	# initialize livesRemaining to 3	
	livesRemaining = 3
	# initialize wordTypedSoFar to an empty string	
	wordTypedSoFar = ""
	# initialize score to 0	
	score = 0
	# initialize the rate at which words are added
	rateOfAddedWords = 0.0007
		
	# while there are lives remaining
	while livesRemaining > 0:
		# if the user typed a key:
		if Draw.hasNextKeyTyped():
			# get the key
			nextKeyTyped = Draw.nextKeyTyped().upper()
			# allow "backspace" key to delete last key typed
			if nextKeyTyped == "BACKSPACE":
				wordTypedSoFar = wordTypedSoFar[:-1]
			# allow "enter" key to erase wordTypedSoFar
			elif nextKeyTyped == "RETURN":
				wordTypedSoFar = ""
			# allow "quoteright" key to appear as an apostrophe
			elif nextKeyTyped == "QUOTERIGHT":
				wordTypedSoFar += "'"
			# if anything else was typed
			elif nextKeyTyped in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
				# increment charactersTypedSoFar
				charactersTypedSoFar += 1
				# add the character to the end of the 
				# word so far
				wordTypedSoFar += nextKeyTyped
				
				#* loop through the lanes
				# call the function that increments the score, 
				# makes wordTypedSoFar an empty string, and 
				# increments the rate of words being added if 
				# wordTypedSoFar matches a word on the screen 
				# set variables to what the function returns
				for i in range(len(lanes)):
					score, wordTypedSoFar, rateOfAddedWords\
						= matchesWordOnScreen(i,\
							wordTypedSoFar, \
							lanes, score,\
							rateOfAddedWords, \
							difficulty)
		
		# move words across the screen
		lanes = shiftWordsInLanes(lanes, laneShiftPixels)
		
		# decrement livesRemaining when a word exits the screen's
		# right end
		livesRemaining = decrementLives(lanes, livesRemaining, \
						lengthOfBoard)
		
		# empty the lane when a word exits the screen's right end 
		emptyLane(lanes, lengthOfBoard)
		
		# add words to the lanes based on the algorithm
		addWords(lanes, score, difficulty, rateOfAddedWords)

		# clear board, draw board, show board
		
		Draw.clear()
		
		# draw the information bar at the bottom of the screen
		drawInfoBar()
		
		# draw the game updates (wordTypedSoFar, score, CpS,
		# livesRemaining, correctly highlighted words, correctly
		# colored words, alert user if necessary)
		gameUpdates(wordTypedSoFar, score, charactersTypedSoFar, \
			   startingTime, livesRemaining, lanes, lengthOfBoard)
		
		Draw.show()
	
	# draw "Game Over" when there are no lives left	
	gameOver(lengthOfBoard, heightOfBoard)

main()
