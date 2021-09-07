from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import pandas as pd
import numpy as np
app=Flask(__name__)

conn = psycopg2.connect("host=ec2-34-196-238-94.compute-1.amazonaws.com dbname=d55jmibbqvabtk user=airlljzbdgskhs password=d95b6b5ed7f0ef331823ce1405c0ab5a0c516095545d78d3456bd527e794b0f6")

port = int(os.environ.get("PORT",5000))



@app.route('/')
def pegar():
    try: 
        cursor = conn.cursor()
        sql_query = """select * from gradeopcoes"""
        cursor.execute(sql_query)
        conn.commit()
        resultado = cursor.fetchall()
        # print(resultado)
        # print('-----')
        # print(type(resultado))
        # print('-----')
        df = pd.DataFrame(resultado, columns = ['index','Nome_ativo','Nome_ticker' , 'Nome_tipo', 'Nome_strike','Nome_aiotm','Nome_ultimo','Nome_delta','Nome_theta','Data_vencimento'])
        df = df.iloc[: , 1:] 
        # print(df)
        # print('-----')
        #df_menores = df[df['ultimo']<0.15]
        # df= df.astype(str)
        # df = df.replace(',','.')
        df[[ 'Nome_strike','Nome_aiotm','Nome_ultimo','Nome_delta','Nome_theta']] = df[['Nome_strike','Nome_aiotm','Nome_ultimo','Nome_delta','Nome_theta']].replace(',','.', regex=True)
        df[[ 'Nome_strike','Nome_aiotm','Nome_ultimo','Nome_delta','Nome_theta']] = df[['Nome_strike','Nome_aiotm','Nome_ultimo','Nome_delta','Nome_theta']].replace('','0.0', regex=True)
       # df = df.astype({'Nome_strike': np.float, 'Nome_aiotm': np.float, 'Nome_ultimo' : np.float, 'Nome_delta': np.float, 'Nome_theta': np.float})
        df[[ 'Nome_strike','Nome_ultimo','Nome_delta','Nome_theta']] = df[['Nome_strike','Nome_ultimo','Nome_delta','Nome_theta']].astype(float)
        # print(df.head())
        # print(df.info())
        df_analise = df[df['Nome_ultimo']<0.15]
        #print(df_analise.head())

        #0º pegar Os nomes ATivo
        lista_nomeativo = []
        lista_nomeativo.append(df_analise['Nome_ativo'].to_list())
        lista_nomeativo = lista_nomeativo[0]

        #1º pegar Os tickers
        lista_ticker = []
        lista_ticker.append(df_analise['Nome_ticker'].to_list())
        tamanholistaticker = len(lista_ticker[0])
        lista_ticker = lista_ticker[0]
        #print(lista_ticker)

        # 2º pegar o Tipo
        lista_tipo = []
        lista_tipo.append(df_analise['Nome_tipo'].to_list())
        lista_tipo = lista_tipo[0]
        # 3º pegar o Strike
        lista_strike = []
        lista_strike.append(df_analise['Nome_strike'].to_list())
        lista_strike = lista_strike[0]
        # 4º pegar o Nome_aiotm
        lista_aiotm = []
        lista_aiotm.append(df_analise['Nome_aiotm'].to_list())
        lista_aiotm = lista_aiotm[0]
        # 5º pegar o Nome_ultimo
        lista_ultimo = []
        lista_ultimo.append(df_analise['Nome_ultimo'].to_list())
        lista_ultimo = lista_ultimo[0]
        # 6º pegar o Nome_delta
        lista_delta = []
        lista_delta.append(df_analise['Nome_delta'].to_list())
        lista_delta = lista_delta[0]

        # 3º pegar o Nome_theta 
        lista_theta = []
        lista_theta.append(df_analise['Nome_theta'].to_list())
        lista_theta = lista_theta[0]

    except Exception as e:
        print("ERROR -----")
        print(e)

    return render_template('index.html', tamanholistaticker=tamanholistaticker , lista_nomeativo= lista_nomeativo,lista_ticker = lista_ticker, lista_tipo = lista_tipo,lista_strike=lista_strike, lista_aiotm=lista_aiotm, lista_ultimo= lista_ultimo,lista_delta=lista_delta, lista_theta=lista_theta)

if __name__ == "__main__":
    app.run(debug=True, port=port)