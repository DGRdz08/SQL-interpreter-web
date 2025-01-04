import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

class DataHandler:
    def execute_select(self, filename, columns, conditions=None):
        try:
            # Cargamos el DF
            df = self._load_and_convert(filename)
            # Aplicamos las condiciones
            df = self._apply_conditions(df, conditions)
            # Si es '*', retornamos todas las columnas; 
            # si no, seleccionamos las que especificó el query
            if columns != '*':
                try:
                    df = df[columns]
                except KeyError as e:
                    return {"error": f"Columnas no encontradas. {e}"}
            
            # Retornamos el DF como lista de dicts
            return df.to_dict(orient="records")
        except Exception as e:
            return {"error": f"Error en SELECT: {e}"}

    def execute_insert(self, filename, values):
        try:
            df = pd.read_csv(filename)
            new_row = pd.DataFrame([values], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(filename, index=False)
            return {"message": "Fila insertada correctamente."}
        except Exception as e:
            return {"error": f"Error al procesar el INSERT: {e}"}

    def execute_update(self, filename, set_clauses, conditions=None):
        try:
            original_df = self._load_and_convert(filename)
            temp_df = original_df.copy()

            updates = {
                col.strip(): self._parse_value(val.strip())
                for col, val in (
                    clause.split(" = ") for clause in set_clauses.split(", ")
                )
            }
            filtered_df = self._apply_conditions(temp_df, conditions)

            for col, val in updates.items():
                original_df.loc[filtered_df.index, col] = val

            original_df.to_csv(filename, index=False)
            return {"message": f"Archivo {filename} actualizado con éxito."}
        except Exception as e:
            return {"error": f"Error al procesar el UPDATE: {e}"}

    def execute_delete(self, filename, conditions=None):
        try:
            original_df = self._load_and_convert(filename)
            temp_df = original_df.copy()

            filtered_df = self._apply_conditions(temp_df, conditions)

            # Si hay condiciones, borramos sólo las filas que cumplan 
            if conditions:
                original_df.drop(filtered_df.index, inplace=True)
            else:
                # Sin condiciones => borrar todo
                original_df = original_df.iloc[0:0]

            original_df.to_csv(filename, index=False)
            return {"message": "Registros eliminados correctamente."}
        except Exception as e:
            return {"error": f"Error al procesar el DELETE: {e}"}

    def _load_and_convert(self, filename):
        df = pd.read_csv(filename)

        # Intentar detectar columnas de fecha
        date_columns = [
            col for col in df.columns
            if pd.api.types.is_string_dtype(df[col]) 
               and not pd.to_datetime(df[col], errors='coerce').isna().all()
        ]
        df[date_columns] = df[date_columns].apply(pd.to_datetime, errors='coerce')

        return df

    def _apply_conditions(self, df, conditions):
        if not conditions:
            return df

        try:
            # Recuerda que tu parser sustituye '=' por '=='
            # en la p_condition. Si no, ajusta aquí.
            return df.query(conditions)
        except Exception as e:
            print(f"Error al procesar condiciones: {e}")
            return df

    def _parse_value(self, value):
        if value.startswith("'") and value.endswith("'"):
            return value[1:-1]  # 'Finance' -> Finance
        elif value.isdigit():
            return int(value)  # 10 -> 10
        try:
            return float(value)  # 10.5 -> 10.5
        except ValueError:
            return value
