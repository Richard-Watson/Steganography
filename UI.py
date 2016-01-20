from steg import steg


# здесь будет парсер

containerName = "google.png"
hideName = "toCrypt"

if not steg(containerName, hideName):
    print("Контейнер мал")
