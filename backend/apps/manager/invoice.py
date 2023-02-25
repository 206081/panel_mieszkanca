import datetime
import os
import random
from typing import List

from django.db.models import Q
from InvoiceGenerator.api import Client, Creator, Invoice, Item, Provider
from InvoiceGenerator.pdf import SimpleInvoice

from apps.manager.models import Apartment, Bill, HousingBill, Income
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
    invoice.currency = "zł"
    invoice.currency_locale = "en_US.UTF-8"

    for bill in bills:
        invoice.add_item(Item(bill.amount, bill.bill_type.price, description=str(bill), unit=bill.bill_type.unit))

    pdf = SimpleInvoice(invoice)
    pdf.gen("invoice.pdf")


def create_report(user, apartment, start_date, end_date):
    def add_months(d, x):
        newmonth = (((d.month - 1) + x) % 12) + 1
        newyear = int(d.year + (((d.month - 1) + x) / 12))
        return datetime.date(newyear, newmonth, d.day) - datetime.timedelta(1)

    def sort_records(_record):
        if isinstance(_record, Bill):
            return _record.start_date
        if isinstance(_record, Income):
            return _record.date

    os.environ["INVOICE_LANG"] = "en"

    start_date = datetime.datetime.strptime(str(start_date), "%Y-%m-%d").strftime("%Y-%m-%d")
    end_date = add_months(datetime.datetime.strptime(str(end_date), "%Y-%m-%d"), 1).strftime("%Y-%m-%d")

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
    provider = Provider("Panel mieszkanca", bank_account=apartment.account, bank_code="", **provider)
    creator = Creator("Administrator")

    invoice = Invoice(client, provider, creator)
    invoice.currency = "zl"
    invoice.currency_locale = "pl_PL.UTF-8"
    invoice.number = round(random.random() * 100)

    bills = Bill.objects.filter(Q(start_date__range=[start_date, end_date]) & Q(apartment__id=apartment.id))
    incomes = Income.objects.filter(Q(date__range=[start_date, end_date]) & Q(apartment__id=apartment.id))

    records = [*bills, *incomes]

    records.sort(key=sort_records)

    for record in records:
        if isinstance(record, Bill):
            invoice.add_item(
                Item(
                    1,
                    -record.price,
                    description=f"{record.bill_type.name} - {record.start_date}-{record.end_date}",
                    unit=record.bill_type.unit,
                )
            )
        if isinstance(record, Income):
            invoice.add_item(Item(1, record.amount, description=f"Wplata {record.date}"))

    pdf = SimpleInvoice(invoice)
    path = f"media/report-apartment_{'_'.join(apartment.address.replace('/','-').split())}_{start_date}-_{end_date}.pdf"
    pdf.gen(path)
    return path
