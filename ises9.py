#!/usr/bin/env python3
import sys
"""
-----------------------------------------
Name:         ises9.py
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
print ("ISES version 9")
print ("Argument: Nom d'un fichier script Python à exécuter dans l'interpréteur")
print ("Commande: \"quit\" ou \"exit\" ou \"stop\" pour quitter")
print ("Commande: \"load <fichier>\" pour charger un programme en mémoire.")
print ("\t<nom_fichier> exécute son contenu.")
print ("\tExécution du code par l'interpréteur Python et le résultat s'affiche.")
print()

# Module de sérialisation de données.
import marshal

# Extraction des arguments du script
fichier = ""
fichier_source = ""
if len(sys.argv) > 1:
	fichier = sys.argv[1]
	print("Chargement du fichier " + fichier)

	# Lecture du contenu du fichier.
	fichier_obj = open(fichier,'r')
	fichier_source = fichier_obj.read()
	fichier_obj.close()


# Console interactive
while True:
	reponse = input('>>> ').lower()
	if reponse == 'quit':
		break
	elif reponse == 'exit':
		break
	elif reponse == 'stop':
		break
	# On exécute le code du fichier 
	elif reponse == fichier:
		reponse = fichier_source
	
	# On charge le fichier en mémoire.
	elif str.split(reponse, " ")[0] == "load":
		fichier = str.split(reponse, " ")[1]

		print("Chargement du fichier " + fichier)

		# Lecture du contenu du fichier.
		fichier_obj = open(fichier,'r')
		fichier_source = fichier_obj.read()
		fichier_obj.close()
		reponse = fichier_source
	try:

		# Compilation du code.
		reponse_compilee = compile(reponse, '<string>', 'exec')

		# Conversion de l'objet en format byte-code.
		reponse_string = marshal.dumps(reponse_compilee)

		## Impression du byte-code.
		#print(repr(reponse_string))
		
		# Exécute le byte-code.
		exec(marshal.loads(reponse_string))

	except:
		print("ERROR: Mauvaise interprétation Python.")
print('Bye')
