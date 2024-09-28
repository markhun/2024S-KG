from pathlib import Path

from streamlit.web import cli

package_dir = Path(__file__).resolve().parents[0]
app_path = package_dir / "app.py"


def main():
    cli.main_run([str(app_path)])


if __name__ == "__main__":
    main()
