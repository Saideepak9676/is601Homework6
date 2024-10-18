import os
import pkgutil
import importlib
import logging
import logging.config
from pathlib import Path
from dotenv import load_dotenv
from app.commands import CommandHandler, Command
from app.plugins.greet import GreetCommand

class App:
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.command_handler = CommandHandler()  # Initialize CommandHandler

    def configure_logging(self):
        """Configure logging settings."""
        logging_conf_path = 'logging.conf'
        if Path(logging_conf_path).exists():
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.getLogger().setLevel(logging.INFO)

    def load_environment_variables(self):
        """Load environment variables into a dictionary."""
        return {key: value for key, value in os.environ.items()}

    def get_environment_variable(self, key):
        """Retrieve the environment variable value for the given key."""
        return os.environ.get(key)

    def load_plugins(self):
        """Load and register plugins from the specified directory."""
        logging.debug("Starting to load plugins.")

        # Register built-in commands
        greet_command = GreetCommand()
        self.command_handler.register_command("greet", greet_command)
        logging.info("Built-in commands registered.")

        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.', '/')
        
        if not Path(plugins_path).exists():
            logging.warning(f"Plugins directory '{plugins_path}' not found.")
            return

        for _, plugin_name, _ in pkgutil.iter_modules([plugins_path]):
            try:
                plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                self.register_plugin_commands(plugin_module, plugin_name)
            except ImportError:
                logging.warning(f"Skipping plugin '{plugin_name}' due to import error.")

    def register_plugin_commands(self, plugin_module, plugin_name):
        """Register commands defined in the plugin module."""
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                command_instance = item()
                self.command_handler.register_command(plugin_name, command_instance)

    def start(self):
        """Start the command line application."""
        self.load_plugins()  # Load the plugins at the start
        logging.info("Application started. Type 'exit' to exit.")
        try:
            while True:
                cmd_input = input(">>> ").strip()
                if cmd_input.lower() == 'exit':
                    break
                self.command_handler.execute_command(cmd_input)
        except KeyboardInterrupt:
            logging.info("Application interrupted by user.")
            print("Application interrupted by user.")
        finally:
            logging.info("Application shutdown.")
            print("Application shutdown.")

if __name__ == "__main__":
    app = App()
    app.start()
