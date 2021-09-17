function buscaQuadroHorariosAtualizado() {
	
	const xhr = new XMLHttpRequest();
	const url = '/'
	
	id_barbeiro = document.querySelector('.barbeiro[checked]').value;
	data = document.querySelector('#calendario').value;
	console.log(id_barbeiro, data)
	return false

	let params = `?id_barbeiro=${id_barbeiro}&data=${data}`

	xhr.onload = e => {
		if (xhr.status === 200) {
			alert('Funcionou')
			// const dados = JSON.parse(xhr.response)
			// atualizaQuadroHorarios(dados);
		} else if (xhr.status >= 400) {
			alert({code: xhr.status,text: xhr.statusText})
		}
	}

	xhr.open("GET", url + params, true);
	xhr.send()
}

function atualizaQuadroHorarios(dados) {
	// aqui ocorrerá as ações do DOM que mudará o quadro de horários
}