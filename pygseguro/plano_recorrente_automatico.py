from decimal import Decimal

import requests

from pygseguro.config import get_config_padrao


def _to_decimal_string(decimal: Decimal):
    return f'{decimal:.2f}'


class PlanoPagamentoRecorrenteAutomatico:
    def __init__(self,
                 reference,
                 pre_approval_name,
                 pre_approval_details,
                 pre_approval_receiver_email,
                 pre_approval_amount_per_payment,
                 pre_approval_trial_period_duration,
                 pre_approval_expiration_value,
                 pre_approval_expiration_unit,
                 pre_approval_membership_fee=None,
                 pre_approval_period='MONTHLY',
                 pre_approval_max_uses=None,
                 redirect_url=None,
                 pre_approval_cancel_url=None,
                 pre_approval_review_url=None,

                 ):
        self.redirect_url = redirect_url
        self.pre_approval_cancel_url = pre_approval_cancel_url
        self.pre_approval_review_url = pre_approval_review_url
        self.pre_approval_max_uses = pre_approval_max_uses
        self.pre_approval_period = pre_approval_period
        self.pre_approval_membership_fee = pre_approval_membership_fee
        self.pre_approval_expiration_unit = pre_approval_expiration_unit
        self.pre_approval_expiration_value = pre_approval_expiration_value
        self.pre_approval_trial_period_duration = pre_approval_trial_period_duration
        self.pre_approval_amount_per_payment = pre_approval_amount_per_payment
        self.pre_approval_receiver_email = pre_approval_receiver_email
        self.pre_approval_details = pre_approval_details
        self.pre_approval_name = pre_approval_name
        self.reference = reference

    def criar_no_pagseguro(self):
        """
        Cria um plano automático na conta do pagseguro
        :return: código do plano criado
        """
        expiration = {
            'value': self.pre_approval_expiration_value,
            'unit': self.pre_approval_expiration_unit,
        }
        pre_approval = {
            'charge': 'AUTO',
            'name': self.pre_approval_name,
            'details': self.pre_approval_details,
            'amountPerPayment': _to_decimal_string(self.pre_approval_amount_per_payment),
            'trialPeriodDuration': self.pre_approval_trial_period_duration,
            'membershipFee': _to_decimal_string(self.pre_approval_membership_fee),
            'period': self.pre_approval_period,
            'cancelURL': self.pre_approval_cancel_url,
            'expiration': expiration
        }
        receiver = {'email': self.pre_approval_receiver_email}
        data = {
            'reference': self.reference,
            'maxUses': self.pre_approval_max_uses,
            'redirectURL': self.redirect_url,
            'reviewURL': self.pre_approval_review_url,
            'preApproval': pre_approval,
            'receiver': receiver,

        }
        config = get_config_padrao()
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/vnd.pagseguro.com.br.v3+json;charset=ISO-8859-1'
        }
        response = requests.post(config.construir_url('/pre-approvals/request'), json=data, headers=headers)
        assert response.status_code == 200
