from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import sys
import re
import logging
from functools import wraps

sys.path.insert(0, os.path.dirname(__file__))

from application.patterns.singleton import DatabaseConnection, SessionManager
from application.repositories.usuario_repository import UsuarioRepository
from application.repositories.materia_repository import MateriaRepository, HorarioRepository
from application.repositories.preferencia_repository import PreferenciaRepository
from application.repositories.notificacion_repository import NotificacionRepository
from application.services.auth_service import AuthService
from application.services.docente_service import DocenteService
from application.services.administrativo_service import AdministrativoService

try:
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )
except:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
logger = logging.getLogger(__name__)

template_dir = os.path.join(os.path.dirname(__file__), 'application', 'templates')
static_dir = os.path.join(os.path.dirname(__file__), 'application', 'static')
app = Flask(__name__, template_folder='application/templates', static_folder='application/static')

app.secret_key = os.environ.get('SECRET_KEY', 'clave-secreta-super-segura-12345')
app.config['DATABASE'] = os.environ.get('DATABASE_PATH', 'database/universidad.db')

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

db = DatabaseConnection()
db.connect(app.config['DATABASE'])

usuario_repo = UsuarioRepository(db)
materia_repo = MateriaRepository(db)
horario_repo = HorarioRepository(db)
preferencia_repo = PreferenciaRepository(db)
notificacion_repo = NotificacionRepository(db)

auth_service = AuthService(usuario_repo)
docente_service = DocenteService(usuario_repo, materia_repo, preferencia_repo,
                                 horario_repo, notificacion_repo)
administrativo_service = AdministrativoService(usuario_repo, materia_repo,
                                               preferencia_repo, notificacion_repo)


def validar_email(email):
    if not email:
        return False
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None


def sanitizar_entrada(texto):
    if not texto:
        return ''
    caracteres_peligrosos = ['<', '>', '"', "'", '&', ';']
    for char in caracteres_peligrosos:
        texto = texto.replace(char, '')
    return texto.strip()


def validar_entero(valor, nombre_campo="campo"):
    try:
        return int(valor)
    except (ValueError, TypeError):
        logger.warning(f"Valor inválido para {nombre_campo}: {valor}")
        return None

