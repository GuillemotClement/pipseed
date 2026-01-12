# Développer une cli avec Bun 

On viens ajouter en premiere ligne le truc pour indiquer quel bin doit lancer le projet 
`#!/usr/bin/env bun` 

On viens rendre le script exécutable 
`chmod +x src/index.ts` 

On peut ensuite lancer le tool 
`.index.ts cmd`

Pour récupérer les commandes : `const [command] = Bun.argv.slice(2);`