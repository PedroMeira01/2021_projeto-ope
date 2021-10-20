const hoje = bloqueiaDatasRetroativas();

const calendario = document.querySelector("#calendario");
calendario.setAttribute('min', hoje);
calendario.value = hoje;

const quadro_horarios = document.querySelector('#quadro-horarios');

function buscaQuadroHorariosAtualizado() {
	const xhr = new XMLHttpRequest();
	const url = '/';
	
	let id_barbeiro;
	const barbeiros = document.querySelectorAll('.barbeiro');
	for (let barbeiro in barbeiros) {
		if (barbeiros[barbeiro].checked == true) {
			id_barbeiro = barbeiros[barbeiro].value
		}
	}

	data = calendario.value;

	const params = `?id_barbeiro=${id_barbeiro}&data=${data}`;

	xhr.onload = e => {
		if (xhr.status === 200) {
			const dados = xhr.response;
			atualizaQuadroHorarios(dados);
		} else if (xhr.status >= 400) {
			console.log({code: xhr.status,text: xhr.statusText});
		}
	}

	xhr.open("GET", url + params, true);
	xhr.send();
}

function atualizaQuadroHorarios(dados) {
	const horarios = JSON.parse(dados);
	// Remove os horários
	while (quadro_horarios.lastChild) {
		quadro_horarios.removeChild(quadro_horarios.lastChild);
	}
	// Recria o quadro
	let x = 0;
	for (let horario in horarios) {
		let hora = 'hour' +  x;
		let boxHorario = document.createElement('div');
		boxHorario.setAttribute('class', 'col-3 bgc-brown schedule__time');

		let input = document.createElement('input');
		input.setAttribute('type', 'radio');
		input.setAttribute('value', horarios[horario]);
		input.setAttribute('name', 'horario');
		input.setAttribute('class', 'form__radio-input');
		input.setAttribute('id', hora);
		
		let label = document.createElement('label');
		label.textContent = horarios[horario];
		label.setAttribute('class', 'form__radio-label');
		label.setAttribute('id', hora);
		label.setAttribute('for', hora);

		let span = document.createElement('span');
		span.setAttribute('class', 'form__radio-button');

		label.append(span);
		boxHorario.append(input, label);
		
		quadro_horarios.appendChild(boxHorario);
		x++;
	}
		
}

function bloqueiaDatasRetroativas() {
    	let hoje = new Date(),
        mes = '' + (hoje.getMonth() + 1),
        dia = '' + hoje.getDate(),
        ano = hoje.getFullYear();

    if (mes.length < 2) 
        mes = '0' + mes;
    if (dia.length < 2) 
        dia = '0' + dia;

    return [ano, mes, dia].join('-');
}