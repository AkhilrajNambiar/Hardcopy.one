from backend import create_app
from logging import FileHandler, WARNING

app = create_app()

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

app.logger.addHandler(file_handler)

if __name__ == '__main__':
	app.run(debug=True)