output "app_url" {
    value = "${heroku_app.webapp.web_url}"
}

output "secret_key" {
    value = "${var.secret_key}"
}