class Hotel:
    def __init__(self):
        self.clientes = []
        self.quartos = []
        self.reservas = []
        self.inicializar_quartos()

    def inicializar_quartos(self):
        """Inicializa alguns quartos padrão no sistema"""
        tipos_quartos = [
            {"tipo": "Standard", "capacidade": 2, "preco_diaria": 150.00},
            {"tipo": "Luxo", "capacidade": 2, "preco_diaria": 250.00},
            {"tipo": "Família", "capacidade": 4, "preco_diaria": 350.00},
            {"tipo": "Suíte", "capacidade": 2, "preco_diaria": 450.00}
        ]
        
        for i, tipo in enumerate(tipos_quartos, start=1):
            self.quartos.append({
                "numero": i * 100,  # 100, 200, 300, 400
                "tipo": tipo["tipo"],
                "capacidade": tipo["capacidade"],
                "preco_diaria": tipo["preco_diaria"],
                "disponivel": True
            })

    def cadastrar_cliente(self, nome, cpf, telefone=None, email=None):
        """Cadastra um novo cliente no sistema"""
        for cliente in self.clientes:
            if cliente["cpf"] == cpf:
                print("Cliente já cadastrado com este CPF.")
                return False
        
        novo_cliente = {
            "nome": nome,
            "cpf": cpf,
            "telefone": telefone,
            "email": email
        }
        self.clientes.append(novo_cliente)
        print("Cliente cadastrado com sucesso!")
        return True

    def listar_quartos_disponiveis(self):
        """Lista todos os quartos disponíveis"""
        disponiveis = [q for q in self.quartos if q["disponivel"]]
        
        if not disponiveis:
            print("Nenhum quarto disponível no momento.")
            return
        
        print("\nQuartos Disponíveis:")
        for quarto in disponiveis:
            print(f"Número: {quarto['numero']} - Tipo: {quarto['tipo']}")
            print(f"Capacidade: {quarto['capacidade']} - Diária: R${quarto['preco_diaria']:.2f}")
            print("-" * 30)

    def fazer_reserva(self, cpf_cliente, numero_quarto, data_checkin, data_checkout):
        """Realiza uma nova reserva"""
        # Verifica se o cliente existe
        cliente = next((c for c in self.clientes if c["cpf"] == cpf_cliente), None)
        if not cliente:
            print("Cliente não encontrado. Cadastre o cliente primeiro.")
            return False
        
        # Verifica se o quarto existe e está disponível
        quarto = next((q for q in self.quartos if q["numero"] == numero_quarto and q["disponivel"]), None)
        if not quarto:
            print("Quarto não disponível ou não encontrado.")
            return False
        
        # Calcula o valor total da reserva
        dias = (data_checkout - data_checkin).days
        if dias <= 0:
            print("Data de checkout deve ser posterior à data de checkin.")
            return False
            
        valor_total = quarto["preco_diaria"] * dias
        
        # Cria a reserva
        nova_reserva = {
            "id": len(self.reservas) + 1,
            "cliente": cliente,
            "quarto": quarto,
            "data_checkin": data_checkin,
            "data_checkout": data_checkout,
            "valor_total": valor_total,
            "status": "confirmada"
        }
        self.reservas.append(nova_reserva)
        
        # Marca o quarto como indisponível
        quarto["disponivel"] = False
        
        print("\nReserva realizada com sucesso!")
        print(f"Número da reserva: {nova_reserva['id']}")
        print(f"Valor total: R${valor_total:.2f}")
        return True

    def cancelar_reserva(self, reserva_id):
        """Cancela uma reserva existente"""
        reserva = next((r for r in self.reservas if r["id"] == reserva_id and r["status"] == "confirmada"), None)
        if not reserva:
            print("Reserva não encontrada ou já cancelada.")
            return False
        
        reserva["status"] = "cancelada"
        # Libera o quarto para novas reservas
        quarto = next(q for q in self.quartos if q["numero"] == reserva["quarto"]["numero"])
        quarto["disponivel"] = True
        
        print("Reserva cancelada com sucesso!")
        return True

    def listar_reservas(self):
        """Lista todas as reservas do sistema"""
        if not self.reservas:
            print("Nenhuma reserva cadastrada.")
            return
        
        print("\nLista de Reservas:")
        for reserva in self.reservas:
            print(f"ID: {reserva['id']} - Status: {reserva['status']}")
            print(f"Cliente: {reserva['cliente']['nome']} (CPF: {reserva['cliente']['cpf']})")
            print(f"Quarto: {reserva['quarto']['numero']} ({reserva['quarto']['tipo']})")
            print(f"Check-in: {reserva['data_checkin'].strftime('%d/%m/%Y')}")
            print(f"Check-out: {reserva['data_checkout'].strftime('%d/%m/%Y')}")
            print(f"Valor total: R${reserva['valor_total']:.2f}")
            print("-" * 50)

def main():
    hotel = Hotel()
    
    while True:
        print("\nSistema de Reserva de Hotel")
        print("1. Cadastrar Cliente")
        print("2. Listar Quartos Disponíveis")
        print("3. Fazer Reserva")
        print("4. Cancelar Reserva")
        print("5. Listar Reservas")
        print("6. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            print("\nCadastro de Cliente")
            nome = input("Nome completo: ")
            cpf = input("CPF: ")
            telefone = input("Telefone (opcional): ")
            email = input("Email (opcional): ")
            hotel.cadastrar_cliente(nome, cpf, telefone, email)
            
        elif opcao == "2":
            hotel.listar_quartos_disponiveis()
            
        elif opcao == "3":
            print("\nNova Reserva")
            cpf = input("CPF do cliente: ")
            hotel.listar_quartos_disponiveis()
            numero_quarto = int(input("Número do quarto desejado: "))
            
            try:
                checkin = input("Data de check-in (dd/mm/aaaa): ")
                dia, mes, ano = map(int, checkin.split('/'))
                data_checkin = datetime(ano, mes, dia)
                
                checkout = input("Data de check-out (dd/mm/aaaa): ")
                dia, mes, ano = map(int, checkout.split('/'))
                data_checkout = datetime(ano, mes, dia)
                
                hotel.fazer_reserva(cpf, numero_quarto, data_checkin, data_checkout)
            except ValueError:
                print("Formato de data inválido. Use dd/mm/aaaa.")
                
        elif opcao == "4":
            print("\nCancelar Reserva")
            hotel.listar_reservas()
            reserva_id = int(input("ID da reserva a cancelar: "))
            hotel.cancelar_reserva(reserva_id)
            
        elif opcao == "5":
            hotel.listar_reservas()
            
        elif opcao == "6":
            print("Saindo do sistema...")
            break
            
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    from datetime import datetime
    main()