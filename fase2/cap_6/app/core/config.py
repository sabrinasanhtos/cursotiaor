import os

class Settings:
    ORACLE_USER = os.getenv("ORACLE_USER", "usuario")
    ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "senha")
    ORACLE_DSN = os.getenv("ORACLE_DSN", "host:porta/servico")

settings = Settings()
