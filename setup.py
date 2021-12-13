from cx_Freeze import setup, Executable

setup(
    name = "SteganoText",
    version = "0.3 beta",
    description = "Шифровка текста стеганографическим методом. Автор: @artmih24",
    executables = [Executable("SteganoText.py")]
)