# Copyright 2020 Leibniz Information Centre for Economics
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


import stwfsapy.thesaurus as t
import stwfsapy.tests.thesaurus.common as c


def test_filters_out_thsys_(tuples_with_thsys):
    thsys_tuple = (c.thsys_ref_print, c.thsys_prefLabel_print_en)
    assert thsys_tuple in tuples_with_thsys
    result = list(t._filter_by_prefix(tuples_with_thsys, c.test_URI_prefix))
    assert thsys_tuple not in result
    assert len(result) == len(tuples_with_thsys)-1
    for tpl in result:
        assert tpl in tuples_with_thsys
