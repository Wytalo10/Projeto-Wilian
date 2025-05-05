import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class HotelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reserva de Hotel")
        self.root.geometry("900x600")
        
        # Dados em memória
        self.clientes = []
        self.quartos = self.inicializar_quartos()
        self.reservas = []
        
        # Criar abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill="both")
        
        # Abas do sistema
        self.criar_aba_clientes()
        self.criar_aba_quartos()
        self.criar_aba_reservas()
        self.criar_aba_relatorios()
    
    def inicializar_quartos(self):
        return [
            {"numero": 101, "tipo": "Standard", "capacidade": 2, "preco": 150.00, "disponivel": True},
            {"numero": 102, "tipo": "Standard", "capacidade": 2, "preco": 150.00, "disponivel": True},
            {"numero": 201, "tipo": "Luxo", "capacidade": 2, "preco": 250.00, "disponivel": True},
            {"numero": 202, "tipo": "Luxo", "capacidade": 2, "preco": 250.00, "disponivel": True},
            {"numero": 301, "tipo": "Família", "capacidade": 4, "preco": 350.00, "disponivel": True},
            {"numero": 401, "tipo": "Suíte", "capacidade": 2, "preco": 450.00, "disponivel": True}
        ]
    
    def criar_aba_clientes(self):
        # Frame principal
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Clientes")
        
        # Frame de cadastro
        cadastro_frame = ttk.LabelFrame(frame, text="Cadastrar Cliente")
        cadastro_frame.pack(pady=10, padx=10, fill="x")
        
        # Campos do formulário
        ttk.Label(cadastro_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.nome_entry = ttk.Entry(cadastro_frame, width=30)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(cadastro_frame, text="CPF:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.cpf_entry = ttk.Entry(cadastro_frame, width=30)
        self.cpf_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(cadastro_frame, text="Telefone:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.telefone_entry = ttk.Entry(cadastro_frame, width=30)
        self.telefone_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(cadastro_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.email_entry = ttk.Entry(cadastro_frame, width=30)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Botão de cadastro
        ttk.Button(cadastro_frame, text="Cadastrar", command=self.cadastrar_cliente).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Lista de clientes
        lista_frame = ttk.LabelFrame(frame, text="Clientes Cadastrados")
        lista_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Treeview para exibir clientes
        self.clientes_tree = ttk.Treeview(lista_frame, columns=("Nome", "CPF", "Telefone", "Email"), show="headings")
        self.clientes_tree.heading("Nome", text="Nome")
        self.clientes_tree.heading("CPF", text="CPF")
        self.clientes_tree.heading("Telefone", text="Telefone")
        self.clientes_tree.heading("Email", text="Email")
        self.clientes_tree.pack(fill="both", expand=True)
        
        # Atualizar lista
        self.atualizar_lista_clientes()
    
    def criar_aba_quartos(self):
        # Frame principal
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Quartos")
        
        # Lista de quartos
        lista_frame = ttk.LabelFrame(frame, text="Quartos Disponíveis")
        lista_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Treeview para exibir quartos
        self.quartos_tree = ttk.Treeview(lista_frame, columns=("Número", "Tipo", "Capacidade", "Preço", "Disponível"), show="headings")
        self.quartos_tree.heading("Número", text="Número")
        self.quartos_tree.heading("Tipo", text="Tipo")
        self.quartos_tree.heading("Capacidade", text="Capacidade")
        self.quartos_tree.heading("Preço", text="Preço (R$)")
        self.quartos_tree.heading("Disponível", text="Disponível")
        self.quartos_tree.pack(fill="both", expand=True)
        
        # Atualizar lista
        self.atualizar_lista_quartos()
    
    def criar_aba_reservas(self):
        # Frame principal
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Reservas")
        
        # Frame de cadastro
        cadastro_frame = ttk.LabelFrame(frame, text="Nova Reserva")
        cadastro_frame.pack(pady=10, padx=10, fill="x")
        
        # Cliente
        ttk.Label(cadastro_frame, text="Cliente (CPF):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.reserva_cpf_entry = ttk.Entry(cadastro_frame, width=30)
        self.reserva_cpf_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Quarto
        ttk.Label(cadastro_frame, text="Quarto:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.quarto_combobox = ttk.Combobox(cadastro_frame, width=27)
        self.quarto_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.atualizar_combo_quartos()
        
        # Datas
        ttk.Label(cadastro_frame, text="Check-in (dd/mm/aaaa):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.checkin_entry = ttk.Entry(cadastro_frame, width=30)
        self.checkin_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(cadastro_frame, text="Check-out (dd/mm/aaaa):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.checkout_entry = ttk.Entry(cadastro_frame, width=30)
        self.checkout_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Botões
        ttk.Button(cadastro_frame, text="Fazer Reserva", command=self.fazer_reserva).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Lista de reservas
        lista_frame = ttk.LabelFrame(frame, text="Reservas Existentes")
        lista_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Treeview para exibir reservas
        self.reservas_tree = ttk.Treeview(lista_frame, columns=("ID", "Cliente", "Quarto", "Check-in", "Check-out", "Valor", "Status"), show="headings")
        self.reservas_tree.heading("ID", text="ID")
        self.reservas_tree.heading("Cliente", text="Cliente")
        self.reservas_tree.heading("Quarto", text="Quarto")
        self.reservas_tree.heading("Check-in", text="Check-in")
        self.reservas_tree.heading("Check-out", text="Check-out")
        self.reservas_tree.heading("Valor", text="Valor (R$)")
        self.reservas_tree.heading("Status", text="Status")
        self.reservas_tree.pack(fill="both", expand=True)
        
        # Botão de cancelamento
        ttk.Button(lista_frame, text="Cancelar Reserva Selecionada", command=self.cancelar_reserva).pack(pady=5)
        
        # Atualizar lista
        self.atualizar_lista_reservas()
    
    def criar_aba_relatorios(self):
        # Frame principal
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Relatórios")
        
        # Relatório de ocupação
        relatorio_frame = ttk.LabelFrame(frame, text="Ocupação do Hotel")
        relatorio_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Texto com estatísticas
        self.relatorio_text = tk.Text(relatorio_frame, height=10, wrap="word")
        self.relatorio_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Botão para atualizar relatório
        ttk.Button(relatorio_frame, text="Atualizar Relatório", command=self.gerar_relatorio).pack(pady=5)
        
        # Atualizar relatório inicial
        self.gerar_relatorio()
    
    def cadastrar_cliente(self):
        nome = self.nome_entry.get()
        cpf = self.cpf_entry.get()
        telefone = self.telefone_entry.get()
        email = self.email_entry.get()
        
        if not nome or not cpf:
            messagebox.showerror("Erro", "Nome e CPF são obrigatórios!")
            return
        
        # Verificar se CPF já existe
        for cliente in self.clientes:
            if cliente["cpf"] == cpf:
                messagebox.showerror("Erro", "CPF já cadastrado!")
                return
        
        # Adicionar cliente
        self.clientes.append({
            "nome": nome,
            "cpf": cpf,
            "telefone": telefone,
            "email": email
        })
        
        # Limpar campos
        self.nome_entry.delete(0, tk.END)
        self.cpf_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        self.atualizar_lista_clientes()
    
    def fazer_reserva(self):
        cpf = self.reserva_cpf_entry.get()
        quarto_num = int(self.quarto_combobox.get().split(" - ")[0])
        checkin_str = self.checkin_entry.get()
        checkout_str = self.checkout_entry.get()
        
        # Validar cliente
        cliente = next((c for c in self.clientes if c["cpf"] == cpf), None)
        if not cliente:
            messagebox.showerror("Erro", "Cliente não encontrado!")
            return
        
        # Validar quarto
        quarto = next((q for q in self.quartos if q["numero"] == quarto_num and q["disponivel"]), None)
        if not quarto:
            messagebox.showerror("Erro", "Quarto não disponível!")
            return
        
        # Validar datas
        try:
            checkin = datetime.strptime(checkin_str, "%d/%m/%Y")
            checkout = datetime.strptime(checkout_str, "%d/%m/%Y")
            
            if checkout <= checkin:
                messagebox.showerror("Erro", "Data de check-out deve ser após check-in!")
                return
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use dd/mm/aaaa.")
            return
        
        # Calcular valor
        dias = (checkout - checkin).days
        valor_total = quarto["preco"] * dias
        
        # Criar reserva
        reserva_id = len(self.reservas) + 1
        self.reservas.append({
            "id": reserva_id,
            "cliente": cliente,
            "quarto": quarto,
            "checkin": checkin,
            "checkout": checkout,
            "valor": valor_total,
            "status": "confirmada"
        })
        
        # Atualizar disponibilidade do quarto
        quarto["disponivel"] = False
        
        # Limpar campos
        self.reserva_cpf_entry.delete(0, tk.END)
        self.checkin_entry.delete(0, tk.END)
        self.checkout_entry.delete(0, tk.END)
        self.atualizar_combo_quartos()
        
        messagebox.showinfo("Sucesso", f"Reserva realizada com sucesso!\nID: {reserva_id}\nValor Total: R${valor_total:.2f}")
        self.atualizar_lista_reservas()
        self.atualizar_lista_quartos()
    
    def cancelar_reserva(self):
        selecionado = self.reservas_tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhuma reserva selecionada!")
            return
        
        item = self.reservas_tree.item(selecionado[0])
        reserva_id = int(item["values"][0])
        
        reserva = next((r for r in self.reservas if r["id"] == reserva_id and r["status"] == "confirmada"), None)
        if not reserva:
            messagebox.showerror("Erro", "Reserva não encontrada ou já cancelada!")
            return
        
        # Confirmar cancelamento
        if not messagebox.askyesno("Confirmar", f"Cancelar reserva ID {reserva_id}?"):
            return
        
        # Atualizar status
        reserva["status"] = "cancelada"
        
        # Liberar quarto
        quarto = next(q for q in self.quartos if q["numero"] == reserva["quarto"]["numero"])
        quarto["disponivel"] = True
        
        messagebox.showinfo("Sucesso", "Reserva cancelada com sucesso!")
        self.atualizar_lista_reservas()
        self.atualizar_lista_quartos()
        self.atualizar_combo_quartos()
    
    def gerar_relatorio(self):
        total_quartos = len(self.quartos)
        quartos_ocupados = sum(1 for q in self.quartos if not q["disponivel"])
        ocupacao_percent = (quartos_ocupados / total_quartos) * 100 if total_quartos > 0 else 0
        
        total_reservas = len(self.reservas)
        reservas_ativas = sum(1 for r in self.reservas if r["status"] == "confirmada")
        
        faturamento_total = sum(r["valor"] for r in self.reservas if r["status"] == "confirmada")
        
        relatorio = f"""=== RELATÓRIO DE OCUPAÇÃO ===
        
Quartos totais: {total_quartos}
Quartos ocupados: {quartos_ocupados}
Taxa de ocupação: {ocupacao_percent:.1f}%

Reservas totais: {total_reservas}
Reservas ativas: {reservas_ativas}

Faturamento total: R$ {faturamento_total:.2f}
"""
        self.relatorio_text.delete(1.0, tk.END)
        self.relatorio_text.insert(tk.END, relatorio)
    
    def atualizar_lista_clientes(self):
        self.clientes_tree.delete(*self.clientes_tree.get_children())
        for cliente in self.clientes:
            self.clientes_tree.insert("", tk.END, values=(
                cliente["nome"],
                cliente["cpf"],
                cliente["telefone"],
                cliente["email"]
            ))
    
    def atualizar_lista_quartos(self):
        self.quartos_tree.delete(*self.quartos_tree.get_children())
        for quarto in self.quartos:
            disponivel = "Sim" if quarto["disponivel"] else "Não"
            self.quartos_tree.insert("", tk.END, values=(
                quarto["numero"],
                quarto["tipo"],
                quarto["capacidade"],
                f"{quarto['preco']:.2f}",
                disponivel
            ))
    
    def atualizar_combo_quartos(self):
        quartos_disponiveis = [f"{q['numero']} - {q['tipo']} (R${q['preco']:.2f}/noite)" 
                              for q in self.quartos if q["disponivel"]]
        self.quarto_combobox["values"] = quartos_disponiveis
        if quartos_disponiveis:
            self.quarto_combobox.current(0)
    
    def atualizar_lista_reservas(self):
        self.reservas_tree.delete(*self.reservas_tree.get_children())
        for reserva in self.reservas:
            self.reservas_tree.insert("", tk.END, values=(
                reserva["id"],
                reserva["cliente"]["nome"],
                f"Quarto {reserva['quarto']['numero']}",
                reserva["checkin"].strftime("%d/%m/%Y"),
                reserva["checkout"].strftime("%d/%m/%Y"),
                f"{reserva['valor']:.2f}",
                reserva["status"].capitalize()
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()