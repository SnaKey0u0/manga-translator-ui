"""
Theme runtime helpers.

This module owns:
- current theme tracking
- palette generation
- application-level shared stylesheet
- lightweight repolish helpers for local widget stylesheets
"""

from __future__ import annotations

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication, QToolTip, QWidget
from theme_registry import AVAILABLE_THEMES, DEFAULT_THEME, THEME_OPTIONS

_ACCENT_BASES = {
    "sky": "#3F9BF5",
    "blue": "#4A8EE0",
    "slate": "#87A3C4",
    "teal": "#2FB9C9",
    "green": "#59B86D",
    "orange": "#EE974C",
    "rose": "#D86E8C",
}

_DARK_THEME_BASES = frozenset({"dark", "gray"})

_THEME_PROFILES = {
    "light": {"base_theme": "light", "accent": "sky"},
    "dark": {"base_theme": "dark", "accent": "blue"},
    "gray": {"base_theme": "gray", "accent": "slate"},
    "ocean": {"base_theme": "dark", "accent": "teal"},
    "forest": {"base_theme": "gray", "accent": "green"},
    "sunset": {"base_theme": "gray", "accent": "orange"},
    "rose": {"base_theme": "dark", "accent": "rose"},
}

DARK_THEMES = frozenset(
    theme_key for theme_key, profile in _THEME_PROFILES.items() if profile["base_theme"] in _DARK_THEME_BASES
)


def normalize_theme(theme: str) -> str:
    return theme if theme in _THEME_PROFILES else DEFAULT_THEME


def resolve_theme_variant(theme: str) -> tuple[str, str]:
    profile = _THEME_PROFILES[normalize_theme(theme)]
    return profile["base_theme"], profile["accent"]


def get_theme_colors(theme: str) -> dict:
    """Return semantic tokens for a theme layered with per-theme surface and accent tokens."""
    normalized_theme = normalize_theme(theme)
    base_theme, accent = resolve_theme_variant(normalized_theme)
    colors = dict(_THEMES[base_theme])
    colors.update(_THEME_TOKEN_OVERRIDES.get(normalized_theme, {}))
    colors.update(_build_accent_overrides(accent, dark_theme=base_theme in _DARK_THEME_BASES))
    return colors


