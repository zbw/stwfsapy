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


class UnknownInputTypeException(Exception):
    def __init__(self) -> None:
        self.message = 'Unknown Input Format. Please specify' + (
            ' "content", "file" or "filename".')
        super().__init__(self.message)


def handle_content(txt):
    return txt


def handle_file(file):
    return file.read()


def handle_filename(f_pth):
    with open(f_pth) as f:
        return f.read()


def get_input_handler(input_type):
    if input_type == 'content':
        return handle_content
    elif input_type == 'file':
        return handle_file
    elif input_type == 'filename':
        return handle_filename
    raise UnknownInputTypeException()
