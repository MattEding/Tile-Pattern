variable "heroku_api_key" {}

variable "heroku_email" {}

variable "secret_key" {
    description = "to be set by Docker with python secrets.token_hex(16)"
}

variable "app_name" {
    default = "tile-pattern-app"
}

variable "region" {
    default = "us"
}