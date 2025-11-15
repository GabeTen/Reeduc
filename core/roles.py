from rolepermissions.roles import AbstractUserRole

# ----------------------------
# ADMINISTRADOR
# ----------------------------
class Admin(AbstractUserRole):
    available_permissions = {
        # Acesso geral
        'view_dashboard': True,
        'manage_users': True,
        'manage_roles': True,

        # Cursos
        'create_course': True,
        'edit_course': True,
        'delete_course': True,
        'view_all_courses': True,

        # Publicações educacionais
        'create_publication': True,
        'edit_publication': True,
        'delete_publication': True,
        'view_all_publications': True,

        # Relatórios / Monitoramento
        'view_reports': True,
    }


# ----------------------------
# PROFESSOR
# ----------------------------
class Professor(AbstractUserRole):
    available_permissions = {
        # Acesso básico
        'view_dashboard': True,

        # Cursos
        'create_course': True,
        'edit_own_course': True,
        'view_own_courses': True,

        # Publicações educacionais
        'create_publication': True,
        'edit_own_publication': True,
        'delete_own_publication': True,
        'view_own_publications': True,
    }


# ----------------------------
# ALUNO
# ----------------------------
class Aluno(AbstractUserRole):
    available_permissions = {
        # Acesso básico
        'view_dashboard': True,

        # Cursos
        'view_available_courses': True,
        'enroll_course': True,
        'view_enrolled_courses': True,

        # Publicações educacionais
        'view_publications': True,
    }
