# Ilmoitustaulu
Taulu, johon voi ilmoittaa asioista






Ympäristö ohje:
	asenna virtual box 
	asenna virtuaalikone snapshotista
	asenna koneelle git "sudo apt install git"
	pullaa gitista
		vaatii rekisteröitymisen githubiin ja kutsun projektiin jotta voi muokata (push)
	virtuaali koneella projekti sijaitseeprojekti koti kansioon esm. "ron@ron-VirtualBox:~$ git clone https://github.com/ronttonen/Ilmoitustaulu.git"
		sen jälkeen projekti sijaitsee kansiossa "~/ilmoitustaulu" / "/home/ron/ilmoitustaulu"
	laita gittiin tietosi
		git config --global user.email "you@example.com"
		git config --global user.name "Your Name"
	Flask/serverin käynnistys ensimmäisen kerran mene kansioon "~/ilmoitustaulu"
		export FLASK_APP=ilmoitustaulu 
		pip install -e . 
		flask run
	Flask/serverin käynnistys jatkossa
		flask run
		
	nettisivun pitäisi olla osoitteessa http://127.0.0.1:5000/ VIRTUAALI KONEESSA
		
		
Editointi:
	Avaa vasemmasta reunasta "Komodo edit"
	jos kysyy jotain ei vanhna palauttamisesta paina "ei"/"No"
	avaa projekti "open project", suunnista kansioon johon aikaisemmin pullasit projekti kuten ~/ilmoitustaulu ja avaa sieltä komodo tiedosto
	
	http://pythonhow.com/building-a-website-with-python-flask/ <--- ohjeita kuinka editoida / ohjelmoid appia.
	
GIT KÄYTTÖ:
	Lataa muiden tekemät muutokset
		git pull
		
	- jokainen commit on oma versionsa, eli kannaattaa aina kun on saanut jotain "konkreettista" aikaiseksi niin tehdä "git add -A" eli lisää kaikki tiedostot committiin ja sen jälkeen "git commit -m "kommentti"" commit luo version ja ns talleettaa sen
	Kaikkia committeja ei tarvitse erikseen puskea esim. voit tehdä vaikka:
		muokkaa etusivu
			git add -A
			git commit -m "korjattu etusivu otsikko"
			muokkaa navi palkkia
			git add -A
			git commit -m "korjattu nav palkki"
			muokkaa backend 
			git add -A 
			git commit -m "backend fix"
			git push
	aina ei tarvitse pull, mutta olisi hyvä kuitenkin kehittää aina ajantasalla olevaan ympäristöön
	gitissä on myös brancheja mutta ne on parempi käyäd läpi kasvotusten tai jättää mahd kokonaan pois mikäli ne eivät ole tuttuja
	
	Confilctit pitää käydä läpi kasvotusten :D
	
	laita omat muutokset muille
		git add -A
		git commit -m "KUVAA MUUTOKSIA YKSINKERTAISESTI"
		git push