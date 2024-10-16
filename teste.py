from werkzeug.security import generate_password_hash, check_password_hash

# Etapa 1: Registrar o usuário
original_password = "Fortrek.1"
hashed_password = generate_password_hash(original_password)
print("Hash gerado:", hashed_password)  # Armazene este hash no banco de dados

# Etapa 2: Verificar a senha
stored_hash = hashed_password  # Simulando que você obteve isso do banco de dados
provided_password = "Fortrek.1"  # A senha que você está tentando verificar

# Verifique se a senha corresponde ao hash
is_valid = check_password_hash(stored_hash, provided_password)
print("Senha é válida?", is_valid)
