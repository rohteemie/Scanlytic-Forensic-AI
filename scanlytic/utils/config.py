"""
Configuration management for Scanlytic-ForensicAI.

Handles loading and validation of configuration from YAML files
and environment variables.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from scanlytic.utils.exceptions import ConfigurationError
from scanlytic.utils.logger import get_logger

logger = get_logger()


class Config:
    """
    Configuration manager for Scanlytic-ForensicAI.

    Loads configuration from YAML files and environment variables,
    with validation and default values.
    """

    DEFAULT_CONFIG = {
        'analysis': {
            'max_file_size': 104857600,  # 100MB
            'timeout': 300,  # seconds
            'parallel_workers': 4
        },
        'features': {
            'extract_strings': True,
            'string_min_length': 4,
            'calculate_entropy': True,
            'compute_hashes': ['md5', 'sha1', 'sha256']
        },
        'scoring': {
            'malicious_threshold': 50,
            'high_risk_threshold': 75
        },
        'output': {
            'format': 'json',
            'verbose': True,
            'include_features': True
        },
        'logging': {
            'level': 'INFO',
            'file': None,
            'console': True
        }
    }

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration.

        Args:
            config_path: Optional path to YAML configuration file
        """
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: Optional[Path]) -> Dict[str, Any]:
        """
        Load configuration from file and environment.

        Args:
            config_path: Path to configuration file

        Returns:
            Dict[str, Any]: Merged configuration

        Raises:
            ConfigurationError: If configuration is invalid
        """
        config = self.DEFAULT_CONFIG.copy()

        # Load from file if provided
        if config_path:
            try:
                config_path = Path(config_path)
                if not config_path.exists():
                    raise ConfigurationError(
                        f"Configuration file not found: {config_path}"
                    )

                with open(config_path, 'r') as f:
                    file_config = yaml.safe_load(f)
                    if file_config:
                        config = self._merge_configs(config, file_config)
                        logger.info(
                            f"Loaded configuration from {config_path}"
                        )

            except yaml.YAMLError as e:
                raise ConfigurationError(
                    f"Invalid YAML in configuration file: {str(e)}"
                )
            except Exception as e:
                raise ConfigurationError(
                    f"Error loading configuration: {str(e)}"
                )

        # Override with environment variables
        config = self._apply_env_overrides(config)

        return config

    def _merge_configs(self, base: Dict, override: Dict) -> Dict:
        """
        Recursively merge two configuration dictionaries.

        Args:
            base: Base configuration
            override: Override configuration

        Returns:
            Dict: Merged configuration
        """
        result = base.copy()
        for key, value in override.items():
            if (key in result and isinstance(result[key], dict) and
                    isinstance(value, dict)):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result

    def _apply_env_overrides(self, config: Dict) -> Dict:
        """
        Apply environment variable overrides.

        Args:
            config: Configuration dictionary

        Returns:
            Dict: Configuration with environment overrides
        """
        # Example: SCANLYTIC_LOGGING_LEVEL=DEBUG
        env_prefix = 'SCANLYTIC_'

        if env_level := os.getenv(f'{env_prefix}LOGGING_LEVEL'):
            config['logging']['level'] = env_level

        if env_format := os.getenv(f'{env_prefix}OUTPUT_FORMAT'):
            config['output']['format'] = env_format

        if env_workers := os.getenv(f'{env_prefix}WORKERS'):
            try:
                config['analysis']['parallel_workers'] = int(env_workers)
            except ValueError:
                logger.warning(
                    f"Invalid SCANLYTIC_WORKERS value: {env_workers}"
                )

        return config

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.

        Args:
            key: Configuration key (dot notation supported)
            default: Default value if key not found

        Returns:
            Any: Configuration value
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def __getitem__(self, key: str) -> Any:
        """
        Get configuration value using dictionary syntax.

        Args:
            key: Configuration key

        Returns:
            Any: Configuration value
        """
        return self.config[key]
