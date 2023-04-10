"""Application entry point, global configuration, application structure"""

from config import app_config
import data
import tab_capacity
import tab_summary
import utils


def main():
    # setup app-wide configuration
    utils.setup_app(app_config)

    # load data
    df_hr = data.load_transform(app_config.data_file)

    # setup app structure
    exec_summary, cap_plan = utils.create_tabs(
        ["Executive Summary 📝", "Capacity Planning 🚀"]
    )
    with exec_summary:
        tab_summary.render(df_hr)
    with cap_plan:
        tab_capacity.render(df_hr)


if __name__ == "__main__":
    main()
