from typing import List

from InvoiceGenerator.api import Client, Creator, Invoice, Item, Provider
from InvoiceGenerator.pdf import SimpleInvoice
import os
from apps.manager.models import Apartment, Bill
from apps.users.models import User


def create_invoice(user: User, apartment: Apartment, bills: List[Bill]) -> None:
    os.environ["INVOICE_LANG"] = "pl"

    client = {
        "email": user.email,
        "summary": " ".join((user.first_name, user.last_name)),
        "address": apartment.address,
    }
    client = Client(**client)
    provider = {
        "email": "admin@panel-mieszkanca.pl",
        "address": "ul. Lekko śmieszna 69/420",
    }
    provider = Provider("Panel mieszkanca", bank_account="'numer konta administracji'", bank_code="2137", **provider)
    creator = Creator("Administrator")

    invoice = Invoice(client, provider, creator)
    invoice.currency = 'zł'
    invoice.currency_locale = "en_US.UTF-8"

    for bill in bills:
        invoice.add_item(Item(bill.amount, bill.bill_type.price, description=str(bill), unit=bill.bill_type.unit))

    pdf = SimpleInvoice(invoice)
    pdf.gen("invoice.pdf")
