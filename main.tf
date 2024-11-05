terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }

  backend "azurerm" {
    resource_group_name  = "cohort32-33_AleYip_ProjectExercise"
    storage_account_name = "m12tfstore"
    container_name       = "m12-tf-store-container"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
  subscription_id = "d33b95c7-af3c-4247-9661-aa96d47fccc0"
}

data "azurerm_resource_group" "main" {
  name = "cohort32-33_AleYip_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}-aleyipsoftwire-m12-exercise"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image_name   = "aleyipsoftwire/todo-app:prod"
      docker_registry_url = "https://docker.io"
    }
  }

  app_settings = {
    WEBSITES_PORT                     = 8000
    MONGODB_PRIMARY_CONNECTION_STRING = azurerm_cosmosdb_account.main.primary_mongodb_connection_string
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-aleyipsoftwire-m12-mongodb-cluster"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  automatic_failover_enabled = true

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
    name = "EnableServerless"
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "todo-app-db"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}
