#!/usr/bin/python3

import argparse
import sqlite3
from os import path

def connect(path):
    try:
        conn = sqlite3.connect(path)
        return conn
    except sqlite3.Error as e:
        print(e)
        exit(1)

def setupDb(conn):
    cur = conn.cursor()

    query = ''' CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL,
        project TEXT,
        notes TEXT,
        done BOOLEAN
        );
        '''
    cur.execute(query)
    conn.close()

def addTask(conn, name, project='', notes=''):
    cur = conn.cursor()
    query = 'INSERT INTO tasks (name, project, notes, done) VALUES (\'%s\', \'%s\', \'%s\', 0);' %  (name, project, notes)
    cur.execute(query)
    conn.commit()
    conn.close()

def delTask(id):
    pass

def taskIsDone(id):
    pass

def listAllTasks(conn):
    cur = conn.cursor()
    query = 'SELECT * FROM tasks;'
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    print('All Tasks in DB:')
    for task in result:
        print('ID: %s, Name: %s, Project %s, Notes: %s, Done: %s' % (task[0], task[1], task[2], task[3], task[4]))

def main():
    homeDir = path.expanduser('~')
    dbPath = path.join(homeDir, '.todo.db')

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', help='Location for the database')

    subparsers = parser.add_subparsers(dest='command')

    parserAdd = subparsers.add_parser('add', help='Add a new task')
    parserAdd.add_argument('name')
    parserAdd.add_argument('project', nargs='?')

    parserDone = subparsers.add_parser('done', help='Mark a task as done')
    parserDone.add_argument('id')

    parserList = subparsers.add_parser('list', help='List tasks')
    parserList.add_argument('-a', '--all', help='List all tasks', action='store_true')
    args = parser.parse_args()

    print(args)

    if(args.database is not None):
        dbPath = args['database']

    conn = connect(dbPath)
    setupDb(conn)
    conn.close()

    match args.command:
        case 'add':
            addTask(connect(dbPath), args.name, args.project, None)
        case 'done':
            taskIsDone(connect(dbPath), args.id)
        case 'list':
            if args.all:
                listAllTasks(connect(dbPath))
   
if __name__ == '__main__':
    main()
