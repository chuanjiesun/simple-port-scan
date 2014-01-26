import threading, socket, sys
from time import ctime, time #多线程并发速度快不少


len_argv = len(sys.argv)
if len_argv == 2:
	#Host = '192.168.167.2'#ip可以作为输入参数argv[]
	Host = sys.argv[1]
	Host = socket.gethostbyname(sys.argv[1])#若果是域名就转换为ip
	print(Host+'  <==>  '+sys.argv[1])
else:
	print('Usage: pyhton portscan.py hostname')
	sys.exit()#错误退出

threads = []#把线程实例t组成存储list类型


def scan(port):
	try:
		#socket.socket.settimeout(5)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(5)#设置超时时间
		result = sock.connect_ex((Host, port))
		if result == 0:
			print('port {} open'.format(port))
		sock.close()
	except Exception as e:
		print(e)
def main():
	for i in range(1,10001,100):#可以将第三个参数作为手动输入的线程数
		
		for j in range(100):#开启100个线程
			j = i+j
			t = threading.Thread(target=scan, args=(j,))#如果参数写为args=j就会报错：参数必须为一个序列
			threads.append(t)
#			print(type(threads)) #<Thread(Thread-39, initial)>
			t.start()
		for k in range(len(threads)):
			threads[k].join()
		threads.clear()#清空进行下一个循环

if __name__ == '__main__':
	print('scan start at : {}'.format(ctime()))
	t1 = time()
	main()
	print('scan stop at : {}'.format(ctime()))
	t2 = time()
	print('端口扫描耗时：{0:.2f} 秒'.format(t2-t1))
