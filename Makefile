.PHONY: init up down help

init:
	@echo "${GREEN}Installing dependencies...${NC}"
	@poetry install
	@cp .env.sample .env
	@echo "${GREEN}Dependencies installed successfully.${NC}"

up:
	@echo "${GREEN}Starting development server...${NC}"
	@docker-compose up

down:
	@echo "${GREEN}Stopping development server...${NC}"
	@docker-compose down
	@echo "${GREEN}Development server stopped...${NC}"

db:
	@echo "${GREEN}Creating database...${NC}"
	@docker-compose exec app python manage.py create_db
	@echo "${GREEN}Database created...${NC}"

clear_db:
	@echo "${GREEN}Recreating database...${NC}"
	@docker-compose exec app python manage.py recreate_db
	@echo "${GREEN}Database recreated...${NC}"

help:
	@echo "${GREEN}Django Application Makefile${NC}"
	@echo "Available commands:"
	@echo "${YELLOW}make init${NC} - Install project dependencies"
	@echo "${YELLOW}make up${NC} - Run the development server"
	@echo "${YELLOW}make down${NC} - Stop the development server"


# Define ANSI color codes
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m