import enum
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/buscar', methods=['POST'])
def buscar():
    try:
        spp = request.form['cui']

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Just_Jose_100",
            database="yessenia"
        )
        cursor = conn.cursor()

        sql = """SELECT semestre FROM alumnos WHERE CUI = %s """
        cursor.execute(sql, (spp,))
        resultado = cursor.fetchone()

        sql5 = """SELECT Correo FROM alumnos WHERE CUI =  %s"""
        cursor.execute(sql5,(spp,))
        resultado01 =cursor.fetchone()

        sql6 = """SELECT Nombre FROM alumnos WHERE CUI = %s"""
        cursor.execute(sql6,(spp,))
        resultado02 = cursor.fetchone()

        sql7 ="""SELECT Apellido FROM alumnos WHERE CUI = %s"""
        cursor.execute(sql7,(spp,))
        resultado03 = cursor.fetchone()

        if resultado:
            semestre_alumno = resultado[0]
            Correo_alumno = resultado01[0]
            NombreCompleto = resultado02[0]
            ApellidoCompleto = resultado03[0]
            sql2 = """SELECT Nombre FROM cursosce WHERE Semestre = %s"""
            cursor.execute(sql2, (semestre_alumno,))
            cursos_resultado = cursor.fetchall()

            if cursos_resultado:
                cursos = [curso[0] for curso in cursos_resultado]
            else:
                cursos = []
            profesores = []
            apellidos = []
            codigoCurso = []
            for i, curso in enumerate(cursos,start=1):

                #Codigo de los nombres del docente
                nuevo = """SELECT Nombres FROM cursosce INNER JOIN docentes ON Codigo_Docente = idDocentes WHERE cursosce.Nombre = %s;"""
                cursor.execute(nuevo,(curso,))
                profesor_resultado = cursor.fetchone()
                profesores.append(profesor_resultado)

                #Codigo de los apellidos del docente
                nuevo1 = """SELECT Apellido FROM cursosce INNER JOIN docentes ON Codigo_Docente = idDocentes WHERE cursosce.Nombre = %s;"""
                cursor.execute(nuevo1,(curso,))
                apellido_resultado = cursor.fetchone()
                apellidos.append(apellido_resultado)

                #Codigo del curso
                nuevo2 = """SELECT Codigo_Curso FROM yessenia.cursosce WHERE yessenia.cursosce.Nombre = %s;"""
                cursor.execute(nuevo2,(curso,))
                codigo_resultado = cursor.fetchone()
                codigoCurso.append(codigo_resultado)

            docentesA = [ap[0] for ap in apellidos]
            docentes = [docente[0] for docente in profesores]
            codigos = [cod[0] for cod in codigoCurso]
            cantidad = len(cursos)
            return render_template('resultado.html',code = codigos,  apellidos=docentesA, cui=spp, semestre=semestre_alumno, correo = Correo_alumno, nombre=NombreCompleto, apellido=ApellidoCompleto, num = cantidad, cursos=cursos, docentes=docentes)
        else:
            return render_template('error.html', mensaje="No se encontró ningún alumno con el CUI proporcionado.")

    except mysql.connector.Error as e:
        return render_template('error.html', mensaje="Error al conectar a la base de datos: " + str(e))

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
