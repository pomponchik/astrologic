import inspect
import textwrap


class FunctionText:
    def __init__(self, function):
        self.function_object = function
        self.source = inspect.getsource(function)
        self.begin_line_number = self.get_begin_line_number(function)
        self.clean_text, self.decorators_num = self.get_clean_text_and_number_of_decorators(self.source)
        self.clean_text_with_pre_breaks = self.get_clean_text_with_pre_breaks(self.clean_text, self.begin_line_number, self.decorators_num)
        self.indent_symbols = self.get_indent_symbols(self.clean_text)

    @staticmethod
    def get_clean_text_with_pre_breaks(clean_text, begin_line_number, decorators_num):
        lines = ['\n' for x in range(begin_line_number - 1 + decorators_num)]
        lines.append(clean_text)
        result = ''.join(lines)
        return result

    @staticmethod
    def get_begin_line_number(function):
        return inspect.getsourcelines(function)[1]

    @staticmethod
    def get_clean_text_and_number_of_decorators(text):
        text = textwrap.dedent(text)
        decorators_num = 0
        for string in text.split('\n'):
            if string.startswith('@'):
                decorators_num += 1
            else:
                break
        clean_text = '\n'.join(text.split('\n')[decorators_num:])
        return clean_text, decorators_num

    @staticmethod
    def get_indent_symbols(text):
        lines = text.split('\n')
        for line in lines:
            if not line.startswith('def '):
                indent_len = len(line) - len(line.lstrip(' \t'))
                return line[:indent_len]
        return ''

    def wrapp_clean_text(self, prefix='', postfix='', indent=0):
        if indent:
            indent_text = textwrap.indent(self.clean_text, indent * self.indent_symbols)
        else:
            indent_text = self.clean_text
        self.clean_text = f'{prefix}\n{indent_text}\n{postfix}'
        n_count = prefix.count('\n')
        self.begin_line_number -= n_count
        if self.begin_line_number < 0:
            self.begin_line_number = 0
        self.clean_text_with_pre_breaks = self.get_clean_text_with_pre_breaks(self.clean_text, self.begin_line_number, self.decorators_num)
