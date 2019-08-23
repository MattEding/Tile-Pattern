provider "heroku" {
    email   = "${var.heroku_email}"
    api_key = "${var.heroku_api_key}"
}

resource "heroku_app" "webapp" {
    name       = "${var.app_name}"
    region     = "${var.region}"
    buildpacks = ["heroku/python"]
}

resource "heroku_build" "webapp" {
    app = "${heroku_app.webapp.name}"
    
    source = {
        path = "../src"
    }
}

resource "heroku_formation" "webapp" {
  app        = "${heroku_app.webapp.name}"
  type       = "web"
  quantity   = 1
  size       = "free"
  depends_on = ["heroku_build.webapp"]
}
