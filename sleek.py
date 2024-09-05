import sys

variables = {}


class Misc:
    def is_str(self, string: str):
        if string.startswith('"') and string.endswith('"') or string.startswith("'") and string.endswith("'"):
            return True
        return False

    def is_str_for_any(self, string: str):
        if string.startswith('"') or string.endswith('"') or string.startswith("'") or string.endswith("'"):
            return True
        return False

    def call_error(self, label: str, code: str, info: str):
        base = f'''Error occurred during parsing:
        {code}
    {label}: {info}'''
        print(base)
        return None


class Builtins:
    def __init__(self, misc: Misc) -> None:
        self.misc = misc
        self.list = ['output', 'input', 'str', 'int',
                     'object', 'as', 'var', 'exit', 'quit', 'type']

    def output(self, content):
        if self.misc.is_str(content[0]):
            print(content[0].replace('"', '').replace("'", ''))
        elif content[0].isdigit():
            print(content[0].replace('"', '').replace("'", ''))
        elif content[0] in variables.keys():
            print(variables[content[0]])
        else:
            return self.misc.call_error('NotDefined', 'output ' + content[0], f'"{content[0]}" is not defined in source code.')
        if len(content) > 1:
            if content[1] == 'as':
                variables[content[2]] = None
        return None

    def input(self, content):
        if self.misc.is_str(content[0]):
            result = input(content[0].replace('"', '').replace("'", ''))
        elif content[0].isdigit():
            result = input(content[0].replace('"', '').replace("'", ''))
        elif content[0] in variables.keys():
            result = input(variables[content[0]])
        else:
            return self.misc.call_error('NotDefined', 'input ' + ' '.join(content), f'"{content[0]}" is not defined in source code.')
        if len(content) > 1:
            if content[1] == 'as':
                variables[content[2]] = result
                return None
        return result

    def type(self, content):
        try:
            int(content[0])
            return 'int object'
        except ValueError:
            if isinstance(content[0], str):
                return 'str object'
        return None
    
    def exit(self, _content):
        return sys.exit()
    
    def quit(self, _content):
        return sys.exit()


def parser(content: str):
    misc = Misc()
    builtins = Builtins(misc)

    content = content.strip()
    first_content = content.split(' ')
    args = first_content[1:]
    str_list = []
    for content in args:
        if misc.is_str_for_any(content):
            str_list.append(content)
    for content in str_list:
        args.remove(content)

    args.append(' '.join(str_list))
    if 'as' in args:
        for old_arg in args[:-1]:
            args.remove(old_arg)
            args.append(old_arg)
    args = list(filter(None, args))

    if first_content[0] in builtins.list:
        if first_content[0] == 'var':
            variables[args[0]] = args[2]
        else:
            result = eval(f'builtins.{first_content[0]}({args})')
            if result:
                return result
    elif first_content[0] in variables.keys():
        return variables[first_content[0]]
    else:
        misc.call_error('NotDefined', first_content[0], f'"{\
                        first_content[0]}" is not defined in source code.')


def run_file(file: str):
    with open(file, encoding='utf-8') as sleek:
        for line in sleek.readlines():
            line = line.strip()
            if line:
                result = parser(line)
                if result:
                    print(result)

