# What is NDFacile
NDFacile, l'outil qui rend les NDFs ... faciles !
    
Marre de passer des heures à scanner, lire, trier et recopier ?
-> Utilisez NDFacile ! 

Prenez des photos de vos factures, et NDFacile s'en occupe en quelques minutes.
L'outil récupère les photos, en extrait le texte, trie les images pour vous et vous donne la liste des factures.
Toutefois, attention à bien vérifier les résultats!

Afin de déterminer la meilleure option pour extraire le texte des photos des factures, NDFacile a été décliné en deux variantes:


**ndfacile-tesseract**
- Tesseract est un des modèles d'OCR à base de ML les plus connus. 
- Il est particulièrement léger et a fait ses preuves depuis des années.
- Cependant, il a du mal avec les documents froissés, effécés, ou abimés.
- Architecture simple: 1 conteneur, le script exécute le binaire tesseract puis parse les résultats

**ndfacile-OvisOCR2**
- OvisOCR2 est un modèle d'OCR à l'état de l'art (2026)
- Ce modèle nécessite une carte graphique, il est lancé dans un conteneur Docker vllm associé à un GPU NVIDIA
- Le conteneur vllm est très lourd (~25Gb)
- ça fonctionne hyper bien


Review honnête: 
- La qualité des résultats avec OvisOCR2 est infiniment meilleures, cependant il requière un stockage et GPU conséquent, et est bien plus lent. 
- Tesseract est bien plus rapide et léger, mais ne fonctionne correctement qu'avec des documents en parfait état (mes ndf sont souvent froissées donc pas très utilisable) 


## TODO
- [x] project layout ✅ 2026-10-22
- [x] dockerize ✅ 2026-10-22
- [x] research OCR ✅ 2026-10-22
- [x] implement basic OCR with Tesseract ✅ 2026-10-22
- [x] Regex only ✅ 2026-11-06
	- [x] take into account verbal dates - ie: 26 mai 2026 ✅ 2026-11-06
- [ ] implement vLLM OCR with OvisOCR2
	- [x] dev a 2 services architecture - app container + vllm ✅ 2026-11-10
		- [x] openai API class for ocr ✅ 2026-11-08
		- [x] use local cached model ✅ 2026-11-10
- [ ] Optimize tool performance
	- [ ] improve vllm performance
	- [ ] Make an image processing pipeline (contrast, etc..)
- [ ] Make tool more user friendly
	- [ ] CLI mode or maybe web interface
		- or simply place images in folder and run docker exec or smth
	- [ ] option to take a zip as input and make a zip as output

TODO: if host user doesn't have same UID as container user (1000), files will not be synced with host bind folder