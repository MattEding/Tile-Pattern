variable "heroku_api_key" {}

variable "heroku_email" {}

variable "secret_key" {
  description = "Secret key used in Flask app for WTForms"
}

variable "app_name" {
  description = "Globally unique Heroku app name"
  default     = "tile-pattern-app"
}

variable "region" {
  default = "us"
}

variable "quantity" {
  description = "Number of dynos to acivate"
  default     = 1
}

variable "size" {
  description = "Heroku dyno type"
  default     = "Free"
}
