"""
driver_factory.py
==========================================================
Factory class responsible for creating and configuring
Selenium WebDriver instances for Chrome, Firefox, and Edge.

Design pattern: Factory Method
- Keeps browser-instantiation logic out of tests/pages.
- Single source of truth for driver configuration
  (timeouts, window size, headless mode, options, etc.)
==========================================================
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utilities.config_reader import config
from utilities.logger import get_logger, log_browser_launch

logger = get_logger("DriverFactory")


class DriverFactory:
    """Creates a configured WebDriver instance for the requested browser."""

    SUPPORTED_BROWSERS = ("chrome", "firefox", "edge")

    @staticmethod
    def get_driver(browser: str = None, headless: bool = None):
        """
        Instantiate and return a configured WebDriver.

        Args:
            browser: "chrome" | "firefox" | "edge". Defaults to config.ini value.
            headless: Overrides config.ini headless flag if provided.

        Returns:
            selenium.webdriver.<Browser>WebDriver instance
        """
        browser = (browser or config.get_browser()).lower().strip()
        headless = config.is_headless() if headless is None else headless
        width, height = config.get_window_size()

        if browser not in DriverFactory.SUPPORTED_BROWSERS:
            raise ValueError(
                f"Unsupported browser: '{browser}'. "
                f"Supported browsers: {DriverFactory.SUPPORTED_BROWSERS}"
            )

        logger.info(f"Initializing '{browser}' driver | headless={headless}")

        if browser == "chrome":
            driver = DriverFactory._create_chrome_driver(headless)
        elif browser == "firefox":
            driver = DriverFactory._create_firefox_driver(headless)
        elif browser == "edge":
            driver = DriverFactory._create_edge_driver(headless)
        else:
            # Unreachable due to earlier validation, kept for safety
            raise ValueError(f"Unsupported browser: {browser}")

        driver.set_window_size(width, height)
        driver.implicitly_wait(config.get_implicit_wait())
        driver.set_page_load_timeout(config.get_page_load_timeout())

        log_browser_launch(logger, browser)
        return driver

    # ------------------------------------------------------------------
    # Browser-specific creation methods
    # ------------------------------------------------------------------
    @staticmethod
    def _create_chrome_driver(headless: bool):
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    @staticmethod
    def _create_firefox_driver(headless: bool):
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")

        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    @staticmethod
    def _create_edge_driver(headless: bool):
        options = EdgeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")

        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
