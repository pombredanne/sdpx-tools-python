# Copyright 2014 Ahmed H. Ismail

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import utils
import document
import checksum

class FileType(object):
    SOURCE = 1
    BINARY = 2
    ARCHIVE = 3
    OTHER = 4


class File(object):

    """Representation of SPDX file.
    Fields:
    name - File name, str mandatory one.
    comment - File comment str, Optional zero or one.
    type - one of FileType.SOURCE, FileType.BINARY, FileType.ARCHIVE
    and FileType.OTHER, optional zero or one.
    chk_sum - SHA1, Mandatory one.
    conc_lics - Mandatory one. document.License or utils.NoAssert or utils.SPDXNone.
    licenses_in_file - list of licenses found in file, mandatory one or more. 
        document.License or utils.SPDXNone or utils.NoAssert.
    document.license or utils.NoAssert or utils.SPDXNone.
    license_comment - Optional.
    copyright - Copyright text, Mandatory one. utils.NoAssert or utils.SPDXNone or str.
    notice - optional One, str.
    contributers - List of strings.
    dependencies - list of file locations.
    artifact_of_project_name - list of project names, possibly empty.
    artifact_of_project_home - list of project home page, possibly empty.
    artifact_of_project_uri - list of project uris, possibly empty.
    """

    def __init__(self, name):
        super(File, self).__init__()
        self.name = name
        self.comment = None
        self.type = None
        self.chk_sum = None
        self.conc_lics = None
        self.licenses_in_file = []
        self.license_comment = None
        self.copyright = None
        self.notice = None
        self.contributers = []
        self.dependencies = []
        self.artifact_of_project_name = []
        self.artifact_of_project_home = []
        self.artifact_of_project_uri = []

    def add_lics(self, lics):
        """Appends lics to licenses_in_file."""
        self.licenses_in_file.append(lics)

    def add_contrib(self, contrib):
        """Appends contrib to contributers."""
        self.contributers.append(contrib)

    def add_depend(self, depend):
        """Appends depend to dependencies."""
        self.dependencies.append(depend)

    def add_artifact(self, symbol, value):
        """Adds value as artifact_of_project{symbol}."""
        expr = 'self.artifact_of_project_{0}.append(value)'.format(symbol)
        eval(expr)

    def validate(self, messages):
        """Validates the fields and appends user friendly messages 
        to messages parameter if there are errors.
        """
        return ( self.validate_lic_conc(messages) & self.validate_type(messages)
            & self.validate_chksum(messages) & self.validate_licenses_in_file(messages) 
            & self.validate_copyright(messages) & self.validate_artifacts(messages) )

    def validate_copyright(self, messages):
        if type(self.copyright) in [str, unicode, utils.NoAssert, utils.SPDXNone]:
            return True
        else:
            messages.append('File copyright must be str or unicode or utils.NoAssert or utils.SPDXNone')
            return False

    def validate_artifacts(self, messages):
        if (len(self.artifact_of_project_home) >=
            max(len(self.artifact_of_project_uri), len(self.artifact_of_project_name)) ):
            return True
        else:
            messages.append('File must have as much artifact of project as uri or homepage')
            return False


    def validate_licenses_in_file(self, messages):
        if len(self.licenses_in_file) == 0:
            messages.append('File must have at least one license in file.')
            return False
        else:
            return True

    def validate_lic_conc(self, messages):
        if type(self.conc_lics) in [utils.NoAssert, 
            utils.SPDXNone] or isinstance(self.conc_lics, document.License):
            return True
        else:
            messages.append('File concluded license must be one of document.License, utils.NoAssert or utils.SPDXNone')
            return False

    def validate_type(self, messages):
        if self.type in [FileType.SOURCE, FileType.OTHER, FileType.BINARY,
            FileType.ARCHIVE]:
            return True
        else:
            messages.append('File type must be one of the constants defined in class spdx.file.FileType')
            return False

    def validate_chksum(self, messages):
        if isinstance(self.chk_sum, checksum.Algorithm):
            if self.chk_sum.identifier == 'SHA1':
                return True
            else:
                messages.append('File checksum algorithm must be SHA1')
                return False
        else:
            messages.append('File checksum must be instance of spdx.checksum.Algorithm')
            return False

    def has_optional_field(self, field):
        expr = 'self.{0} is not None'.format(field)
        return eval(expr)
