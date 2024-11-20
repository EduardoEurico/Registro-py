
document.getElementById("cadastroCrime").addEventListener("submit", async (event) => {
    event.preventDefault();

    const crimeDate = document.getElementById("crime_date").value;

    // Se houver um valor para a data, formate para o padrão ISO "YYYY-MM-DD"
    const formattedCrimeDate = crimeDate ? new Date(crimeDate).toISOString().split('T')[0] : null;

    if (!formattedCrimeDate) {
        alert("Data do crime é obrigatória.");
        return;
    }

    const dados = {
        crime_name: document.getElementById("crime_name").value,
        description: document.getElementById("description").value,
        crime_date: formattedCrimeDate, // Convertendo para o formato adequado
        res_hero: document.getElementById("res_hero").value,
        severity: parseInt(document.getElementById("severity").value) // Garantir que severidade seja número
    };

    console.log("Dados a serem enviados:", dados);

    try {
        const response = await fetch("/crimes/cadastrar", { // Certifique-se de usar a rota correta aqui
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        const result = await response.json();
        alert(result.message || result.error);
        window.location.reload();  // Recarrega a página

    } catch (error) {
        console.error("Erro ao cadastrar crime:", error);
    }
});

// Função para excluir um crime
document.querySelectorAll('.delete-button').forEach(button => {
    button.addEventListener('click', function() {
        let crimeId = this.dataset.id;  // Pega o ID do crime
        fetch(`/crimes/${crimeId}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                // Remover a linha da tabela após a exclusão
                let crimeRow = document.querySelector(`#crime-${crimeId}`);
                if (crimeRow) {
                    crimeRow.remove();  // Remove a linha da tabela
                }

                alert(data.message);  // Exibe a mensagem de sucesso
                window.location.reload();  // Recarrega a página após a exclusão
            } else {
                alert("Erro ao excluir o crime");
            }
        })
        .catch(error => {
            console.error('Erro ao excluir crime:', error);
            alert("Erro na comunicação com o servidor.");
        });
    });
});


document.addEventListener("DOMContentLoaded", function() {
    // Seleciona todos os botões de editar
    const editButtons = document.querySelectorAll('.edit-button');

    document.querySelectorAll(".edit-button").forEach(button => {
        button.addEventListener("click", async (event) => {
            const crimeId = event.target.dataset.id; // ID do crime
            const heroSelect = document.getElementById(`res_hero_${crimeId}`);

            if (!heroSelect) {
                console.error(`Elemento com ID 'res_hero_${crimeId}' não encontrado.`);
                return;
            }

            try {
                // Realiza a chamada à API para buscar os heróis
                const response = await fetch("/heroes/heroes");
                const heroes = await response.json();

                // Limpa as opções existentes
                heroSelect.innerHTML = '';

                // Adiciona os heróis como opções no select
                heroes.forEach(hero => {
                    const option = document.createElement("option");
                    option.value = hero.id;
                    option.textContent = hero.hero_name;

                    // Marca o herói já associado como selecionado
                    if (hero.id == heroSelect.dataset.selectedHero) {
                        option.selected = true;
                    }

                    heroSelect.appendChild(option);
                });

                // Exibe o formulário de edição (caso esteja oculto)
                const editForm = document.querySelector(`#crime-${crimeId} .edit-form`);
                if (editForm) {
                    editForm.style.display = "block";
                }
            } catch (error) {
                console.error("Erro ao carregar os heróis:", error);
            }
        });
    });

    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const crimeId = this.dataset.id; // Obtém o ID do crime

            // Encontra a linha correspondente ao crime
            const crimeRow = document.getElementById(`crime-${crimeId}`);

            if (!crimeRow) {
                console.error(`Linha do crime com ID ${crimeId} não encontrada.`);
                return;
            }

            // Encontra o formulário de edição dentro dessa linha
            const editForm = crimeRow.querySelector('.edit-form');

            // Alterna a visibilidade do formulário de edição
            if (editForm.style.display === 'none' || editForm.style.display === '') {
                editForm.style.display = 'block';
            } else {
                editForm.style.display = 'none';
            }

            // Carrega os dados do crime para o formulário de edição
            fetch(`/crimes/${crimeId}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById(`crime_name_edit_${crimeId}`).value = data.crime_name;
                    document.getElementById(`description_edit_${crimeId}`).value = data.description;
                    document.getElementById(`crime_date_edit_${crimeId}`).value = data.crime_date ? new Date(data.crime_date).toISOString().split('T')[0] : '';
                    document.getElementById(`severity_edit_${crimeId}`).value = data.severity;
                    document.getElementById(`res_hero_${crimeId}`).value = data.res_hero;
                })
                .catch(error => console.error('Erro ao obter dados do crime:', error));
        });
    });

    // Lógica para salvar as alterações do crime
    const submitEditButtons = document.querySelectorAll('.submit-edit');

    submitEditButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const crimeId = this.dataset.id;

            // Pega os dados do formulário de edição
            const crimeName = document.getElementById(`crime_name_edit_${crimeId}`).value;
            const description = document.getElementById(`description_edit_${crimeId}`).value;
            const crimeDate = document.getElementById(`crime_date_edit_${crimeId}`).value;
            const severity = document.getElementById(`severity_edit_${crimeId}`).value;
            const resHero = document.getElementById(`res_hero_${crimeId}`).value;

            const formattedCrimeDate = crimeDate ? new Date(crimeDate).toISOString().split('T')[0] : null;

            const dados = {
                crime_name: crimeName,
                description: description,
                crime_date: formattedCrimeDate,
                severity: severity,
                res_hero: resHero
            };

            try {
                const response = await fetch(`/crimes/${crimeId}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(dados)
                });

                const result = await response.json();
                alert(result.message || result.error);
                window.location.reload(); // Recarrega a página após a ação
            } catch (error) {
                console.error("Erro ao editar crime:", error);
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", async () => {
    const heroSelect = document.getElementById("res_hero");

    if (!heroSelect) {
        console.error("Elemento com ID 'res_hero' não encontrado.");
        return;
    }

    try {
        const response = await fetch('/heroes/heroes');
        const heroes = await response.json();

        heroes.forEach(hero => {
            const option = document.createElement('option');
            option.textContent = hero.hero_name;

            heroSelect.appendChild(option);
        });
        //log dos dados
        console.log("Dados dos heróis carregados:", heroes);
    } catch (error) {
        console.error('Erro ao carregar os heróis:', error);
    }
});

// Removed duplicate DOMContentLoaded event listener