_THEMES = {
    "dark": {
        "bg_gradient_start": "#070B19",
        "bg_gradient_mid": "#0E1428",
        "bg_gradient_end": "#161F3C",
        "bg_window_shell": "#070B19",
        "bg_shell_edge": "rgba(255, 255, 255, 0.08)",
        "bg_sidebar": "rgba(7, 10, 20, 0.85)",
        "bg_card": "rgba(20, 28, 48, 0.65)",
        "bg_card_border": "rgba(255, 255, 255, 0.08)",
        "bg_panel": "rgba(22, 32, 54, 0.60)",
        "bg_toolbar": "rgba(9, 13, 26, 0.96)",
        "bg_toolbar_border": "rgba(255, 255, 255, 0.08)",
        "bg_input": "rgba(15, 22, 38, 0.90)",
        "bg_input_focus": "rgba(22, 32, 54, 0.95)",
        "bg_text_edit": "rgba(12, 18, 32, 0.94)",
        "bg_list": "rgba(12, 18, 32, 0.80)",
        "bg_dropdown": "#0E1428",
        "bg_header_card": "rgba(22, 32, 54, 0.65)",
        "bg_desc_panel": "rgba(18, 26, 44, 0.85)",
        "bg_scroll": "rgba(10, 16, 30, 0.74)",
        "bg_settings_input": "rgba(15, 22, 38, 0.92)",
        "bg_canvas": "#0D1322",
        "bg_canvas_overlay": "rgba(13, 19, 34, 0.95)",
        "bg_surface_raised": "rgba(26, 37, 62, 0.96)",
        "bg_surface_soft": "rgba(20, 28, 48, 0.55)",
        "text_primary": "#E2E8F0",
        "text_secondary": "#94A3B8",
        "text_accent": "#F8FAFC",
        "text_bright": "#FFFFFF",
        "text_muted": "#64748B",
        "text_disabled": "rgba(148, 163, 184, 0.40)",
        "text_brand": "#EEF2F6",
        "text_sidebar_group": "#64748B",
        "text_card_title": "#E2E8F0",
        "text_page_title": "#F8FAFC",
        "text_page_subtitle": "#94A3B8",
        "text_row_label": "#CBD5E1",
        "text_desc_header": "#CBD5E1",
        "text_desc_name": "#F8FAFC",
        "text_desc_key": "#6366F1",
        "text_desc_text": "#94A3B8",
        "text_settings_label": "#CBD5E1",
        "text_divider_title": "#E2E8F0",
        "text_divider_sub": "#94A3B8",
        "text_divider_dot": "#6366F1",
        "border_input": "rgba(255, 255, 255, 0.12)",
        "border_input_focus": "rgba(99, 102, 241, 0.92)",
        "border_input_hover": "rgba(99, 102, 241, 0.50)",
        "border_card": "rgba(255, 255, 255, 0.08)",
        "border_list": "rgba(255, 255, 255, 0.08)",
        "border_sidebar": "rgba(255, 255, 255, 0.06)",
        "border_tab": "rgba(255, 255, 255, 0.08)",
        "border_tab_selected": "rgba(99, 102, 241, 0.82)",
        "border_settings_input": "rgba(255, 255, 255, 0.10)",
        "border_settings_input_hover": "rgba(99, 102, 241, 0.50)",
        "border_subtle": "rgba(255, 255, 255, 0.06)",
        "btn_soft_bg": "rgba(255, 255, 255, 0.06)",
        "btn_soft_border": "rgba(255, 255, 255, 0.08)",
        "btn_soft_hover": "rgba(255, 255, 255, 0.12)",
        "btn_soft_pressed": "rgba(255, 255, 255, 0.18)",
        "btn_soft_checked_bg": "rgba(99, 102, 241, 0.15)",
        "btn_soft_checked_border": "rgba(99, 102, 241, 0.50)",
        "btn_soft_text": "#E2E8F0",
        "btn_primary_bg": "#4F46E5",
        "btn_primary_hover": "#4338CA",
        "btn_primary_pressed": "#3730A3",
        "btn_primary_border": "rgba(99, 102, 241, 0.50)",
        "btn_primary_text": "#FFFFFF",
        "btn_bg": "#4F46E5",
        "btn_border": "rgba(99, 102, 241, 0.50)",
        "btn_hover": "#4338CA",
        "btn_pressed": "#3730A3",
        "btn_disabled_bg": "rgba(255, 255, 255, 0.04)",
        "btn_disabled_border": "rgba(255, 255, 255, 0.04)",
        "btn_checked_bg": "#4F46E5",
        "btn_checked_border": "rgba(99, 102, 241, 0.60)",
        "btn_chip_bg": "rgba(255, 255, 255, 0.06)",
        "btn_chip_border": "rgba(255, 255, 255, 0.08)",
        "btn_chip_hover": "rgba(255, 255, 255, 0.12)",
        "btn_settings_bg": "rgba(99, 102, 241, 0.10)",
        "btn_settings_border": "rgba(99, 102, 241, 0.30)",
        "btn_settings_hover": "rgba(99, 102, 241, 0.20)",
        "btn_settings_hover_border": "rgba(99, 102, 241, 0.50)",
        "nav_hover_bg": "rgba(255, 255, 255, 0.08)",
        "nav_hover_border": "rgba(255, 255, 255, 0.08)",
        "nav_checked_bg": "rgba(99, 102, 241, 0.15)",
        "nav_checked_border": "rgba(99, 102, 241, 0.40)",
        "cta_gradient_start": "#6366F1",
        "cta_gradient_end": "#4F46E5",
        "cta_border": "rgba(99, 102, 241, 0.40)",
        "cta_text": "#FFFFFF",
        "cta_hover_start": "#4F46E5",
        "cta_hover_end": "#4338CA",
        "accent_soft": "rgba(99, 102, 241, 0.15)",
        "tab_bg": "rgba(255, 255, 255, 0.04)",
        "tab_selected_start": "rgba(99, 102, 241, 0.20)",
        "tab_selected_end": "rgba(99, 102, 241, 0.05)",
        "tab_hover": "rgba(255, 255, 255, 0.08)",
        "list_item_hover": "rgba(255, 255, 255, 0.06)",
        "list_item_selected": "rgba(99, 102, 241, 0.20)",
        "list_item_selected_text": "#FFFFFF",
        "dropdown_selection": "rgba(99, 102, 241, 0.25)",
        "scroll_handle": "rgba(255, 255, 255, 0.10)",
        "scroll_handle_hover": "rgba(255, 255, 255, 0.20)",
        "splitter_handle": "rgba(255, 255, 255, 0.06)",
        "splitter_handle_hover": "rgba(99, 102, 241, 0.40)",
        "divider_sidebar": "rgba(255, 255, 255, 0.06)",
        "divider_accent_start": "#6366F1",
        "divider_accent_end": "#4F46E5",
        "divider_line_start": "rgba(99, 102, 241, 0.35)",
        "divider_line_end": "rgba(99, 102, 241, 0.02)",
        "divider_sub_line": "rgba(255, 255, 255, 0.06)",
        "divider_desc": "rgba(99, 102, 241, 0.40)",
        "divider_desc_end": "rgba(99, 102, 241, 0.02)",
        "checkbox_border": "rgba(255, 255, 255, 0.15)",
        "checkbox_bg": "rgba(15, 22, 38, 0.90)",
        "checkbox_checked_start": "#6366F1",
        "checkbox_checked_end": "#4F46E5",
        "checkbox_checked_border": "rgba(99, 102, 241, 0.80)",
        "checkbox_hover_border": "rgba(99, 102, 241, 0.50)",
        "slider_groove": "rgba(255, 255, 255, 0.10)",
        "slider_handle_start": "#6366F1",
        "slider_handle_end": "#4F46E5",
        "slider_handle_border": "rgba(99, 102, 241, 0.60)",
        "slider_handle_hover_start": "#818CF8",
        "slider_handle_hover_end": "#6366F1",
        "separator_color": "rgba(255, 255, 255, 0.08)",
        "desc_panel_border": "rgba(255, 255, 255, 0.08)",
        "settings_desc_panel_bg": "rgba(18, 26, 44, 0.85)",
        "danger_bg": "#EF4444",
        "danger_hover": "#DC2626",
        "danger_border": "rgba(239, 68, 68, 0.50)",
        "danger_text": "#FFFFFF",
        "success_color": "#10B981",
        "warning_color": "#F59E0B",
        "shadow_color": "rgba(0, 0, 0, 0.40)",
    },
    "light": {
        "bg_gradient_start": "#F8FAFC",
        "bg_gradient_mid": "#F1F5F9",
        "bg_gradient_end": "#E2E8F0",
        "bg_window_shell": "#F8FAFC",
        "bg_shell_edge": "rgba(0, 0, 0, 0.06)",
        "bg_sidebar": "rgba(241, 245, 249, 0.95)",
        "bg_card": "rgba(255, 255, 255, 0.75)",
        "bg_card_border": "rgba(0, 0, 0, 0.06)",
        "bg_panel": "rgba(255, 255, 255, 0.65)",
        "bg_toolbar": "rgba(241, 245, 249, 0.96)",
        "bg_toolbar_border": "rgba(0, 0, 0, 0.06)",
        "bg_input": "rgba(255, 255, 255, 0.90)",
        "bg_input_focus": "rgba(255, 255, 255, 1.00)",
        "bg_text_edit": "rgba(255, 255, 255, 0.95)",
        "bg_list": "rgba(255, 255, 255, 0.80)",
        "bg_dropdown": "#FFFFFF",
        "bg_header_card": "rgba(255, 255, 255, 0.80)",
        "bg_desc_panel": "rgba(255, 255, 255, 0.85)",
        "bg_scroll": "rgba(226, 232, 240, 0.82)",
        "bg_settings_input": "rgba(255, 255, 255, 0.92)",
        "bg_canvas": "#F1F5F9",
        "bg_canvas_overlay": "rgba(241, 245, 249, 0.96)",
        "bg_surface_raised": "rgba(255, 255, 255, 1.0)",
        "bg_surface_soft": "rgba(241, 245, 249, 0.90)",
        "text_primary": "#1E293B",
        "text_secondary": "#64748B",
        "text_accent": "#0F172A",
        "text_bright": "#020617",
        "text_muted": "#94A3B8",
        "text_disabled": "rgba(148, 163, 184, 0.50)",
        "text_brand": "#1E293B",
        "text_sidebar_group": "#94A3B8",
        "text_card_title": "#1E293B",
        "text_page_title": "#0F172A",
        "text_page_subtitle": "#64748B",
        "text_row_label": "#334155",
        "text_desc_header": "#334155",
        "text_desc_name": "#0F172A",
        "text_desc_key": "#3B82F6",
        "text_desc_text": "#475569",
        "text_settings_label": "#334155",
        "text_divider_title": "#1E293B",
        "text_divider_sub": "#64748B",
        "text_divider_dot": "#3B82F6",
        "border_input": "rgba(0, 0, 0, 0.12)",
        "border_input_focus": "rgba(59, 130, 246, 0.80)",
        "border_input_hover": "rgba(59, 130, 246, 0.50)",
        "border_card": "rgba(0, 0, 0, 0.06)",
        "border_list": "rgba(0, 0, 0, 0.06)",
        "border_sidebar": "rgba(0, 0, 0, 0.05)",
        "border_tab": "rgba(0, 0, 0, 0.08)",
        "border_tab_selected": "rgba(59, 130, 246, 0.70)",
        "border_settings_input": "rgba(0, 0, 0, 0.08)",
        "border_settings_input_hover": "rgba(59, 130, 246, 0.50)",
        "border_subtle": "rgba(0, 0, 0, 0.04)",
        "btn_soft_bg": "rgba(0, 0, 0, 0.04)",
        "btn_soft_border": "rgba(0, 0, 0, 0.06)",
        "btn_soft_hover": "rgba(0, 0, 0, 0.08)",
        "btn_soft_pressed": "rgba(0, 0, 0, 0.12)",
        "btn_soft_checked_bg": "rgba(59, 130, 246, 0.10)",
        "btn_soft_checked_border": "rgba(59, 130, 246, 0.40)",
        "btn_soft_text": "#334155",
        "btn_primary_bg": "#3B82F6",
        "btn_primary_hover": "#2563EB",
        "btn_primary_pressed": "#1D4ED8",
        "btn_primary_border": "rgba(59, 130, 246, 0.50)",
        "btn_primary_text": "#FFFFFF",
        "btn_bg": "#3B82F6",
        "btn_border": "rgba(59, 130, 246, 0.50)",
        "btn_hover": "#2563EB",
        "btn_pressed": "#1D4ED8",
        "btn_disabled_bg": "rgba(0, 0, 0, 0.02)",
        "btn_disabled_border": "rgba(0, 0, 0, 0.02)",
        "btn_checked_bg": "#3B82F6",
        "btn_checked_border": "rgba(59, 130, 246, 0.60)",
        "btn_chip_bg": "rgba(0, 0, 0, 0.04)",
        "btn_chip_border": "rgba(0, 0, 0, 0.06)",
        "btn_chip_hover": "rgba(0, 0, 0, 0.08)",
        "btn_settings_bg": "rgba(59, 130, 246, 0.08)",
        "btn_settings_border": "rgba(59, 130, 246, 0.20)",
        "btn_settings_hover": "rgba(59, 130, 246, 0.15)",
        "btn_settings_hover_border": "rgba(59, 130, 246, 0.40)",
        "nav_hover_bg": "rgba(0, 0, 0, 0.05)",
        "nav_hover_border": "rgba(0, 0, 0, 0.05)",
        "nav_checked_bg": "rgba(59, 130, 246, 0.10)",
        "nav_checked_border": "rgba(59, 130, 246, 0.40)",
        "cta_gradient_start": "#3B82F6",
        "cta_gradient_end": "#2563EB",
        "cta_border": "rgba(59, 130, 246, 0.40)",
        "cta_text": "#FFFFFF",
        "cta_hover_start": "#2563EB",
        "cta_hover_end": "#1D4ED8",
        "accent_soft": "rgba(59, 130, 246, 0.10)",
        "tab_bg": "rgba(0, 0, 0, 0.03)",
        "tab_selected_start": "rgba(59, 130, 246, 0.12)",
        "tab_selected_end": "rgba(59, 130, 246, 0.04)",
        "tab_hover": "rgba(0, 0, 0, 0.06)",
        "list_item_hover": "rgba(0, 0, 0, 0.04)",
        "list_item_selected": "rgba(59, 130, 246, 0.12)",
        "list_item_selected_text": "#0F172A",
        "dropdown_selection": "rgba(59, 130, 246, 0.15)",
        "scroll_handle": "rgba(0, 0, 0, 0.15)",
        "scroll_handle_hover": "rgba(0, 0, 0, 0.25)",
        "splitter_handle": "rgba(0, 0, 0, 0.05)",
        "splitter_handle_hover": "rgba(59, 130, 246, 0.40)",
        "divider_sidebar": "rgba(0, 0, 0, 0.05)",
        "divider_accent_start": "#3B82F6",
        "divider_accent_end": "#2563EB",
        "divider_line_start": "rgba(59, 130, 246, 0.35)",
        "divider_line_end": "rgba(59, 130, 246, 0.02)",
        "divider_sub_line": "rgba(0, 0, 0, 0.05)",
        "divider_desc": "rgba(59, 130, 246, 0.40)",
        "divider_desc_end": "rgba(59, 130, 246, 0.02)",
        "checkbox_border": "rgba(0, 0, 0, 0.15)",
        "checkbox_bg": "#FFFFFF",
        "checkbox_checked_start": "#3B82F6",
        "checkbox_checked_end": "#2563EB",
        "checkbox_checked_border": "rgba(59, 130, 246, 0.70)",
        "checkbox_hover_border": "rgba(59, 130, 246, 0.50)",
        "slider_groove": "rgba(0, 0, 0, 0.10)",
        "slider_handle_start": "#3B82F6",
        "slider_handle_end": "#2563EB",
        "slider_handle_border": "rgba(59, 130, 246, 0.50)",
        "slider_handle_hover_start": "#60A5FA",
        "slider_handle_hover_end": "#3B82F6",
        "separator_color": "rgba(0, 0, 0, 0.06)",
        "desc_panel_border": "rgba(0, 0, 0, 0.06)",
        "settings_desc_panel_bg": "rgba(255, 255, 255, 0.85)",
        "danger_bg": "#EF4444",
        "danger_hover": "#DC2626",
        "danger_border": "rgba(239, 68, 68, 0.50)",
        "danger_text": "#FFFFFF",
        "success_color": "#10B981",
        "warning_color": "#F59E0B",
        "shadow_color": "rgba(0, 0, 0, 0.10)",
    },
    "gray": {
        "bg_gradient_start": "#121418",
        "bg_gradient_mid": "#1C1E24",
        "bg_gradient_end": "#262930",
        "bg_window_shell": "#121418",
        "bg_shell_edge": "rgba(255, 255, 255, 0.08)",
        "bg_sidebar": "rgba(18, 20, 24, 0.85)",
        "bg_card": "rgba(32, 35, 42, 0.65)",
        "bg_card_border": "rgba(255, 255, 255, 0.08)",
        "bg_panel": "rgba(30, 33, 40, 0.60)",
        "bg_toolbar": "rgba(18, 20, 24, 0.96)",
        "bg_toolbar_border": "rgba(255, 255, 255, 0.08)",
        "bg_input": "rgba(24, 27, 32, 0.90)",
        "bg_input_focus": "rgba(32, 35, 42, 0.95)",
        "bg_text_edit": "rgba(20, 22, 27, 0.94)",
        "bg_list": "rgba(20, 22, 27, 0.80)",
        "bg_dropdown": "#1C1E24",
        "bg_header_card": "rgba(32, 35, 42, 0.65)",
        "bg_desc_panel": "rgba(26, 29, 35, 0.85)",
        "bg_scroll": "rgba(25, 29, 36, 0.78)",
        "bg_settings_input": "rgba(24, 27, 32, 0.92)",
        "bg_canvas": "#1A1C20",
        "bg_canvas_overlay": "rgba(26, 28, 32, 0.95)",
        "bg_surface_raised": "rgba(38, 42, 50, 0.96)",
        "bg_surface_soft": "rgba(32, 35, 42, 0.55)",
        "text_primary": "#E2E8F0",
        "text_secondary": "#94A3B8",
        "text_accent": "#F8FAFC",
        "text_bright": "#FFFFFF",
        "text_muted": "#64748B",
        "text_disabled": "rgba(148, 163, 184, 0.40)",
        "text_brand": "#EEF2F6",
        "text_sidebar_group": "#64748B",
        "text_card_title": "#E2E8F0",
        "text_page_title": "#F8FAFC",
        "text_page_subtitle": "#94A3B8",
        "text_row_label": "#CBD5E1",
        "text_desc_header": "#CBD5E1",
        "text_desc_name": "#F8FAFC",
        "text_desc_key": "#94A3B8",
        "text_desc_text": "#94A3B8",
        "text_settings_label": "#CBD5E1",
        "text_divider_title": "#E2E8F0",
        "text_divider_sub": "#94A3B8",
        "text_divider_dot": "#94A3B8",
        "border_input": "rgba(255, 255, 255, 0.10)",
        "border_input_focus": "rgba(148, 163, 184, 0.92)",
        "border_input_hover": "rgba(148, 163, 184, 0.50)",
        "border_card": "rgba(255, 255, 255, 0.08)",
        "border_list": "rgba(255, 255, 255, 0.08)",
        "border_sidebar": "rgba(255, 255, 255, 0.06)",
        "border_tab": "rgba(255, 255, 255, 0.08)",
        "border_tab_selected": "rgba(148, 163, 184, 0.82)",
        "border_settings_input": "rgba(255, 255, 255, 0.08)",
        "border_settings_input_hover": "rgba(148, 163, 184, 0.50)",
        "border_subtle": "rgba(255, 255, 255, 0.06)",
        "btn_soft_bg": "rgba(255, 255, 255, 0.06)",
        "btn_soft_border": "rgba(255, 255, 255, 0.08)",
        "btn_soft_hover": "rgba(255, 255, 255, 0.12)",
        "btn_soft_pressed": "rgba(255, 255, 255, 0.18)",
        "btn_soft_checked_bg": "rgba(148, 163, 184, 0.15)",
        "btn_soft_checked_border": "rgba(148, 163, 184, 0.50)",
        "btn_soft_text": "#E2E8F0",
        "btn_primary_bg": "#64748B",
        "btn_primary_hover": "#475569",
        "btn_primary_pressed": "#334155",
        "btn_primary_border": "rgba(148, 163, 184, 0.50)",
        "btn_primary_text": "#FFFFFF",
        "btn_bg": "#64748B",
        "btn_border": "rgba(148, 163, 184, 0.50)",
        "btn_hover": "#475569",
        "btn_pressed": "#334155",
        "btn_disabled_bg": "rgba(255, 255, 255, 0.04)",
        "btn_disabled_border": "rgba(255, 255, 255, 0.04)",
        "btn_checked_bg": "#64748B",
        "btn_checked_border": "rgba(148, 163, 184, 0.60)",
        "btn_chip_bg": "rgba(255, 255, 255, 0.06)",
        "btn_chip_border": "rgba(255, 255, 255, 0.08)",
        "btn_chip_hover": "rgba(255, 255, 255, 0.12)",
        "btn_settings_bg": "rgba(148, 163, 184, 0.10)",
        "btn_settings_border": "rgba(148, 163, 184, 0.30)",
        "btn_settings_hover": "rgba(148, 163, 184, 0.20)",
        "btn_settings_hover_border": "rgba(148, 163, 184, 0.50)",
        "nav_hover_bg": "rgba(255, 255, 255, 0.08)",
        "nav_hover_border": "rgba(255, 255, 255, 0.08)",
        "nav_checked_bg": "rgba(148, 163, 184, 0.15)",
        "nav_checked_border": "rgba(148, 163, 184, 0.40)",
        "cta_gradient_start": "#94A3B8",
        "cta_gradient_end": "#64748B",
        "cta_border": "rgba(148, 163, 184, 0.40)",
        "cta_text": "#FFFFFF",
        "cta_hover_start": "#64748B",
        "cta_hover_end": "#475569",
        "accent_soft": "rgba(148, 163, 184, 0.15)",
        "tab_bg": "rgba(255, 255, 255, 0.04)",
        "tab_selected_start": "rgba(148, 163, 184, 0.20)",
        "tab_selected_end": "rgba(148, 163, 184, 0.05)",
        "tab_hover": "rgba(255, 255, 255, 0.08)",
        "list_item_hover": "rgba(255, 255, 255, 0.06)",
        "list_item_selected": "rgba(148, 163, 184, 0.20)",
        "list_item_selected_text": "#FFFFFF",
        "dropdown_selection": "rgba(148, 163, 184, 0.25)",
        "scroll_handle": "rgba(255, 255, 255, 0.10)",
        "scroll_handle_hover": "rgba(255, 255, 255, 0.20)",
        "splitter_handle": "rgba(255, 255, 255, 0.06)",
        "splitter_handle_hover": "rgba(148, 163, 184, 0.40)",
        "divider_sidebar": "rgba(255, 255, 255, 0.06)",
        "divider_accent_start": "#94A3B8",
        "divider_accent_end": "#64748B",
        "divider_line_start": "rgba(148, 163, 184, 0.35)",
        "divider_line_end": "rgba(148, 163, 184, 0.02)",
        "divider_sub_line": "rgba(255, 255, 255, 0.06)",
        "divider_desc": "rgba(148, 163, 184, 0.40)",
        "divider_desc_end": "rgba(148, 163, 184, 0.02)",
        "checkbox_border": "rgba(255, 255, 255, 0.15)",
        "checkbox_bg": "rgba(24, 27, 32, 0.90)",
        "checkbox_checked_start": "#94A3B8",
        "checkbox_checked_end": "#64748B",
        "checkbox_checked_border": "rgba(148, 163, 184, 0.80)",
        "checkbox_hover_border": "rgba(148, 163, 184, 0.50)",
        "slider_groove": "rgba(255, 255, 255, 0.10)",
        "slider_handle_start": "#94A3B8",
        "slider_handle_end": "#64748B",
        "slider_handle_border": "rgba(148, 163, 184, 0.60)",
        "slider_handle_hover_start": "#CBD5E1",
        "slider_handle_hover_end": "#94A3B8",
        "separator_color": "rgba(255, 255, 255, 0.08)",
        "desc_panel_border": "rgba(255, 255, 255, 0.08)",
        "settings_desc_panel_bg": "rgba(26, 29, 35, 0.85)",
        "danger_bg": "#EF4444",
        "danger_hover": "#DC2626",
        "danger_border": "rgba(239, 68, 68, 0.50)",
        "danger_text": "#FFFFFF",
        "success_color": "#10B981",
        "warning_color": "#F59E0B",
        "shadow_color": "rgba(0, 0, 0, 0.40)",
    },
}


