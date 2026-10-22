import mysql.connector
from conexao import conectar


def popular_produtos_iniciais():
    conexao = conectar()
    cursor = conexao.cursor()

    # Verifica se já existem produtos para não duplicar toda vez que abrir o sistema
    cursor.execute("SELECT COUNT(*) FROM produtos")
    total = cursor.fetchone()[0]

    if total == 0:
        produtos_para_cadastrar = [
            ("Maca Gala kg", 1.99, 150),
            ("Banana Nanica kg", 1.50, 200),
            ("Tomate Long Vida kg", 2.20, 80),
            ("Alface Crespa unidade", 0.80, 50),
            ("Batata Inglesa kg", 1.60, 300),
            ("Cebola Branca kg", 1.40, 120),
            ("Cenoura kg", 1.30, 90),
            ("Limao Taiti kg", 1.10, 110),
            ("Mamao Formosa kg", 1.80, 60),
            ("Melancia kg", 0.90, 40),
            ("Abacaxi Unidade", 1.50, 70),
            ("Uva Crimson kg", 2.90, 85),
            ("Morango Bandeja", 1.99, 45),
            ("Ovos Brancos Duzia", 2.50, 150),
            ("Pimentao Amarelo kg", 2.80, 75),
            ("Pepino Japones kg", 1.20, 65),
            ("Abobrinha Italiana kg", 1.10, 80),
            ("Repolho Verde kg", 0.95, 55),
            ("Arroz Branco Tipo 1 5kg", 5.90, 250),
            ("Feijao Carioca 1kg", 1.90, 180),
            ("Acucar Cristal 5kg", 4.20, 140),
            ("Cafe em Po Torrado 500g", 3.80, 220),
            ("Oleo de Soja 900ml", 1.70, 300),
            ("Macarrao Espaguete 500g", 1.00, 190),
            ("Farinha de Trigo 1kg", 1.20, 130),
            ("Sal Refinado 1kg", 0.70, 100),
            ("Molho de Tomate Sache 340g", 0.65, 160),
            ("Atum em Lata 170g", 1.50, 95),
            ("Sardinha em Lata 125g", 0.95, 85),
            ("Farinha de Mandioca 500g", 1.10, 70),
            ("Milho Verde Lata 200g", 0.80, 110),
            ("Ervilha em Lata 200g", 0.80, 105),
            ("Azeite de Oliva Extra Virgem 500ml", 6.90, 90),
            ("Vinagre de Almoco 500ml", 0.75, 60),
            ("Maionese 500g", 1.80, 120),
            ("Ketchup 400g", 1.90, 110),
            ("Mostarda 400g", 1.70, 95),
            ("Leite Integral UHT 1L", 0.95, 400),
            ("Manteiga com Sal 200g", 2.50, 130),
            ("Queijo Mussarela Fatiado kg", 8.90, 70),
            ("Presunto Cozido Fatiado kg", 7.90, 65),
            ("Iogurte Natural 170g", 0.85, 150),
            ("Requeijao Cremoso 200g", 1.90, 85),
            ("Leite Condensado 395g", 1.50, 175),
            ("Creme de Leite 200g", 0.95, 160),
            ("Queijo Prato Fatiado kg", 9.50, 50),
            ("Queijo Minas Frescal kg", 8.20, 45),
            ("Mortadela Fatiada kg", 4.90, 80),
            ("Carne Bovina Alcatra kg", 10.90, 90),
            ("Carne Bovina Acem kg", 6.50, 110),
            ("Peito de Frango Desossado kg", 4.90, 200),
            ("Linguica Toscana para Churrasco kg", 5.50, 130),
            ("Carne Bovina Patinho kg", 9.20, 95),
            ("Costela Bovina kg", 6.00, 85),
            ("Coxa e Sobrecoxa de Frango kg", 3.20, 180),
            ("Carne Moida Bovina kg", 7.50, 140),
            ("Bisteca Suina kg", 4.50, 100),
            ("Camarao Limpo kg", 14.50, 30),
            ("File de Tilapia kg", 7.90, 75),
            ("Refrigerante Cola 2 Litros", 2.10, 250),
            ("Agua Mineral sem Gas 500ml", 0.50, 500),
            ("Suco de Laranja 1L", 1.80, 120),
            ("Cerveja Pilsen Lata 350ml", 0.95, 350),
            ("Refrigerante Guaraná 2 Litros", 2.00, 240),
            ("Agua com Gas 500ml", 0.60, 200),
            ("Energetico 250ml", 1.90, 150),
            ("Cha Gelado 1.5L", 1.60, 90),
            ("Agua de Coco 1L", 1.80, 110),
            ("Vinho Tinto Seco 750ml", 7.90, 70),
            ("Sabao em Po 1kg", 2.70, 130),
            ("Amaciante de Roupas 2L", 3.20, 95),
            ("Detergente Liquido 500ml", 0.55, 300),
            ("Desinfetante 500ml", 1.10, 140),
            ("Papel Higienico Folha Dupla 16un", 5.90, 160),
            ("Sabonete em Barra 90g", 0.60, 220),
            ("Creme Dental 90g", 0.95, 190),
            ("Shampoo 400ml", 3.50, 110),
            ("Condicionador 400ml", 3.80, 105),
            ("Esponja de Laco 4un", 1.00, 130),
            ("Lava Roupas Liquido 3L", 6.90, 60),
            ("Multiuso Limpador 500ml", 1.40, 115),
            ("Alvejante Sem Cloro 1L", 2.20, 85),
            ("Limpador de Piso 1L", 1.70, 90),
            ("Guanapo de Papel 50un", 0.70, 100),
            ("Sacos de Lixo 50L 30un", 2.90, 120),
            ("Fosforo Caixa", 0.35, 250),
            ("Vela de Aniversario Pacote", 0.90, 80),
            ("Biscoito Recheado 140g", 0.80, 210),
            ("Biscoito Maisena 400g", 1.40, 160),
            ("Chocolate Barra 90g", 1.50, 180),
            ("Pao de Forma Tradicional 500g", 1.90, 95),
            ("Bolacha Agua e Sal 400g", 1.50, 140),
            ("Pipoca de Microondas", 0.75, 170),
            ("Aveia em Flocos 200g", 1.00, 110),
            ("Granola Tradicional 500g", 2.50, 85),
            ("Gelatina em Po", 0.45, 200),
            ("Pudim em Po", 0.80, 150),
            ("Farinha de Rosca 500g", 0.90, 95),
            ("Fubá Mimoso 1kg", 1.00, 110),
            ("Acucar Refinado 1kg", 1.10, 100)
        ]

        sql_produto = "INSERT INTO produtos (nome, preco) VALUES (%s, %s)"
        sql_mov = "INSERT INTO movimentacoes (produto_id, tipo, quantidade) VALUES (%s, 'ENTRADA', %s)"

        for nome, preco, quantidade in produtos_para_cadastrar:
            cursor.execute(sql_produto, (nome, preco))
            produto_id = cursor.lastrowid
            cursor.execute(sql_mov, (produto_id, quantidade))

        conexao.commit()
        print(f"Sucesso! {len(produtos_para_cadastrar)} produtos foram cadastrados com os stocks definidos.")

    cursor.close()
    conexao.close()