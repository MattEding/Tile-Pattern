output "app_url" {
  value = heroku_app.web_app.web_url
}

output "secret_key" {
  value = var.secret_key
}
