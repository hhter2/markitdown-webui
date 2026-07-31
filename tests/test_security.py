import pytest

from app.security import output_filename, safe_filename, validate_extension


def test_safe_filename_removes_paths() -> None:
    assert safe_filename("../../report.pdf") == "report.pdf"
    assert safe_filename(r"C:\\Users\\A\\report.docx") == "report.docx"


def test_validate_extension_is_allowlisted() -> None:
    assert validate_extension("report.PDF") == ".pdf"
    with pytest.raises(ValueError):
        validate_extension("payload.exe")


def test_output_filename_is_safe() -> None:
    assert output_filename('quarter:1?.xlsx') == "quarter1.md"
