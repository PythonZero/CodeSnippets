class ConfigValues:  # pylint: disable=too-few-public-methods
    """Holds the config keys and values."""

    config_dict: Dict[str, str]
    VARIBLE1: str
    START_DATE: str 

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> None:
        """Loads the config variables from the file & loads the
        keys as class parameters.
        :param: config_path: path/to/config_file
                if None, uses the config.yaml file in the root folder.
        """
        cls._load_config_vars_from_file(config_path=config_path)
        cls._load_config_vars_as_class_properties()

    @classmethod
    def _load_config_vars_from_file(cls, config_path: Optional[str] = None) -> None:
        """Loads the config_variables
        :param: config_path: path/to/config_file
                if None, uses the config.yaml file in the root folder.
                """
        config_path = (
            os.path.join(os.path.dirname(__file__), "../", "config.yaml")
            if not config_path
            else config_path
        )

        cls.config_dict = mylib.config.load_config_vars(
            path=config_path, include_environ_vars=[], output_validator=None
        )

    @classmethod
    def _load_config_vars_as_class_properties(cls) -> None:
        """Loads the dictionary configuration file as the classes properties"""
        for key in cls.config_dict:
            setattr(cls, key, cls.config_dict[key])

