from app import create_app

# Cria a aplicação com base na factory
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
