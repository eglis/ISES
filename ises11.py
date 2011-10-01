#!/usr/bin/env python3
import sys
"""
-----------------------------------------
Name:         ises11py
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
print ("ISES version 11 avec mini-SGF")
print ("Argument: Nom d'un fichier script Python à exécuter dans l'interpréteur")
print ("Commande: \"quit\" ou \"exit\" ou \"stop\" pour quitter")
print ("Commande: \"loadbin <fichier>\" pour charger un programme exécutable.")
print ("Commande: \"loadtxt <fichier>\" pour charger un programme texte.")
print ("Commande: \"mkfs <taille>\" pour créer un disque virtuelle.")
print ("Commande: \"ls\" pour la liste des fichiers dans le SGF.")
print ("Commande: \"ls -l\" pour la liste des fichiers et leur taille resp.")
print ("Commande: \"cat <fichier>\" pour afficher le contenu d'un fichier.")
print ("Commande: \"catfs\" pour afficher le contenu du disque virtuelle.")
print ("Commande: \"rm <fichier>\" pour supprimer le fichier du disque virtuelle.")
print ("Commande: \"file <fichier>\" pour afficher le type de fichier (exe ou txt).")
print ("Commande: \"wc <fichier>\" pour afficher le taille du fichier.")
print ("Commande: \"stat <fichier>\" pour afficher la position du i-node du fichier .")
print ("Commande: \"df\" pour afficher le taille max du disque virtuelle et la taille de l'espace libre.")
print ("\t<nom_fichier> exécute son contenu.")
print ("\tExécution du code par l'interpréteur Python et le résultat s'affiche.")
print()

# Module de sérialisation de données.
import marshal

# Système de fichier virtuelle en code binaire (type byte).
fs = b""

# Taille du système de fichier virtuelle.
taille_fs = 0

# Table des inodes (des descripteurs de fichiers)
# Un i-node est une liste contenant le nom du fichier, 
# le type de fichier ('x' ou 't'),
# la position du fichier dans le système de fichier "fs"
# et la taille du fichier.  Par exemple,
# [ 'fichier.py', 'x', 45, 90 ]
# Au départ, la table est vide.
table_inodes = []

# Console interactive
while True:
	reponse = input('>>> ').lower()
	if reponse == 'quit':
		break
	elif reponse == 'exit':
		break
	elif reponse == 'stop':
		break
	
	# On charge le fichier en mémoire.
	elif str.split(reponse, " ")[0] == "loadbin":
		fichier = str.split(reponse, " ")[1]

		print("Chargement du fichier exécutable " + fichier)

		# Lecture du contenu du fichier.
		fichier_obj = open(fichier,'r')
		fichier_source = fichier_obj.read()
		fichier_obj.close()
		reponse = fichier_source

		# Compilation du code.
		reponse_compilee = compile(reponse, '<string>', 'exec')

		# Conversion de l'objet en format byte-code.
		reponse_byte = marshal.dumps(reponse_compilee)

		if len(fs)  < taille_fs + len(reponse_byte):
			print ("Impossible de charger le fichier")
			print ("Le système de fichier est plein (taille = " + len(fs) + ")")
		else:
			debut = taille_fs 
			taille = int(len(reponse_byte))

			# On ajoute le code dans le système de fichier.
			fs = fs[:debut] + reponse_byte + fs[debut+taille:]

			# On crée le i-node du fichier chargé.
			table_inodes += [[ fichier, 'x', debut, len(reponse_byte) ]] 

			taille_fs += taille

	# On charge le fichier en mémoire.
	elif str.split(reponse, " ")[0] == "loadtxt":
		fichier = str.split(reponse, " ")[1]

		print("Chargement du fichier texte " + fichier)

		# Lecture du contenu du fichier.
		fichier_obj = open(fichier,'r')
		fichier_source = fichier_obj.read()
		fichier_obj.close()
		reponse = fichier_source

		# Conversion du texte en format byte-code.
		reponse_byte = bytes(reponse, 'iso-8859-1')

		# On vérifie 
		if len(fs)  < taille_fs + len(reponse_byte):
			print ("Impossible de charger le fichier")
			print ("Le système de fichier est plein (taille = " + str(len(fs)) + ")")
		else:
			debut = taille_fs 
			taille = int(len(reponse_byte))

			# On ajoute le code dans le système de fichier.
			fs = fs[:debut] + reponse_byte + fs[debut+taille:]

			# On crée le i-node du fichier chargé.
			table_inodes += [[ fichier, 't', debut, len(reponse_byte) ]] 

			taille_fs += taille

	elif str.split(reponse, " ")[0] == "mkfs":
		
		taille = str.split(reponse, " ")[1]
		
		# Format le système de fichier contenant que des car. nuls (\x00).
		fs = b'\x00' * int(taille)

		# Le système est vide au départ.
		taille_fs = 0
		
	# Affichage de la liste des fichiers.
	elif "ls" == reponse:
		for inode in table_inodes:
			print(str(inode[0]))
	
	# Affichage de la liste des fichiers en format long.
	elif "ls -l" == reponse:
		for inode in table_inodes:
			print(inode[0] + "\t" + inode[1] + "\t" + str(inode[3]))

	elif str.split(reponse, " ")[0] == "cat":
		
		fichier = str.split(reponse, " ")[1]


		# On cherche le inode du fichier dans la table des i-nodes.
		inode_fichier = []
		for inode in table_inodes:
			if inode[0] == fichier:
				inode_fichier = inode
				break

		if inode_fichier != []:

			debut = inode_fichier[2]
			taille = inode_fichier[3]
			contenu = fs[debut:debut+taille]

			# Si c'est un fichier texte, il faut le convertir.  Sinon, on le laisse tel quel.
			if inode_fichier[1] == 'x':
				contenu_a_afficher = marshal.loads(contenu)
			else:
				contenu_a_afficher = str(contenu, 'iso-8859-1')

			print(contenu_a_afficher)
		else:
			print("ERREUR: le fichier n'existe pas.")
		

	# Afficher le système de fichier tel quel.
	elif "catfs" == reponse:

		print(fs)

	# Effacer un fichier dans le système de fichier.
	elif str.split(reponse, " ")[0] == "rm":
	
		fichier = str.split(reponse, " ")[1]

		# On cherche le inode du fichier dans la table des i-nodes.
		for inode in table_inodes:
			if inode[0] == fichier:
				inode_fichier = inode
				break
		#inode_fichier = find(lambda inode: inode[0] == fichier, table_inodes)

		debut = inode_fichier[2]
		taille = inode_fichier[3]

		# On supprime le contenu du fichier.
		fs = fs[:debut] + b'\x00' * taille + fs[debut+taille:]
		
		# On supprime le inode du fichier dans la table des i-nodes.
		nouvelle_table_inodes = []
		for inode in table_inodes:
			if inode[0] != fichier:
				nouvelle_table_inodes += [inode]
		table_inodes = nouvelle_table_inodes

	# Afficher le type d'un fichier (texte ou exécutable)
	elif str.split(reponse, " ")[0] == "file":
		
		fichier = str.split(reponse, " ")[1]

		# On cherche le inode du fichier dans la table des i-nodes.
		for inode in table_inodes:
			if inode[0] == fichier:
				inode_fichier = inode
				break

		# On affiche le type du fichier inscrit dans son i-node.
		print(inode_fichier[1])

	# Afficher la position du inode dans la liste des inodes.
	elif str.split(reponse, " ")[0] == "stat":
		fichier = str.split(reponse, " ")[1]
		position = 0
		for inode in table_inodes:
			if inode[0] == fichier:
				break
			else:
				position += 1
		print("i-node: " + str(position))

	# Afficher la taille maximale du disque virtelle et la taille de l'espace libre.
	elif "df" == reponse:
		print("Taille maximale: " + str(len(fs)) + " caractères binaires.")
		print("Espace libre disponible: " + str(len(fs) - taille_fs) + " caractères binaires.")
	
	# Si on veut exécuter un fichier exécutable...
	elif reponse[-2:] == 'py':

		# On cherche le inode du fichier dans la table des i-nodes.
		inode_fichier = ''
		for inode in table_inodes:
			if inode[0] == reponse:
				inode_fichier = inode
				break

		# Si le nom du fichier est bon...
		if inode_fichier != '':

			# Si le fichier est exécutable, on l'exécute sinon on affiche un erreur.
			if inode_fichier[1] == 'x':
				debut = inode_fichier[2]
				taille = inode_fichier[3]
				contenu_fichier = fs[debut:debut+taille]
				try:
					exec(marshal.loads(contenu_fichier))
				except:
					print("ERREUR: Mauvaise interprétation Python.")
			else:
				print("ERREUR: le fichier n'est pas exécutable")
		else:
			print("ERREUR: le fichier n'existe pas.")


	else:
		try:
			print(exec(reponse))
		except:
			print("ERREUR: Mauvaise interprétation Python.")

print('Bye')
