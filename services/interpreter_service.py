from .SQLLexer import SQLLexer
from .SQLParser import SQLParser
from .data_handler import DataHandler

class SQLInterpreter:
    def __init__(self):
        self.lexer = SQLLexer()
        self.parser = SQLParser(self.lexer)
        self.data_handler = DataHandler()

    def execute_query(self, query, filename):
        try:
            parsed_query = self._parse_query(query)
            operation = parsed_query["operation"]
            print(f"Operación recibida: {operation}")
            match operation:
                case "SELECT":
                    print(f"Parsed SELECT Query: {parsed_query}")
                    return self.data_handler.execute_select(
                        filename,
                        parsed_query["columns"],
                        parsed_query.get("conditions")
                    )
                case "INSERT":
                    return self.data_handler.execute_insert(
                        filename,
                        parsed_query["values"]
                    )
                case "UPDATE":
                    return self.data_handler.execute_update(
                        filename,
                        parsed_query["set_clauses"],
                        parsed_query.get("conditions")
                    )
                case "DELETE":
                    return self.data_handler.execute_delete(
                        filename,
                        parsed_query.get("conditions")
                    )
                case _:
                    return {"error": f"Operación no soportada: {operation}"}
        except Exception as e:
            return {"error": f"Error al ejecutar el query: {str(e)}"}


    def _parse_query(self, query):
        print(f"Procesando query: {query}")
        parsed_data = self.parser.parser.parse(query)

        if not parsed_data:
            print("Error: El parser devolvió None o datos inválidos.")
            raise ValueError("El parser no pudo interpretar el query.")

        print(f"Resultado del parser: {parsed_data}")
        return parsed_data
