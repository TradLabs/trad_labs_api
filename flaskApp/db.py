#!/usr/bin/python3
"""
Wraps all calls to DB to ensure consistent error handling and logging
"""
__author__ = 'sfblackl'

import sys
import traceback
import os
import logging
import datetime
import time

import flask.json



# Import our common code
import flaskApp.config

# Specific Items
import mysql.connector
import mysql.connector.errorcode

# Create Logger
LOGGER = logging.getLogger('tradlabs.api.db')
LOGGER.setLevel(flaskApp.config.LOG_LEVEL_DB)


def if_null(var, val):
    """ Quick function to ensure Nulls don't cause problems with string concat

    :param var: Variable to be evaluted for null
    :param val: replacement value if null
    :return: variable
    """

    if var is None:
        return val
    return var


def db_stored_procedure(procedure_name, args):
    """ Used to Call a stored procedure
    :param procedure_name: name of stored procedure (SP) in DB
    :param args: tuple of arguments required by SP
    :return: dictionary of returned arguments (IN/OUT) and results
    ex. {'args':returnArgs, 'results':<fetched results>}
    """

    # Start timer
    start_time = time.time()

    # I. Create reproducible procedure call
    procedure_statement = format_statement(procedure_name, args, True)

    # Create Connection
    connection = db_connection()

    # II. Call DB
    LOGGER.debug("About to call procedure statement: %s", procedure_statement)

    try:
        cursor = connection.cursor()
        return_args = cursor.callproc(procedure_name, args)

    except mysql.connector.Error as err:
        LOGGER.error("DB Error: %s with statement: %s", if_null(err.msg, ""), procedure_statement)
        connection.close()
        raise

    except Exception:
        LOGGER.error("Unknown DB Error: %s with statement: %s",
                     traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]), procedure_statement)
        connection.close()
        raise

    # III. Get Results
    results = []
    try:
        return_results = cursor.stored_results()
        for row in return_results:
            fetched = row.fetchall()
            results.append(fetched)

    except Exception:
        results = []

    finally:
        cursor.close()
        connection.close()

    results_dict = {'args': return_args, 'results': results}
    LOGGER.debug('Results from Procedure Statement: %s', results_dict)

    end_time = time.time()
    delta_time = datetime.timedelta(seconds=(end_time - start_time))

    if delta_time.total_seconds() > float(10.0):
        LOGGER.warning("Stored Procedure Complete. | Elapsed Time: %s | Called: %s",
                       str(delta_time), procedure_statement)
    else:
        LOGGER.info("Stored Procedure Complete. | Elapsed Time: %s | Called: %s",
                    str(delta_time), procedure_statement)

    return results_dict


def db_query(query_call, args):
    """ Used to call a SQL query that might be parametrized
    :param query_call: SQL to be performed, may include variables
    :param args: Arguments for SQL, may be blank
    :return: DB Results
    """

    # I. Initialize
    start_time = time.time()
    connection = db_connection()
    statement = format_statement(query_call, args, False)

    # II. Call DB
    try:
        LOGGER.debug("About to call query statement: %s", statement)
        cursor = connection.cursor()
        cursor.execute(query_call, args)

    except mysql.connector.Error as err:
        LOGGER.error("DB Error: %s with statement: %s", if_null(err.msg, ""), statement)
        connection.close()
        raise

    except Exception:
        LOGGER.error("DB Error: %s with statement: %s",
                     traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]), statement)
        connection.close()
        raise

    # III. Get Results
    try:
        return_results = cursor.fetchall()

    except Exception:
        return_results = None

    finally:
        cursor.close()
        connection.close()

    end_time = time.time()
    delta_time = datetime.timedelta(seconds=(end_time - start_time))

    if delta_time.total_seconds() > float(10.0):
        LOGGER.warning("Query Complete. | Elapsed Time: %s | Called: %s",
                       str(delta_time), statement)
    else:
        LOGGER.info("Query Complete. | Elapsed Time: %s | Called: %s",
                    str(delta_time), statement)

    return return_results


def db_connection():
    """ Creates mySQL DB Connection Object
    :return: mySQL connection object
    """

    # I. Get Connection String
    # DB Information is in env, example like
    # {"host":"hostname","port":3306,"user":"username","password":"password","db_name":"db"}
    try:
        # DB
        db_info = os.getenv('trad_labs_api_db',
                            '{"host":"hostname","port":3306,"user":"username","password":"password","db_name":"db"}')
        host = flask.json.loads(db_info)['host']
        port = flask.json.loads(db_info)['port']
        user = flask.json.loads(db_info)['user']
        password = flask.json.loads(db_info)['password']
        db_name = flask.json.loads(db_info)['db_name']

    except Exception:
        LOGGER.critical('Error getting connection string: %s',
                        traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))
        raise

    # II. Create New Connection
    try:
        connection = mysql.connector.connect(host=host,
                                             port=port,
                                             user=user,
                                             password=password,
                                             db=db_name,
                                             connection_timeout=2)
        connection.autocommit = True
        connection.raise_on_warnings = True

    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            LOGGER.critical("DB Connection to %s:%s, db=%s failed for user %s due to user/pwd being incorrect",
                            host, port, db_name, user)
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            LOGGER.critical("DB Connection to %s:%s, db=%s failed as db does not exist",
                            host, port, db_name)
        else:
            LOGGER.critical("DB Connection to %s:%s, db=%s failed for user %s due to %s",
                            host, port, db_name, user, err)
        raise

    return connection


def format_statement(statement, args, sp_indicator):
    """
    :param statement: SQL Statement that may have parametrized values
    :param args: Optional set of parameters, all different types
    :param sp_indicator: True if stored procedure
    :return: String that could be entered mysql workbench
    """

    # Get Variables

    if sp_indicator:
        try:
            procedure_statement = "call " + statement + "("

            for arg in args:
                if arg is None:
                    procedure_statement += "NULL,"
                elif isinstance(arg, int) or isinstance(arg, float) or isinstance(arg, bool):
                    procedure_statement += str(arg) + ","
                else:
                    procedure_statement += "'" + str(arg) + "',"

            # Remove end comma - which won't exist if there were no arguments
            if procedure_statement.endswith(','):
                procedure_statement = procedure_statement[:-1]

            # Close this and done
            procedure_statement += ");"

        except Exception:
            LOGGER.error("Error building procedure logging statement: %s with args: %s",
                         traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]), args)
            raise

    else:
        procedure_statement = 'exec ' + statement % args

    return procedure_statement
