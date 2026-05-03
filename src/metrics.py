# mypy: ignore-errors
"""Модуль для сбора и экспорта метрик приложения.

Содержит бизнес-метрики для мониторинга работы с контактами:
- счётчики для операций CRUD
- гистограмму распределения возрастов
- датчик размера базы данных
"""

try:
    from prometheus_client import Counter, Gauge, Histogram
except ImportError:
    # Заглушка для тестов или если prometheus_client не установлен
    class _DummyMetric:
        def inc(self, *args, **kwargs):
            pass

        def set(self, *args, **kwargs):
            pass

        def observe(self, *args, **kwargs):
            pass

    Counter = _DummyMetric
    Gauge = _DummyMetric
    Histogram = _DummyMetric


# ========== БИЗНЕС-МЕТРИКИ (с префиксом business_) ==========

# Счётчики операций
business_contacts_views_total = Counter(
    "business_contacts_views_total", "Total number of contacts list views"
)
business_contact_views_total = Counter(
    "business_contact_views_total", "Total number of single contact views"
)
business_contacts_created_total = Counter(
    "business_contacts_created_total", "Total number of contacts created"
)
business_contacts_updated_total = Counter(
    "business_contacts_updated_total", "Total number of contacts fully updated"
)
business_contacts_patched_total = Counter(
    "business_contacts_patched_total", "Total number of contacts partially updated"
)

# Датчик текущего размера БД
business_contacts_db_size = Gauge(
    "business_contacts_db_size", "Current number of contacts in database"
)

# Гистограмма распределения возрастов
business_contact_age_histogram = Histogram(
    "business_contact_age_years",
    "Distribution of contact ages",
    buckets=[18, 25, 35, 45, 55, 65, 80],
)


def update_db_size_gauge(size: int) -> None:
    """Обновляет значение датчика размера базы данных.

    Args:
        size: Текущее количество контактов в базе данных.
    """
    business_contacts_db_size.set(size)