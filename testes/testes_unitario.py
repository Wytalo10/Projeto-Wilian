import pytest
from datetime import datetime
from src.hotel_app import HotelApp
from unittest.mock import MagicMock

@pytest.fixture
def mock_supabase():
    mock = MagicMock()
    mock.table.return_value.select.return_value.execute.return_value.data = []
    return mock

def test_calculo_valor_reserva():
    """Testa o cálculo correto do valor da reserva"""
    # Dados de teste
    quarto = {"preco": 200.00}
    checkin = datetime(2023, 1, 1)
    checkout = datetime(2023, 1, 5)  # 4 noites
    
    # Cálculo esperado: 200 * 4 = 800
    hotel = HotelApp(None)
    valor = hotel._calcular_valor_reserva(quarto, checkin, checkout)
    
    assert valor == 800.00

def test_validar_datas_reserva():
    """Testa a validação de datas da reserva"""
    hotel = HotelApp(None)
    
    # Caso válido
    checkin = datetime(2023, 1, 1)
    checkout = datetime(2023, 1, 5)
    assert hotel._validar_datas_reserva(checkin, checkout) is True
    
    # Caso inválido (checkout antes do checkin)
    with pytest.raises(ValueError):
        hotel._validar_datas_reserva(checkout, checkin)

def test_cadastro_cliente(mock_supabase):
    """Testa o cadastro de cliente"""
    hotel = HotelApp(None)
    hotel.supabase = mock_supabase
    
    # Configurar mock
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = []
    
    # Testar cadastro válido
    result = hotel.cadastrar_cliente("João", "12345678901", "(11) 9999-8888", "joao@test.com")
    assert result is True
    
    # Verificar se o insert foi chamado
    mock_supabase.table.return_value.insert.assert_called_once()