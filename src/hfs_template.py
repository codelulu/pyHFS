import re

class HFS_Template:

    src = ''
    sections = {}
    
    def __init__(self, src):
        self.src = src

        section_content = ''
        section_name = ''
        with open(src) as f:
            for line in f:
                m = re.search('\[(?P<name>(.+))\]', line)
                if m:
                    self.add_section(section_name, section_content)
                    section_name = m.group('name')
                    section_content = ''
                else:
                    section_content += line

        self.add_section(section_name, section_content)

    def add_section(self, name, content):
        section = {}
        section['name'] = name
        section['content'] = content
        self.sections[name] = content

    def getTxt(self, section_name = ''):
        if section_name in self.sections:
            return self.sections[section_name]

        return ''

    def __getitem__(self, index):
        return self.getTxt(index)

    def sectionExist(self, section_name = ''):
        if section_name in self.sections:
            return True

        return False
