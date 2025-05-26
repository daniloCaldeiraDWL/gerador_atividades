document.getElementById('tipo_habilidade').addEventListener('change', function() {
    const outraDiv = document.getElementById('outra_habilidade_div');
    const outraInput = document.getElementById('outra_habilidade');
    if (this.value === 'outra') {
        outraDiv.style.display = 'block';
        outraInput.required = true;
    } else {
        outraDiv.style.display = 'none';
        outraInput.required = false;
    }
});

document.getElementById('atividade-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const errorDiv = document.querySelector('.alert-danger') || document.createElement('div');
    if (!errorDiv.classList.contains('alert-danger')) {
        errorDiv.classList.add('alert', 'alert-danger', 'mt-3');
        document.querySelector('.container').appendChild(errorDiv);
    }
    const loadingDiv = document.getElementById('loading');
    errorDiv.style.display = 'none';
    loadingDiv.style.display = 'block';

    const numAtividades = document.getElementById('num_atividades').value;
    let tipoHabilidade = document.getElementById('tipo_habilidade').value;
    if (tipoHabilidade === 'outra') {
        tipoHabilidade = document.getElementById('outra_habilidade').value;
    }

    if (!numAtividades || isNaN(numAtividades) || numAtividades <= 0) {
        errorDiv.textContent = 'Por favor, insira um número válido de atividades.';
        errorDiv.style.display = 'block';
        loadingDiv.style.display = 'none';
        return;
    }

    if (!tipoHabilidade) {
        errorDiv.textContent = 'Por favor, selecione ou especifique uma habilidade.';
        errorDiv.style.display = 'block';
        loadingDiv.style.display = 'none';
        return;
    }

    try {
        console.log('Enviando requisição para /gerar:', { num_atividades: numAtividades, tipo_habilidade: tipoHabilidade });
        const response = await axios.post('/gerar', {
            num_atividades: numAtividades,
            tipo_habilidade: tipoHabilidade
        });

        console.log('Resposta recebida:', response.data);
        if (response.data.resultado) {
            localStorage.setItem('resultado', response.data.resultado);
            window.location.href = '/resultado';
        } else {
            errorDiv.textContent = response.data.erro || 'Não foi possível gerar o texto.';
            errorDiv.style.display = 'block';
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
        errorDiv.textContent = 'Erro ao conectar ao servidor: ' + (error.response?.data?.erro || error.message);
        errorDiv.style.display = 'block';
    } finally {
        loadingDiv.style.display = 'none';
    }
});