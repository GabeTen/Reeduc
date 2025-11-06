// ⚡ Configura o Ajax globalmente

const addCSRFTokenInAllPOSTRequests = (csrftoken) => {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            // Só adiciona o token se não for requisição "segura"
            if (!(/^GET|HEAD|OPTIONS|TRACE$/i.test(settings.type)) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        error: function(xhr, status, error) {
            // Tratamento genérico de erro (pode personalizar)
            if (xhr.status === 403) {
                toastr.error("Ação não permitida — falha no token CSRF.");
            } else if (xhr.status >= 500) {
                toastr.error("Erro interno no servidor.");
            } else {
                toastr.error("Erro inesperado ao processar requisição.");
            }
        }
    });
}
    
                    



//recupera o tema preferido do usuário (light ou dark) do localStorage ou das preferências do sistema

const THEME_KEY = 'theme';

// Retorna o elemento <html>, que é o “elemento raiz” da árvore DOM.
const HTML_ELEMENT = document.documentElement;

const getPreferredTheme = () => {
    const savedTheme = localStorage.getItem(THEME_KEY);
    if (savedTheme) {
        return savedTheme;
    }

    // Fallback para preferencias do sistema
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
};

$(HTML_ELEMENT).attr('data-bs-theme', getPreferredTheme());




//

/**
 * @param {string} theme - 'light' or 'dark'
 */
const updateIcons = (theme) => {
    $('.theme-toggle').each((index, toggle) => {
        const lightIcon = $(toggle).find('.theme-icon-light');
        const darkIcon = $(toggle).find('.theme-icon-dark');

        if (theme === 'dark') {
            $(lightIcon).addClass('d-none');
            $(darkIcon).removeClass('d-none');
        } else {
            $(lightIcon).removeClass('d-none');
            $(darkIcon).addClass('d-none');
        }
    });
};

/**
 * Toggles the theme between light and dark.
 */
const toggleTheme = () => {
    const currentTheme = $(HTML_ELEMENT).attr('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    // Set attribute and save choice
    $(HTML_ELEMENT).attr('data-bs-theme', newTheme);
    localStorage.setItem(THEME_KEY, newTheme);
    
    // Update icons
    updateIcons(newTheme);
};

// Set the initial ICON STATE on page load (theme is already set by <head> script)
updateIcons($(HTML_ELEMENT).attr('data-bs-theme'));

// Add click listeners to all theme toggle buttons
$('.theme-toggle').each((index, toggle) => {
    $(toggle).on('click', (event) => {
        event.preventDefault();
        toggleTheme();
    });
});









// Inicializa os tooltips do Bootstrap
$('[data-bs-toggle="tooltip"]').tooltip();


// Configuração do Toastr
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": true,
        "progressBar": true,
        "positionClass": "toast-top-right",
        "preventDuplicates": true,
        "showDuration": "300",
        "hideDuration": "500",
        "timeOut": "4000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };


