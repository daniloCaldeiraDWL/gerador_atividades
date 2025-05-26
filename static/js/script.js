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
    const errorDiv = document.querySelector('.alert-danger');
    const loadingDiv = document.getElementById('loading');
    if (errorDiv) errorDiv.style.display = 'none';
    loadingDiv.style.display = 'block';

    const numAtividades = document.getElementById('num_atividades').value;
    let tipoHabilidade = document.getElementById('tipo_habilidade').value;
    if (tipoHabilidade === 'outra') {
        tipoHabilidade = document.getElementById('outra_habilidade').value;
    }

    if (!numAtividades || isNaN(numAtividades) || numAtividades <= 0) {
        if (errorDiv) errorDiv.textContent = 'Por favor, insira um número válido de atividades.';
        if (errorDiv) errorDiv.style.display = 'block';
        loadingDiv.style.display = 'none';
        return;
    }

    if (!tipoHabilidade) {
        if (errorDiv) errorDiv.textContent = 'Por favor, selecione ou especifique uma habilidade.';
        if (errorDiv) errorDiv.style.display = 'block';
        loadingDiv.style.display = 'none';
        return;
    }

    try {
        const response = await axios.post('/gerar', {
            num_atividades: numAtividades,
            tipo_habilidade: tipoHabilidade
        });

        if (response.data.resultado) {
            localStorage.setItem('resultado', response.data.resultado);
            window.location.href = '/resultado';
        } else {
            if (errorDiv) errorDiv.textContent = response.data.erro || 'Não foi possível gerar o texto.';
            if (errorDiv) errorDiv.style.display = 'block';
        }
    } catch (error) {
        if (errorDiv) errorDiv.textContent = 'Erro ao conectar ao servidor: ' + error.message;
        if (errorDiv) errorDiv.style.display = 'block';
    } finally {
        loadingDiv.style.display = 'none';
    }
});