import dns.resolver
import dns.exception
from typing import List

def check_emails(emails: List[str]):
    results = {}

    for email in emails:
        try:
            domain = email.split("@")[1]
        except IndexError:
            results[email] = "некорректный email"
            continue

        # Проверка: существует ли домен (DNS A или NS)
        try:
            dns.resolver.resolve(domain, 'NS')
            domain_exists = True
        except dns.exception.DNSException:
            domain_exists = False

        if not domain_exists:
            results[email] = "домен отсутствует"
            continue

        # Проверка MX
        try:
            dns.resolver.resolve(domain, 'MX')
            results[email] = "домен валиден"
        except dns.exception.DNSException:
            results[email] = "MX-записи отсутствуют или некорректны"

    return results


if __name__ == "__main__":
    test_emails = [
        "test@gmail.com",
        "info@nonexistentdomain123454321.com",
        "hello@example.com"
    ]

    result = check_emails(test_emails)
    for email, status in result.items():
        print(f"{email}: {status}")
