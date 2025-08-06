#!/usr/bin/env python3 -m pytest
import io
import pytest

# Skip the entire module if required dependencies are missing
pandas = pytest.importorskip("pandas")
pytest.importorskip("requests")

from markitdown import MarkItDown, StreamInfo


@pytest.mark.parametrize(
    "extension,write_engine,read_dep",
    [
        (".xlsx", "openpyxl", "openpyxl"),
        (".xls", "xlwt", "xlrd"),
    ],
)
def test_excel_empty_cells_no_nan(extension, write_engine, read_dep):
    pytest.importorskip(write_engine)
    pytest.importorskip(read_dep)

    df = pandas.DataFrame({"A": [1, None], "B": ["text", None]})

    bio = io.BytesIO()
    df.to_excel(bio, index=False, engine=write_engine)
    bio.seek(0)

    markitdown = MarkItDown()
    result = markitdown.convert(bio, stream_info=StreamInfo(extension=extension))

    assert "NaN" not in result.markdown
