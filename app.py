import os
import bcrypt

from flask import (
    Flask,
    request,
    session,
    jsonify
)

from dotenv import load_dotenv

from sqlalchemy import (
    create_engine,
    text
)

load_dotenv()

HOST = os.getenv(
    "DB_HOST"
)

PORT = os.getenv(
    "DB_PORT"
)

DATABASE = os.getenv(
    "DB_NAME"
)

USER = os.getenv(
    "DB_USER"
)

PASSWORD = os.getenv(
    "DB_PASSWORD"
)

engine = create_engine(

f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

)

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY"
)

app.config.update(

SESSION_COOKIE_HTTPONLY=True,

SESSION_COOKIE_SECURE=False,

SESSION_COOKIE_SAMESITE="Lax"

)


@app.route(
"/login",
methods=["POST"]
)

def login():

    username = request.form.get(
        "username"
    )

    password = request.form.get(
        "password"
    )

    with engine.connect() as conn:

        result = conn.execute(

        text(

        """

        SELECT id,

        username,

        password

        FROM users

        WHERE username=:username

        """

        ),

        {

        "username":

        username

        }

        )

        user = result.fetchone()

    if user:

        senha_hash = user[2]

        if bcrypt.checkpw(

        password.encode(),

        senha_hash.encode()

        ):

            session[
            "user_id"
            ] = user[0]

            return jsonify({

            "mensagem":

            "Login OK"

            })

    return jsonify({

    "erro":

    "Falha login"

    }),401


@app.route(
"/transferir",
methods=["POST"]
)

def transferir():

    if "user_id" not in session:

        return jsonify({

        "erro":

        "Não autenticado"

        }),401

    usuario_logado = session[
    "user_id"
    ]

    id_origem = int(

    request.form.get(
    "id_origem"
    )

    )

    id_destino = int(

    request.form.get(
    "id_destino"
    )

    )

    valor = float(

    request.form.get(
    "valor"
    )

    )

    if usuario_logado != id_origem:

        return jsonify({

        "erro":

        "Operação não autorizada"

        }),403

    with engine.begin() as conn:

        conn.execute(

        text(

        """

        UPDATE contas

        SET saldo=

        saldo-:valor

        WHERE id=:origem

        """

        ),

        {

        "valor":

        valor,

        "origem":

        id_origem

        }

        )

        conn.execute(

        text(

        """

        UPDATE contas

        SET saldo=

        saldo+:valor

        WHERE id=:destino

        """

        ),

        {

        "valor":

        valor,

        "destino":

        id_destino

        }

        )

    return jsonify({

    "mensagem":

    "Transferência OK"

    })


if __name__=="__main__":

    app.run(

    debug=False

    )