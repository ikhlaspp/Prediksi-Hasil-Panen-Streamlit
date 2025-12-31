import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st

from config.settings import APP_TITLE, APP_ICON, APP_LAYOUT, PAGES
from utils.styling import apply_custom_css
from components.sidebar import render_sidebar
from views import (
    home,
    single_prediction,
    model_performance,
    shap_analysis,
    data_visualization,
    batch_prediction,
    model_comparison,
)


def main() -> None:
    """MVC entrypoint: configure page, apply theme, render selected view."""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=APP_LAYOUT,
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com",
            "Report a bug": "https://github.com",
            "About": f"# {APP_TITLE}\nPowered by Machine Learning",
        },
    )

    # Global theme and custom CSS (glass, gradients, variables)
    apply_custom_css()

    # Sidebar navigation
    selected_page = render_sidebar()

    # Route to the chosen view
    if selected_page == PAGES["home"]:
        home.render()
    elif selected_page == PAGES["prediction"]:
        single_prediction.render()
    elif selected_page == PAGES["performance"]:
        model_performance.render()
    elif selected_page == PAGES["shap"]:
        shap_analysis.render()
    elif selected_page == PAGES["visualization"]:
        data_visualization.render()
    elif selected_page == PAGES["batch"]:
        batch_prediction.render()
    elif selected_page == PAGES["comparison"]:
        model_comparison.render()


if __name__ == "__main__":
    main()