_THEME_TOKEN_OVERRIDES = {
    "ocean": {
        "bg_gradient_start": "#061821",
        "bg_gradient_mid": "#0B2731",
        "bg_gradient_end": "#123947",
        "bg_window_shell": "#071922",
        "bg_shell_edge": "rgba(102, 184, 196, 0.18)",
        "bg_sidebar": "rgba(5, 18, 25, 0.97)",
        "bg_card": "rgba(11, 29, 39, 0.93)",
        "bg_card_border": "rgba(102, 176, 188, 0.24)",
        "bg_panel": "rgba(12, 31, 41, 0.95)",
        "bg_toolbar": "rgba(8, 21, 29, 0.97)",
        "bg_toolbar_border": "rgba(106, 180, 192, 0.24)",
        "bg_input": "rgba(8, 22, 31, 0.94)",
        "bg_input_focus": "rgba(11, 28, 37, 0.98)",
        "bg_text_edit": "rgba(8, 22, 30, 0.95)",
        "bg_list": "rgba(7, 19, 27, 0.82)",
        "bg_dropdown": "#0B2430",
        "bg_header_card": "rgba(14, 34, 45, 0.94)",
        "bg_desc_panel": "rgba(10, 25, 34, 0.96)",
        "bg_scroll": "rgba(10, 24, 33, 0.78)",
        "bg_settings_input": "rgba(8, 22, 31, 0.96)",
        "bg_canvas": "#10232D",
        "bg_canvas_overlay": "rgba(16, 35, 45, 0.95)",
        "bg_surface_raised": "rgba(17, 39, 50, 0.97)",
        "bg_surface_soft": "rgba(13, 31, 40, 0.76)",
        "text_primary": "#D7EDF2",
        "text_secondary": "#C0D7DC",
        "text_accent": "#F1FCFE",
        "text_bright": "#F8FEFF",
        "text_muted": "#9DBBC1",
        "text_brand": "#DDF2F5",
        "text_sidebar_group": "#84A8B0",
        "text_card_title": "#CCE1E5",
        "text_page_title": "#F0FCFF",
        "text_page_subtitle": "#95BBC2",
        "text_row_label": "#C4DDE2",
        "text_desc_header": "#D4ECF0",
        "text_desc_key": "#6F949C",
        "text_desc_text": "#B7CED3",
        "text_settings_label": "#BFD8DC",
        "text_divider_title": "#D7EEF2",
        "text_divider_sub": "#98BDC3",
        "border_input": "rgba(110, 146, 156, 0.48)",
        "border_input_hover": "rgba(126, 173, 183, 0.60)",
        "border_card": "rgba(102, 176, 188, 0.24)",
        "border_list": "rgba(103, 146, 156, 0.34)",
        "border_sidebar": "rgba(108, 151, 161, 0.20)",
        "border_tab": "rgba(81, 123, 133, 0.36)",
        "border_settings_input": "rgba(92, 134, 143, 0.40)",
        "border_settings_input_hover": "rgba(122, 169, 178, 0.58)",
        "border_subtle": "rgba(123, 162, 171, 0.14)",
        "btn_soft_bg": "rgba(21, 47, 58, 0.48)",
        "btn_soft_border": "rgba(104, 149, 159, 0.44)",
        "btn_soft_hover": "rgba(29, 59, 71, 0.70)",
        "btn_soft_pressed": "rgba(36, 72, 85, 0.86)",
        "btn_chip_bg": "rgba(20, 44, 55, 0.86)",
        "btn_chip_border": "rgba(89, 132, 142, 0.48)",
        "btn_chip_hover": "rgba(32, 61, 73, 0.96)",
        "tab_bg": "rgba(19, 42, 53, 0.84)",
        "scroll_handle": "rgba(108, 141, 149, 0.48)",
        "scroll_handle_hover": "rgba(130, 169, 179, 0.68)",
        "splitter_handle": "rgba(121, 155, 164, 0.20)",
        "divider_sidebar": "rgba(119, 162, 172, 0.26)",
        "divider_sub_line": "rgba(131, 168, 177, 0.18)",
        "checkbox_border": "rgba(97, 139, 148, 0.58)",
        "checkbox_bg": "rgba(8, 22, 31, 0.96)",
        "slider_groove": "rgba(53, 85, 94, 0.54)",
        "separator_color": "rgba(121, 155, 164, 0.32)",
        "desc_panel_border": "rgba(102, 176, 188, 0.26)",
        "settings_desc_panel_bg": "rgba(10, 25, 34, 0.96)",
    },
    "forest": {
        "bg_gradient_start": "#1B2319",
        "bg_gradient_mid": "#263024",
        "bg_gradient_end": "#334034",
        "bg_window_shell": "#1C241A",
        "bg_shell_edge": "rgba(126, 167, 117, 0.20)",
        "bg_sidebar": "rgba(27, 34, 28, 0.98)",
        "bg_card": "rgba(36, 46, 38, 0.95)",
        "bg_card_border": "rgba(108, 144, 102, 0.30)",
        "bg_panel": "rgba(37, 47, 39, 0.96)",
        "bg_toolbar": "rgba(30, 39, 31, 0.98)",
        "bg_toolbar_border": "rgba(110, 144, 103, 0.28)",
        "bg_input": "rgba(42, 52, 43, 0.95)",
        "bg_input_focus": "rgba(47, 58, 48, 0.98)",
        "bg_text_edit": "rgba(40, 51, 42, 0.96)",
        "bg_list": "rgba(31, 40, 33, 0.92)",
        "bg_dropdown": "#2C362E",
        "bg_header_card": "rgba(37, 48, 39, 0.96)",
        "bg_desc_panel": "rgba(34, 45, 36, 0.98)",
        "bg_scroll": "rgba(48, 60, 49, 0.80)",
        "bg_settings_input": "rgba(41, 51, 42, 0.96)",
        "bg_canvas": "#19221B",
        "bg_canvas_overlay": "rgba(25, 34, 27, 0.96)",
        "bg_surface_raised": "rgba(41, 52, 43, 1.0)",
        "bg_surface_soft": "rgba(35, 45, 37, 0.80)",
        "text_primary": "#E2E9DF",
        "text_secondary": "#D0D8CC",
        "text_accent": "#F6FAF4",
        "text_bright": "#FFFFFF",
        "text_muted": "#AEB9A8",
        "text_brand": "#E7EEE4",
        "text_sidebar_group": "#9BA995",
        "text_card_title": "#D7E0D3",
        "text_page_title": "#F3F7F0",
        "text_page_subtitle": "#A5B29F",
        "text_row_label": "#D0D9CC",
        "text_desc_header": "#E1E9DE",
        "text_desc_key": "#91A18A",
        "text_desc_text": "#C7D0C3",
        "text_settings_label": "#CDD6CA",
        "text_divider_title": "#E1E9DE",
        "text_divider_sub": "#A6B39F",
        "border_input": "rgba(114, 126, 108, 0.54)",
        "border_input_hover": "rgba(130, 145, 124, 0.60)",
        "border_card": "rgba(105, 119, 100, 0.34)",
        "border_list": "rgba(109, 123, 104, 0.40)",
        "border_sidebar": "rgba(99, 112, 94, 0.28)",
        "border_tab": "rgba(100, 113, 95, 0.34)",
        "border_settings_input": "rgba(106, 119, 101, 0.44)",
        "border_settings_input_hover": "rgba(128, 144, 122, 0.58)",
        "border_subtle": "rgba(123, 137, 118, 0.14)",
        "btn_soft_bg": "rgba(57, 68, 58, 0.56)",
        "btn_soft_border": "rgba(127, 140, 122, 0.46)",
        "btn_soft_hover": "rgba(70, 82, 72, 0.80)",
        "btn_soft_pressed": "rgba(82, 96, 84, 0.94)",
        "btn_chip_bg": "rgba(54, 65, 55, 0.88)",
        "btn_chip_border": "rgba(107, 120, 101, 0.42)",
        "btn_chip_hover": "rgba(67, 79, 68, 0.96)",
        "tab_bg": "rgba(52, 61, 53, 0.88)",
        "scroll_handle": "rgba(129, 141, 124, 0.48)",
        "scroll_handle_hover": "rgba(151, 166, 145, 0.66)",
        "splitter_handle": "rgba(121, 133, 116, 0.24)",
        "divider_sidebar": "rgba(111, 123, 106, 0.30)",
        "divider_sub_line": "rgba(117, 129, 112, 0.18)",
        "checkbox_border": "rgba(113, 126, 107, 0.56)",
        "checkbox_bg": "rgba(40, 50, 41, 0.96)",
        "slider_groove": "rgba(90, 100, 85, 0.52)",
        "separator_color": "rgba(115, 127, 110, 0.36)",
        "desc_panel_border": "rgba(100, 112, 95, 0.34)",
        "settings_desc_panel_bg": "rgba(34, 45, 36, 0.98)",
    },
    "sunset": {
        "bg_gradient_start": "#2A1E1A",
        "bg_gradient_mid": "#372621",
        "bg_gradient_end": "#48312B",
        "bg_window_shell": "#2B1F1B",
        "bg_shell_edge": "rgba(199, 151, 109, 0.22)",
        "bg_sidebar": "rgba(37, 27, 24, 0.98)",
        "bg_card": "rgba(49, 35, 31, 0.95)",
        "bg_card_border": "rgba(148, 111, 88, 0.32)",
        "bg_panel": "rgba(47, 34, 30, 0.96)",
        "bg_toolbar": "rgba(39, 29, 25, 0.98)",
        "bg_toolbar_border": "rgba(147, 110, 88, 0.30)",
        "bg_input": "rgba(53, 39, 34, 0.95)",
        "bg_input_focus": "rgba(59, 43, 38, 0.98)",
        "bg_text_edit": "rgba(51, 37, 32, 0.96)",
        "bg_list": "rgba(40, 29, 25, 0.92)",
        "bg_dropdown": "#3A2A25",
        "bg_header_card": "rgba(49, 35, 31, 0.96)",
        "bg_desc_panel": "rgba(45, 33, 28, 0.98)",
        "bg_scroll": "rgba(60, 45, 39, 0.80)",
        "bg_settings_input": "rgba(52, 38, 33, 0.96)",
        "bg_canvas": "#251A17",
        "bg_canvas_overlay": "rgba(37, 26, 23, 0.96)",
        "bg_surface_raised": "rgba(52, 38, 33, 1.0)",
        "bg_surface_soft": "rgba(45, 32, 28, 0.80)",
        "text_primary": "#F0E1D8",
        "text_secondary": "#E0CBBE",
        "text_accent": "#FFF8F2",
        "text_bright": "#FFFFFF",
        "text_muted": "#C2A99A",
        "text_brand": "#F5E7DE",
        "text_sidebar_group": "#C29B86",
        "text_card_title": "#E9D5C8",
        "text_page_title": "#FFF6F0",
        "text_page_subtitle": "#C89F88",
        "text_row_label": "#E5D1C4",
        "text_desc_header": "#F2E3DA",
        "text_desc_key": "#B88E7B",
        "text_desc_text": "#D8C1B5",
        "text_settings_label": "#DEC8BB",
        "text_divider_title": "#F2E3DA",
        "text_divider_sub": "#C7A08B",
        "border_input": "rgba(145, 116, 98, 0.54)",
        "border_input_hover": "rgba(165, 133, 112, 0.60)",
        "border_card": "rgba(138, 102, 84, 0.34)",
        "border_list": "rgba(142, 104, 86, 0.40)",
        "border_sidebar": "rgba(130, 96, 79, 0.28)",
        "border_tab": "rgba(131, 97, 80, 0.34)",
        "border_settings_input": "rgba(137, 101, 84, 0.44)",
        "border_settings_input_hover": "rgba(161, 128, 108, 0.58)",
        "border_subtle": "rgba(154, 120, 101, 0.14)",
        "btn_soft_bg": "rgba(63, 45, 40, 0.56)",
        "btn_soft_border": "rgba(158, 122, 102, 0.46)",
        "btn_soft_hover": "rgba(78, 57, 50, 0.80)",
        "btn_soft_pressed": "rgba(92, 67, 59, 0.94)",
        "btn_chip_bg": "rgba(60, 43, 38, 0.88)",
        "btn_chip_border": "rgba(136, 101, 84, 0.42)",
        "btn_chip_hover": "rgba(75, 54, 47, 0.96)",
        "tab_bg": "rgba(58, 42, 37, 0.88)",
        "scroll_handle": "rgba(158, 125, 106, 0.48)",
        "scroll_handle_hover": "rgba(184, 148, 127, 0.66)",
        "splitter_handle": "rgba(140, 109, 92, 0.24)",
        "divider_sidebar": "rgba(135, 103, 86, 0.30)",
        "divider_sub_line": "rgba(140, 108, 91, 0.18)",
        "checkbox_border": "rgba(139, 106, 89, 0.56)",
        "checkbox_bg": "rgba(51, 37, 32, 0.96)",
        "slider_groove": "rgba(114, 86, 73, 0.52)",
        "separator_color": "rgba(138, 106, 89, 0.36)",
        "desc_panel_border": "rgba(132, 98, 82, 0.34)",
        "settings_desc_panel_bg": "rgba(45, 33, 28, 0.98)",
    },
    "rose": {
        "bg_gradient_start": "#180D15",
        "bg_gradient_mid": "#24101E",
        "bg_gradient_end": "#361A2B",
        "bg_window_shell": "#190D16",
        "bg_shell_edge": "rgba(214, 137, 169, 0.18)",
        "bg_sidebar": "rgba(21, 10, 19, 0.97)",
        "bg_card": "rgba(37, 17, 30, 0.94)",
        "bg_card_border": "rgba(191, 114, 145, 0.22)",
        "bg_panel": "rgba(38, 18, 31, 0.95)",
        "bg_toolbar": "rgba(27, 12, 22, 0.97)",
        "bg_toolbar_border": "rgba(193, 118, 149, 0.22)",
        "bg_input": "rgba(30, 14, 24, 0.94)",
        "bg_input_focus": "rgba(37, 17, 30, 0.98)",
        "bg_text_edit": "rgba(29, 13, 23, 0.95)",
        "bg_list": "rgba(25, 11, 21, 0.84)",
        "bg_dropdown": "#2C1424",
        "bg_header_card": "rgba(42, 19, 34, 0.94)",
        "bg_desc_panel": "rgba(32, 15, 27, 0.96)",
        "bg_scroll": "rgba(33, 15, 27, 0.78)",
        "bg_settings_input": "rgba(30, 14, 24, 0.96)",
        "bg_canvas": "#21111B",
        "bg_canvas_overlay": "rgba(33, 17, 27, 0.95)",
        "bg_surface_raised": "rgba(45, 22, 37, 0.97)",
        "bg_surface_soft": "rgba(36, 17, 30, 0.76)",
        "text_primary": "#F0DDE7",
        "text_secondary": "#DEC5D2",
        "text_accent": "#FFF4F8",
        "text_bright": "#FFFFFF",
        "text_muted": "#C3A3B2",
        "text_brand": "#F7E5EE",
        "text_sidebar_group": "#C090A7",
        "text_card_title": "#EACFDC",
        "text_page_title": "#FFF4F9",
        "text_page_subtitle": "#CD9FB6",
        "text_row_label": "#E6CDD9",
        "text_desc_header": "#F2DEE8",
        "text_desc_key": "#B6839A",
        "text_desc_text": "#D7BCC9",
        "text_settings_label": "#E0C7D3",
        "text_divider_title": "#F2DEE8",
        "text_divider_sub": "#CAA0B3",
        "border_input": "rgba(156, 119, 136, 0.48)",
        "border_input_hover": "rgba(185, 141, 160, 0.60)",
        "border_card": "rgba(184, 116, 143, 0.24)",
        "border_list": "rgba(148, 108, 126, 0.34)",
        "border_sidebar": "rgba(162, 117, 136, 0.20)",
        "border_tab": "rgba(124, 84, 104, 0.36)",
        "border_settings_input": "rgba(138, 98, 117, 0.40)",
        "border_settings_input_hover": "rgba(180, 138, 157, 0.58)",
        "border_subtle": "rgba(168, 122, 141, 0.14)",
        "btn_soft_bg": "rgba(55, 27, 44, 0.50)",
        "btn_soft_border": "rgba(150, 109, 128, 0.44)",
        "btn_soft_hover": "rgba(70, 37, 56, 0.72)",
        "btn_soft_pressed": "rgba(83, 47, 68, 0.88)",
        "btn_chip_bg": "rgba(51, 25, 41, 0.86)",
        "btn_chip_border": "rgba(136, 95, 115, 0.48)",
        "btn_chip_hover": "rgba(67, 37, 54, 0.96)",
        "tab_bg": "rgba(49, 25, 40, 0.86)",
        "scroll_handle": "rgba(149, 112, 129, 0.48)",
        "scroll_handle_hover": "rgba(178, 139, 157, 0.68)",
        "splitter_handle": "rgba(165, 124, 143, 0.20)",
        "divider_sidebar": "rgba(178, 136, 156, 0.24)",
        "divider_sub_line": "rgba(171, 129, 149, 0.18)",
        "checkbox_border": "rgba(143, 104, 122, 0.58)",
        "checkbox_bg": "rgba(30, 14, 24, 0.96)",
        "slider_groove": "rgba(93, 60, 77, 0.54)",
        "separator_color": "rgba(163, 121, 140, 0.32)",
        "desc_panel_border": "rgba(184, 116, 143, 0.26)",
        "settings_desc_panel_bg": "rgba(32, 15, 27, 0.96)",
    },
}


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise ValueError(f"Unsupported hex color: {value}")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def _mix_hex(source: str, target: str, amount: float) -> str:
    source_rgb = _hex_to_rgb(source)
    target_rgb = _hex_to_rgb(target)
    mixed = tuple(
        max(0, min(255, round(src + (dst - src) * amount)))
        for src, dst in zip(source_rgb, target_rgb)
    )
    return _rgb_to_hex(mixed)


