// Bloqueia datas retroativas a partir da data atual e seta data padrão
const hoje = new Date().toISOString().split('T')[0];

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
	for (let horario in horarios) {
		div = document.createElement('div');

		input = document.createElement('input');
		input.setAttribute('type', 'radio');
		input.setAttribute('value', horarios[horario]);
		input.setAttribute('name', 'horario');
		
		label = document.createElement('label');
		label.textContent = horarios[horario];

		div.append(input, label);
		
		quadro_horarios.appendChild(div)
	}
}