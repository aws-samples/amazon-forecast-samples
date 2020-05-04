SCHEMA_DEF = {
    "type":
        "object",
    "properties":
        {
            "DatasetGroup":
                {
                    "type": "object",
                    "properties":
                        {
                            "DatasetGroupName": {
                                "type": "string"
                            },
                            "Domain": {
                                "type": "string"
                            }
                        },
                    "required": ["DatasetGroupName", "Domain"]
                },
            "Predictor":
                {
                    "type":
                        "object",
                    "properties":
                        {
                            "PredictorName": {
                                "type": "string"
                            },
                            "ForecastHorizon": {
                                "type": "integer"
                            },
                            "FeaturizationConfig":
                                {
                                    "type": "object",
                                    "properties":
                                        {
                                            "ForecastFrequency":
                                                {
                                                    "type": "string"
                                                }
                                        },
                                    "required": ["ForecastFrequency"]
                                },
                            "PerformAutoML": {
                                "type": "boolean"
                            }
                        },
                    "required":
                        [
                            "PredictorName", "ForecastHorizon",
                            "FeaturizationConfig"
                        ]
                },
            "Forecast":
                {
                    "type": "object",
                    "properties":
                        {
                            "ForecastName": {
                                "type": "string"
                            },
                            "ForecastTypes": {
                                "type": "array"
                            }
                        },
                    "required": ["ForecastName", "ForecastTypes"]
                },
            "TimestampFormat": {
                "type": "string"
            },
            "Datasets":
                {
                    "type":
                        "array",
                    "items":
                        [
                            {
                                "type":
                                    "object",
                                "properties":
                                    {
                                        "DatasetName": {
                                            "type": "string"
                                        },
                                        "Domain": {
                                            "type": "string"
                                        },
                                        "DatasetType": {
                                            "type": "string"
                                        },
                                        "DataFrequency": {
                                            "type": "string"
                                        },
                                        "Schema":
                                            {
                                                "type": "object",
                                                "properties":
                                                    {
                                                        "Attributes":
                                                            {
                                                                "type": "array"
                                                            }
                                                    },
                                                "required": ["Attributes"]
                                            }
                                    },
                                "required":
                                    [
                                        "DatasetName", "Domain", "DatasetType",
                                        "DataFrequency", "Schema"
                                    ]
                            }
                        ]
                }
        },
    "required":
        [
            "DatasetGroup", "Predictor", "Forecast", "TimestampFormat",
            "Datasets"
        ]
}
