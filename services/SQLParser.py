import ply.yacc as yacc
# Ajusta la ruta de tu DataHandler según tu estructura de proyecto
from .data_handler import DataHandler

class SQLParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.data_handler = DataHandler()

    def p_statement_select(self, p):
        """statement : SELECT columns FROM table WHERE conditions eos
                    | SELECT columns FROM table eos
                    | SELECT ASTERISK FROM table WHERE conditions eos
                    | SELECT ASTERISK FROM table eos"""
        p[0] = {
            "operation": "SELECT",
            "columns": p[2] if p[1].upper() != "SELECT *" else ["*"],
            "table": p[4],
            "conditions": p[6] if len(p) > 6 else None,
        }


    def p_statement_insert(self, p):
        """statement : INSERT INTO table VALUES LPAREN values RPAREN eos"""
        p[0] = {
            "operation": "INSERT",
            "table": p[3],
            "values": p[6]
        }


    def p_statement_update(self, p):
        """statement : UPDATE table SET set_clauses WHERE conditions eos
                      | UPDATE table SET set_clauses eos"""
        p[0] = {
        "operation": "UPDATE",
        "table": p[2],
        "set_clauses": p[4],
        "conditions": p[6] if len(p) == 8 else None
        }

    def p_statement_delete(self, p):
        """statement : DELETE FROM table WHERE conditions eos
                      | DELETE FROM table eos"""
        p[0] = {
        "operation": "DELETE",
        "table": p[3],
        "conditions": p[5] if len(p) == 7 else None
        }

    def p_columns(self, p):
        """columns : columns COMMA column
                   | column"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_column(self, p):
        """column : IDENTIFIER"""
        p[0] = p[1]
    def p_table(self, p):
        """table : IDENTIFIER
                 | STRING"""
        p[0] = p[1]


    def p_values(self, p):
        """values : values COMMA value
                  | value"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_value(self, p):
        """value : NUMBER
                 | STRING"""
        p[0] = p[1]

    def p_set_clauses(self, p):
        """set_clauses : set_clauses COMMA set_clause
                       | set_clause"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + ", " + p[3]

    def p_set_clause(self, p):
        """set_clause : column EQUALS value"""
        p[0] = f"{p[1]} = {p[3]}"

    def p_conditions(self, p):
        """conditions : LPAREN conditions RPAREN
                      | conditions logical condition
                      | condition"""
        # Manejo de recursión en las condiciones
        if len(p) == 4 and p[1] == '(' and p[3] == ')':
            # Ej: ( conditions )
            p[0] = f"({p[2]})"
        elif len(p) == 4:
            # Ej: conditions AND/OR condition
            p[0] = f"{p[1]} {p[2]} {p[3]}"
        else:
            # Solo condition
            p[0] = p[1]

    def p_condition(self, p):
        """condition : column EQUALS value
                      | column GREATER value
                      | column LESS value
                      | column LEQ value
                      | column GEQ value"""
        # Mapeo de operadores SQL a Python
        op_map = {"=": "==", ">": ">", "<": "<", "<=": "<=", ">=": ">="}
        col = p[1]
        op = op_map[p[2]]
        val = p[3]

        # Si el valor es STRING, ponerlo entre comillas en la expresión final
        if isinstance(val, str):
            val = f"'{val}'"

        p[0] = f"{col} {op} {val}"

    def p_logical(self, p):
        """logical : AND
                   | OR"""
        # Mapeamos AND -> 'and', OR -> 'or'
        if p[1].lower() == 'and':
            p[0] = 'and'
        else:
            p[0] = 'or'

    def p_eos(self, p):
        """eos : SEMICOLON"""
        pass

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")