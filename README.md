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

		
Editointi:
	Avaa vasemmasta reunasta "Komodo edit"
	jos kysyy jotain ei vanhna palauttamisesta paina "ei"/"No"
	avaa projekti "open project", suunnista kansioon johon aikaisemmin pullasit projekti kuten ~/ilmoitustaulu ja avaa sieltä komodo tiedosto
	
	http://pythonhow.com/building-a-website-with-python-flask/ <--- ohjeita kuinka editoida / ohjelmoid appia.