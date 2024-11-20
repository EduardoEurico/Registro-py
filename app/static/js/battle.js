// static/js/battle.js
document.getElementById("cadastroBatalha").addEventListener("submit", function(event) {
    event.preventDefault();

    const hero1_id = document.getElementById("hero1_id").value;
    const hero2_id = document.getElementById("hero2_id").value;
    const battle_date = document.getElementById("battle_date").value;

    fetch('/battles/criar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            hero1_id: hero1_id,
            hero2_id: hero2_id,
            battle_date: battle_date
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Erro: " + data.error);
        } else {
            alert("Batalha cadastrada com sucesso!");
            location.reload();  // Recarrega a página para atualizar a lista
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert("Erro ao cadastrar batalha.");
    });
});

const hero1Select = document.getElementById("hero1_id");
const hero2Select = document.getElementById("hero2_id");

hero1Select.addEventListener("change", function() {
    updateHeroOptions();
});

hero2Select.addEventListener("change", function() {
    updateHeroOptions();
});

function updateHeroOptions() {
    const hero1Id = hero1Select.value;
    const hero2Id = hero2Select.value;

    [...hero1Select.options].forEach(option => {
        if (option.value && option.value === hero2Id) {
            option.disabled = true;
        } else {
            option.disabled = false;
        }
    });

    [...hero2Select.options].forEach(option => {
        if (option.value && option.value === hero1Id) {
            option.disabled = true;
        } else {
            option.disabled = false;
        }
    });
}
