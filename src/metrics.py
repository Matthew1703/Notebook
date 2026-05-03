"""Модуль для сбора и экспорта метрик приложения.

Содержит бизнес-метрики для мониторинга работы с контактами:
- счётчики для операций CRUD
- гистограмму распределения возрастов
- датчик размера базы данных
"""

from typing import Any, Callable, Optional, Union

# Подавляем ошибку импорта для mypy/pylint (библиотека установлена)
try:
    from prometheus_client import (  # type: ignore[import-not-found]
        Counter,
        Gauge,
        Histogram,
    )
except ImportError:
    # Заглушка для тестов или если prometheus_client не установлен
    class _DummyMetric:
        """Заглушка для метрик, когда prometheus_client не установлен."""

        def inc(self, *args: Any, **kwargs: Any) -> None:
            """Заглушка для inc."""
            pass

        def set(self, *args: Any, **kwargs: Any) -> None:
            """Заглушка для set."""
            pass

        def observe(self, *args: Any, **kwargs: Any) -> None:
            """Заглушка для observe."""
            pass

    # Используем type: ignore для подавления ошибок mypy
    Counter = _DummyMetric  # type: ignore[assignment]
    Gauge = _DummyMetric  # type: ignore[assignment]
    Histogram = _DummyMetric  # type: ignore[assignment]


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
