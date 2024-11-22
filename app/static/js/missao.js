// Cadastro de Missão
document.getElementById("cadastroMissao").addEventListener("submit", async (event) => {
    event.preventDefault();

    const assignedHeroes = document.getElementById("assigned_heroes").selectedOptions;
    const difficulty = parseInt(document.getElementById("difficulty").value);
    const heroData = await fetch("/heroes/herois").then((res) => {
        if (!res.ok) {
            throw new Error(`Erro na resposta: ${res.statusText}`);
        }
        return res.json();
    })
    .catch((error) => {
        console.error("Erro ao carregar os heróis:", error);
        return null;
    });
    const incompatibleHeroes = [];

    // Verifica força dos heróis
    Array.from(assignedHeroes).forEach((heroOption) => {
        if (!heroData || heroData.length === 0) {
            console.error("Nenhum dado de herói disponível.");
            return null;
        }
        
        const hero = heroData.find((h) => h.id == heroOption.value);
        if (hero && Math.abs(hero.strength_level - difficulty) > 2) {
            incompatibleHeroes.push(hero.hero_name);
        }
    });

    if (incompatibleHeroes.length > 0) {
        alert(
            `Os seguintes heróis não podem ser designados devido à incompatibilidade de força: ${incompatibleHeroes.join(
                ", "
            )}`
        );
        return;
    }

    const dados = {
        mission_name: document.getElementById("mission_name").value,
        description: document.getElementById("description").value,
        des_heroes: Array.from(assignedHeroes).map((option) => option.value).join(","),
        difficulty: parseInt(document.getElementById("difficulty").value), // Garantir que dificuldade seja número
        reward: document.getElementById("reward").value,
        resultado: document.getElementById("result").value
    };

    console.log("Dados a serem enviados:", dados);

    try {
        const response = await fetch("/missoes/cadastrar", { // Certifique-se de usar a rota correta aqui
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        const result = await response.json();
        alert(result.message || result.error);
        window.location.reload(); // Recarrega a página

    } catch (error) {
        console.error("Erro ao cadastrar missão:", error);
        alert("Erro ao criar missão.");
    }
});

// Função para listar missões
document.addEventListener("DOMContentLoaded", async () => {
    const missionList = document.getElementById("missionList");

    if (!missionList) {
        console.error("Elemento 'missionList' não encontrado.");
        return;
    }

    try {
        const response = await fetch('/missoes'); // Certifique-se de que essa rota existe no backend
        const missions = await response.json();

        if (missions.length === 0) {
            console.log("Nenhuma missão cadastrada.");
            missionList.innerHTML = "<tr><td colspan='7'>Nenhuma missão encontrada.</td></tr>";
            return;
        }

        // Limpa a tabela antes de adicionar novas missões
        missionList.innerHTML = "";

        missions.forEach(mission => {
            const row = document.createElement('tr');
            row.id = `mission-${mission.id}`;
            row.innerHTML = `
                <td>${mission.mission_name}</td>
                <td>${mission.description}</td>
                <td>${mission.difficulty}</td>
                <td>${mission.des_heroes}</td>
                <td>${mission.resultado}</td>
                <td>${mission.reward}</td>
                <td>
                    <button class="mission-action-link delete-button" data-id="${mission.id}">Excluir</button>
                </td>
            `;
            missionList.appendChild(row);
        });

        console.log("Missões carregadas com sucesso:", missions);

    } catch (error) {
        console.error("Erro ao carregar as missões:", error);
    }
});


// Função para excluir uma missão
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('delete-button')) {
        const missionId = event.target.dataset.id; // Pega o ID da missão
        fetch(`/missoes/deletar/${missionId}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                // Remover a linha da tabela após a exclusão
                let missionRow = document.querySelector(`#mission-${missionId}`);
                if (missionRow) {
                    missionRow.remove(); // Remove a linha da tabela
                }

                alert(data.message); // Exibe a mensagem de sucesso
                window.location.reload(); // Recarrega a página após a exclusão
            } else {
                alert("Erro ao excluir a missão");
            }
        })
        .catch(error => {
            console.error('Erro ao excluir missão:', error);
            alert("Erro na comunicação com o servidor.");
        });
    }
});


document.addEventListener("DOMContentLoaded", async () => {
    const heroSelect = document.getElementById("assigned_heroes");

    if (!heroSelect) {
        console.error("Elemento com ID 'des_heroes' não encontrado.");
        return;
    }

    try {
        const response = await fetch('/heroes/herois');
        const heroes = await response.json();

        if (heroes.length === 0) {
            console.log("Nenhum herói encontrado.");
            return;
        }

        heroes.forEach(hero => {
            const option = document.createElement('option');
            option.value = hero.id;
            option.textContent = hero.hero_name;

            heroSelect.appendChild(option);
        });
        //log dos dados
        console.log("Dados dos heróis carregados:", heroes);
    } catch (error) {
        console.error('Erro ao carregar os heróis:', error);
    }
});
