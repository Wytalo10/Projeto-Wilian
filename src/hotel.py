import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from supabase import create_client, Client
import os

class HotelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reserva de Hotel")
        self.root.geometry("900x600")
        
        # Configuração do Supabase
        self.supabase_url = "https://dwgfiurnepjllhinztza.supabase.co"
        self.supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3Z2ZpdXJuZXBqbGxoaW56dHphIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NzA4OTQwMCwiZXhwIjoyMDYyNjY1NDAwfQ.kVanzt1ehDYrebKoV-uBhgQkF-sTQlAN2_N8hxrkFCY"
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        
        # Criar abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill="both")
        
        # Abas do sistema
        self.criar_aba_clientes()
        self.criar_aba_quartos()
        self.criar_aba_reservas()
        self.criar_aba_relatorios()
        
        # Carregar dados iniciais
        self.carregar_dados_iniciais()
    
    def carregar_dados_iniciais(self):
        """Carrega dados iniciais do Supabase ou cria estrutura se não existir"""
        try:
            # Verificar se tabela de quartos existe e tem dados
            response = self.supabase.table("quartos").select("*").execute()
            if not response.data:
                self.inicializar_quartos_supabase()
            
            # Carregar clientes e reservas
            self.atualizar_lista_clientes()
            self.atualizar_lista_quartos()
            self.atualizar_lista_reservas()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar com o banco de dados: {str(e)}")
    
    def inicializar_quartos_supabase(self):
        """Inicializa os quartos no Supabase"""
        quartos = [
            {"numero": 101, "tipo": "Standard", "capacidade": 2, "preco": 150.00, "disponivel": True},
            {"numero": 102, "tipo": "Standard", "capacidade": 2, "preco": 150.00, "disponivel": True},
            {"numero": 201, "tipo": "Luxo", "capacidade": 2, "preco": 250.00, "disponivel": True},
            {"numero": 202, "tipo": "Luxo", "capacidade": 2, "preco": 250.00, "disponivel": True},
            {"numero": 301, "tipo": "Família", "capacidade": 4, "preco": 350.00, "disponivel": True},
            {"numero": 401, "tipo": "Suíte", "capacidade": 2, "preco": 450.00, "disponivel": True}
        ]
        
        for quarto in quartos:
            self.supabase.table("quartos").insert(quarto).execute()
    
    def criar_aba_clientes(self):
        """Cria a aba de gerenciamento de clientes"""
        clientes_frame = ttk.Frame(self.notebook)
        self.notebook.add(clientes_frame, text="Clientes")
        
        # Frame de cadastro
        cadastro_frame = ttk.LabelFrame(clientes_frame, text="Cadastro de Cliente")
        cadastro_frame.pack(fill="x", padx=10, pady=10)
        
        # Campos de entrada
        ttk.Label(cadastro_frame, text="Nome:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.nome_entry = ttk.Entry(cadastro_frame, width=40)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(cadastro_frame, text="CPF:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.cpf_entry = ttk.Entry(cadastro_frame, width=20)
        self.cpf_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(cadastro_frame, text="Telefone:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.telefone_entry = ttk.Entry(cadastro_frame, width=20)
        self.telefone_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(cadastro_frame, text="Email:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = ttk.Entry(cadastro_frame, width=40)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Botão de cadastro
        cadastrar_btn = ttk.Button(cadastro_frame, text="Cadastrar Cliente", command=self.cadastrar_cliente)
        cadastrar_btn.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Frame de lista de clientes
        lista_frame = ttk.LabelFrame(clientes_frame, text="Clientes Cadastrados")
        lista_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Árvore de clientes
        self.clientes_tree = ttk.Treeview(lista_frame, columns=("nome", "cpf", "telefone", "email"), show="headings")
        self.clientes_tree.heading("nome", text="Nome")
        self.clientes_tree.heading("cpf", text="CPF")
        self.clientes_tree.heading("telefone", text="Telefone")
        self.clientes_tree.heading("email", text="Email")
        
        self.clientes_tree.column("nome", width=200)
        self.clientes_tree.column("cpf", width=120)
        self.clientes_tree.column("telefone", width=120)
        self.clientes_tree.column("email", width=200)
        
        self.clientes_tree.pack(fill="both", expand=True)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.clientes_tree.yview)
        self.clientes_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill="y")
    
    def criar_aba_quartos(self):
        """Cria a aba de gerenciamento de quartos"""
        quartos_frame = ttk.Frame(self.notebook)
        self.notebook.add(quartos_frame, text="Quartos")
        
        # Lista de quartos
        lista_frame = ttk.LabelFrame(quartos_frame, text="Quartos do Hotel")
        lista_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Árvore de quartos
        self.quartos_tree = ttk.Treeview(lista_frame, 
                                        columns=("numero", "tipo", "capacidade", "preco", "disponivel"), 
                                        show="headings")
        self.quartos_tree.heading("numero", text="Número")
        self.quartos_tree.heading("tipo", text="Tipo")
        self.quartos_tree.heading("capacidade", text="Capacidade")
        self.quartos_tree.heading("preco", text="Preço (R$)")
        self.quartos_tree.heading("disponivel", text="Disponível")
        
        self.quartos_tree.column("numero", width=80)
        self.quartos_tree.column("tipo", width=150)
        self.quartos_tree.column("capacidade", width=100)
        self.quartos_tree.column("preco", width=100)
        self.quartos_tree.column("disponivel", width=100)
        
        self.quartos_tree.pack(fill="both", expand=True)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.quartos_tree.yview)
        self.quartos_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill="y")
    
    def criar_aba_reservas(self):
        """Cria a aba de gerenciamento de reservas"""
        reservas_frame = ttk.Frame(self.notebook)
        self.notebook.add(reservas_frame, text="Reservas")
        
        # Frame de nova reserva
        nova_frame = ttk.LabelFrame(reservas_frame, text="Nova Reserva")
        nova_frame.pack(fill="x", padx=10, pady=10)
        
        # Campos de reserva
        ttk.Label(nova_frame, text="CPF do Cliente:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.reserva_cpf_entry = ttk.Entry(nova_frame, width=20)
        self.reserva_cpf_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(nova_frame, text="Quarto:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.quarto_combobox = ttk.Combobox(nova_frame, width=30)
        self.quarto_combobox.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(nova_frame, text="Check-in (dd/mm/aaaa):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.checkin_entry = ttk.Entry(nova_frame, width=15)
        self.checkin_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(nova_frame, text="Check-out (dd/mm/aaaa):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.checkout_entry = ttk.Entry(nova_frame, width=15)
        self.checkout_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Botões de reserva
        botoes_frame = ttk.Frame(nova_frame)
        botoes_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        reservar_btn = ttk.Button(botoes_frame, text="Fazer Reserva", command=self.fazer_reserva)
        reservar_btn.pack(side=tk.LEFT, padx=5)
        
        cancelar_btn = ttk.Button(botoes_frame, text="Cancelar Reserva", command=self.cancelar_reserva)
        cancelar_btn.pack(side=tk.LEFT, padx=5)
        
        # Lista de reservas
        lista_frame = ttk.LabelFrame(reservas_frame, text="Reservas Realizadas")
        lista_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Árvore de reservas
        self.reservas_tree = ttk.Treeview(lista_frame, 
                                         columns=("id", "cliente", "quarto", "checkin", "checkout", "valor", "status"), 
                                         show="headings")
        self.reservas_tree.heading("id", text="ID")
        self.reservas_tree.heading("cliente", text="Cliente")
        self.reservas_tree.heading("quarto", text="Quarto")
        self.reservas_tree.heading("checkin", text="Check-in")
        self.reservas_tree.heading("checkout", text="Check-out")
        self.reservas_tree.heading("valor", text="Valor (R$)")
        self.reservas_tree.heading("status", text="Status")
        
        self.reservas_tree.column("id", width=60)
        self.reservas_tree.column("cliente", width=150)
        self.reservas_tree.column("quarto", width=80)
        self.reservas_tree.column("checkin", width=100)
        self.reservas_tree.column("checkout", width=100)
        self.reservas_tree.column("valor", width=100)
        self.reservas_tree.column("status", width=100)
        
        self.reservas_tree.pack(fill="both", expand=True)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.reservas_tree.yview)
        self.reservas_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill="y")
    
    def criar_aba_relatorios(self):
        """Cria a aba de relatórios"""
        relatorios_frame = ttk.Frame(self.notebook)
        self.notebook.add(relatorios_frame, text="Relatórios")
        
        # Botão para gerar relatório
        gerar_btn = ttk.Button(relatorios_frame, text="Gerar Relatório de Ocupação", command=self.gerar_relatorio)
        gerar_btn.pack(pady=10)
        
        # Área de texto para relatório
        self.relatorio_text = tk.Text(relatorios_frame, width=80, height=20)
        self.relatorio_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def cadastrar_cliente(self):
        nome = self.nome_entry.get()
        cpf = self.cpf_entry.get()
        telefone = self.telefone_entry.get()
        email = self.email_entry.get()
        
        if not nome or not cpf:
            messagebox.showerror("Erro", "Nome e CPF são obrigatórios!")
            return
        
        try:
            # Verificar se CPF já existe
            response = self.supabase.table("clientes").select("*").eq("cpf", cpf).execute()
            if response.data:
                messagebox.showerror("Erro", "CPF já cadastrado!")
                return
            
            # Adicionar cliente no Supabase
            cliente = {
                "nome": nome,
                "cpf": cpf,
                "telefone": telefone,
                "email": email
            }
            self.supabase.table("clientes").insert(cliente).execute()
            
            # Limpar campos
            self.nome_entry.delete(0, tk.END)
            self.cpf_entry.delete(0, tk.END)
            self.telefone_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.atualizar_lista_clientes()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar cliente: {str(e)}")
    
    def fazer_reserva(self):
        cpf = self.reserva_cpf_entry.get()
        quarto_num = int(self.quarto_combobox.get().split(" - ")[0])
        checkin_str = self.checkin_entry.get()
        checkout_str = self.checkout_entry.get()
        
        try:
            # Validar cliente
            response = self.supabase.table("clientes").select("*").eq("cpf", cpf).execute()
            if not response.data:
                messagebox.showerror("Erro", "Cliente não encontrado!")
                return
            cliente = response.data[0]
            
            # Validar quarto
            response = self.supabase.table("quartos").select("*").eq("numero", quarto_num).eq("disponivel", True).execute()
            if not response.data:
                messagebox.showerror("Erro", "Quarto não disponível!")
                return
            quarto = response.data[0]
            
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
            
            # Criar reserva no Supabase
            reserva = {
                "cliente_id": cliente["id"],
                "quarto_numero": quarto["numero"],
                "checkin": checkin.strftime("%Y-%m-%d"),
                "checkout": checkout.strftime("%Y-%m-%d"),
                "valor": valor_total,
                "status": "confirmada"
            }
            reserva_response = self.supabase.table("reservas").insert(reserva).execute()
            
            # Atualizar disponibilidade do quarto
            self.supabase.table("quartos").update({"disponivel": False}).eq("numero", quarto["numero"]).execute()
            
            # Limpar campos
            self.reserva_cpf_entry.delete(0, tk.END)
            self.checkin_entry.delete(0, tk.END)
            self.checkout_entry.delete(0, tk.END)
            self.atualizar_combo_quartos()
            
            messagebox.showinfo("Sucesso", f"Reserva realizada com sucesso!\nValor Total: R${valor_total:.2f}")
            self.atualizar_lista_reservas()
            self.atualizar_lista_quartos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao fazer reserva: {str(e)}")
            
    def cancelar_reserva(self):
        selecionado = self.reservas_tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Nenhuma reserva selecionada!")
            return
        
        item = self.reservas_tree.item(selecionado[0])
        reserva_id = item["values"][0]
        
        try:
            # Verificar reserva
            response = self.supabase.table("reservas").select("*").eq("id", reserva_id).eq("status", "confirmada").execute()
            if not response.data:
                messagebox.showerror("Erro", "Reserva não encontrada ou já cancelada!")
                return
            reserva = response.data[0]
            
            # Confirmar cancelamento
            if not messagebox.askyesno("Confirmar", f"Cancelar reserva ID {reserva_id}?"):
                return
            
            # Atualizar status no Supabase
            self.supabase.table("reservas").update({"status": "cancelada"}).eq("id", reserva_id).execute()
            
            # Liberar quarto
            self.supabase.table("quartos").update({"disponivel": True}).eq("numero", reserva["quarto_numero"]).execute()
            
            messagebox.showinfo("Sucesso", "Reserva cancelada com sucesso!")
            self.atualizar_lista_reservas()
            self.atualizar_lista_quartos()
            self.atualizar_combo_quartos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cancelar reserva: {str(e)}")
    
    def atualizar_lista_clientes(self):
        self.clientes_tree.delete(*self.clientes_tree.get_children())
        try:
            response = self.supabase.table("clientes").select("*").execute()
            for cliente in response.data:
                self.clientes_tree.insert("", tk.END, values=(
                    cliente["nome"],
                    cliente["cpf"],
                    cliente["telefone"],
                    cliente["email"]
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar clientes: {str(e)}")
    
    def atualizar_lista_quartos(self):
        self.quartos_tree.delete(*self.quartos_tree.get_children())
        try:
            response = self.supabase.table("quartos").select("*").execute()
            for quarto in response.data:
                disponivel = "Sim" if quarto["disponivel"] else "Não"
                self.quartos_tree.insert("", tk.END, values=(
                    quarto["numero"],
                    quarto["tipo"],
                    quarto["capacidade"],
                    f"{quarto['preco']:.2f}",
                    disponivel
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar quartos: {str(e)}")
    
    def atualizar_combo_quartos(self):
        try:
            response = self.supabase.table("quartos").select("*").eq("disponivel", True).execute()
            quartos_disponiveis = [f"{q['numero']} - {q['tipo']} (R${q['preco']:.2f}/noite)" 
                                  for q in response.data]
            self.quarto_combobox["values"] = quartos_disponiveis
            if quartos_disponiveis:
                self.quarto_combobox.current(0)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar quartos disponíveis: {str(e)}")
    
    def atualizar_lista_reservas(self):
        self.reservas_tree.delete(*self.reservas_tree.get_children())
        try:
            # Busca reservas com join para cliente
            response = self.supabase.rpc("get_reservas_com_clientes", {}).execute()
            
            for reserva in response.data:
                status = reserva["status"].capitalize()
                self.reservas_tree.insert("", tk.END, values=(
                    reserva["id"],
                    reserva["cliente_nome"],
                    f"Quarto {reserva['quarto_numero']}",
                    datetime.strptime(reserva["checkin"], "%Y-%m-%d").strftime("%d/%m/%Y"),
                    datetime.strptime(reserva["checkout"], "%Y-%m-%d").strftime("%d/%m/%Y"),
                    f"{reserva['valor']:.2f}",
                    status
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar reservas: {str(e)}")
    
    def gerar_relatorio(self):
        try:
            # Obter estatísticas do banco de dados
            quartos_response = self.supabase.table("quartos").select("*").execute()
            total_quartos = len(quartos_response.data)
            quartos_ocupados = len([q for q in quartos_response.data if not q["disponivel"]])
            ocupacao_percent = (quartos_ocupados / total_quartos) * 100 if total_quartos > 0 else 0
            
            reservas_response = self.supabase.table("reservas").select("*").execute()
            total_reservas = len(reservas_response.data)
            reservas_ativas = len([r for r in reservas_response.data if r["status"] == "confirmada"])
            
            faturamento_response = self.supabase.rpc("get_faturamento_total", {}).execute()
            faturamento_total = faturamento_response.data[0]["faturamento_total"] if faturamento_response.data else 0
            
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
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar relatório: {str(e)}")

# Código para iniciar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()