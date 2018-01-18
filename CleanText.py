import click
import os.path
import re
@click.command()
@click.option('--text-file', default='', help='name of text file to input')
@click.option('--remove-eol', default=False, type=bool, help='Remove spaces at end')
@click.option('--save-as', default='cleaned.txt', help='name of text file to input')


def textClean(text_file, remove_eol, save_as):

	with open(text_file, 'r') as myfile:
		data=myfile.read()
		data = re.sub(r"[^a-zA-Z\s]",'',data)
		# This isnt working.. 
		data = re.sub(r"([^ \t\r\n])[ \t]+$",r"\1",data)
		# sed -i 's/[ \t]*$//' "$1" - this will have to do
		
	with open(save_as,'w') as save_file:
		for line in data:
			save_file.write(line)
	save_file.close() 
	
	
if __name__ == '__main__':
	textClean()
