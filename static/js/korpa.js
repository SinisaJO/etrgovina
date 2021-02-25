var updateBtns = document.getElementsByClassName('update-korpa')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var proizvodId = this.dataset.proizvod
		var action = this.dataset.action
		console.log('proizvodId:', proizvodId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieProizvod(proizvodId, action)
		}else{
			updateUserNarudzbina(proizvodId, action)
		}
	})
}

function addCookieProizvod(proizvodId, action){
	console.log('Korisnik nije prijavljen..')

	if (action == 'dodaj'){
		if (korpa[proizvodId] == undefined){
			korpa[proizvodId] = {'kolicina':1}
		}else{
			korpa[proizvodId]['kolicina'] += 1
		}
	}
	if (action == 'oduzmi'){
		korpa[proizvodId]['kolicina'] -= 1

		if(korpa[proizvodId]['kolicina'] <= 0){
			console.log('Obrisi proizvod')
			delete korpa[proizvodId]
		}
	}
	console.log('Korpa:', korpa)
	document.cookie = 'korpa=' + JSON.stringify(korpa) + ";domain;path=/"
	location.reload()
}


function updateUserNarudzbina(proizvodId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_proizvod/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body: JSON.stringify({'proizvodId': proizvodId, 'action': action})
		})
		.then((response) => {
			return response.json();
		})
		.then((data) => {
			location.reload()
		});
}
