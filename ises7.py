#!/usr/bin/env python3
"""
-----------------------------------------
Name:         ises7.py
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

import marshal

print ("ISES version 7")
print ("Commande: \"quit\" ou \"exit\" ou \"stop\" pour quitter")
print ("\tExécution du code par l'interpréteur Python et le résultat s'affiche.")
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
		reponse_compilee = compile(reponse, '<string>', 'exec')
		reponse_string = marshal.dumps(reponse_compilee)
		
		# Impression du byte-code.
		print(repr(reponse_string))

		# Exécution après conversion en format objet.
		exec(marshal.loads(reponse_string))
	except:
		print("ERROR: Mauvaise interprétation Python.")
print('Bye')

