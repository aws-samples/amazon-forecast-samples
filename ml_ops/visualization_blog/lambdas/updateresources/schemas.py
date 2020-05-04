SCHEMAS_DEF = {
    "RETAIL":
        {
            "fields": ["item_id", "timestamp", "demand"],
            "identifier": "item_id",
            "metric": "demand",
            "date": "timestamp"
        },
    "CUSTOM":
        {
            "fields": ["item_id", "timestamp", "target_value"],
            "identifier": "item_id",
            "metric": "target_value",
            "date": "timestamp"
        },
    "INVENTORY_PLANNING":
        {
            "fields": ["item_id", "timestamp", "demand"],
            "identifier": "item_id",
            "metric": "demand",
            "date": "timestamp"
        },
    "EC2 CAPACITY":
        {
            "fields": ["instance_type", "timestamp", "number_of_instances"],
            "identifier": "instance_type",
            "metric": "number_of_instances",
            "date": "timestamp"
        },
    "WORK_FORCE":
        {
            "fields": ["workforce_type", "timestamp", "workforce_demand"],
            "identifier": "workforce_type",
            "metric": "workforce_demand",
            "date": "timestamp"
        },
    "WEB_TRAFFIC":
        {
            "fields": ["item_id", "timestamp", "value"],
            "identifier": "item_id",
            "metric": "value",
            "date": "timestamp"
        },
    "METRICS":
        {
            "fields": ["metric_name", "timestamp", "metric_value"],
            "identifier": "metric_name",
            "metric": "metric_value",
            "date": "timestamp"
        }
}
