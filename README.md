# Python-Chess
#### Video Demo:  https://youtu.be/dqfEToL8qfU
#### Description:
A Command Line, Object-Oriented implementation of Chess made in Python 3

##### INTRODUCTION

As someone who is interested in computer programming as it relates to game development, and also just the game of chess in general, I thought that teaching a computer how to play chess, understand its rules and make decisions, might be an interesting exercise to improve my understanding of both. I set out on this project with the goal of doing a ground up implementation of a classic game with easily understood(to a human) rules but considerable strategic depth, and found that it brought forth a number of concerns and challenges that I enjoyed overcoming.

##### LANGUAGE AND PARADIGM

I set out to make it in Python 3 out of an appreciation for and a desire to familiarize myself with such a common language in modern computing. It’s flexible, well supported, and multi-paradigm. As someone who learned to program in C, I have greater familiarity with imperative programming concepts, but I decided to implement primarily using object oriented programming concepts, that is, representing the different entities in the game as objects of different classes that are capable of using self contained methods to act upon their internal state. Chess as a game is consistent enough in scope that this was not strictly necessary, and I would like to come back to this project to try making an implementation that uses functional programming. However, object oriented programming is so common in game development that I thought it prudent to go with that here.

##### CLASSES

The classes created for this program, from the most general to the most specific, are as follows. All of them follow the convention of having capitalized names. First there is the Game class, which can be seen as representing an instance of the game as a whole. This contains data like information about the game mode, turn, and the Board the game is played on. The methods of the game are responsible for presenting the main menu, taking in commands, asking the AI player to make decisions, and file i/o for saving and loading. The Board class stores the current state of the board, including each instance of a Spot. The Board instance is queried to place and move pieces on the board, as well as find out what spots are occupied, threatened, or available. Each Spot can either be empty, or can be occupied by an instance of a Piece. A Piece instance contains data such as what kind of piece it is, what color it is, and methods to call that can generate the moves it is capable of making, represented as 2D vectors. In addition is the Position class, which is just an easy way to represent a position on the chess board, both as a vector and as the chess notation for that position(“ex. A1, E6, etc.”) in the same object.

##### GAME MODES AND STATES

This implementation supports multiple game modes, it supports the ability for two players to alternate inputting commands via the keyboard, for a player to play against an AI player, and even for the user to just watch the AI play against itself. In all cases, the program is aware of the rules of chess, and it stops both the players and the AI from making illegal moves. Invalid moves are rejected, the game detects and displays a notification when one player has the other in check, and the game also stops players from taking moves that leave themselves in check. When one player has checkmate on the other, the win condition is reached, a message is printed to display the winner and their final score, and the game ends.
