from collections import deque


class CalculatorFunctions:
    EXIT = '/exit'
    HELP = '/help'
    INVALID_ASSIGNMENT = 'Invalid assignment'
    INVALID_IDENTIFIER = 'Invalid identifier'
    UNKNOWN_VARIABLE = 'Unknown variable'
    INVALID_EXPRESSION = 'Invalid expression'
    vars = {}
    order_of_operations = {'+': 0, '-': 0, '*': 1, '/': 1, '^': 2}

    def __init__(self, input_):
        '''Input_ takes a string in the form of an expression or a variable declaration and this expression is then used 
           in the functions for the class'''
        contains_letters = any([input_[i].isalpha() for i in range(len(input_))])
        if not contains_letters and input_ != '':
            self.expression = input_
        else:
            if self.EXIT in input_:
                self.exit()
                run_calculator()
            elif self.HELP in input_:
                self.help()
                run_calculator()
            elif '/' in input_ and input_.find('/') == 0:
                print('Unknown command')
                run_calculator()
            elif input_ == '':
                run_calculator()
            elif '=' in input_:
                self.var_declaration = input_.replace(' ', '')
                self.terms = []
                self.read_vars()
            else:
                self.expression = input_
                if self.var_in_expression():
                    self.sub_vars()
                else:
                    print(self.INVALID_EXPRESSION)
                    run_calculator()

        self.x = 1
        self.y = 1

        self.arithmetic_functions = {'*': self.multiply, '/': self.divide, '^': self.raise_to_power,
                                     '+': self.add, '-': self.subtract}

    def var_in_expression(self):
        '''Checks if vars in an expression are known'''
        possible_vars = {i for i in self.expression.split() if all([char.isalpha() for char in i])}
        all_vars = {i for i in CalculatorFunctions.vars}
        if all([i in all_vars for i in possible_vars]):
            return True
        else:
            print(self.UNKNOWN_VARIABLE)
            run_calculator()

    def sub_vars(self):
        '''Substitutes variables into an expression'''
        for var in CalculatorFunctions.vars:
            self.expression = self.expression.replace(var, CalculatorFunctions.vars[var])

    def read_vars(self):
        '''Reads a variable declaration and then adds it to the vars for the class'''
        self.terms = self.var_declaration.split('=')
        if self.invalid_identifier_check():
            print(self.INVALID_IDENTIFIER)
            run_calculator()
        elif self.invalid_assignment_check_basic():
            print(self.INVALID_ASSIGNMENT)
            run_calculator()
        else:
            if self.terms[1] in CalculatorFunctions.vars:
                CalculatorFunctions.vars[self.terms[0]] = CalculatorFunctions.vars[self.terms[1]]
                run_calculator()
            elif all(i.isalpha() for i in self.terms[1]):
                print(self.UNKNOWN_VARIABLE)
                run_calculator()
            elif any(i.isalpha() for i in self.terms[1]):
                print(self.INVALID_ASSIGNMENT)
                run_calculator()
            else:
                CalculatorFunctions.vars[self.terms[0]] = self.terms[1]
                run_calculator()

    def invalid_assignment_check_basic(self):
        return self.var_declaration.count('=') > 1

    def invalid_identifier_check(self):
        return not all([i.isalpha() for i in self.terms[0]])

    def evaluate_expression(self):
        '''Evaluates the postfix expression defined in the __init__ method for this class.'''
        postfix = self.expression_to_postfix()
        postfix_example = list(postfix)
        result = deque()
        while len(postfix) > 0:
            if self.isdigit(postfix[0]):
                result.append(postfix.popleft())
            else:
                self.x = int(result.pop())
                self.y = int(result.pop())

                result.append(self.arithmetic_functions[postfix.popleft()]())
        return str(result.pop()) + f'\nPostfix notation example: {" ".join(postfix_example)}'

    def multiply(self):
        return self.x * self.y

    def divide(self):
        return self.y / self.x

    def raise_to_power(self):
        return self.x ** self.y

    def add(self):
        return self.x + self.y

    def subtract(self):
        return self.y - self.x

    def expression_to_postfix(self, expression=None):
        '''Takes an infix expression defined in __init_ and converts it to postfix notation. 
           You must make an object in order to use this function.
           
           The "expression" parameter of this function is used recursively to evaluate parenthesis but
           It can also be used once an expression object is defined or by defining self as a static class.'''
        postfix = deque()
        infix = deque(self.expression_to_list(self.expression)) if expression is None else deque(expression)
        operations = deque()

        while len(infix) > 0:
            if (''.join(infix).count('(') + ''.join(infix).count(')')) % 2 != 0:
                print(self.INVALID_EXPRESSION)
                run_calculator()
            elif self.isdigit(infix[0]):
                postfix.append(infix.popleft())
            elif '(' in infix[0]:
                finder = ' '.join(infix).replace(')', '', infix[0].count('(') - 1).split()
                selection = list(infix)[0:int(''.join([str(i) for i in range(len(infix)) if ')' in finder[i]][0])) + 1]
                selection = [selection[0].replace('(', '', 1)] + selection[1:len(selection) - 1] + \
                            [selection[len(selection) - 1].replace(')', '', 1)]
                selection_postfix = self.expression_to_postfix(selection)
                for term in selection_postfix:
                    postfix.append(str(term))
                infix = deque(list(infix)[len(selection):])
            elif len(operations) == 0:
                operations.appendleft(self.handle_symbols(infix.popleft()))
            else:
                for operation in list(operations):
                    if self.order_of_operations[self.handle_symbols(infix[0])] <= self.order_of_operations[operation]:
                        postfix.append(self.handle_symbols(operations.popleft()))
                    else:
                        break
                operations.appendleft(self.handle_symbols(infix.popleft()))

        for _ in range(len(operations)):
            postfix.append(operations.popleft())
        return postfix

    def expression_to_list(self, expression):
        '''Converts expression to a list
           Can be used outside of an object in the form "CalculatorFunctions.expression_to_list(CalculatorFunctions, "1+2")"'''
        updated_expression = list(expression)
        difference = 0
        for i in range(len(list(expression))):
            if i == 0:
                continue
            elif not self.not_split_value(expression[i]) and self.not_split_value(expression[i - 1]):
                updated_expression.insert(i + difference, ' ')
                difference += 1
            elif self.not_split_value(expression[i]) and not self.not_split_value(expression[i - 1]) and i != 1:
                updated_expression.insert(i + difference, ' ')
                difference += 1

        return ''.join(updated_expression).split()

    def handle_symbols(self, term):
        for _ in range(len(term)):
            if '--' in term:
                term = term.replace('--', '+')
            elif '+-' in term:
                term = term.replace('+-', '-')
            elif '-+' in term:
                term = term.replace('-+', '-')
            elif '++' in term:
                term = term.replace('++', '+')
            elif ('*' in term or '/' in term or '^' in term) and len(term) > 1:
                print(self.INVALID_EXPRESSION)
                run_calculator()
        return term

    @staticmethod
    def not_split_value(char):
        return char.isdigit() or char == ')' or char == '(' or char == ' '

    @staticmethod
    def isdigit(num):
        try:
            int(num)
            return True
        except ValueError:
            return False

    @staticmethod
    def exit():
        print('Bye!')
        quit()

    @staticmethod
    def help():
        print('The program calculates the sum of numbers')
        run_calculator()


def run_calculator():
    while True:
        c = CalculatorFunctions(input('Enter an expression or var declaration: '))
        print(c.evaluate_expression())


if __name__ == '__main__':
    run_calculator()
