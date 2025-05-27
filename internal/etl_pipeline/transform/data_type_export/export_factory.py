from transform.data_type_export.base_exporter import BaseExporter
from transform.data_type_export.excel_exporter import ExcelExporter

class ExportFactory:
    @staticmethod
    def get_exporter(export_type: str) -> BaseExporter:
        if export_type == "excel":
            return ExcelExporter()
        # Can add "json", "csv", "db", etc. in future
        raise ValueError(f"Unsupported export type: {export_type}")