def _lighten(color: str, amount: float) -> str:
    return _mix_hex(color, "#FFFFFF", amount)


def _darken(color: str, amount: float) -> str:
    return _mix_hex(color, "#000000", amount)


def _rgba(color: str, alpha: float) -> str:
    red, green, blue = _hex_to_rgb(color)
    return f"rgba({red}, {green}, {blue}, {alpha:.2f})"


def _build_accent_overrides(accent: str, *, dark_theme: bool) -> dict:
    base = _ACCENT_BASES[accent]

    strong = _lighten(base, 0.16 if dark_theme else 0.04)
    soft = _lighten(base, 0.08 if dark_theme else 0.18)
    deep = _darken(base, 0.22 if dark_theme else 0.16)
    deeper = _darken(base, 0.32 if dark_theme else 0.24)

    return {
        "text_divider_dot": strong,
        "border_input_focus": _rgba(base, 0.92 if dark_theme else 0.80),
        "border_tab_selected": _rgba(strong, 0.76 if dark_theme else 0.70),
        "btn_soft_checked_bg": _rgba(base, 0.30 if dark_theme else 0.18),
        "btn_soft_checked_border": _rgba(strong, 0.76 if dark_theme else 0.78),
        "btn_primary_bg": _rgba(base, 0.30 if dark_theme else 0.18),
        "btn_primary_hover": _rgba(soft, 0.42 if dark_theme else 0.28),
        "btn_primary_pressed": _rgba(deep, 0.58 if dark_theme else 0.36),
        "btn_primary_border": _rgba(strong, 0.74 if dark_theme else 0.62),
        "btn_bg": _rgba(base, 0.94 if dark_theme else 0.92),
        "btn_border": _rgba(strong, 0.60 if dark_theme else 0.48),
        "btn_hover": _rgba(soft, 0.98 if dark_theme else 0.96),
        "btn_pressed": _rgba(deeper, 0.98 if dark_theme else 0.98),
        "btn_checked_bg": _rgba(deep, 0.90 if dark_theme else 0.92),
        "btn_checked_border": _rgba(strong, 0.78 if dark_theme else 0.78),
        "btn_settings_bg": _rgba(base, 0.22 if dark_theme else 0.14),
        "btn_settings_border": _rgba(strong, 0.42 if dark_theme else 0.30),
        "btn_settings_hover": _rgba(soft, 0.34 if dark_theme else 0.24),
        "btn_settings_hover_border": _rgba(strong, 0.62 if dark_theme else 0.48),
        "nav_hover_bg": _rgba(base, 0.28 if dark_theme else 0.10),
        "nav_hover_border": _rgba(strong, 0.38 if dark_theme else 0.24),
        "nav_checked_bg": _rgba(base, 0.42 if dark_theme else 0.16),
        "nav_checked_border": _rgba(strong, 0.82 if dark_theme else 0.58),
        "cta_gradient_start": strong,
        "cta_gradient_end": soft,
        "cta_border": _rgba(_lighten(base, 0.34), 0.90 if dark_theme else 0.82),
        "cta_hover_start": _lighten(base, 0.24 if dark_theme else 0.14),
        "cta_hover_end": _lighten(base, 0.34 if dark_theme else 0.24),
        "accent_soft": _rgba(base, 0.20 if dark_theme else 0.14),
        "tab_selected_start": _rgba(strong, 0.88 if dark_theme else 0.16),
        "tab_selected_end": _rgba(deep, 0.84 if dark_theme else 0.08),
        "tab_hover": _rgba(base, 0.24 if dark_theme else 0.12),
        "list_item_hover": _rgba(base, 0.26 if dark_theme else 0.08),
        "list_item_selected": _rgba(soft, 0.46 if dark_theme else 0.18),
        "dropdown_selection": _rgba(soft, 0.42 if dark_theme else 0.18),
        "splitter_handle_hover": _rgba(strong, 0.46 if dark_theme else 0.46),
        "divider_accent_start": strong,
        "divider_accent_end": deep,
        "divider_line_start": _rgba(strong, 0.34 if dark_theme else 0.36),
        "divider_line_end": _rgba(strong, 0.05),
        "divider_desc": _rgba(strong, 0.40 if dark_theme else 0.40),
        "divider_desc_end": _rgba(strong, 0.05),
        "checkbox_checked_start": strong,
        "checkbox_checked_end": deep,
        "checkbox_checked_border": _rgba(_lighten(base, 0.28), 0.82 if dark_theme else 0.72),
        "checkbox_hover_border": _rgba(strong, 0.66 if dark_theme else 0.52),
        "slider_handle_start": strong,
        "slider_handle_end": deep,
        "slider_handle_border": _rgba(_lighten(base, 0.28), 0.64 if dark_theme else 0.50),
        "slider_handle_hover_start": _lighten(base, 0.26 if dark_theme else 0.18),
        "slider_handle_hover_end": _lighten(base, 0.12 if dark_theme else 0.06),
    }

