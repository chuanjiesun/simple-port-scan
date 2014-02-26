import threading, socket, sys
from time import ctime, time

changgui_port = [21,22,23,25,53,80,81,110,139,161,443,445,513,514,873,1433,1434,1521,3306,
			3389,3690,5432,6000,6001,7001,7071,8008,8080,8088,10050,10051,]
threads = []#把线程实例t组成存储list类型

def scan(port):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(5)#设置超时时间
		result = sock.connect_ex((Host, port))
	#	print(result)
		if result == 0:
			print('port {} open'.format(port))
		sock.close()
	except Exception as e:
		print(e)
def wanquan():
	for i in range(1,65535,100):#可以将第三个参数作为手动输入的线程数
		k = 65535-i
		if k>100:  #如果剩下不到100个端口，就开启剩下的端口数的线程
			k = 100
		else:
			k = k
		for j in range(k):#开启100个线程
			j = i+j
			t = threading.Thread(target=scan, args=(j,))#如果参数写为args=j就会报错：参数必须为一个序列
			threads.append(t)
#			print(type(threads)) #<Thread(Thread-39, initial)>
		for m in range(len(threads)):
			threads[m].start()
		for n in range(len(threads)):
			threads[n].join()
		threads.clear()#清空进行下一个循环

def changgui():
	len_changgui = len(changgui_port)
	for i in range(0,len_changgui,10):
		k = len_changgui - i
		if k > 10:
			k = 10
		else:
			k = k
		for j in range(k):
			j = i+j
			t = threading.Thread(target=scan, args=(changgui_port[j],))	
			threads.append(t)
		for m in range(len(threads)):
			threads[m].start()
		for n in range(len(threads)):
			threads[n].join()
		threads.clear()

def main():
	if sys.argv[2] == 'cg':#changgui
		print('\n常见端口扫描模式')
		changgui()
	elif sys.argv[2] == 'wq':#wanquan
		print('\n完全端口扫描模式')
		wanquan()

if __name__ == '__main__':
	length_canshu = len(sys.argv)
	if length_canshu == 3:
		try:
			#Host = '192.168.167.2'#ip可以作为输入参数argv[]
			Host = sys.argv[1]
			print('Host is : {}'.format(Host))
			Host = socket.gethostbyname(sys.argv[1])#若果是域名就转换为ip
			print('{0}  <==>  {1}'.format(Host,sys.argv[1]))
			t1 = time()
			print('scan start at : {}'.format(ctime()))
			main()
			print('\nscan stop at : {}'.format(ctime()))
			t2 = time()
			print('端口扫描耗时：{0:.2f} 秒'.format(t2-t1))
		except Exception as e:
			print('哥们，可能网络不行或者输错了！{}'.format(e))
			print('\nUsage: xx.py ip/hostname  cg/wq')
			print('example: xx.py www.baidu.com cg')
			print('cg:常见端口扫描\nwq:完整端口扫描')
	else:
		print('\nUsage: xx.py ip/hostname  cg/wq')
		print('example: xx.py www.baidu.com cg')
		print('cg:常见端口扫描\nwq:完整端口扫描')
		sys.exit()
	#对于time()函数返回float类型，只取两位小数  具体更多用法查format()
	#{:.2f}与{0:.2f}结果一样
	
		
	

		
