from app.data.auth import register, authenticate

print("Registering user:")
print(register("atha", "dogtooth123"))

print("Trying to login:")
print(authenticate("atha", "dogtooth123"))

print("Wrong password test:")
print(authenticate("bernard", "wrongpass"))