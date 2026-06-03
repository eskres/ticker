import sqlite3

DB = 'ticker.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS auth ('
            'state TEXT,'
            'code_verifier TEXT,'
            'access_token TEXT,'
            'refresh_token TEXT'
        ')')

def save_pkce(state, code_verifier):
    with sqlite3.connect(DB) as conn:
        conn.execute('DELETE FROM auth')
        conn.execute('INSERT INTO auth VALUES (?, ?, NULL, NULL)', (state, code_verifier))

def get_pkce(state):
    with sqlite3.connect(DB) as conn:
        return conn.execute('SELECT code_verifier FROM auth WHERE state = ?', (state,)).fetchone()

def save_tokens(access_token, refresh_token):
    with sqlite3.connect(DB) as conn:
        conn.execute('UPDATE auth SET access_token = ?, refresh_token = ?', (access_token, refresh_token))
        if conn.execute('SELECT changes()').fetchone()[0] != 1:
            raise Exception("Unexpected number of rows")

def get_tokens():
    with sqlite3.connect(DB) as conn:
        return conn.execute('SELECT access_token, refresh_token, code_verifier FROM auth').fetchone()