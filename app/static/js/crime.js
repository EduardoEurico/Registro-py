document.getElementById("cadastroCrime").addEventListener("submit", async (event) => {
    event.preventDefault();

    const crimeDate = document.getElementById("crime_date").value;

    // Se houver um valor para a data, formate para o padrão ISO "YYYY-MM-DD"
    const formattedCrimeDate = crimeDate ? new Date(crimeDate).toISOString().split('T')[0] : null;

    const dados = {
        crime_name: document.getElementById("crime_name").value,
        description: document.getElementById("description").value,
        crime_date: formattedCrimeDate, // Convertendo para o formato adequado
        res_hero: document.getElementById("res_hero").value,
        severity: document.getElementById("severity").value // Campo de severidade
        
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


document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.edit-button');
    
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const crimeId = this.getAttribute('data-id');
            // Fetch crime data using the crimeId
            fetch(`/crime/${crimeId}`)
                .then(response => response.json())
                .then(data => {
                    // Populate the form with the fetched data
                    document.getElementById('crime_name').value = data.crime_name;
                    document.getElementById('description').value = data.description;
                    document.getElementById('crime_date').value = data.crime_date;
                    document.getElementById('res_hero').value = data.res_hero;
                    document.getElementById('severity').value = data.severity;
                    
                    // Change form action to update the crime
                    document.getElementById('cadastroCrime').action = `/crime/update/${crimeId}`;
                })
                .catch(error => console.error('Error:', error));
        });
    });
});
document.addEventListener("DOMContentLoaded", async () => {
    const heroSelect = document.getElementById("res_hero");

    try {
        const response = await fetch("/heroes/heroes");  // Ajuste o caminho conforme necessário
        const heroes = await response.json();

        if (heroes.error) {
            console.error("Erro do servidor:", heroes.error);
            return;
        }

        heroes.forEach(hero => {
            const option = document.createElement("option");
            option.value = hero.hero_name;  // ID do herói
            option.textContent = hero.hero_name;  // Alterado para 'hero_name'

            heroSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Erro ao carregar os heróis:", error);
    }
});