_VALID_THEMES = set(AVAILABLE_THEMES)
_CURRENT_THEME = "light"


def _to_qcolor(value: str) -> QColor:
    """Parse Qt-safe colors, including CSS-like rgb()/rgba() strings."""
    color = QColor(value)
    if color.isValid():
        return color

    normalized = value.strip().lower()
    if normalized.startswith("rgba(") and normalized.endswith(")"):
        parts = [part.strip() for part in normalized[5:-1].split(",")]
        if len(parts) == 4:
            red = int(float(parts[0]))
            green = int(float(parts[1]))
            blue = int(float(parts[2]))
            alpha_raw = float(parts[3])
            alpha = int(round(alpha_raw * 255)) if alpha_raw <= 1 else int(round(alpha_raw))
            return QColor(red, green, blue, max(0, min(255, alpha)))

    if normalized.startswith("rgb(") and normalized.endswith(")"):
        parts = [part.strip() for part in normalized[4:-1].split(",")]
        if len(parts) == 3:
            red = int(float(parts[0]))
            green = int(float(parts[1]))
            blue = int(float(parts[2]))
            return QColor(red, green, blue)

    return QColor("#000000")


def set_current_theme(theme: str) -> None:
    global _CURRENT_THEME
    normalized_theme = normalize_theme(theme)
    _CURRENT_THEME = normalized_theme if normalized_theme in _VALID_THEMES else "light"

