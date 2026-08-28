"""
Page Object Models (POM) package.
"""
from src.pages.base_page import BasePage
from src.pages.settings_page import SettingsPage
from src.pages.screencast_page import ScreencastPage
from src.pages.roles_permissions_page import RolesPermissionsPage
from src.pages.monitoring_control_page import MonitoringControlPage
from src.pages.auto_email_reports_page import AutoEmailReportsPage
from src.pages.reseller_client_page import ResellerClientPage

__all__ = [
    "BasePage",
    "SettingsPage",
    "ScreencastPage",
    "RolesPermissionsPage",
    "MonitoringControlPage",
    "AutoEmailReportsPage",
    "ResellerClientPage"
]


