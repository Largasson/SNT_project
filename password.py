from werkzeug.security import generate_password_hash

# Ваш реальный пароль
real_password = "12345"

# Генерация хэша для пароля
hashed_password = generate_password_hash(real_password)
print(f"Хэш пароля: {hashed_password}")