def get_current_theme() -> str:
    return _CURRENT_THEME


def get_current_theme_colors() -> dict:
    return get_theme_colors(_CURRENT_THEME)


def is_dark_theme(theme: str | None = None) -> bool:
    active_theme = normalize_theme(theme or _CURRENT_THEME)
    return active_theme in DARK_THEMES


def build_tooltip_stylesheet(colors: dict) -> str:
    return f"""
        QToolTip {{
            background-color: {colors["bg_dropdown"]};
            color: {colors["text_accent"]};
            border: 1px solid {colors["border_input"]};
            border-radius: 10px;
            padding: 8px 12px;
            font-size: 12px;
            font-weight: 500;
        }}
    """


def build_shared_button_stylesheet(colors: dict) -> str:
    return f"""
        QPushButton,
        QToolButton {{
            background: {colors["btn_soft_bg"]};
            border: 1px solid {colors["btn_soft_border"]};
            border-radius: 10px;
            color: {colors["btn_soft_text"]};
            padding: 7px 12px;
            font-weight: 500;
        }}
        QPushButton:hover,
        QToolButton:hover {{
            background: {colors["btn_soft_hover"]};
            border-color: {colors["border_input_hover"]};
        }}
        QPushButton:pressed,
        QToolButton:pressed {{
            background: {colors["btn_soft_pressed"]};
            border-color: {colors["btn_soft_checked_border"]};
        }}
        QPushButton:disabled,
        QToolButton:disabled {{
            background: {colors["btn_disabled_bg"]};
            border-color: {colors["btn_disabled_border"]};
            color: {colors["text_disabled"]};
        }}
        QPushButton:checked,
        QToolButton:checked {{
            background: {colors["btn_soft_checked_bg"]};
            border-color: {colors["btn_soft_checked_border"]};
            color: {colors["btn_soft_text"]};
        }}

        QPushButton[chipButton="true"],
        QToolButton[chipButton="true"] {{
            background: {colors["btn_soft_bg"]};
            border: 1px solid {colors["btn_soft_border"]};
            color: {colors["btn_soft_text"]};
            padding: 6px 10px;
            font-weight: 500;
        }}
        QPushButton[chipButton="true"]:hover,
        QToolButton[chipButton="true"]:hover {{
            background: {colors["btn_soft_hover"]};
            border-color: {colors["border_input_hover"]};
            color: {colors["btn_soft_text"]};
        }}

        QPushButton[variant="accent"],
        QToolButton[variant="accent"] {{
            background: {colors["btn_primary_bg"]};
            border: 1px solid {colors["btn_primary_border"]};
            color: {colors["btn_primary_text"]};
            border-radius: 10px;
            font-weight: 600;
        }}
        QPushButton[variant="accent"]:hover,
        QToolButton[variant="accent"]:hover {{
            background: {colors["btn_primary_hover"]};
        }}
        QPushButton[variant="accent"]:pressed,
        QToolButton[variant="accent"]:pressed {{
            background: {colors["btn_primary_pressed"]};
        }}

        QPushButton[variant="danger"],
        QToolButton[variant="danger"] {{
            background: {colors["danger_bg"]};
            border: 1px solid {colors["danger_border"]};
            color: {colors["danger_text"]};
            font-weight: 500;
        }}
        QPushButton[variant="danger"]:hover,
        QToolButton[variant="danger"]:hover {{
            background: {colors["danger_hover"]};
        }}
    """


def build_section_icon_button_stylesheet(colors: dict) -> str:
    return f"""
        QPushButton[sectionIconButton="true"],
        QToolButton[sectionIconButton="true"] {{
            min-width: 28px;
            max-width: 28px;
            min-height: 24px;
            max-height: 24px;
            padding: 0px;
            border: none;
            border-radius: 6px;
            background: transparent;
            color: {colors["text_muted"]};
            font-size: 14px;
            font-weight: 700;
        }}
        QPushButton[sectionIconButton="true"]:hover,
        QToolButton[sectionIconButton="true"]:hover {{
            background: {colors["btn_soft_hover"]};
            color: {colors["text_bright"]};
        }}
        QPushButton[sectionIconButton="true"]:pressed,
        QToolButton[sectionIconButton="true"]:pressed {{
            background: {colors["btn_soft_pressed"]};
            color: {colors["text_bright"]};
        }}
        QPushButton[sectionIconButton="true"]:disabled,
        QToolButton[sectionIconButton="true"]:disabled {{
            background: transparent;
            color: {colors["text_disabled"]};
        }}
        QPushButton[sectionIconButton="true"][variant="danger"],
        QToolButton[sectionIconButton="true"][variant="danger"] {{
            background: transparent;
            color: {colors["danger_bg"]};
        }}
        QPushButton[sectionIconButton="true"][variant="danger"]:hover,
        QToolButton[sectionIconButton="true"][variant="danger"]:hover {{
            background: {colors["danger_hover"]};
            color: {colors["danger_text"]};
        }}
        QPushButton[sectionIconButton="true"][variant="danger"]:pressed,
        QToolButton[sectionIconButton="true"][variant="danger"]:pressed {{
            background: {colors["danger_bg"]};
            color: {colors["danger_text"]};
        }}
        QPushButton[sectionIconButton="true"][variant="danger"]:disabled,
        QToolButton[sectionIconButton="true"][variant="danger"]:disabled {{
            background: transparent;
            color: {colors["text_disabled"]};
        }}
    """


