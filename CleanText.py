import click
import os.path
import re
@click.command()
@click.option('--text-file', default='examples/vocab.txt', type=str, help='name of text file to input')
@click.option('--save-as', default='examples/vocab-cleaned.txt', type=str, help='name of text file to input')


def textClean(text_file, save_as):

	with open(text_file, 'r') as myfile:
		data=myfile.read()
		newData = strClean(data)
		
	with open(save_as,'w') as save_file:
		save_file.write(newData)
	save_file.close() 
	
def strClean(data):
		data = re.sub(r"[^a-zA-Z\s]",'',data)
		data = re.sub(r' {2,}' , ' ', data)
		lines = data.splitlines()
		newData = []
		for line in lines:
			if (line.strip()!=''):
				newData.append(line.strip()+'\n')
		return ''.join(newData)

if __name__ == '__main__':
	textClean()
