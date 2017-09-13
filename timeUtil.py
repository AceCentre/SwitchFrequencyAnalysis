
import click

@click.command()
@click.option('--ms',  default=1000, help='ms to convert')

def mstotime(ms):
	s=ms/1000
	m,s=divmod(s,60)
	h,m=divmod(m,60)
	d,h=divmod(h,24)

	print ("%d:%d:%d:%d" % (d, h, m, s))

if __name__ == '__main__':
    mstotime()
