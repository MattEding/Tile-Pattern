provider "heroku" {
  email   = var.heroku_email
  api_key = var.heroku_api_key
}

resource "heroku_app" "web_app" {
  name       = var.app_name
  region     = var.region
  buildpacks = ["heroku/python"]

  sensitive_config_vars = {
    SECRET_KEY = var.secret_key
  }
}

resource "heroku_build" "web_app" {
  app = heroku_app.web_app.name

  source = {
    path = "../src"
  }
}

resource "heroku_formation" "web_app" {
  app        = heroku_app.web_app.name
  type       = "web"
  quantity   = var.quantity
  size       = var.size
  depends_on = ["heroku_build.web_app"]
}
