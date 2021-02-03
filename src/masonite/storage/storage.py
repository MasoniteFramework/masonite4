class StorageCapsule:
    def __init__(self, base_path=None):
        self.storage_templates = {}
        self.base_path = base_path or {}

    def add_storage_assets(self, templates):
        self.storage_templates.update(templates)
        return self

    def get_storage_assets(self):
        return self.storage_templates
