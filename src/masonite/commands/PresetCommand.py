"""New Preset Command."""

from .Command import Command
from ..presets import Tailwind, Vue

# from ..commands.presets.React import React
# from ..commands.presets.Bootstrap import Bootstrap


class PresetCommand(Command):
    """
    Scaffold frontend preset in your project

    preset
        {name : Name of the preset [tailwind, vue, react, bootstrap]}
    """

    presets = ["vue", "tailwind", "react", "boostrap"]

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        preset_name = self.argument("name")
        if preset_name not in self.presets:
            return self.error(
                f"Invalid preset. Available presets are: {', '.join(self.presets)}"
            )

        self.info(f"Scaffolding {preset_name} preset...")
        return getattr(self, preset_name)()

    # def remove(self):
    #     """Removes frontend scaffolding"""
    #     Remove().install()
    #     self.info("Frontend scaffolding removed successfully.")

    # def react(self):
    #     """Add React frontend while also removing Vue (if it was previously selected)"""
    #     React().install()
    #     self.info("React scaffolding installed successfully.")
    #     self.comment(
    #         'Please run "npm install && npm run dev" to compile your fresh scaffolding.'
    #     )

    def vue(self):
        Vue().install()
        self.info("Vue 3.0 installed successfully.")
        self.comment(
            'Please run "npm install && npm run dev" to compile your fresh scaffolding.'
        )
        self.comment("Then you can use the view app_vue3 as demo.")

    # def bootstrap(self):
    #     """Add Bootstrap Sass scafolding"""
    #     Bootstrap().install()
    #     self.info("Bootstrap scaffolding installed successfully.")
    #     self.comment(
    #         'Please run "npm install && npm run dev" to compile your fresh scaffolding.'
    #     )

    def tailwind(self):
        Tailwind().install()
        self.info("TailwindCSS 3 installed successfully.")
        self.comment(
            'Please run "npm install && npm run dev" to compile your fresh scaffolding.'
        )
