import psycopg2
import os


name_database = "db_name"
name_user = "db_user"
db_password = "db_password"
db_host = "db_host"
db_port = "db_port"

path_directory = 'D:/Project/test'


def find_sql_files(path):
    result = []
    for root, directory, file in os.walk(path):
        for f in file:
            if f[-4:] == '.sql':
                result.append(root + '\\' + f)
    return result


def read_file(path_sql):
    with open(path_sql) as file:
        sql_script = file.read()
    return sql_script


def split_sql(sql_script):
    line_comment = False
    multiline_comment = False
    flg_text = False
    i = 0
    j = 0
    result = []
    while i < len(sql_script):
        if sql_script[i:i + 2] == '--':
            line_comment = True
        if sql_script[i] == '\n':
            line_comment = False
        if sql_script[i:i + 2] == '/*':
            multiline_comment = True
        if sql_script[i:i + 2] == '*/':
            multiline_comment = False
        if sql_script[i] == "'":
            flg_text = not flg_text

        if sql_script[i] == ';' and not line_comment and not multiline_comment \
                and not flg_text:
            result.append(sql_script[j:i + 1])
            j = i + 1
        i += 1
    if len(sql_script) != 0 and sql_script[-1] != ';' and not line_comment \
            and not multiline_comment and not flg_text:
        result.append(sql_script[j:i + 1].strip())
    return result


def validate_syntax(sql_command):
    try:
        connection = psycopg2.connect(database=name_database, user=name_user,
                                      password=db_password, host=db_host,
                                      port=db_port)
        cursor = connection.cursor()
        a = """DO $SYNTAX_CHECK$ BEGIN RETURN; {query} END;
         $SYNTAX_CHECK$;""".format(query=sql_command)
        cursor.execute(a)
        cursor.close()
        connection.close()
    except psycopg2.errors.SyntaxError as e:
        return str(e)


def validate_package(path):
    result = {}
    for path_sql in find_sql_files(path):
        syntax_error = []
        script_file = read_file(path_sql)
        if len(script_file) != 0:
            for sql_command in split_sql(script_file):
                if validate_syntax(sql_command) is not None:
                    syntax_error.append(validate_syntax(sql_command))
            result[path_sql] = syntax_error
        else:
            result[path_sql] = ["This file is empty!!!" + '\n']
    return result


def error_format(files_and_errors):
    result = []
    num = 1
    for i in files_and_errors:
        result.append(i + '\n')
        for x in files_and_errors[i]:
            result.append(str(num) + ')')
            num += 1
            result.append(x)
        result.append('-' * 50 + '\n')
    return result


def main():
    result_validate = validate_package(path_directory)
    result_txt = error_format(result_validate)

    with open(path_directory + '/error.txt', 'w') as f:
        f.write(' '.join(result_txt))


if __name__ == '__main__':
    main()