def build_theme_palette(theme: str) -> QPalette:
    c = get_theme_colors(theme)
    palette = QPalette()

    active_roles = {
        QPalette.ColorRole.Window: c["bg_window_shell"],
        QPalette.ColorRole.WindowText: c["text_primary"],
        QPalette.ColorRole.Base: c["bg_input"],
        QPalette.ColorRole.AlternateBase: c["bg_surface_soft"],
        QPalette.ColorRole.ToolTipBase: c["bg_dropdown"],
        QPalette.ColorRole.ToolTipText: c["text_accent"],
        QPalette.ColorRole.Text: c["text_primary"],
        QPalette.ColorRole.Button: c["bg_surface_raised"],
        QPalette.ColorRole.ButtonText: c["text_accent"],
        QPalette.ColorRole.BrightText: c["text_bright"],
        QPalette.ColorRole.Light: c["bg_gradient_end"],
        QPalette.ColorRole.Midlight: c["border_input_hover"],
        QPalette.ColorRole.Dark: c["bg_gradient_start"],
        QPalette.ColorRole.Mid: c["border_list"],
        QPalette.ColorRole.Shadow: c["bg_gradient_start"],
        QPalette.ColorRole.Highlight: c["cta_gradient_start"],
        QPalette.ColorRole.HighlightedText: c["cta_text"],
        QPalette.ColorRole.Link: c["divider_accent_start"],
        QPalette.ColorRole.LinkVisited: c["divider_accent_end"],
        QPalette.ColorRole.PlaceholderText: c["text_muted"],
    }

    for group in (QPalette.ColorGroup.Active, QPalette.ColorGroup.Inactive):
        for role, value in active_roles.items():
            palette.setColor(group, role, _to_qcolor(value))

    disabled_roles = {
        QPalette.ColorRole.WindowText: c["text_disabled"],
        QPalette.ColorRole.Text: c["text_disabled"],
        QPalette.ColorRole.ButtonText: c["text_disabled"],
        QPalette.ColorRole.PlaceholderText: c["text_disabled"],
        QPalette.ColorRole.Button: c["btn_disabled_bg"],
        QPalette.ColorRole.Base: c["bg_input"],
        QPalette.ColorRole.Highlight: c["btn_disabled_border"],
        QPalette.ColorRole.HighlightedText: c["text_muted"],
    }
    for role, value in disabled_roles.items():
        palette.setColor(QPalette.ColorGroup.Disabled, role, _to_qcolor(value))

    accent_role = getattr(QPalette.ColorRole, "Accent", None)
    if accent_role is not None:
        for group in (QPalette.ColorGroup.Active, QPalette.ColorGroup.Inactive):
            palette.setColor(group, accent_role, _to_qcolor(c["cta_gradient_start"]))
        palette.setColor(QPalette.ColorGroup.Disabled, accent_role, _to_qcolor(c["btn_disabled_border"]))

    return palette


def generate_application_stylesheet(theme: str) -> str:
    c = get_theme_colors(theme)
    return f"""
        QMainWindow, QDialog {{
            background: {c["bg_window_shell"]};
        }}
        QWidget {{
            font-family: "Microsoft YaHei UI", "Segoe UI", sans-serif;
            font-size: 12px;
            color: {c["text_primary"]};
        }}
        QWidget:disabled {{
            color: {c["text_disabled"]};
        }}

        {build_tooltip_stylesheet(c)}

        QMenu {{
            background: {c["bg_dropdown"]};
            background-color: {c["bg_dropdown"]};
            color: {c["text_accent"]};
            border: 1px solid {c["border_card"]};
            border-radius: 10px;
            padding: 6px 4px;
        }}
        QMenu::item {{
            background: transparent;
            background-color: transparent;
            padding: 7px 16px;
            margin: 1px 4px;
            border-radius: 6px;
        }}
        QMenu::item:selected {{
            background: {c["tab_hover"]};
            background-color: {c["tab_hover"]};
            color: {c["text_bright"]};
        }}
        QMenu::separator {{
            height: 1px;
            margin: 5px 10px;
            background: {c["divider_sub_line"]};
        }}

        QGroupBox {{
            background: {c["bg_card"]};
            border: 1px solid {c["border_subtle"]};
            border-radius: 16px;
            margin-top: 12px;
            padding: 12px;
            font-weight: 500;
            color: {c["text_card_title"]};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            margin-left: 10px;
            padding: 0 8px;
            background: transparent;
            color: {c["text_card_title"]};
        }}

        QProgressDialog {{
            background: {c["bg_panel"]};
            border: 1px solid {c["border_card"]};
            border-radius: 14px;
        }}
        QProgressDialog QLabel {{
            background: transparent;
            color: {c["text_page_title"]};
            font-size: 13px;
            font-weight: 600;
            min-width: 280px;
        }}
        QProgressDialog QProgressBar {{
            background: {c["bg_surface_soft"]};
            border: 1px solid {c["border_input"]};
            border-radius: 8px;
            min-height: 12px;
            text-align: center;
            color: {c["text_secondary"]};
        }}
        QProgressDialog QProgressBar::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 {c["btn_primary_bg"]}, stop:1 {c["btn_primary_hover"]});
            border-radius: 7px;
        }}
        QProgressDialog QPushButton {{
            background: {c["btn_soft_bg"]};
            border: 1px solid {c["btn_soft_border"]};
            border-radius: 10px;
            color: {c["btn_soft_text"]};
            padding: 6px 12px;
            font-weight: 500;
            min-width: 88px;
            min-height: 32px;
        }}
        QProgressDialog QPushButton:hover {{
            background: {c["btn_soft_hover"]};
            border-color: {c["border_input_hover"]};
        }}
        QProgressDialog QPushButton:pressed {{
            background: {c["btn_soft_pressed"]};
        }}

        QInputDialog {{
            background: {c["bg_panel"]};
            border: 1px solid {c["border_card"]};
            border-radius: 14px;
        }}
        QInputDialog QLabel {{
            background: transparent;
            color: {c["text_page_title"]};
            font-size: 13px;
            font-weight: 600;
            min-width: 280px;
        }}
        QInputDialog QLineEdit {{
            min-height: 24px;
            padding: 8px 10px;
        }}
        QInputDialog QPushButton {{
            min-width: 88px;
            min-height: 32px;
        }}
        QInputDialog QPushButton:default {{
            background: {c["btn_primary_bg"]};
            border-color: {c["btn_primary_border"]};
            color: {c["btn_primary_text"]};
        }}
        QInputDialog QPushButton:default:hover {{
            background: {c["btn_primary_hover"]};
        }}
        QInputDialog QPushButton:default:pressed {{
            background: {c["btn_primary_pressed"]};
        }}

        QDialog#errorDialog,
        QMessageBox#themedMessageBox {{
            background: {c["bg_panel"]};
            border: 1px solid {c["border_input"]};
            border-radius: 14px;
        }}
        QDialog#errorDialog QLabel,
        QMessageBox#themedMessageBox QLabel {{
            background: transparent;
            color: {c["text_primary"]};
            font-family: "Microsoft YaHei UI", "Segoe UI", sans-serif;
            font-size: 12px;
        }}
        QDialog#errorDialog QLabel#errorDialogTitle,
        QMessageBox#themedMessageBox QLabel#qt_msgbox_label {{
            color: {c["text_primary"]};
            font-size: 13px;
            font-weight: 600;
        }}
        QMessageBox#themedMessageBox QLabel#qt_msgbox_informativelabel {{
            color: {c["text_primary"]};
            font-size: 12px;
        }}
        QDialog#errorDialog QWidget#dialogHeader {{
            background: transparent;
        }}
        QDialog#errorDialog QLabel#dialogWindowTitle {{
            color: {c["text_primary"]};
            font-size: 12px;
            font-weight: 600;
        }}
        QDialog#errorDialog QLabel#dialogIcon {{
            background: transparent;
        }}
        QDialog#errorDialog QToolButton#dialogCloseButton {{
            background: transparent;
            border: none;
            border-radius: 8px;
            color: {c["text_muted"]};
            font-size: 16px;
            font-weight: 600;
            min-width: 28px;
            min-height: 28px;
            padding: 0;
        }}
        QDialog#errorDialog QToolButton#dialogCloseButton:hover {{
            background: {c["btn_soft_bg"]};
            color: {c["text_primary"]};
        }}
        QDialog#errorDialog QToolButton#dialogCloseButton:pressed {{
            background: {c["btn_soft_pressed"]};
        }}
        QDialog#errorDialog QScrollArea#errorDialogScroll {{
            background: transparent;
            border: none;
        }}
        QDialog#errorDialog QScrollArea#errorDialogScroll > QWidget > QWidget {{
            background: transparent;
        }}
        QDialog#errorDialog QLabel#errorDialogDetails {{
            background: transparent;
            color: {c["text_primary"]};
            border: none;
            font-family: "Microsoft YaHei UI", "Segoe UI", sans-serif;
            font-size: 12px;
            padding: 0;
        }}
        QDialog#errorDialog QDialogButtonBox QPushButton,
        QMessageBox#themedMessageBox QPushButton {{
            min-width: 88px;
            min-height: 34px;
            border-radius: 8px;
            padding: 6px 14px;
            font-size: 12px;
            font-weight: 500;
            background: {c["btn_soft_bg"]};
            border: 1px solid {c["btn_soft_border"]};
            color: {c["btn_soft_text"]};
        }}
        QDialog#errorDialog QDialogButtonBox QPushButton:hover,
        QMessageBox#themedMessageBox QPushButton:hover {{
            background: {c["btn_soft_hover"]};
            border-color: {c["border_input_focus"]};
        }}
        QDialog#errorDialog QDialogButtonBox QPushButton:pressed,
        QMessageBox#themedMessageBox QPushButton:pressed {{
            background: {c["btn_soft_pressed"]};
        }}
        QDialog#errorDialog QDialogButtonBox QPushButton[dialogDefault="true"],
        QMessageBox#themedMessageBox QPushButton[dialogDefault="true"] {{
            background: {c["btn_primary_bg"]};
            border: 1px solid {c["btn_primary_border"]};
            color: {c["btn_primary_text"]};
        }}
        QDialog#errorDialog QDialogButtonBox QPushButton[dialogDefault="true"]:hover,
        QMessageBox#themedMessageBox QPushButton[dialogDefault="true"]:hover {{
            background: {c["btn_primary_hover"]};
        }}
        QDialog#errorDialog QDialogButtonBox QPushButton[dialogDefault="true"]:pressed,
        QMessageBox#themedMessageBox QPushButton[dialogDefault="true"]:pressed {{
            background: {c["btn_primary_pressed"]};
        }}

        QLineEdit,
        QTextEdit,
        QPlainTextEdit,
        QComboBox,
        QSpinBox,
        QDoubleSpinBox {{
            background: {c["bg_input"]};
            border: 1px solid {c["border_input"]};
            border-radius: 8px;
            color: {c["text_accent"]};
            padding: 7px 10px;
            selection-background-color: {c["dropdown_selection"]};
            selection-color: {c["list_item_selected_text"]};
        }}
        QLineEdit:hover,
        QTextEdit:hover,
        QPlainTextEdit:hover,
        QComboBox:hover,
        QSpinBox:hover,
        QDoubleSpinBox:hover {{
            border-color: {c["border_input_hover"]};
        }}
        QLineEdit:focus,
        QTextEdit:focus,
        QPlainTextEdit:focus,
        QComboBox:focus,
        QSpinBox:focus,
        QDoubleSpinBox:focus {{
            border-color: {c["border_input_focus"]};
            background: {c["bg_input_focus"]};
        }}
        QComboBox {{
            padding-right: 24px;
            min-height: 22px;
        }}
        QComboBox::drop-down {{
            border: none;
            width: 24px;
        }}
        QComboBoxPrivateContainer {{
            background: {c["bg_dropdown"]};
            background-color: {c["bg_dropdown"]};
            border: 1px solid {c["border_input"]};
        }}
        QComboBox QAbstractItemView {{
            background: {c["bg_dropdown"]};
            background-color: {c["bg_dropdown"]};
            alternate-background-color: {c["bg_dropdown"]};
            color: {c["text_accent"]};
            border: 1px solid {c["border_input"]};
            selection-background-color: {c["dropdown_selection"]};
            selection-color: {c["list_item_selected_text"]};
            outline: none;
        }}
        QComboBox QAbstractItemView::item:selected {{
            background: {c["dropdown_selection"]};
            background-color: {c["dropdown_selection"]};
            color: {c["list_item_selected_text"]};
        }}

        {build_shared_button_stylesheet(c)}

        QCheckBox {{
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 1px solid {c["checkbox_border"]};
            background: {c["checkbox_bg"]};
        }}
        QCheckBox::indicator:checked {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                        stop:0 {c["checkbox_checked_start"]}, stop:1 {c["checkbox_checked_end"]});
            border-color: {c["checkbox_checked_border"]};
        }}
        QCheckBox::indicator:hover {{
            border-color: {c["checkbox_hover_border"]};
        }}

        QSlider::groove:horizontal {{
            background: {c["slider_groove"]};
            height: 4px;
            border-radius: 2px;
        }}
        QSlider::handle:horizontal {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                        stop:0 {c["slider_handle_start"]}, stop:1 {c["slider_handle_end"]});
            width: 14px;
            height: 14px;
            margin: -5px 0;
            border-radius: 7px;
            border: 1px solid {c["slider_handle_border"]};
        }}
        QSlider::handle:horizontal:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                        stop:0 {c["slider_handle_hover_start"]}, stop:1 {c["slider_handle_hover_end"]});
        }}

        QTabWidget::pane {{
            border: none;
            background: transparent;
        }}
        QTabBar::tab {{
            background: transparent;
            border: none;
            border-radius: 8px;
            color: {c["text_secondary"]};
            padding: 6px 14px;
            margin: 2px 3px;
            font-weight: 500;
        }}
        QTabBar::tab:selected {{
            background: {c["nav_checked_bg"]};
            color: {c["text_bright"]};
            font-weight: 600;
        }}
        QTabBar::tab:hover:!selected {{
            background: {c["nav_hover_bg"]};
            color: {c["text_accent"]};
        }}

        QListWidget,
        QListView,
        QTreeWidget,
        QTreeView,
        QTableWidget,
        QTableView {{
            background: {c["bg_list"]};
            border: 1px solid {c["border_list"]};
            border-radius: 10px;
            color: {c["text_accent"]};
            outline: none;
        }}
        QListWidget::item,
        QListView::item,
        QTreeWidget::item,
        QTreeView::item {{
            padding: 6px 8px;
            border-radius: 6px;
        }}
        QListWidget::item:hover,
        QListView::item:hover,
        QTreeWidget::item:hover,
        QTreeView::item:hover {{
            background: {c["list_item_hover"]};
        }}
        QListWidget::item:selected,
        QListView::item:selected,
        QTreeWidget::item:selected,
        QTreeView::item:selected,
        QTableView::item:selected,
        QTableWidget::item:selected {{
            background: {c["list_item_selected"]};
            color: {c["list_item_selected_text"]};
        }}
        QHeaderView::section {{
            background: {c["bg_surface_soft"]};
            color: {c["text_secondary"]};
            border: none;
            border-bottom: 1px solid {c["border_subtle"]};
            padding: 8px 10px;
            font-weight: 600;
        }}

        QScrollArea {{
            background: transparent;
            border: none;
        }}
        QScrollBar:vertical,
        QScrollBar:horizontal {{
            background: {c["bg_scroll"]};
            border: none;
            border-radius: 6px;
        }}
        QScrollBar:vertical {{
            width: 10px;
        }}
        QScrollBar:horizontal {{
            height: 10px;
        }}
        QScrollBar::handle:vertical,
        QScrollBar::handle:horizontal {{
            background: {c["scroll_handle"]};
            border-radius: 6px;
            min-height: 24px;
            min-width: 24px;
        }}
        QScrollBar::handle:vertical:hover,
        QScrollBar::handle:horizontal:hover {{
            background: {c["scroll_handle_hover"]};
        }}
        QScrollBar::add-line,
        QScrollBar::sub-line {{
            width: 0px;
            height: 0px;
        }}

        QSplitter::handle {{
            background: {c["splitter_handle"]};
        }}
        QSplitter::handle:hover {{
            background: {c["splitter_handle_hover"]};
        }}

        QLabel[status="success"] {{
            color: {c["success_color"]};
        }}
        QLabel[status="error"] {{
            color: {c["danger_bg"]};
        }}
    """