def requiere_autenticacion(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if not auth_service.esta_autenticado():
            flash('Debes iniciar sesión para acceder', 'warning')
            return redirect(url_for('login_docente'))
        return f(*args, **kwargs)
    return decorador


def requiere_rol(rol_requerido):
    def decorador_rol(f):
        @wraps(f)
        def decorador(*args, **kwargs):
            if not auth_service.tiene_rol(rol_requerido):
                flash(f'Acceso denegado. Se requiere rol: {rol_requerido}', 'danger')
                return redirect(url_for('login_docente'))
            return f(*args, **kwargs)
        return decorador
    return decorador_rol


@app.route('/')
def index():
    if auth_service.esta_autenticado():
        usuario = auth_service.obtener_usuario_actual()
        if usuario['rol'] == 'docente':
            return redirect(url_for('docente_dashboard'))
        else:
            return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login_docente'))


@app.route('/login/docente')
def login_docente():
    return render_template('auth/login_docente.html')


@app.route('/login/administrativo')
def login_administrativo():
    return render_template('auth/login_administrativo.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('login_docente'))

    email = request.form.get('email')
    password = request.form.get('password')

    exito, mensaje, datos = auth_service.iniciar_sesion(email, password)

    if exito:
        session['usuario_id'] = datos['id']
        session['rol'] = datos['rol']

        if datos['rol'] == 'docente':
            return redirect(url_for('docente_dashboard'))
        else:
            return redirect(url_for('admin_dashboard'))
    else:
        flash(mensaje, 'danger')
        return redirect(request.referrer or url_for('login_docente'))


@app.route('/logout')
def logout():
    auth_service.cerrar_sesion()
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('login_docente'))


@app.route('/docente/dashboard')
@requiere_autenticacion
@requiere_rol('docente')
def docente_dashboard():
    usuario = auth_service.obtener_usuario_actual()
    resumen = docente_service.obtener_resumen_dashboard(usuario['id'])
    notificaciones_count = docente_service.obtener_notificaciones_no_leidas(usuario['id'])

    return render_template('docente/dashboard.html',
                         usuario=usuario,
                         resumen=resumen,
                         notificaciones_count=notificaciones_count)


@app.route('/docente/perfil')
@requiere_autenticacion
@requiere_rol('docente')
def docente_perfil():
    usuario = auth_service.obtener_usuario_actual()
    docente = docente_service.obtener_perfil(usuario['id'])
    notificaciones_count = docente_service.obtener_notificaciones_no_leidas(usuario['id'])

    return render_template('docente/perfil.html',
                         usuario=usuario,
                         docente=docente,
                         notificaciones_count=notificaciones_count)


@app.route('/docente/perfil/actualizar', methods=['POST'])
@requiere_autenticacion
@requiere_rol('docente')
def docente_actualizar_perfil():
    usuario = auth_service.obtener_usuario_actual()
    docente = docente_service.obtener_perfil(usuario['id'])

    docente.nombre_completo = request.form.get('nombre_completo')
    docente.telefono = request.form.get('telefono')
    docente.oficina = request.form.get('oficina')
    docente.departamento = request.form.get('departamento')
    docente.especialidad = request.form.get('especialidad')
    docente.biografia = request.form.get('biografia')

    exito, mensaje = docente_service.actualizar_perfil(docente)
    flash(mensaje, 'success' if exito else 'danger')

    return redirect(url_for('docente_perfil'))


@app.route('/docente/calendario')
@requiere_autenticacion
@requiere_rol('docente')
def docente_calendario():
    usuario = auth_service.obtener_usuario_actual()
    horario_data = docente_service.obtener_horario_semanal(usuario['id'])
    notificaciones_count = docente_service.obtener_notificaciones_no_leidas(usuario['id'])

    return render_template('docente/calendario.html',
                         usuario=usuario,
                         horario_data=horario_data,
                         notificaciones_count=notificaciones_count)


@app.route('/docente/asignaturas')
@requiere_autenticacion
@requiere_rol('docente')
def docente_asignaturas():
    usuario = auth_service.obtener_usuario_actual()
    materias = docente_service.obtener_materias_asignadas(usuario['id'])
    notificaciones_count = docente_service.obtener_notificaciones_no_leidas(usuario['id'])

    materias_con_horarios = []
    for materia in materias:
        horarios = horario_repo.obtener_por_materia(materia.id)
        materias_con_horarios.append({
            'materia': materia,
            'horarios': horarios
        })

    return render_template('docente/asignaturas.html',
                         usuario=usuario,
                         materias=materias_con_horarios,
                         notificaciones_count=notificaciones_count)


@app.route('/docente/preferencias')
@requiere_autenticacion
@requiere_rol('docente')
def docente_preferencias():
    usuario = auth_service.obtener_usuario_actual()
    preferencias = docente_service.obtener_preferencias(usuario['id'])
    materias = materia_repo.obtener_todos()
    notificaciones_count = docente_service.obtener_notificaciones_no_leidas(usuario['id'])

    return render_template('docente/preferencias.html',
                         usuario=usuario,
                         preferencias=preferencias,
                         materias=materias,
                         notificaciones_count=notificaciones_count)


@app.route('/docente/preferencias/crear', methods=['POST'])
@requiere_autenticacion
@requiere_rol('docente')
def docente_crear_preferencia():
    usuario = auth_service.obtener_usuario_actual()

    materia_id = request.form.get('materia_id')
    dia_semana = request.form.get('dia_semana')
    horario = request.form.get('horario')

    exito, mensaje = docente_service.crear_preferencia(
        usuario['id'], int(materia_id), dia_semana, horario
    )

    flash(mensaje, 'success' if exito else 'danger')
    return redirect(url_for('docente_preferencias'))


@app.route('/docente/preferencias/eliminar/<int:preferencia_id>', methods=['POST'])
@requiere_autenticacion
@requiere_rol('docente')
def docente_eliminar_preferencia(preferencia_id):
    """Elimina una preferencia"""
    preferencia_repo.eliminar(preferencia_id)
    flash('Preferencia eliminada exitosamente', 'success')
    return redirect(url_for('docente_preferencias'))


@app.route('/docente/notificaciones')
@requiere_autenticacion
@requiere_rol('docente')
def docente_notificaciones():
    """Notificaciones del docente"""
    usuario = auth_service.obtener_usuario_actual()
    notificaciones = docente_service.obtener_notificaciones(usuario['id'])
    notificaciones_count = docente_service.obtener_notificaciones_no_leidas(usuario['id'])

    return render_template('docente/notificaciones.html',
                         usuario=usuario,
                         notificaciones=notificaciones,
                         notificaciones_count=notificaciones_count)


@app.route('/docente/notificaciones/marcar-leida/<int:notificacion_id>', methods=['POST'])
@requiere_autenticacion
@requiere_rol('docente')
def docente_marcar_notificacion_leida(notificacion_id):
    """Marca una notificación como leída"""
    notificacion = notificacion_repo.obtener_por_id(notificacion_id)
    if notificacion:
        notificacion.leida = True
        notificacion_repo.actualizar(notificacion)
    return redirect(url_for('docente_notificaciones'))


# ==================== RUTAS ADMINISTRATIVO ====================

@app.route('/admin/dashboard')
@requiere_autenticacion
@requiere_rol('administrativo')
def admin_dashboard():
    """Dashboard administrativo"""
    usuario = auth_service.obtener_usuario_actual()
    resumen = administrativo_service.obtener_resumen_dashboard()
    notificaciones_count = administrativo_service.obtener_notificaciones_no_leidas(usuario['id'])

    return render_template('administrativo/dashboard.html',
                         usuario=usuario,
                         resumen=resumen,
                         notificaciones_count=notificaciones_count)


@app.route('/admin/perfil')
@requiere_autenticacion
@requiere_rol('administrativo')
def admin_perfil():
    """Perfil del administrativo"""
    usuario = auth_service.obtener_usuario_actual()
    admin = usuario_repo.obtener_por_id(usuario['id'], 'administrativo')
    notificaciones_count = administrativo_service.obtener_notificaciones_no_leidas(usuario['id'])

    return render_template('administrativo/perfil.html',
                         usuario=usuario,
                         admin=admin,
                         notificaciones_count=notificaciones_count)


@app.route('/admin/perfil/actualizar', methods=['POST'])
@requiere_autenticacion
@requiere_rol('administrativo')
def admin_actualizar_perfil():
    """Actualiza el perfil del administrativo"""
    usuario = auth_service.obtener_usuario_actual()
    admin = usuario_repo.obtener_por_id(usuario['id'], 'administrativo')

    if admin:
        admin.email = request.form.get('email')
        admin.telefono = request.form.get('telefono')
        usuario_repo.actualizar(admin, 'administrativo')
        flash('Perfil actualizado exitosamente', 'success')
    else:
        flash('Error al actualizar perfil', 'danger')

    return redirect(url_for('admin_perfil'))


@app.route('/admin/perfil/cambiar-contrasena', methods=['POST'])
@requiere_autenticacion
@requiere_rol('administrativo')
def admin_cambiar_contrasena():
    """Cambia la contraseña del administrativo"""
    from werkzeug.security import check_password_hash, generate_password_hash

    usuario = auth_service.obtener_usuario_actual()
    admin = usuario_repo.obtener_por_id(usuario['id'], 'administrativo')

    contrasena_actual = request.form.get('contrasena_actual')
    contrasena_nueva = request.form.get('contrasena_nueva')
    contrasena_confirmar = request.form.get('contrasena_confirmar')

    if not check_password_hash(admin.password_hash, contrasena_actual):
        flash('Contraseña actual incorrecta', 'danger')
    elif contrasena_nueva != contrasena_confirmar:
        flash('Las contraseñas nuevas no coinciden', 'danger')
    elif len(contrasena_nueva) < 6:
        flash('La contraseña debe tener al menos 6 caracteres', 'danger')
    else:
        admin.password_hash = generate_password_hash(contrasena_nueva)
        usuario_repo.actualizar(admin, 'administrativo')
        flash('Contraseña actualizada exitosamente', 'success')

    return redirect(url_for('admin_perfil'))


@app.route('/admin/docentes')
@requiere_autenticacion
@requiere_rol('administrativo')
def admin_docentes():
    """Gestión de docentes"""
    usuario = auth_service.obtener_usuario_actual()
    docentes = administrativo_service.obtener_docentes()
    notificaciones_count = administrativo_service.obtener_notificaciones_no_leidas(usuario['id'])

    return render_template('administrativo/docentes.html',
                         usuario=usuario,
                         docentes=docentes,
                         notificaciones_count=notificaciones_count)


@app.route('/admin/docentes/crear', methods=['POST'])
@requiere_autenticacion
@requiere_rol('administrativo')
def admin_crear_docente():
    """Crea un nuevo docente"""
    from application.models.usuario import Docente
    from werkzeug.security import generate_password_hash

    docente = Docente(
        nombre_completo=request.form.get('nombre_completo'),
        email=request.form.get('email'),
        password_hash=generate_password_hash(request.form.get('password', 'docente123')),
        telefono=request.form.get('telefono'),
        oficina=request.form.get('oficina'),
        departamento=request.form.get('departamento'),
        especialidad=request.form.get('especialidad')
    )

    usuario_repo.crear(docente, 'docente')
    flash('Docente creado exitosamente', 'success')
    return redirect(url_for('admin_docentes'))


@app.route('/admin/docentes/editar/<int:docente_id>', methods=['POST'])
@requiere_autenticacion
@requiere_rol('administrativo')
def admin_editar_docente(docente_id):
    """Edita un docente existente"""
    docente = usuario_repo.obtener_por_id(docente_id, 'docente')

    if docente:
        docente.nombre_completo = request.form.get('nombre_completo')
        docente.email = request.form.get('email')
        docente.telefono = request.form.get('telefono')
        docente.oficina = request.form.get('oficina')
        docente.departamento = request.form.get('departamento')
        docente.especialidad = request.form.get('especialidad')

        usuario_repo.actualizar(docente, 'docente')
        flash('Docente actualizado exitosamente', 'success')
    else:
        flash('Docente no encontrado', 'danger')

    return redirect(url_for('admin_docentes'))


@app.route('/admin/docentes/eliminar/<int:docente_id>', methods=['POST'])
@requiere_autenticacion
@requiere_rol('administrativo')
def admin_eliminar_docente(docente_id):
    """Elimina un docente"""
    usuario_repo.eliminar(docente_id, 'docente')
    flash('Docente eliminado exitosamente', 'success')
    return redirect(url_for('admin_docentes'))


@app.route('/admin/asignaciones')
@requiere_autenticacion
@requiere_rol('administrativo')
def admin_asignaciones():
    """Gestión de asignaciones"""
    usuario = auth_service.obtener_usuario_actual()
    materias = materia_repo.obtener_todos()
    docentes = usuario_repo.obtener_docentes()
    notificaciones_count = administrativo_service.obtener_notificaciones_no_leidas(usuario['id'])

    return render_template('administrativo/asignaciones.html',
                         usuario=usuario,
                         materias=materias,
                         docentes=docentes,
                         notificaciones_count=notificaciones_count)


@app.route('/admin/asignar', methods=['POST'])
@requiere_autenticacion
@requiere_rol('administrativo')
def admin_asignar():
    """Asigna una materia a un docente"""
    materia_id = int(request.form.get('materia_id'))
    docente_id = request.form.get('docente_id')
    docente_id = int(docente_id) if docente_id else None

    exito, mensaje = administrativo_service.asignar_materia_docente(materia_id, docente_id)
    flash(mensaje, 'success' if exito else 'danger')

    return redirect(url_for('admin_asignaciones'))


@app.route('/admin/calendario')
@requiere_autenticacion
@requiere_rol('administrativo')
def admin_calendario():
    """Calendario administrativo"""
    usuario = auth_service.obtener_usuario_actual()
    notificaciones_count = administrativo_service.obtener_notificaciones_no_leidas(usuario['id'])
    return render_template('administrativo/calendario.html', 
                         usuario=usuario,
                         notificaciones_count=notificaciones_count)


# ==================== MAIN ====================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  SISTEMA UNIVERSITARIO - GESTIÓN ACADÉMICA")
    print("=" * 60)
    print("\nServidor iniciado en: http://127.0.0.1:5000")
    print("\nCredenciales de acceso:")
    print("-" * 60)
    print("DOCENTE:")
    print("  URL: http://127.0.0.1:5000/login/docente")
    print("  Email: docente@demo.com")
    print("  Password: docente123")
    print("\nADMINISTRATIVO:")
    print("  URL: http://127.0.0.1:5000/login/administrativo")
    print("  Email: administrativo@demo.com")
    print("  Password: admin123")
    print("=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
