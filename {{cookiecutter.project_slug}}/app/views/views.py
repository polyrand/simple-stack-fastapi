from starlette.templating import JinjaTemplates

templates = JinjaTemplates(directory=str(settings.TEMPLATES_DIR))
