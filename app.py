from flask import Flask, render_template, request

app = Flask(__name__)

# Funções de conversão próprias
def decimal_para_binario(n):
    n = int(n)
    if n == 0:
        return "0"
    resultado = ""
    while n > 0:
        resultado = str(n % 2) + resultado
        n //= 2
    return resultado

def decimal_para_hexadecimal(n):
    n = int(n)
    hex_chars = "0123456789ABCDEF"
    if n == 0:
        return "0"
    resultado = ""
    while n > 0:
        resultado = hex_chars[n % 16] + resultado
        n //= 16
    return resultado

def binario_para_decimal(b):
    resultado = 0
    for i, digito in enumerate(reversed(b)):
        if digito not in "01":
            return "Erro: número binário inválido"
        resultado += int(digito) * (2 ** i)
    return resultado

def binario_para_hexadecimal(b):
    dec = binario_para_decimal(b)
    if isinstance(dec, str):  # erro
        return dec
    return decimal_para_hexadecimal(dec)

def hexadecimal_para_decimal(h):
    hex_chars = "0123456789ABCDEF"
    h = h.upper()
    resultado = 0
    for i, digito in enumerate(reversed(h)):
        if digito not in hex_chars:
            return "Erro: número hexadecimal inválido"
        resultado += hex_chars.index(digito) * (16 ** i)
    return resultado

def hexadecimal_para_binario(h):
    dec = hexadecimal_para_decimal(h)
    if isinstance(dec, str):  # erro
        return dec
    return decimal_para_binario(dec)

# Função principal de conversão
def converter(numero, origem, destino):
    if origem == "decimal":
        if destino == "binario":
            return decimal_para_binario(numero)
        elif destino == "hexadecimal":
            return decimal_para_hexadecimal(numero)

    elif origem == "binario":
        if destino == "decimal":
            return str(binario_para_decimal(numero))
        elif destino == "hexadecimal":
            return binario_para_hexadecimal(numero)

    elif origem == "hexadecimal":
        if destino == "decimal":
            return str(hexadecimal_para_decimal(numero))
        elif destino == "binario":
            return hexadecimal_para_binario(numero)

    return "Conversão não implementada"

# Rotas Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grupo')
def grupo():
    return render_template('grupo.html')

@app.route('/conversor', methods=['GET', 'POST'])
def conversor():
    resultado1 = resultado2 = resultado3 = None
    if request.method == 'POST':
        coluna = request.form['coluna']
        numero = request.form['numero']
        destino = request.form['base_destino']

        if coluna == "1":  # Decimal
            resultado1 = converter(numero, "decimal", destino)
        elif coluna == "2":  # Binário
            resultado2 = converter(numero, "binario", destino)
        elif coluna == "3":  # Hexadecimal
            resultado3 = converter(numero, "hexadecimal", destino)

    return render_template(
        'conversor.html',
        resultado1=resultado1,
        resultado2=resultado2,
        resultado3=resultado3
    )

if __name__ == "__main__":
    app.run(debug=True)
