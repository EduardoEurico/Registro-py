document.getElementById("cadastroHeroi").addEventListener("submit", async (event) => {
    event.preventDefault();

    const dataNascimento = document.getElementById("data_nascimento").value;

    // Se houver um valor para a data, formate para o padrão ISO "YYYY-MM-DD"
    const formattedDate = dataNascimento ? new Date(dataNascimento).toISOString().split('T')[0] : null;

    const dados = {
        nome_real: document.getElementById("nome_real").value,
        nome_heroi: document.getElementById("nome_heroi").value,
        poderes: document.getElementById("poderes").value,
        nivel_forca: parseInt(document.getElementById("nivel_forca").value),
        genero: document.getElementById("genero").value, // Novo campo para o gênero
        altura: parseFloat(document.getElementById("altura").value), // Novo campo para altura
        peso: parseFloat(document.getElementById("peso").value), // Novo campo para peso
        data_nascimento: formattedDate, // Convertendo para o formato adequado
        local_nascimento: document.getElementById("local_nascimento").value, // Novo campo para local de nascimento
        popularidade: parseInt(document.getElementById("popularidade").value), // Novo campo para popularidade
        status: document.getElementById("status").value // Novo campo para status
    };

    console.log("Dados a serem enviados:", dados);

    try {
        const response = await fetch("/heroes/cadastrar", { // Certifique-se de usar a rota correta aqui
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        const result = await response.json();
        alert(result.message || result.error);
    } catch (error) {
        console.error("Erro ao cadastrar herói:", error);
    }
});
