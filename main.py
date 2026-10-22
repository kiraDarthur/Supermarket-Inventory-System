from conexao import conectar
from gerar_produtos import popular_produtos_iniciais
from interface import iniciar_sistema


def main():
    print("--- A iniciar o Sistema de Supermercado ---")


    popular_produtos_iniciais()


    iniciar_sistema()


if __name__ == "__main__":
    main()