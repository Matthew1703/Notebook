from prometheus_client import Counter, Gauge, Histogram

# ========== БИЗНЕС-МЕТРИКИ (с префиксом business_) ==========
business_contacts_views_total = Counter('business_contacts_views_total', 'Total number of contacts list views')
business_contact_views_total = Counter('business_contact_views_total', 'Total number of single contact views')
business_contacts_created_total = Counter('business_contacts_created_total', 'Total number of contacts created')
business_contacts_updated_total = Counter('business_contacts_updated_total', 'Total number of contacts fully updated')
business_contacts_patched_total = Counter('business_contacts_patched_total', 'Total number of contacts partially updated')
business_contacts_db_size = Gauge('business_contacts_db_size', 'Current number of contacts in database')
business_contact_age_histogram = Histogram('business_contact_age_years', 'Distribution of contact ages', buckets=[18, 25, 35, 45, 55, 65, 80])

def update_db_size_gauge(size: int):
    business_contacts_db_size.set(size)
