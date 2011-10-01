#!/usr/bin/env python3
"""
-----------------------------------------
Name:         ises5.py
Author:       Francois-Nicola Demers
Copyright:    (C) 2011 Francois-Nicola Demers
Licence:      GNU General Public Licence version 3
Website:      http://info.techorange.ca
Email:        fndemers at cegep-ste-foy.qc.ca
-----------------------------------------
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
-----------------------------------------
"""
print ("ISES version 5")
print ("Commande: \"quit\" ou \"exit\" ou \"stop\" pour quitter")
print ("\tEvaluation du texte par l'interpréteur Python et le résultat s'affiche.")
print()
while True:
	reponse = input('>>> ')
	if reponse == 'quit':
		break
	elif reponse == 'exit':
		break
	elif reponse == 'stop':
		break
	try:
		print(eval(reponse))
	except:
		print("ERROR: Mauvaise interprétation Python.")
print('Bye')

