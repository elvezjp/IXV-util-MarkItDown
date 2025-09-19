"""ASCII アートロゴ表示モジュール

CLI での使用方法:
    CLI関数の最初にロゴを表示するために、以下のコードを追加してください:
    ```
    from .utils.ascii_logo import display_project_logo

    display_project_logo(display_name="アプリケーション名")
    ```

PyInstaller ビルド時の注意:
    ビルド時に pyfiglet のフォントファイルを追加データとして含める必要があります。
    .spec ファイルまたはビルドスクリプトで必要な設定を記述してください:

    .spec ファイルの場合
    ```
    from src.utils.ascii_logo import get_pyfiglet_fonts_path

    font_data = (get_pyfiglet_fonts_path(), "pyfiglet/fonts")

    a = Analysis(
        ...
        datas=[font_data],
        ...
    )
    ```

    ビルドスクリプトの場合
    ```
    import subprocess
    import sys
    from src.utils.ascii_logo import get_pyfiglet_fonts_path

    fonts_data = f"{get_pyfiglet_fonts_path()}:pyfiglet/fonts"

    pyinstaller_args = [
        sys.executable, "-m", "PyInstaller",
        ...
        "--add-data", fonts_data,
        ...
    ]

    subprocess.run(pyinstaller_args)
    ```
"""

import sys
from importlib.metadata import metadata
from pathlib import Path

import pyfiglet


def _get_executable_name():
    """実行ファイル名から表示名を取得する。"""
    try:
        # sys.argv[0]から実行ファイル名を取得
        executable_path = Path(sys.argv[0])
        name = executable_path.stem
        return name
    except Exception:
        return "App"


def display_project_logo(package_name=None, display_name=None, font="standard"):
    """
    Display project logo as ASCII art.

    Args:
        package_name (str, optional): Package name to lookup in metadata
        display_name (str, optional): Display name to use. If None, derives from executable name
        font (str): Font name for ASCII art (default: 'standard')

    Returns:
        str: The logo text that was displayed
    """
    # プロジェクト名を取得
    if package_name and display_name:
        try:
            # pyproject.tomlからプロジェクト名を取得（メタデータの存在確認用）
            project_metadata = metadata(package_name)
            logo_name = display_name  # 表示用の正規化された名前を使用
        except Exception:
            # メタデータが取得できない場合は実行ファイル名から取得
            logo_name = _get_executable_name()
    elif display_name:
        logo_name = display_name
    else:
        # 実行ファイル名から自動取得
        logo_name = _get_executable_name()

    try:
        figlet = pyfiglet.Figlet(font=font, width=1000)  # 幅制限を大きく設定
        logo_text = figlet.renderText(logo_name)
        print(logo_text, end="")
        return logo_text.rstrip("\n")
    except Exception:
        # フォントが利用できない場合（PyInstallerビルド時など）
        print(logo_name)
        return logo_name


def display_custom_logo(text, font="standard"):
    """
    Display custom text as ASCII art.
    @deprecated use display_project_logo instead

    Args:
        text (str): Text to display as ASCII art
        font (str): Font name for ASCII art (default: 'standard')

    Returns:
        str: The logo text that was displayed
    """

    try:
        figlet = pyfiglet.Figlet(font=font, width=1000)  # 幅制限を大きく設定
        logo_text = figlet.renderText(text)
        print(logo_text, end="")
        return logo_text.rstrip("\n")
    except Exception:
        # フォントが利用できない場合（PyInstallerビルド時など）
        print(text)
        return text


def get_pyfiglet_fonts_path() -> str:
    """
    PyInstallerビルド時に--add-dataオプションで使用するための
    フォントディレクトリのパスを返します。

    Returns:
        str: pyfigletフォントディレクトリの絶対パス。
    """
    try:
        fonts_dir = Path(pyfiglet.__file__).parent / "fonts"
        return str(fonts_dir)
    except ImportError:
        return ""
