function redirect_to_www_subdomain() {
    // Get the requested URL
    $requested_url = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . "://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";

    // Check if the requested domain does not start with 'www'
    if (strpos($_SERVER['HTTP_HOST'], 'www.') === false) {
        // Redirect to the 'www' subdomain
        $redirect_url = preg_replace('/^(https?:\/\/)([^\/]+)(.*)$/', '$1www.$2$3', $requested_url);
        wp_redirect($redirect_url, 301);
        exit;
    }
}
add_action('template_redirect', 'redirect_to_www_subdomain');
