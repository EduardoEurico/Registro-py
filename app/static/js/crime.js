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
    } catch (error) {
        console.error("Erro ao cadastrar crime:", error);
    }
});
