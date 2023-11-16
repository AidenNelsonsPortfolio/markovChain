# Author: Aiden Nelson
# Date of Start: 11/14/2023
# Date of Completion: 11/16/2023
# 
# Running Instructions: python project.py
# 
# Input Instructions:
# 	1. Choose a text file (by index) from the list of text files in the CWD
# 	2. Enter a kGram (depth) to use for the Markov Chain
# 	3. Enter the length of text to generate
#
# Description: 
# This file will implement a Markov Chain to generate text based on a given text file.
# It takes in a text file path (based upon text files in CWD), 
# a kGram (depth), as well as the length of text to generate.
# 
# The program works by using a trie to store prefixes of up to the order depth, and then
# the program will then generate text by randomly selecting a prefix given the last n characters.
#
# All generated text is output to the console, and the selections are similarly made through there.
#


# Imports
import random
import os


# TrieNode class
class TrieNode:
	def __init__(self, val:str):
		self.val = val
		self.children = {}
		self.freq = 0

	def __repr__(self):
		return self.freq.__repr__()


# Function definitions
# Function to add a prefix to the tree (or increment its frequency if it has been seen)
def addPrefix(root: TrieNode, prefix: str):
	curNode = root
	for ch in prefix:
		childNode = None
		if ch not in curNode.children:
			childNode = TrieNode(ch)
			curNode.children[ch] = childNode
		else:
			childNode = curNode.children[ch]
		childNode.freq += 1
		curNode = childNode


# Function to get a random prefix from the trie
def getRandomPrefix(root: TrieNode, curPrefix:str):
	# print("Current prefix: " + curPrefix)
	curNode = root
	# Get down to the level of the current prefix
	for ch in curPrefix:
		curNode = curNode.children[ch]

	# First generate a random number between 0 and the total frequency
	randNum = random.randint(0, curNode.freq)

	# Now, iterate over the children and find the one that matches the random number
	for ch in curNode.children.keys():
		if randNum <= curNode.children[ch].freq:
			# print("Chosen char: " + ch)
			return ch
		randNum -= curNode.children[ch].freq


# Main driver function of the file
def main(filepath: str, kGram: int, outputLen: int):
	prefixLength = kGram + 1

	# Read in the file (ASSUMES A UTF-8 ENCODING)
	try: 
		with open(filepath, "r", encoding="utf-8") as f:
			text = f.read()
		if len(text) < prefixLength:
			print("Text file is shorter than kGram requires, exiting...")
			exit()
	except:
		print("Error reading file, exiting...")
		exit()

	# Iterate over all characters, use the trie structure to store prefixes
	root = TrieNode("ROOT")

	# Iterate over all characters in the text
	for i in range(len(text)):
		# Get the prefix (INCLUDING the current character)
		prefix = text[i:i+prefixLength]

		# If the prefix is shorter than the kGram requires, grab the rest from the beginning
		if(len(prefix) < prefixLength):
			prefix = prefix + text[0:prefixLength-len(prefix)]

		# Add the prefix to the trie
		addPrefix(root, prefix)

	# Set the root's frequency for probability
	root.freq = len(text)

	# Print out results
	print("Generating results...\n")

	# Now, generate text
	totalLength = 0
	curPrefix = ""
	while(totalLength < outputLen):
		# Get a random prefix
		newPrefix = getRandomPrefix(root, curPrefix)

		# Add the new prefix to the output
		print(newPrefix, end="")
		totalLength += 1

		curPrefix += newPrefix

		# Update the current prefix, slide window or add depending on current length
		if len(curPrefix) == prefixLength:
			curPrefix = curPrefix[1:]

	print("\n\nProgram has finished.")


# Call main function
if(__name__ == "__main__"):
	# Get user to choose from available text files:
	print("Choose the number of the text file to read from:")
	files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.txt')]
	for idx, file in enumerate(files, 1):
		print(f"\t{idx}. {file}")

	# Read in file (number) choice from user
	fileChoice = input("Selection: ")
	if fileChoice == "" or not fileChoice.isdigit() or int(fileChoice) <= 0 or int(fileChoice) > len(files):
		print("Bad file choice, exiting...")
		exit()
	
	# Get the filepath corresponding to the numerical choice by the user
	filepath = files[int(fileChoice)-1]

	# Read in kGram input from user
	kGram = input("Enter kGram: ")
	if kGram == "" or not kGram.isdigit() or int(kGram) < 0 or int(kGram) > 8:
		print("Invalid kGram entered (0 <= kGram <= 8), exiting...")
		exit()

	# Read in output length input from user
	outputLen = input("Enter output length: ")
	if outputLen == "" or not outputLen.isdigit() or int(outputLen) < 1:
		print("Invalid output length entered, exiting...")
		exit()

	print("\nComputing Markov chain...\n")

	# Call main function
	main(filepath, int(kGram), int(outputLen))
