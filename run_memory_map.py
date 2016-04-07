import argparse
import re
import subprocess
from teamcity.messages import TeamcityServiceMessages


class Section(object):
    def __init__(self: object, name: str, size: int, addr: int) -> object:
        self.name = name
        self.size = size
        self.addr = addr


def parse_size(toolchain: str, binutils_prefix: str, file: str) -> list:
    args = '{0}/{1}-size --format=sysv --radix=10 {2}'.format(toolchain, binutils_prefix, file)
    process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    sections = []
    if process.returncode == 0:
        p = re.compile('(\.\S+)[ ]+(\d+)[ ]+(\d+)')
        for section in p.finditer(process.stdout):
            sections.append(Section(section.group(1), int(section.group(2)), int(section.group(3))))
    return sections


def main():
    parser = argparse.ArgumentParser(description='run_memory_map')
    parser.add_argument('--toolchain', type=str, help='GCC toolchain path', default='')
    parser.add_argument('--binutils_prefix', type=str, help='GNU binutils prefix', default='')
    parser.add_argument('--file', type=str, help='Binary file')
    parser.add_argument('--key_name', type=str, help='TeamCity buildStatisticValue key name suffix', default='none')
    args = parser.parse_args()

    tsm = TeamcityServiceMessages()

    sections = parse_size(args.toolchain, args.binutils_prefix, args.file)
    if sections:
        flash_size = 0
        ram_size = 0
        other_size = 0
        for section in sections:
            if section.name in ['.text', '.ARM.exidx', '.relocate']:
                flash_size += section.size
            elif section.name in ['.bss', '.stack']:
                ram_size += section.size
            else:
                other_size += section.size
        tsm.message('buildStatisticValue', key='FLASH ({0})'.format(args.key_name), value=str(flash_size))
        tsm.message('buildStatisticValue', key='RAM ({0})'.format(args.key_name), value=str(ram_size))
        # tsm.message('buildStatisticValue', key='OTHER ({0})'.format(args.key_name), value=str(other_size))
    else:
        tsm.buildProblem('Unable to detect sections', '')


if __name__ == '__main__':
    main()
