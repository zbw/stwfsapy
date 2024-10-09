# Copyright 2020-2024 Leibniz Information Centre for Economics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from stwfsapy.util import input_handler as h
import pytest

file_content = "Some text inside a file"


@pytest.fixture
def handler_file(tmp_path):
    p = tmp_path / "hello.txt"
    p.write_text(file_content)
    return p


def test_content_handler():
    assert file_content == h.handle_content(file_content)


def test_file_handler(handler_file):
    with open(handler_file) as f:
        assert file_content == h.handle_file(f)


def test_filepath_handler(handler_file):
    assert file_content == h.handle_filename(handler_file.resolve())


def test_get_content_handler():
    assert h.handle_content == h.get_input_handler('content')


def test_get_file_handler():
    assert h.handle_file == h.get_input_handler('file')


def test_get_filename_handler():
    assert h.handle_filename == h.get_input_handler('filename')


def test_get_unknown_handler():
    with pytest.raises(h.UnknownInputTypeException):
        h.get_input_handler('dfsjdfs')
