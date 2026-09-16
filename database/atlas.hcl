variable "url" {
  type    = string
  default = getenv("URL")
}

variable "dev_url" {
  type    = string
  default = getenv("DEV_URL")
}

variable "dir" {
  type = string
  default = "file://migrations"
}

env "test-dev" {
  dev = var.dev_url
  migration {
    dir = var.dir
  }
  lint {
    latest = 1
    destructive { error = true }
    incompatible { error = true }
  }
}

env "test" {
  dev = var.dev_url
  migration {
    dir = var.dir
  }
  lint {
    git {
      base = "origin/main"
    }
    destructive { error = true }
    incompatible { error = true }
  }
}

env "production" {
  url = var.url
  migration {
    dir = var.dir
  }
}