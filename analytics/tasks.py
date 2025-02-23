import csv
import os
from uuid import uuid4

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from sales.models import SalesOrder
from trading.models import Order


def generate_unique_filename(extension="csv"):
    """
    Create a unique filename using the current timestamp and a short UUID.

    :param extension: Desired file extension (default: "csv").
    :return: A unique filename as a string.
    """
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid4().hex[:6]
    return f"analytics_{timestamp}_{unique_id}.{extension}"


def ensure_reports_directory():
    """
    Ensure the reports directory exists in MEDIA_ROOT and return its path.

    :return: Path to the reports directory.
    """
    reports_path = os.path.join(settings.MEDIA_ROOT, "reports")
    os.makedirs(reports_path, exist_ok=True)
    return reports_path


def write_csv_report(file_path, orders, sales_orders):
    """
    Write the given orders and sales orders into a structured CSV report.

    :param file_path: Full path where the CSV will be saved.
    :param orders: Queryset of Order objects.
    :param sales_orders: Queryset of SalesOrder objects.
    """
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Orders section
        writer.writerow(["Orders Report"])
        writer.writerow(
            ["ID", "User", "Product", "Type", "Quantity", "Price", "Created At"]
        )
        for order in orders:
            writer.writerow(
                [
                    order.id,
                    order.user.username,
                    order.product.name,
                    order.order_type.capitalize(),
                    order.quantity,
                    f"{order.price:.2f}",
                    order.created_at.strftime("%d-%m-%Y %H:%M"),
                ]
            )

        writer.writerow([])  # Separator

        # Sales Orders section
        writer.writerow(["Sales Orders Report"])
        writer.writerow(["ID", "Customer", "Status", "Created At", "Total"])
        for sales_order in sales_orders:
            writer.writerow(
                [
                    sales_order.id,
                    sales_order.customer.username,
                    sales_order.status.title(),
                    sales_order.created_at.strftime("%d-%m-%Y %H:%M"),
                    f"{sales_order.total:.2f}",
                ]
            )


def fetch_data():
    """
    Retrieve data from the database for Orders and Sales Orders.

    :return: Tuple containing querysets for orders and sales orders.
    """
    orders = Order.objects.select_related("product", "user").all()
    sales_orders = SalesOrder.objects.select_related("customer").all()
    return orders, sales_orders


@shared_task
def generate_report_task(extension="csv"):
    """
    Generate a report asynchronously using Celery.

    :param extension: Desired file extension (default: "csv").
    :return: Path to the generated report file.
    """
    filename = generate_unique_filename(extension)
    reports_dir = ensure_reports_directory()
    file_path = os.path.join(reports_dir, filename)

    orders, sales_orders = fetch_data()
    write_csv_report(file_path, orders, sales_orders)

    return file_path


def generate_report_synchronously():
    """
    Generate a report synchronously for immediate use.

    :return: Path to the generated report file.
    """
    filename = generate_unique_filename("csv")
    reports_dir = ensure_reports_directory()
    file_path = os.path.join(reports_dir, filename)

    orders, sales_orders = fetch_data()
    write_csv_report(file_path, orders, sales_orders)

    return file_path
