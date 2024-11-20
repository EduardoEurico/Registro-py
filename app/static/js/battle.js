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