def repolish_widget(widget: QWidget) -> None:
    try:
        style = widget.style()
        if style is not None:
            style.unpolish(widget)
            style.polish(widget)
        widget.update()
    except RuntimeError:
        return


def apply_widget_stylesheet(widget: QWidget, stylesheet: str) -> None:
    """Apply a local stylesheet without walking the entire widget tree."""
    if widget.styleSheet() != stylesheet:
        widget.setStyleSheet(stylesheet)
    repolish_widget(widget)


def apply_native_title_bar_theme(widget: QWidget, theme: str | None = None, logger=None) -> None:
    """Apply the current theme colors to a native Windows title bar for a widget."""
    import sys

    if sys.platform != "win32":
        return

    try:
        import ctypes
        from ctypes import wintypes

        from PyQt6.QtGui import QColor

        resolved_theme = normalize_theme(theme or _CURRENT_THEME)
        hwnd = int(widget.winId())
        if not hwnd:
            return

        colors = get_theme_colors(resolved_theme)
        dwmapi = ctypes.windll.dwmapi
        user32 = ctypes.windll.user32

        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19
        DWMWA_BORDER_COLOR = 34
        DWMWA_CAPTION_COLOR = 35
        DWMWA_TEXT_COLOR = 36
        SWP_NOSIZE = 0x0001
        SWP_NOMOVE = 0x0002
        SWP_NOZORDER = 0x0004
        SWP_NOACTIVATE = 0x0010
        SWP_FRAMECHANGED = 0x0020

        def _to_colorref(value: str):
            color = QColor(value)
            return wintypes.DWORD(color.red() | (color.green() << 8) | (color.blue() << 16))

        def _set_dwm_attr(attribute: int, data):
            return dwmapi.DwmSetWindowAttribute(
                wintypes.HWND(hwnd),
                ctypes.c_uint(attribute),
                ctypes.byref(data),
                ctypes.sizeof(data),
            )

        is_dark_caption = is_dark_theme(resolved_theme)
        dark_mode = ctypes.c_int(1 if is_dark_caption else 0)
        result = _set_dwm_attr(DWMWA_USE_IMMERSIVE_DARK_MODE, dark_mode)
        if result != 0:
            _set_dwm_attr(DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1, dark_mode)

        caption_color = _to_colorref(colors["bg_window_shell"])
        border_color = _to_colorref(colors["border_sidebar"])
        text_color = _to_colorref(colors["text_bright"] if is_dark_caption else colors["text_accent"])

        _set_dwm_attr(DWMWA_CAPTION_COLOR, caption_color)
        _set_dwm_attr(DWMWA_BORDER_COLOR, border_color)
        _set_dwm_attr(DWMWA_TEXT_COLOR, text_color)

        user32.SetWindowPos(
            wintypes.HWND(hwnd),
            wintypes.HWND(0),
            0,
            0,
            0,
            0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE | SWP_FRAMECHANGED,
        )
    except Exception as exc:
        if logger is not None:
            logger.debug(f"应用原生标题栏主题失败: {exc}")


def apply_application_theme(theme: str, app: QApplication | None = None) -> None:
    app = app or QApplication.instance()
    if app is None:
        return

    resolved_theme = normalize_theme(theme)

    set_current_theme(resolved_theme)
    palette = build_theme_palette(resolved_theme)
    app.setPalette(palette)
    app.setStyleSheet(generate_application_stylesheet(resolved_theme))
    QToolTip.setPalette(palette)
    QToolTip.setFont(app.font())
