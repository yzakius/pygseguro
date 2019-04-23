from decimal import Decimal

import pytest

from pygseguro import PlanoPagamentoRecorrenteAutomatico, set_config_padrao, ConfigConta


@pytest.fixture
def pagamento_recorrente_automatico():
    set_config_padrao(ConfigConta('renz.o@python.pro.br', 'token', 'https://ws.sandbox.pagseguro.uol.com.br'))
    return PlanoPagamentoRecorrenteAutomatico(
        redirect_url='https://seusite.com.br/obrigado',
        reference='SEU_CODIGO_DE_REFERENCIA',
        pre_approval_name='Plano Turma de Curso de Python',
        pre_approval_period='MONTHLY',
        pre_approval_amount_per_payment=Decimal('180.00'),
        pre_approval_membership_fee=Decimal('30.39'),
        pre_approval_trial_period_duration=2,
        pre_approval_expiration_value=10,
        pre_approval_expiration_unit='MONTHS',
        pre_approval_details='Plano de pagamento da turma Luciano Ramalho',
        pre_approval_cancel_url='https://seusite.com.br/cancelar',
        pre_approval_review_url='https://seusite.com.br/cancelar',
        pre_approval_max_uses=100,
        pre_approval_receiver_email='renz.o@python.pro.br'
    )

def test_construcao_de_plano_com_expericao(pagamento_recorrente_automatico):
    assert pagamento_recorrente_automatico is not None


def test_criar_plano_no_pagseguro(pagamento_recorrente_automatico:PlanoPagamentoRecorrenteAutomatico):
    pagamento_recorrente_automatico.criar_no_pagseguro()

